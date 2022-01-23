"""Create cross-reference lookup."""

import logging

from .patterns import (
    FIGURE,
    FIGURE_ALT,
    FIGURE_CAP,
    FIGURE_SRC,
    HEADING_ID,
    TABLE_ID,
    TABLE_START,
)
from .util import LOGGER_NAME, McColeExc, err

# Where to report.
LOGGER = logging.getLogger(LOGGER_NAME)


def cross_reference(config):
    """Create cross-reference tables for all pages."""
    # Exclude un-indexed pages (e.g., home page).
    pages = [p for p in config["pages"] if p["major"] is not None]
    
    xref = {}
    _headings(config, xref, pages)
    _figures(config, xref, pages)
    _tables(config, xref, pages)

    return xref


# ----------------------------------------------------------------------


def _figures(config, xref, pages):
    """Build cross-references for figures."""
    fig_id_to_index = {}
    fig_id_to_slug = {}
    xref |= {
        "fig_id_to_index": fig_id_to_index,
        "fig_id_to_slug": fig_id_to_slug
    }

    for info in pages:
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
                err(config, "Badly-formatted figure ({info['src']}/{token.map[1]}).")

            if fig_id in fig_id_to_index:
                err(
                    config,
                    "Duplicate figure ID {fig_id} ({info['src']}/{token.map[1]}).",
                )

            current[1] += 1
            label = tuple(current)
            fig_id_to_index[fig_id] = label
            fig_id_to_slug[fig_id] = info["slug"]


def _headings(config, xref, pages):
    """Compile headings."""
    hd_id_to_index = {}
    hd_id_to_title = {}
    hd_id_to_slug = {}
    hd_index_to_id = {}
    xref |= {
        "hd_id_to_index": hd_id_to_index,
        "hd_id_to_title": hd_id_to_title,
        "hd_id_to_slug": hd_id_to_slug,
        "hd_index_to_id": hd_index_to_id,
    }

    for info in pages:
        label_stack = [info["major"]]
        info["major"] = str(info["major"])
        previous = None
        for token in info["tokens"]:
            if (previous is None) or (previous.type != "heading_open"):
                previous = token
                continue

            if token.type != "inline":
                raise McColeExc(
                    f"Unexpected token type {token.type} for heading{_line(token)}."
                )

            title, label = _heading_info(token)
            if not label:
                previous = token
                continue

            level = _heading_level(previous)
            index = _heading_index(config, info["src"], token, label_stack, level)

            if (label in hd_id_to_index) or (label in hd_id_to_title):
                err(
                    config,
                    f"Duplicate heading label {label} ({info['src']}/{_line(token)}).",
                )

            hd_id_to_index[label] = index
            hd_id_to_title[label] = title
            hd_id_to_slug[label] = info["slug"]
            hd_index_to_id[index] = label

            previous = token


def _heading_index(config, filename, token, stack, level):
    """Get the next heading level, adjusting `stack` as a side effect."""
    # Treat chapter titles specially.
    if level == 1:
        return tuple(str(i) for i in stack)

    # Moving up
    if level > len(stack):
        if level > len(stack) + 1:
            err(config, f"Heading {level} out of place ({filename}/{_line(token)})")
        while len(stack) < level:
            stack.append(1)

    # Same level
    elif level == len(stack):
        stack[-1] += 1

    # Going down
    else:
        while len(stack) > level:
            stack.pop()
        stack[-1] += 1

    # Report.
    return tuple(str(i) for i in stack)


def _heading_info(token):
    """Get title and label (or None) from token."""
    assert token.type == "inline"
    match = HEADING_ID.search(token.content)
    if not match:
        return None, None
    return match.group(1), match.group(3)


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


def _tables(config, xref, pages):
    """Build cross-references for tables."""
    tbl_id_to_index = {}
    tbl_id_to_slug = {}
    xref |= {
        "tbl_id_to_index": tbl_id_to_index,
        "tbl_id_to_slug": tbl_id_to_slug
    }

    for info in pages:
        current = [info["major"], 0]

        for token in info["tokens"]:
            if token.type != "html_block":
                continue

            match = TABLE_START.search(token.content)
            if not match:
                continue

            tbl_id = TABLE_ID.search(token.content).group(1)

            if tbl_id in tbl_id_to_index:
                err(
                    config,
                    f"Duplicate table ID on line ({info['src']}/{token.map[1]}).",
                )

            current[1] += 1
            label = tuple(current)
            tbl_id_to_index[tbl_id] = label
            tbl_id_to_slug[tbl_id] = info["slug"]
