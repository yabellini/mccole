"""Utilities."""

import re
import sys

# Field separator inside directives.
SEP = ":"


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


def visit(path, node, func, *accum):
    """Visit document nodes recursively."""
    func(path, node, *accum)
    if hasattr(node, "children"):
        for child in node.children:
            visit(path, child, func, *accum)


def _make_extractor(name, code, width):
    """Create function to handle `@code(p1:p2:...)` (with `width` args)."""

    def handler(match):
        result = [s.strip() for s in match.group(1).split(SEP)]
        len_ok = ((width == "*") and (len(result) > 0)) or (len(result) == width)
        if (not len_ok) or not all(len(r) > 0 for r in result):
            raise McColeExc(f"Badly-formatted {name}: @{code}({match.group(1)}).")
        return result

    return handler


# Regular expressions and functions for extensions.
EXTENSIONS = {
    "@b": {
        "re": re.compile(r"@b\((.*?)\)"),
        "func": _make_extractor("citation", "b", "*"),
    },
    "@g": {
        "re": re.compile(r"@g\((.*?)\)"),
        "func": _make_extractor("glossary reference", "g", 2),
    },
    "@i": {
        "re": re.compile(r"@i\((.*?)\)"),
        "func": _make_extractor("index reference", "i", 2),
    },
    "@gi": {
        "re": re.compile(r"@gi\((.*?)\)"),
        "func": _make_extractor("glossary/index reference", "gi", 3),
    },
    "@f": {
        "re": re.compile(r"@f\((.*?)\)"),
        "func": _make_extractor("figure reference", "f", 1),
    },
    "@t": {
        "re": re.compile(r"@t\((.*?)\)"),
        "func": _make_extractor("table reference", "t", 1),
    },
    "@fig": {
        "re": re.compile(r"@fig\((.*?)\)"),
        "func": _make_extractor("figure definition", "fig", 4),
    },
    "@tbl": {
        "re": re.compile(r"@tbl\((.*?)\)"),
        "func": _make_extractor("table definition", "tbl", 3),
    },
}
