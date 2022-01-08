"""Utilities."""

import sys
from collections.abc import Sequence
from types import SimpleNamespace


class McColeExc(Exception):
    """Problems we expect."""

    def __init__(self, msg):
        """Save the message."""
        self.msg = msg


def fail(arg):
    """Report failure and exit."""
    if isinstance(arg, McColeExc):
        arg = arg.msg
    print(arg, file=sys.stderr)
    sys.exit(1)


def json_to_ns(obj, root=False):
    """Recursively convert JSON-compatible structure to namespace."""
    if (obj is None) and root:
        return {}
    if isinstance(obj, str):
        return obj
    elif isinstance(obj, Sequence):
        return list(obj)
    elif isinstance(obj, dict):
        return SimpleNamespace(**{k: json_to_ns(v) for (k, v) in obj.items()})
    else:
        return obj
