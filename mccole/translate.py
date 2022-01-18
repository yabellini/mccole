"""Parse Markdown files."""

from markdown_it import MarkdownIt
from markdown_it.presets import commonmark
from markdown_it.renderer import RendererHTML
from markdown_it.utils import OptionsDict
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.deflist import deflist_plugin

from .util import pretty


def tokenize(chapters):
    """Parse each file in turn."""
    md = MarkdownIt("commonmark").enable("table").use(front_matter_plugin).use(deflist_plugin)
    for info in chapters:
        with open(info["src"], "r") as reader:
            info["tokens"] = md.parse(reader.read())


def untokenize(tokens):
    """Turn token stream into HTML."""
    options = OptionsDict(commonmark.make()["options"])
    renderer = RendererHTML()
    return renderer.render(tokens, options, {})
