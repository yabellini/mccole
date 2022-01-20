"""Parse Markdown files."""

from markdown_it import MarkdownIt
from markdown_it.presets import commonmark
from markdown_it.renderer import RendererHTML
from markdown_it.utils import OptionsDict
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from .bib import bib_to_html
from .patterns import (
    BIBLIOGRAPHY,
    FIGURE_REF,
    GLOSS_DEF,
    GLOSS_INDEX_DEF,
    HEADING_KEY,
    INDEX_DEF,
    SECTION_REF,
    TABLE_BODY,
    TABLE_CAP,
    TABLE_LBL,
    TABLE_REF,
    TABLE_START,
)


def tokenize(config, chapters):
    """Parse each file in turn."""
    md = _make_md()
    links_table = _make_links_table(config)
    for info in chapters:
        with open(info["src"], "r") as reader:
            text = reader.read()
            text += links_table
            info["tokens"] = md.parse(text)


def untokenize(config, xref, tokens):
    """Turn token stream into HTML."""
    options = OptionsDict(commonmark.make()["options"])
    renderer = McColeRenderer(config, xref)
    return renderer.render(tokens, options, {})


def _make_md():
    return (
        MarkdownIt("commonmark")
        .enable("table")
        .use(deflist_plugin)
        .use(front_matter_plugin)
    )


# ----------------------------------------------------------------------


class McColeRenderer(RendererHTML):
    """Translate token stream to HTML."""

    def __init__(self, config, xref):
        """Remember settings and cross-reference information."""
        super().__init__(self)
        self.config = config
        self.xref = xref

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
            (TABLE_START, self._table),
        ):
            match = pat.search(tokens[idx].content)
            if match:
                return method(tokens, idx, options, env, match)
        return RendererHTML.renderToken(self, tokens, idx, options, env)

    def html_inline(self, tokens, idx, options, env):
        """Fill in span elements with cross-references."""
        for (pat, method) in (
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
        return bib_to_html(self.config["bib"])

    def _figure_ref(self, tokens, idx, options, env, match):
        """Fill in figure reference."""
        key = match.group(1)
        label = self.xref["fig_lbl_to_index"].get(key, None)
        if label:
            label = ".".join(str(i) for i in label)
        else:
            label = "MISSING"
        return f'<a class="figref" href="{key}">Figure&nbsp;{label}</a>'

    def _gloss_def(self, tokens, idx, options, env, match):
        """Fill in glossary definition."""
        key = match.group(1)
        return f'<span g="{key}">'

    def _gloss_index_def(self, tokens, idx, options, env, match):
        """Fill in glossary+index definition."""
        gloss_key = match.group(1)
        index_key = match.group(2)
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
        md = _make_md()
        html = md.render(body)
        html = html.replace("<table>", opening).replace("</table>", closing)
        return html

    def _table_ref(self, tokens, idx, options, env, match):
        """Fill in table reference."""
        key = match.group(1)
        label = self.xref["tbl_lbl_to_index"].get(key, None)
        if label:
            label = ".".join(str(i) for i in label)
        else:
            label = "MISSING"
        return f'<a class="tblref" href="{key}">Table&nbsp;{label}</a>'


def _make_links_table(config):
    """Make Markdown links table from configuration."""
    if "links" not in config:
        return ""

    return "\n\n" + "\n".join(f"[{ln['key']}]: {ln['url']}" for ln in config["links"])
