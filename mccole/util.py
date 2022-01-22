"""Utilities."""

import json
from types import SimpleNamespace as SN

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


def obj_to_namespace(obj):
    """Convert JSON object to simple namespace."""
    if isinstance(obj, dict):
        result = SN()
        for key in obj:
            setattr(result, key, obj_to_namespace(obj[key]))
        return result
    if isinstance(obj, list) or isinstance(obj, tuple):
        return [obj_to_namespace(x) for x in obj]
    return obj


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
