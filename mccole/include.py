"""Handle file inclusion."""

import os


from .patterns import (
    INCLUSION_FILE,
    INCLUSION_KEEP,
    INCLUSION_ERASE,
    INCLUSION_KEEP_ERASE,
    INCLUSION_MULTI,
)
from .util import err, make_md


def inclusion_to_html(config, info, spec):
    """Handle a file inclusion."""
    for (pat, handler) in (
        (INCLUSION_FILE, _file),
        (INCLUSION_KEEP, _keep),
        (INCLUSION_ERASE, _erase),
        (INCLUSION_KEEP_ERASE, _keep_erase),
        (INCLUSION_MULTI, _multi),
    ):
        match = pat.search(spec)
        if match:
            return handler(config, info, match)
    err(config, f"Unrecognized inclusion spec '{spec}'.")
    return ""


# ----------------------------------------------------------------------


def _erase(config, info, match):
    """Handle an erasing file inclusion."""
    filename = _make_filename(info, match.group(1))
    kind = filename.split('.')[-1]
    key = match.group(2)
    with open(filename, "r") as reader:
        lines = reader.readlines()
        lines = _remove_lines(config, lines, key)
        return _make_html(lines, kind)


def _file(config, info, match):
    """Handle a simple file inclusion."""
    filename = _make_filename(info, match.group(1))
    kind = filename.split('.')[-1]
    with open(filename, "r") as reader:
        lines = reader.readlines()
        return _make_html(lines, kind)


def _keep(config, info, match):
    """Handle a sliced file inclusion."""
    filename = _make_filename(info, match.group(1))
    kind = filename.split('.')[-1]
    key = match.group(2)
    with open(filename, "r") as reader:
        lines = reader.readlines()
        lines = _select_lines(config, lines, key)
        return _make_html(lines, kind)


def _keep_erase(config, info, match):
    """Handle an inclusion that keeps some content but erases other."""
    filename = _make_filename(info, match.group(1))
    kind = filename.split('.')[-1]
    keep_key = match.group(2)
    erase_key = match.group(3)
    with open(filename, "r") as reader:
        lines = reader.readlines()
        lines = _select_lines(config, lines, keep_key)
        lines = _remove_lines(config, lines, erase_key)
        return _make_html(lines, kind)


def _multi(config, info, match):
    """Handle multiple file inclusion."""
    result = []
    pat = match.group(1)
    for fill in [s.strip() for s in match.group(2).split()]:
        filename = _make_filename(info, pat.replace("*", fill))
        kind = filename.split('.')[-1]
        with open(filename, "r") as reader:
            lines = reader.readlines()
            result.append(_make_html(lines, kind))
    return "\n\n".join(result)


# ----------------------------------------------------------------------


def _find_markers(lines, key):
    start = f"[{key}]"
    stop = f"[/{key}]"
    i_start = None
    i_stop = None
    for (i, line) in enumerate(lines):
        if start in line:
            i_start = i
        elif stop in line:
            i_stop = i
    return i_start, i_stop


def _make_filename(info, name):
    """Construct full path name."""
    return os.path.join(os.path.dirname(info["src"]), name)


def _make_html(lines, kind):
    """Construct HTML inclusion from lines."""
    body = "\n".join(x.rstrip() for x in lines)
    markdown = f"```{kind}\n{body}\n```"
    md = make_md()
    return md.render(markdown)


def _remove_lines(config, lines, key):
    """Remove lines between markers."""
    start, stop = _find_markers(lines, key)
    if start is None:
        err(config, f"Failed to match {start} / {stop}")
        return []
    return lines[:start] + lines[stop+1:]


def _select_lines(config, lines, key):
    """Select lines between markers."""
    start, stop = _find_markers(lines, key)
    if start is None:
        err(config, f"Failed to match {start} / {stop}")
        return []
    return lines[start+1:stop]
