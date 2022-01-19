"""Parse Markdown files."""

import re

from markdown_it import MarkdownIt
from markdown_it.presets import commonmark
from markdown_it.renderer import RendererHTML
from markdown_it.utils import OptionsDict
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin


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


HEADING_KEY = re.compile(r'\{\#(.+?)\}')
class McColeRenderer(RendererHTML):
    def heading_open(self, tokens, idx, options, env):
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


def untokenize(config, xref, tokens):
    """Turn token stream into HTML."""
    options = OptionsDict(commonmark.make()["options"])
    renderer = McColeRenderer()
    return renderer.render(tokens, options, {})


# ----------------------------------------------------------------------


def _make_links_table(config):
    """Make Markdown links table from configuration."""
    if "links" not in config:
        return ""

    return "\n\n" + "\n".join(f"[{ln['key']}]: {ln['url']}" for ln in config["links"])
