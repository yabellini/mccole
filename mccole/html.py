"""Generate HTML."""

from mistletoe import Document
from mistletoe.html_renderer import HTMLRenderer

from .parse import PARSERS
from .evaluate import evaluate
from .patch import patch_divs
from .util import McColeExc


def md_to_html(text, config=None):
    """Convert Markdown to HTML using information in `config` (if any)."""
    with McColeHtml(config) as renderer:
        doc = Document(text)
        patch_divs(doc)
        return renderer.render(doc)


class McColeHtml(HTMLRenderer):
    """Convert directly to HTML."""

    def __init__(self, config=None):
        """Add special handlers to conversion chain."""
        super().__init__(*PARSERS)
        self.config = config
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
        if label not in self.config["fig_defs"]:
            raise McColeExc(f"Reference to unknown figure label {label}")
        major, minor = self.config["fig_defs"][label]
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
        if label not in self.config["headings"]:
            raise McColeExc(f"Reference to unknown section label {label}")
        parts = [str(i) for i in self.config["headings"][label]]
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
        if label not in self.config["tbl_defs"]:
            raise McColeExc(f"Reference to unknown table label {label}")
        major, minor = self.config["tbl_defs"][label]
        return f'<a href="#{label}">Table&nbsp;{major}.{minor}</a>'

    def render_toc(self, token):
        """Render table of contents."""
        spec = token.label.strip()
        if not spec:
            raise McColeExc(f"Badly-formatted ToC specified {spec}")
        try:
            levels = [int(x) for x in spec.split(":")]
        except ValueError:
            raise McColeExc(f"Cannot convert all levels to numbers: {spec}")
        if len(levels) > 2:
            raise McColeExc(f"Too many levels specified for ToC {spec}")
        links = []
        for key in sorted(self.config.toc.keys()):
            if len(key) < levels[0]:
                pass
            elif (len(levels) == 2) and (len(key) > levels[1]):
                pass
            else:
                links.append(self.config.toc[key])
        return "<ul>\n{links}\n</ul>\n"
