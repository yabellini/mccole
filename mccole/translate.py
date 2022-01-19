"""Parse Markdown files."""

from markdown_it import MarkdownIt
from markdown_it.presets import commonmark
from markdown_it.renderer import RendererHTML
from markdown_it.utils import OptionsDict
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

from .bib import bib_to_html
from .patterns import *


def tokenize(config, chapters):
    """Parse each file in turn."""
    md = (
        MarkdownIt("commonmark")
        .enable("table")
        .use(deflist_plugin)
        .use(front_matter_plugin)
    )
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
        match = BIBLIOGRAPHY.search(tokens[idx].content)
        if match:
            return self._bibliography(tokens, idx, options, env, match)
        return RendererHTML.renderToken(self, tokens, idx, options, env)

    def html_inline(self, tokens, idx, options, env):
        """Fill in span elements with cross-references."""
        match = FIG_REF.search(tokens[idx].content)
        if match:
            return self._figref(tokens, idx, options, env, match)

        match = SEC_REF.search(tokens[idx].content)
        if match:
            return self._secref(tokens, idx, options, env, match)

        return RendererHTML.renderToken(self, tokens, idx, options, env)

    def _bibliography(self, tokens, idx, options, env, match):
        """Generate a bibliography."""
        return bib_to_html(self.config["bib"])

    def _figref(self, tokens, idx, options, env, match):
        """Fill in figure reference."""
        key = match.group(1)
        label = self.xref["fig_lbl_to_index"].get(key, None)
        if label:
            label = ".".join(str(i) for i in label)
        else:
            label = "MISSING"
        return f'<a class="figref" href="{key}">Figure&nbsp;{label}</a>'

    def _secref(self, tokens, idx, options, env, match):
        """Fill in figure reference."""
        key = match.group(1)
        label = self.xref["heading_lbl_to_index"].get(key, None)
        if label:
            word = "Chapter" if label[0].isdigit() else "Appendix"
            label = ".".join(str(i) for i in label)
            fill = "{word}&nbsp;{label}"
        else:
            fill = "MISSING"
        return f'<a class="secref" href="{key}">{fill}</a>'


def _make_links_table(config):
    """Make Markdown links table from configuration."""
    if "links" not in config:
        return ""

    return "\n\n" + "\n".join(f"[{ln['key']}]: {ln['url']}" for ln in config["links"])
