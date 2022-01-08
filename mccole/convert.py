"""Convert Markdown to other formats."""

import re

from mistletoe import Document
from mistletoe.html_renderer import HTMLRenderer
from mistletoe.span_token import SpanToken

from .util import McColeExc


def md_to_html(text):
    """Convert Markdown to HTML."""
    with McColeHtml() as renderer:
        return renderer.render(Document(text))


class BibCite(SpanToken):
    """Parse `@b(key,key)` bibliographic citation."""

    pattern = re.compile(r"@b\(([^)]*)\)")

    def __init__(self, match):
        """Check contained value during construction."""
        self.cites = [s.strip() for s in match.group(1).split(",")]
        if (not self.cites) or not all(len(s) > 0 for s in self.cites):
            raise McColeExc("Empty @b() bibliographic citation.")


class GlossRef(SpanToken):
    """Parse `@g(text|key)` glossary reference."""

    pattern = re.compile(r"@g\((.+?)\)")

    def __init__(self, match):
        """Check contained value during construction."""
        content = [s.strip() for s in match.group(1).split("|")]
        if (len(content) != 2) or not all(len(x) > 0 for x in content):
            raise McColeExc(f"Unrecognized glossary content '{match.group(1)}'")
        self.text = content[0]
        self.key = content[1]


class IndexRef(SpanToken):
    """Parse `@i(text|key)` index reference."""

    pattern = re.compile(r"@i\((.+?)\)")

    def __init__(self, match):
        """Check contained value during construction."""
        content = [s.strip() for s in match.group(1).split("|")]
        if (len(content) != 2) or not all(len(x) > 0 for x in content):
            raise McColeExc(f"Unrecognized index content '{match.group(1)}'")
        self.text = content[0]
        self.key = content[1]


class GlossIndexRef(SpanToken):
    """Parse combined `@gi(text|gloss|index)` glossary/index reference."""

    pattern = re.compile(r"@gi\((.+?)\)")

    def __init__(self, match):
        """Check contained value during construction."""
        content = [s.strip() for s in match.group(1).split("|")]
        if (len(content) != 3) or not all(len(x) > 0 for x in content):
            raise McColeExc(f"Unrecognized glossary/index content '{match.group(1)}'")
        self.text = content[0]
        self.gloss_key = content[1]
        self.index_key = content[2]


class McColeHtml(HTMLRenderer):
    """Convert directly to HTML."""

    def __init__(self):
        """Add special handlers to conversion chain."""
        super().__init__(BibCite, GlossRef, IndexRef, GlossIndexRef)

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
