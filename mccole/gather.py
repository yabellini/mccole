"""Gather data from files."""

from mistletoe.span_token import RawText

from .util import EXTENSIONS


def gather_data(config, files):
    """Collect cross-reference data from ASTs."""
    overall = {
        "order": {}
    }
    for (i, info) in enumerate(files):
        assert info["action"] == "transform"
        assert set(info.keys()).issuperset({"from", "raw", "header", "doc"})
        overall["order"][info["from"]] = i + 1
        for (key, func) in VISITORS:
            if key not in overall:
                overall[key] = {}
            _visit(info["from"], info["doc"], func, overall[key])
    return overall


def _visit(path, node, func, accum):
    """Visit nodes recursively."""
    func(path, node, accum)
    if hasattr(node, "children"):
        for child in node.children:
            _visit(path, child, func, accum)


def _get_bib_keys(path, node, accum):
    """Collect bibliographic citation keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@b"]["re"].finditer(node.content):
            for key in EXTENSIONS["@b"]["func"](match):
                if key not in accum:
                    accum[key] = set()
                accum[key].add(path)


def _get_gloss_keys(path, node, accum):
    """Collect glossary keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@g"]["re"].finditer(node.content):
            _, key = EXTENSIONS["@g"]["func"](match)
            if key not in accum:
                accum[key] = set()
            accum[key].add(path)


def _get_index_keys(path, node, accum):
    """Collect index keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@i"]["re"].finditer(node.content):
            _, key = EXTENSIONS["@i"]["func"](match)
            if key not in accum:
                accum[key] = set()
            accum[key].add(path)

# All visitor functions and their overall keys.
VISITORS = (
    ("bib_keys", _get_bib_keys),
    ("gloss_keys", _get_gloss_keys),
    ("index_keys", _get_index_keys),
)
