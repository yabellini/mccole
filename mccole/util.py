"""Utilities."""

import re
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


def _bib_cite(match):
    """Handle `@b(key,key)` during parsing."""
    result = [s.strip() for s in match.group(1).split(",")]
    if (not result) or not all(len(s) > 0 for s in result):
        raise McColeExc("Empty @b() bibliographic citation.")
    return result


def _gloss_ref(match):
    """Handle `@g(text|key)` glossary reference during parsing."""
    content = [s.strip() for s in match.group(1).split("|")]
    if (len(content) != 2) or not all(len(x) > 0 for x in content):
        raise McColeExc(f"Unrecognized glossary content '{match.group(1)}'")
    return content


def _index_ref(match):
    """Handle `@i(text|key)` index reference during parsing."""
    content = [s.strip() for s in match.group(1).split("|")]
    if (len(content) != 2) or not all(len(x) > 0 for x in content):
        raise McColeExc(f"Unrecognized index content '{match.group(1)}'")
    return content


def _gloss_index_ref(match):
    """Handle combined `@gi(text|gloss|index)` glossary/index reference during parsing."""
    content = [s.strip() for s in match.group(1).split("|")]
    if (len(content) != 3) or not all(len(x) > 0 for x in content):
        raise McColeExc(f"Unrecognized glossary/index content '{match.group(1)}'")
    return content


# Regular expressions and functions for extensions.
EXTENSIONS = {
    "@b": {
        "re": re.compile(r"@b\(([^)]*)\)"),
        "func": _bib_cite
    },
    "@g": {
        "re": re.compile(r"@g\((.+?)\)"),
        "func": _gloss_ref
    },
    "@i": {
        "re": re.compile(r"@i\((.+?)\)"),
        "func": _index_ref
    },
    "@gi": {
        "re": re.compile(r"@gi\((.+?)\)"),
        "func": _gloss_index_ref
    }
}
