"""Create cross-reference lookup."""

import logging
import re

from .patterns import FIGURE, FIGURE_ALT, FIGURE_CAP, FIGURE_SRC, HEADING_KEY, TABLE_START, TABLE_LBL, TABLE_CAP, TABLE_BODY
from .util import LOGGER_NAME, McColeExc

# Where to report.
LOGGER = logging.getLogger(LOGGER_NAME)


def cross_reference(config, chapters):
    """Create cross-reference tables for all chapters."""
    xref = {}
    _headings(config, xref, chapters)
    _figures(config, xref, chapters)
    _tables(config, xref, chapters)
    return xref


# ----------------------------------------------------------------------


def _figures(config, xref, chapters):
    """Build cross-references for figures."""

    lookup = {}
    xref |= {"fig_lbl_to_index": lookup}

    for info in chapters:
        current = [info["major"], 0]

        for token in info["tokens"]:
            if token.type != "html_block":
                continue

            match = FIGURE.search(token.content)
            if not match:
                continue

            fig_id = match.group(1)
            src = FIGURE_SRC.search(match.group(0))
            alt = FIGURE_ALT.search(match.group(0))
            caption = FIGURE_CAP.search(match.group(0))
            if not all([fig_id, src, alt, caption]):
                raise McColeExc(f"Badly-formatted figure on line {token.map[1]}.")

            if fig_id in lookup:
                raise McColeExc(f"Duplicate figure ID on line {token.map[1]}.")

            current[1] += 1
            label = tuple(current)
            lookup[fig_id] = label


def _headings(config, xref, chapters):
    """Compile headings."""
    lbl_to_index = {}
    lbl_to_title = {}
    index_to_lbl = {}
    xref |= {
        "heading_lbl_to_index": lbl_to_index,
        "heading_lbl_to_title": lbl_to_title,
        "heading_index_to_lbl": index_to_lbl,
    }

    for info in chapters:
        label_stack = [info["major"]]
        previous = None
        for token in info["tokens"]:
            if (previous is None) or (previous.type != "heading_open"):
                previous = token
                continue

            if token.type != "inline":
                raise McColeExc(
                    f"Unexpected token type {token.type} for heading{_line(token)}."
                )

            label, title = _heading_info(token)
            if not label:
                previous = token
                continue

            level = _heading_level(previous)
            index = tuple(str(i) for i in _heading_index(token, label_stack, level))

            if (label in lbl_to_index) or (label in lbl_to_title):
                raise McColeExc(f"Duplicate label {label}{_line(token)}.")

            lbl_to_index[label] = index
            lbl_to_title[label] = title
            index_to_lbl[index] = label

            previous = token


def _heading_index(token, stack, level):
    """Get the next heading level, adjusting `stack` as a side effect."""
    # Treat chapter titles specially.
    if level == 1:
        return tuple(stack)

    # Moving up too quickly?
    if level > len(stack) + 1:
        raise McColeExc(
            f"Heading {level} immediately under {len(stack)}{_line(token)}."
        )

    # Next level up?
    elif level == len(stack) + 1:
        stack.append(1)

    # Same level?
    elif level == len(stack):
        if len(stack) == 1:
            raise McColeExc(f"Can only have one title per chapter{_line(token)}.")
        stack[-1] += 1

    # Going down?
    else:
        while len(stack) > level:
            stack.pop()
        stack[-1] += 1

    # Report.
    return tuple(stack)


def _heading_info(token):
    """Get title and label (or None) from token."""
    assert token.type == "inline"
    match = HEADING_KEY.search(token.content)
    if not match:
        return None, token
    return match.group(1), token


def _heading_level(token):
    """Return the number level of a heading level."""
    tag = token.tag[1]
    try:
        level = int(tag)
    except ValueError:
        raise McColeExc(f"Cannot convert {tag} to heading level{_line(token)}.")
    if (level < 1) or (level > 5):
        raise McColeExc(f"Heading level {level} out of range{_line(token)}.")
    return level


def _line(token):
    """Return line number message or empty string."""
    if (token is None) or (token.map is None):
        return f" ({str(token)})"
    return f" (line {token.map[1]})"


def _tables(config, xref, chapters):
    """Build cross-references for tables."""

    lookup = {}
    xref |= {"tbl_lbl_to_index": lookup}

    for info in chapters:
        current = [info["major"], 0]

        for token in info["tokens"]:
            if token.type != "html_block":
                continue

            match = TABLE_START.search(token.content)
            if not match:
                continue

            tbl_id = TABLE_LBL.search(token.content).group(1)
            cap = TABLE_CAP.search(token.content).group(1)
            body = TABLE_BODY.search(token.content).group(1)

            if tbl_id in lookup:
                raise McColeExc(f"Duplicate table ID on line {token.map[1]}.")

            current[1] += 1
            label = tuple(current)
            lookup[tbl_id] = label
