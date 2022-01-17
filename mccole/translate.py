"""Parse Markdown files."""

from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.deflist import deflist_plugin


def tokenize(chapters):
    """Parse each file in turn."""
    md = MarkdownIt("commonmark").enable("table").use(front_matter_plugin).use(deflist_plugin)
    for info in chapters:
        with open(info["src"], "r") as reader:
            info["tokens"] = md.parse(reader.read())
