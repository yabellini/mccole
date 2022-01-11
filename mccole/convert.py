"""Convert Markdown to other formats."""

from mistletoe import Document
from mistletoe.ast_renderer import ASTRenderer
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.span_token import SpanToken

from .patch import patch_divs
from .util import EXTENSIONS


def md_to_doc(md):
    """Convert Markdown to plain mistletoe Document.

    Need the plain Document in order to find uses of special tags.
    """
    with ASTRenderer() as renderer:  # noqa F841
        return Document(md)


def md_to_html(text, config=None):
    """Convert Markdown to HTML using information in `config` (if any)."""
    with McColeHtml(config) as renderer:
        doc = Document(text)
        patch_divs(doc)
        return renderer.render(doc)


class BibCite(SpanToken):
    """Parse `@b(key1:key2:key3 citation."""

    pattern = EXTENSIONS["@b"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.cites = EXTENSIONS["@b"]["func"](match)


class GlossRef(SpanToken):
    """Parse `@g(text:key)` glossary reference."""

    pattern = EXTENSIONS["@g"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.text, self.key = EXTENSIONS["@g"]["func"](match)


class IndexRef(SpanToken):
    """Parse `@i(text:key)` index reference."""

    pattern = EXTENSIONS["@i"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.text, self.key = EXTENSIONS["@i"]["func"](match)


class GlossIndexRef(SpanToken):
    """Parse combined `@gi(text:gloss:index)` glossary/index reference."""

    pattern = EXTENSIONS["@gi"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.text, self.gloss_key, self.index_key = EXTENSIONS["@gi"]["func"](match)


class FigDef(SpanToken):
    """Parse `@fig(label:filename:alt:caption)`."""

    pattern = EXTENSIONS["@fig"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.label, self.file, self.alt, self.cap = EXTENSIONS["@fig"]["func"](match)


class TblDef(SpanToken):
    """Parse `@tbl(label:filename:caption)`."""

    pattern = EXTENSIONS["@tbl"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.label, self.file, self.cap = EXTENSIONS["@tbl"]["func"](match)


class McColeHtml(HTMLRenderer):
    """Convert directly to HTML."""

    def __init__(self, config=None):
        """Add special handlers to conversion chain."""
        super().__init__(BibCite, GlossRef, IndexRef, GlossIndexRef, FigDef, TblDef)
        self.config = config
        self.render_map["Div"] = self.render_div

    def render_div(self, token):
        """Render a <div>."""
        template = "<div{}>\n{}\n</div>"
        attrs = "".join(f' {k}="{v}"' for (k, v) in token.attributes.items())
        return template.format(attrs, self.render_inner(token))

    def render_bib_cite(self, token):
        """Render bibliographic citations."""
        cites = [f'<a href="bib.html#{c}">{c}</a>' for c in token.cites]
        return f"[{','.join(cites)}]"

    def render_gloss_ref(self, token):
        """Render glossary references."""
        text = token.text.strip()
        key = token.key.strip()
        return f'<a href="gloss.html#{key}">{text}</a>'

    def render_index_ref(self, token):
        """Render index references."""
        text = token.text.strip()
        key = token.key.strip()
        return f'<a href="index.html#{key}">{text}</a>'

    def render_gloss_index_ref(self, token):
        """Render combined glossary/index references."""
        text = token.text.strip()
        gloss_ref = f'href="gloss.html#{token.gloss_key.strip()}"'
        index_ref = f'index="index.html#{token.index_key.strip()}'
        return f'<a {gloss_ref} {index_ref}">{text}</a>'

    def render_fig_def(self, token):
        """Render figure definition."""
        label = token.label.strip()
        img = f'<img src="{token.file.strip()}" alt="{token.alt.strip()}"/>'
        caption = f"<figcaption>{token.cap.strip()}</figcaption>"
        return f'<figure id="{label}">{img}{caption}</figure>'

    def render_tbl_def(self, token):
        """Render table definition."""
        label = token.label.strip()
        caption = f"<caption>{token.cap.strip()}</caption>"
        file = token.file.strip()
        return f'<table id="{label}">\n{file}\n{caption}\n</table>'
