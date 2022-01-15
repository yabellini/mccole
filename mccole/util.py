"""Utilities."""

import re

# Field separator inside directives.
SEP = ":"


class McColeExc(Exception):
    """Problems we expect."""

    def __init__(self, msg):
        """Save the message."""
        self.msg = msg


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
        "re": re.compile(r"@b\{(.*?)\}"),
        "func": _make_extractor("citation", "b", "*"),
    },
    "@f": {
        "re": re.compile(r"@f\{(.*?)\}"),
        "func": _make_extractor("figure reference", "f", 1),
    },
    "@fig": {
        "re": re.compile(r"@fig\{(.*?)\}"),
        "func": _make_extractor("figure definition", "fig", 4),
    },
    "@g": {
        "re": re.compile(r"@g\{(.*?)\}"),
        "func": _make_extractor("glossary reference", "g", 2),
    },
    "@gi": {
        "re": re.compile(r"@gi\{(.*?)\}"),
        "func": _make_extractor("glossary/index reference", "gi", 3),
    },
    "@i": {
        "re": re.compile(r"@i\{(.*?)\}"),
        "func": _make_extractor("index reference", "i", 2),
    },
    "@s": {
        "re": re.compile(r"@s\{(.*?)\}"),
        "func": _make_extractor("section reference", "s", 1),
    },
    "@sec": {
        "re": re.compile(r"@sec\{(.*?)\}"),
        "func": _make_extractor("section label", "sec", 2),
    },
    "@t": {
        "re": re.compile(r"@t\{(.*?)\}"),
        "func": _make_extractor("table reference", "t", 1),
    },
    "@tbl": {
        "re": re.compile(r"@tbl\{(.*?)\}"),
        "func": _make_extractor("table definition", "tbl", 3),
    },
    "@toc": {
        "re": re.compile(r"@toc\{(.*?)\}"),
        "func": _make_extractor("table of contents", "toc", "*"),
    },
    "@x": {
        "re": re.compile(r"@x\{(.*?)\}"),
        "func": _make_extractor("expression", "x", 1),
    },
}
