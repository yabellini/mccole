"""Convert Markdown to other formats."""

import re

from mistletoe import Document
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.span_token import SpanToken

from .patch import patch_divs
from .util import McColeExc, EXTENSIONS


def md_to_html(text):
    """Convert Markdown to HTML."""
    with McColeHtml() as renderer:
        doc = Document(text)
        patch_divs(doc)
        return renderer.render(doc)


class BibCite(SpanToken):
    """Parse `@b(key,key)` bibliographic citation."""

    pattern = EXTENSIONS["@b"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.cites = EXTENSIONS["@b"]["func"](match)


class GlossRef(SpanToken):
    """Parse `@g(text|key)` glossary reference."""

    pattern = EXTENSIONS["@g"]["re"]

    def __init__(self, match):
        self.text, self.key = EXTENSIONS["@g"]["func"](match)


class IndexRef(SpanToken):
    """Parse `@i(text|key)` index reference."""

    pattern = EXTENSIONS["@i"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.text, self.key = EXTENSIONS["@i"]["func"](match)


class GlossIndexRef(SpanToken):
    """Parse combined `@gi(text|gloss|index)` glossary/index reference."""

    pattern = EXTENSIONS["@gi"]["re"]

    def __init__(self, match):
        """Check contained value during construction."""
        self.text, self.gloss_key, self.index_key = EXTENSIONS["@gi"]["func"](match)


class McColeHtml(HTMLRenderer):
    """Convert directly to HTML."""

    def __init__(self):
        """Add special handlers to conversion chain."""
        super().__init__(BibCite, GlossRef, IndexRef, GlossIndexRef)
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
