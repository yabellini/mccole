"""Gather data from files."""

from mistletoe.block_token import Heading
from mistletoe.span_token import RawText

from .util import EXTENSIONS, McColeExc


def gather_data(config, files):
    """Collect cross-reference data from ASTs."""
    overall = {"order": {}, "labels": {}}
    for (i, info) in enumerate(files):
        assert info["action"] == "transform"
        assert set(info.keys()).issuperset({"from", "raw", "header", "doc"})
        major = i + 1
        overall["order"][info["from"]] = major
        _gather_embedded(overall, info)
        _gather_heading_labels(overall, major, info)
    return overall


def _gather_embedded(overall, info):
    """Get simple embedded references like `@b(...)`."""
    for (keys, func) in VISITORS:
        for k in keys:
            if k not in overall:
                overall[k] = {}
        _visit(info["from"], info["doc"], func, *[overall[k] for k in keys])


def _gather_heading_labels(overall, major, info):
    """Collect all heading labels, numbering along the way."""
    path = info["from"]
    stack = [major - 1]
    accum = {}
    _visit(path, info["doc"], _enumerate_headings, stack, accum)
    overall["labels"][path] = accum


def _visit(path, node, func, *accum):
    """Visit document nodes recursively."""
    func(path, node, *accum)
    if hasattr(node, "children"):
        for child in node.children:
            _visit(path, child, func, *accum)


def _enumerate_headings(path, node, stack, labels):
    """Add numbering information to headings."""
    if isinstance(node, Heading):
        _ensure_attr(node, "attr", {})
        label = _update_heading_stack(node.level, stack)
        node.attr["label"] = label
        labels[label] = _get_heading_text(node)


def _update_heading_stack(level, stack):
    """Modify the current stack of heading numbers."""
    if level > len(stack) + 1:
        raise McColeExc(
            f"Level {level} heading immediately under level {len(stack)} heading."
        )
    elif level == len(stack) + 1:
        stack.append(0)
    else:
        # Use `pop` rather than slicing to modify stack in place.
        while level < len(stack):
            stack.pop()
    stack[-1] += 1
    return tuple(stack)


def _get_heading_text(node):
    """Get the text of a heading node."""
    assert isinstance(node, Heading)
    assert len(node.children) == 1
    assert isinstance(node.children[0], RawText)
    return node.children[0].content.strip()


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


def _add_to_set(accum, key, value):
    """Add a value to a set under a key in a dict."""
    if key not in accum:
        accum[key] = set()
    accum[key].add(value)


def _ensure_attr(obj, field, value):
    if not hasattr(obj, field):
        setattr(obj, field, value)
