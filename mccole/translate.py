"""Parse Markdown files."""

from markdown_it import MarkdownIt
from markdown_it.presets import commonmark
from markdown_it.renderer import RendererHTML
from markdown_it.utils import OptionsDict
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.deflist import deflist_plugin

from .util import pretty


def tokenize(config, chapters):
    """Parse each file in turn."""
    md = MarkdownIt("commonmark").enable("table").use(front_matter_plugin).use(deflist_plugin)
    links_table = _make_links_table(config)
    for info in chapters:
        with open(info["src"], "r") as reader:
            text = reader.read()
            text += links_table
            info["tokens"] = md.parse(text)


def untokenize(tokens):
    """Turn token stream into HTML."""
    options = OptionsDict(commonmark.make()["options"])
    renderer = RendererHTML()
    return renderer.render(tokens, options, {})


# ----------------------------------------------------------------------


def _make_links_table(config):
    """Make Markdown links table from configuration."""
    if "links" not in config:
        return ""

    return "\n\n" + "\n".join(f"[{ln['key']}]: {ln['url']}" for ln in config["links"])
