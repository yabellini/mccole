"""Utilities."""

import json

from markdown_it import MarkdownIt
from markdown_it.token import Token
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin

# Identify this module's logger.
LOGGER_NAME = "mccole"


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
