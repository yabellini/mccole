"""Gather data from files."""

from mistletoe.block_token import Heading
from mistletoe.span_token import RawText

from .util import EXTENSIONS, McColeExc, visit


def gather_data(config, files):
    """Collect cross-reference data from ASTs."""
    overall = {"order": {}, "labels": {}}
    for (i, info) in enumerate(files):
        assert info["action"] == "transform"
        assert set(info.keys()).issuperset({"from", "raw", "header", "doc"})
        major = i + 1
        overall["order"][info["from"]] = major
        _label_headings(overall, major, info)
        _run_collectors(overall, info)
        _run_enumerators(overall, major, info)
    return overall


# ----------------------------------------------------------------------


def _label_headings(overall, major, info):
    """Collect all heading labels, numbering along the way."""
    path = info["from"]
    stack = [major - 1]
    accum = {}
    visit(path, info["doc"], _label_single_heading, stack, accum)
    overall["labels"][path] = accum


def _label_single_heading(path, node, stack, labels):
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


# ----------------------------------------------------------------------


def _run_collectors(overall, info):
    """Get simple embedded references like `@b(...)`."""
    for (func, keys) in COLLECTORS:
        for k in keys:
            if k not in overall:
                overall[k] = {}
        visit(info["from"], info["doc"], func, *[overall[k] for k in keys])


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


# Collector functions and their overall keys.
COLLECTORS = (
    [_get_bib_keys, ["bib_keys"]],
    [_get_gloss_keys, ["gloss_keys"]],
    [_get_index_keys, ["index_keys"]],
    [_get_gloss_index_keys, ["gloss_keys", "index_keys"]],
)

# ----------------------------------------------------------------------


def _run_enumerators(overall, major, info):
    """Get enumerated items `@fig(...)`."""
    for (func, key) in ENUMERATORS:
        if key not in overall:
            overall[key] = {}
        enumerator = [major, 0]
        visit(info["from"], info["doc"], func, overall[key], enumerator)


def _enumerate_fig_defs(path, node, fig_def_accum, enumerator):
    """Enumerate figure definitions."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@fig"]["re"].finditer(node.content):
            key, _, _, _ = EXTENSIONS["@fig"]["func"](match)
            _add_counter(fig_def_accum, key, _update_enumerator(enumerator))


def _update_enumerator(enumerator):
    """Update the counter in place, returning a tuple for storage."""
    assert len(enumerator) == 2
    enumerator[1] += 1
    return tuple(enumerator)


# Enumerator functions and their overall keys.
ENUMERATORS = ([_enumerate_fig_defs, "fig_defs"],)

# ----------------------------------------------------------------------


def _add_counter(accum, key, value):
    """Add a new value directly to a dict, disallowing duplicates."""
    if key in accum:
        raise McColeExc(f"Duplicate identifier {key}.")
    accum[key] = value


def _add_to_set(accum, key, value):
    """Add a value to a set under a key in a dict."""
    if key not in accum:
        accum[key] = set()
    accum[key].add(value)


def _ensure_attr(obj, field, value):
    if not hasattr(obj, field):
        setattr(obj, field, value)
