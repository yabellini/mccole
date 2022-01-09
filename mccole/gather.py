"""Gather data from files."""

from mistletoe.span_token import RawText

from .util import EXTENSIONS


def gather_data(config, files):
    """Collect cross-reference data from ASTs."""
    overall = {
        "bib_keys": {},
        "order": {}
    }
    for (i, info) in enumerate(files):
        assert info["action"] == "transform"
        assert set(info.keys()).issuperset({"from", "raw", "header", "doc"})
        overall["order"][info["from"]] = i + 1
        _visit(info["from"], info["doc"], _get_bib_keys, overall["bib_keys"])
    return overall


def _visit(path, node, func, accum):
    """Visit nodes recursively."""
    func(path, node, accum)
    if hasattr(node, "children"):
        for child in node.children:
            _visit(path, child, func, accum)


def _get_bib_keys(path, node, accum):
    if isinstance(node, RawText):
        for match in EXTENSIONS["@b"]["re"].finditer(node.content):
            for key in EXTENSIONS["@b"]["func"](match):
                if key not in accum:
                    accum[key] = set()
                accum[key].add(path)
