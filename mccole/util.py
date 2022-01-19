"""Utilities."""

import json

from markdown_it.token import Token


# Identify this module's logger.
LOGGER_NAME = "mccole"


class McColeExc(Exception):
    """Problems we expect."""

    def __init__(self, msg):
        """Save the message."""
        self.msg = msg


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
