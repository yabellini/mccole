"""Generate HTML."""

from mistletoe import Document
from mistletoe.html_renderer import HTMLRenderer

from .parse import PARSERS
from .evaluate import evaluate
from .patch import patch_divs
from .util import McColeExc


def md_to_html(config, xref, text):
    """Convert Markdown to HTML using information in `config` (if any)."""
    with McColeHtml(config, xref) as renderer:
        doc = Document(text)
        patch_divs(doc)
        return renderer.render(doc)


class McColeHtml(HTMLRenderer):
    """Convert directly to HTML."""

    def __init__(self, config=None, xref=None):
        """Add special handlers to conversion chain."""
        super().__init__(*PARSERS)
        self.config = config
        self.xref = xref
        self.render_map["Div"] = self.render_div

    def render_bib_cite(self, token):
        """Render bibliographic citations."""
        cites = [f'<a href="bib.html#{c}">{c}</a>' for c in token.cites]
        return f"[{','.join(cites)}]"

    def render_div(self, token):
        """Render a <div>."""
        template = "<div{}>\n{}\n</div>"
        attrs = "".join(f' {k}="{v}"' for (k, v) in token.attributes.items())
        return template.format(attrs, self.render_inner(token))

    def render_expression(self, token):
        """Render embedded expression."""
        expr = token.expr.strip()
        value = evaluate(self.config, expr)
        return value

    def render_fig_def(self, token):
        """Render figure definition."""
        label = token.label.strip()
        img = f'<img src="{token.file.strip()}" alt="{token.alt.strip()}"/>'
        caption = f"<figcaption>{token.cap.strip()}</figcaption>"
        return f'<figure id="{label}">{img}{caption}</figure>'

    def render_fig_ref(self, token):
        """Render figure references."""
        label = token.label.strip()
        if label not in self.xref["fig_keys"]:
            raise McColeExc(f"Reference to unknown figure label {label}")
        major, minor = self.xref["fig_keys"][label]
        return f'<a href="#{label}">Figure&nbsp;{major}.{minor}</a>'

    def render_gloss_ref(self, token):
        """Render glossary references."""
        text = token.text.strip()
        key = token.key.strip()
        return f'<a href="gloss.html#{key}">{text}</a>'

    def render_gloss_index_ref(self, token):
        """Render combined glossary/index references."""
        text = token.text.strip()
        gloss_ref = f'href="gloss.html#{token.gloss_key.strip()}"'
        index_ref = f'index="index.html#{token.index_key.strip()}'
        return f'<a {gloss_ref} {index_ref}">{text}</a>'

    def render_index_ref(self, token):
        """Render index references."""
        text = token.text.strip()
        key = token.key.strip()
        return f'<a href="index.html#{key}">{text}</a>'

    def render_sec_ref(self, token):
        """Render section references."""
        label = token.label.strip()
        if label not in self.xref["sec_lbl_to_seq"]:
            raise McColeExc(f"Reference to unknown section label {label}")
        parts = [str(i) for i in self.xref["sec_lbl_to_seq"][label]]
        kind = "Chapter" if len(parts) == 1 else "Section"
        return f'<a href="#{label}">{kind}&nbsp;{".".join(parts)}</a>'

    def render_tbl_def(self, token):
        """Render table definition."""
        label = token.label.strip()
        caption = f"<caption>{token.cap.strip()}</caption>"
        file = token.file.strip()
        return f'<table id="{label}">\n{file}\n{caption}\n</table>'

    def render_tbl_ref(self, token):
        """Render table references."""
        label = token.label.strip()
        if label not in self.xref["tbl_keys"]:
            raise McColeExc(f"Reference to unknown table label {label}")
        major, minor = self.xref["tbl_keys"][label]
        return f'<a href="#{label}">Table&nbsp;{major}.{minor}</a>'

    def render_toc(self, token):
        """Render table of contents."""
        if not token.levels:
            raise McColeExc(f"Badly-formatted ToC specified {token.levels}")
        try:
            levels = [int(x) for x in token.levels]
        except ValueError:
            raise McColeExc(f"Cannot convert all levels to numbers: {token.levels}")
        if len(levels) > 2:
            raise McColeExc(f"Too many levels specified for ToC {levels}")
        seq_to_sec_lbl = self.xref["seq_to_sec_lbl"]
        seq_to_sec_title = self.xref["seq_to_sec_title"]
        links = []
        for key in sorted(seq_to_sec_lbl.keys()):
            assert key in seq_to_sec_title
            if (len(levels) == 1) and (len(key) > levels[0]):
                pass
            elif (len(levels) == 2) and ((len(key) < levels[0]) or (levels[1] < len(key))):
                pass
            else:
                links.append({"lbl": seq_to_sec_lbl[key], "title": seq_to_sec_title[key]})
        links = [f'<li><a href="#{link["lbl"]}">{link["title"]}</a></li>' for link in links]
        links = "\n".join(links)
        return f'<ul class="toc">\n{links}\n</ul>\n'
