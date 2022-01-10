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
        for (keys, func) in VISITORS:
            for k in keys:
                if k not in overall:
                    overall[k] = {}
            _visit(info["from"], info["doc"], func, *[overall[k] for k in keys])
    return overall


def _visit(path, node, func, *accum):
    """Visit nodes recursively."""
    func(path, node, *accum)
    if hasattr(node, "children"):
        for child in node.children:
            _visit(path, child, func, *accum)


def _add_to_set(accum, key, path):
    if key not in accum:
        accum[key] = set()
    accum[key].add(path)


def _get_bib_keys(path, node, accum):
    """Collect bibliographic citation keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@b"]["re"].finditer(node.content):
            for key in EXTENSIONS["@b"]["func"](match):
                _add_to_set(accum, key, path)


def _get_gloss_keys(path, node, accum):
    """Collect glossary keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@g"]["re"].finditer(node.content):
            _, key = EXTENSIONS["@g"]["func"](match)
            _add_to_set(accum, key, path)


def _get_index_keys(path, node, accum):
    """Collect index keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@i"]["re"].finditer(node.content):
            _, key = EXTENSIONS["@i"]["func"](match)
            _add_to_set(accum, key, path)


def _get_gloss_index_keys(path, node, gloss_accum, index_accum):
    """Collect combined glossary + index keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@gi"]["re"].finditer(node.content):
            _, gloss_key, index_key = EXTENSIONS["@gi"]["func"](match)
            _add_to_set(gloss_accum, gloss_key, path)
            _add_to_set(index_accum, index_key, path)


# All visitor functions and their overall keys.
VISITORS = (
    [["bib_keys"], _get_bib_keys],
    [["gloss_keys"], _get_gloss_keys],
    [["index_keys"], _get_index_keys],
    [["gloss_keys", "index_keys"], _get_gloss_index_keys],
)
