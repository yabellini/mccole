"""Utilities."""

import json
import re

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

# Identify this module's logger.
LOGGER_NAME = "mccole"

# Cross-references are `<a type="key"/>`
FIGURE_REF = re.compile(r'<a\s+figure="(.+?)"\s*/>')
SECTION_REF = re.compile(r'<a\s+section="(.+?)"\s*/>')
TABLE_REF = re.compile(r'<a\s+table="(.+?)"\s*/>')

# Bibliographic citations are `<cite>key,key</cite>`.
CITE = re.compile(r"<cite>")

# Definitions are `<span g="key">text</span>` for glossary terms,
# `<span i="key">text</span>` for indexing terms,
# and `<span g="key" i="other_key">text</span>` for both.
GLOSS_DEF = re.compile(r'<span\s+g="(.+?)">')
INDEX_DEF = re.compile(r'<span\s+i="(.+?)">')
GLOSS_INDEX_DEF = re.compile(r'<span\s+g="(.+?)"\s+i="(.+?)">')

# Headings are `## Text {#key}`.
HEADING_KEY = re.compile(r"\{\#(.+?)\}")

# `<div class="bibliography"/>` and `<div class="glossary"/>`
# show where the bibliography and glossary should go.
BIBLIOGRAPHY = re.compile(r'<div\s+class="bibliography"\s*/>')
GLOSSARY = re.compile(r'<div\s+class="glossary"\s*/>')

# Figures are:
# <figure id="key">
#   <img src="file" alt="short"/>
#   <figcaption>long</figcaption>
# </figure>
FIGURE = re.compile(r'<figure\s+id="(.+?)"\s*>\s*.+?</figure>', re.DOTALL)
FIGURE_SRC = re.compile(r'<img\b.+?src="(.+?)".+?>')
FIGURE_ALT = re.compile(r'<img\b.+?alt="(.+?)".+?>')
FIGURE_CAP = re.compile(r"<figcaption>(.+?)</figcaption>")

# Since there isn't a way to add an ID to a Markdown table, they are:
# <div class="table" id="key" cap="caption">
# ...Markdown table...
# </div>
TABLE_START = re.compile(r'<div.+?class="table"')
TABLE_LBL = re.compile(r'id="(.+?)"')
TABLE_CAP = re.compile(r'cap="(.+?)"')
TABLE_BODY = re.compile(r"<div.+?>\n(.+)\n</div>", re.DOTALL)


# ----------------------------------------------------------------------


class McColeExc(Exception):
    """Problems we expect."""

    def __init__(self, msg):
        """Save the message."""
        self.msg = msg


def err(config, msg):
    """Record an error for later display."""
    if "error_log" not in config:
        config["error_log"] = []
    config["error_log"].append(msg)


def make_md():
    """Make Markdown parser."""
    return (
        MarkdownIt("commonmark")
        .enable("table")
        .use(deflist_plugin)
        .use(front_matter_plugin)
    )


def pretty(obj):
    """Create pretty-printed JSON string."""
    return json.dumps(_pretty_keys(obj), indent=2)


def _pretty_keys(obj):
    """Replace tuple keys for pretty-printing."""
    if isinstance(obj, tuple):
        return f"({', '.join(str(x) for x in obj)})"
    elif isinstance(obj, dict):
        return {_pretty_keys(k): _pretty_keys(obj[k]) for k in obj}
    elif isinstance(obj, list):
        return [_pretty_keys(x) for x in obj]
    elif isinstance(obj, Token):
        return obj.type
    else:
        return obj
