"""Gather data from files."""

from mistletoe.block_token import Heading
from mistletoe.span_token import RawText

from .util import EXTENSIONS, McColeExc, visit


def gather_data(config, files):
    """Collect cross-reference data."""
    subset = [info for info in files if info["action"] == "transform"]
    xref = {"order": {}, "sec_lbl_to_seq": {}, "seq_to_sec_lbl": {},
            "seq_to_sec_title": {}}
    for (i, info) in enumerate(subset):
        major = i + 1
        xref["order"][info["from"]] = major
        _label_headings(xref, major, info)
        _run_collectors(xref, info)
        _run_enumerators(xref, major, info)
    return xref


# ----------------------------------------------------------------------


def _label_headings(xref, major, info):
    """Collect all heading labels, numbering along the way."""
    path = info["from"]
    stack = [major - 1]
    visit(path, info["doc"], _label_single_heading, stack,
          xref["sec_lbl_to_seq"], xref["seq_to_sec_lbl"],
          xref["seq_to_sec_title"])


def _label_single_heading(path, node, stack, sec_lbl_to_seq, seq_to_sec_lbl, seq_to_sec_title):
    """Add numbering information to headings."""
    if isinstance(node, Heading):
        seq = _update_heading_stack(node.level, stack)
        label, title = _get_heading_label_and_title(node)
        if label is not None:
            sec_lbl_to_seq[label] = seq
            seq_to_sec_lbl[seq] = label
            seq_to_sec_title[seq] = title


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


def _get_heading_label_and_title(node):
    """Get the label of a heading node or None."""
    assert isinstance(node, Heading)
    assert len(node.children) == 1
    assert isinstance(node.children[0], RawText)
    text = node.children[0].content
    match = EXTENSIONS["@sec"]["re"].search(text)
    if not match:
        return None, None
    label, title = EXTENSIONS["@sec"]["func"](match)
    return label, title


# ----------------------------------------------------------------------


def _run_collectors(xref, info):
    """Get simple embedded references like `@b(...)`."""
    for (func, keys) in COLLECTORS:
        for k in keys:
            if k not in xref:
                xref[k] = {}
        visit(info["from"], info["doc"], func, *[xref[k] for k in keys])


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


def _get_gloss_index_keys(path, node, gloss_accum, index_accum):
    """Collect combined glossary + index keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@gi"]["re"].finditer(node.content):
            _, gloss_key, index_key = EXTENSIONS["@gi"]["func"](match)
            _add_to_set(gloss_accum, gloss_key, path)
            _add_to_set(index_accum, index_key, path)


def _get_index_keys(path, node, accum):
    """Collect index keys."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@i"]["re"].finditer(node.content):
            _, key = EXTENSIONS["@i"]["func"](match)
            _add_to_set(accum, key, path)


# Collector functions and their xref keys.
COLLECTORS = (
    [_get_bib_keys, ["bib_keys"]],
    [_get_gloss_index_keys, ["gloss_keys", "index_keys"]],
    [_get_gloss_keys, ["gloss_keys"]],
    [_get_index_keys, ["index_keys"]],
)

# ----------------------------------------------------------------------


def _run_enumerators(xref, major, info):
    """Get enumerated items `@fig(...)`."""
    for (func, key) in ENUMERATORS:
        if key not in xref:
            xref[key] = {}
        enumerator = [major, 0]
        visit(info["from"], info["doc"], func, xref[key], enumerator)


def _enumerate_fig_defs(path, node, fig_def_accum, enumerator):
    """Enumerate figure definitions."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@fig"]["re"].finditer(node.content):
            key, _, _, _ = EXTENSIONS["@fig"]["func"](match)
            _add_counter(fig_def_accum, key, _update_enumerator(enumerator))


def _enumerate_tbl_defs(path, node, tbl_def_accum, enumerator):
    """Enumerate table definitions."""
    if isinstance(node, RawText):
        for match in EXTENSIONS["@tbl"]["re"].finditer(node.content):
            key, _, _ = EXTENSIONS["@tbl"]["func"](match)
            _add_counter(tbl_def_accum, key, _update_enumerator(enumerator))


def _update_enumerator(enumerator):
    """Update the counter in place, returning a tuple for storage."""
    assert len(enumerator) == 2
    enumerator[1] += 1
    return tuple(enumerator)


# Enumerator functions and their xref keys.
ENUMERATORS = (
    [_enumerate_fig_defs, "fig_keys"],
    [_enumerate_tbl_defs, "tbl_keys"],
)

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
