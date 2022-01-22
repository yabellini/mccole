"""Convert token streams to HTML."""

import yaml

from markdown_it.presets import commonmark
from markdown_it.renderer import RendererHTML
from markdown_it.utils import OptionsDict

from .bib import bib_to_html
from .gloss import gloss_to_html
from .patterns import (
    BIBLIOGRAPHY,
    CITE,
    FIGURE,
    FIGURE_REF,
    GLOSS_DEF,
    GLOSS_INDEX_DEF,
    GLOSSARY,
    HEADING_KEY,
    INDEX_DEF,
    SECTION_REF,
    TABLE_BODY,
    TABLE_CAP,
    TABLE_LBL,
    TABLE_REF,
    TABLE_START,
)
from .util import make_md


def render(config, xref, seen, tokens):
    """Turn token stream into HTML."""
    options = OptionsDict(commonmark.make()["options"])
    renderer = McColeRenderer(config, xref, seen)
    return renderer.render(tokens, options, {})


# ----------------------------------------------------------------------


class McColeRenderer(RendererHTML):
    """Translate token stream to HTML."""

    def __init__(self, config, xref, seen):
        """Remember settings and cross-reference information."""
        super().__init__(self)
        self.config = config
        self.xref = xref
        self.seen = seen

    def heading_open(self, tokens, idx, options, env):
        """Add IDs to headings if requested."""
        inline = tokens[idx + 1]
        assert inline.type == "inline"
        for child in inline.children:
            if child.type == "text":
                match = HEADING_KEY.search(child.content)
                if match:
                    heading_id = match.group(1)
                    child.content = child.content.replace(match.group(0), "")
                    tokens[idx].attrSet("id", heading_id)
        return RendererHTML.renderToken(self, tokens, idx, options, env)

    def html_block(self, tokens, idx, options, env):
        """Look for special entries for bibliography, glossary, etc."""
        for (pat, method) in (
            (BIBLIOGRAPHY, self._bibliography),
            (FIGURE, self._figure),
            (GLOSSARY, self._glossary),
            (TABLE_START, self._table),
        ):
            match = pat.search(tokens[idx].content)
            if match:
                return method(tokens, idx, options, env, match)
        return RendererHTML.renderToken(self, tokens, idx, options, env)

    def html_inline(self, tokens, idx, options, env):
        """Fill in span elements with cross-references."""
        for (pat, method) in (
            (CITE, self._cite),
            (FIGURE_REF, self._figure_ref),
            (GLOSS_DEF, self._gloss_def),
            (INDEX_DEF, self._index_def),
            (GLOSS_INDEX_DEF, self._gloss_index_def),
            (SECTION_REF, self._section_ref),
            (TABLE_REF, self._table_ref),
        ):
            match = pat.search(tokens[idx].content)
            if match:
                return method(tokens, idx, options, env, match)
        if tokens[idx].content == "</span>":
            return "</span>"
        return RendererHTML.renderToken(self, tokens, idx, options, env)

    def _bibliography(self, tokens, idx, options, env, match):
        """Generate a bibliography."""
        return bib_to_html(self.config)

    def _cite(self, tokens, idx, options, env, match):
        """Translate bibliographic citations."""
        assert tokens[idx + 1].type == "text"
        keys = [k.strip() for k in tokens[idx + 1].content.split(",")]
        self.seen["cite"].update(keys)
        refs = [f'<a href="../bibliography/#{k}">{k}</a>' for k in keys]
        # Get rid of `<cite>`, text, `</cite>`
        del tokens[idx : idx + 3]  # noqa e203
        return f"[{', '.join(refs)}]"

    def _figure(self, tokens, idx, options, env, match):
        """Generate a figure."""
        return tokens[idx].content

    def _glossary(self, tokens, idx, options, env, match):
        """Generate a glossary."""
        return gloss_to_html(self.config)

    def _figure_ref(self, tokens, idx, options, env, match):
        """Fill in figure reference."""
        key = match.group(1)
        self.seen["figure_ref"].add(key)
        label = self.xref["fig_lbl_to_index"].get(key, None)
        if label:
            label = ".".join(str(i) for i in label)
        else:
            label = "MISSING"
        return f'<a class="figref" href="{key}">Figure&nbsp;{label}</a>'

    def _gloss_def(self, tokens, idx, options, env, match):
        """Fill in glossary definition."""
        key = match.group(1)
        self.seen["gloss_ref"].add(key)
        return f'<span g="{key}">'

    def _gloss_index_def(self, tokens, idx, options, env, match):
        """Fill in glossary+index definition."""
        gloss_key = match.group(1)
        index_key = match.group(2)
        self.seen["gloss_ref"].add(gloss_key)
        self.seen["index_ref"].add(index_key)
        return f'<span g="{gloss_key}" i="{index_key}">'

    def _index_def(self, tokens, idx, options, env, match):
        """Fill in index definition."""
        key = match.group(1)
        return f'<span i="{key}">'

    def _section_ref(self, tokens, idx, options, env, match):
        """Fill in figure reference."""
        key = match.group(1)
        label = self.xref["heading_lbl_to_index"].get(key, None)
        if label:
            word = "Chapter" if label[0].isdigit() else "Appendix"
            label = ".".join(str(i) for i in label)
            fill = f"{word}&nbsp;{label}"
        else:
            fill = "MISSING"
        return f'<a class="secref" href="{key}">{fill}</a>'

    def _table(self, tokens, idx, options, env, match):
        """Parse a table nested inside a div."""
        content = tokens[idx].content
        lbl = TABLE_LBL.search(content).group(1)
        cap = TABLE_CAP.search(content).group(1)
        body = TABLE_BODY.search(content).group(1)
        opening = f'<table id="{lbl}">'
        closing = f"<caption>{cap}</caption>\n</table>"
        md = make_md()
        html = md.render(body)
        html = html.replace("<table>", opening).replace("</table>", closing)
        return html

    def _table_ref(self, tokens, idx, options, env, match):
        """Fill in table reference."""
        key = match.group(1)
        self.seen["table_ref"].add(key)
        label = self.xref["tbl_lbl_to_index"].get(key, None)
        if label:
            label = ".".join(str(i) for i in label)
        else:
            label = "MISSING"
        return f'<a class="tblref" href="{key}">Table&nbsp;{label}</a>'
