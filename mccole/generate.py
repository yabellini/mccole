"""Generate pages, copying other files along the way."""

import logging
from pathlib import Path

from .translate import untokenize
from .util import LOGGER_NAME

# Directory permissions.
DIR_PERMS = 0o755

# Character encoding.
ENCODING = "utf-8"

# Where to report.
LOGGER = logging.getLogger(LOGGER_NAME)


def generate(config, xref, chapters):
    """Generate output for each chapter in turn, filling in cross-references."""
    for info in chapters:
        tokens = _transform(xref, info["tokens"])
        html = untokenize(tokens)
        _write_file(info["dst"], html)


def _transform(xref, tokens):
    """Transform a token stream using cross-reference information."""
    return tokens  # FIXME


def _write_file(dst, html):
    """Write a file, making directories if needed."""
    LOGGER.debug(f"Writing {dst}.")
    dst = Path(dst)
    dst.parent.mkdir(mode=DIR_PERMS, parents=True, exist_ok=True)
    dst.write_text(html, encoding=ENCODING)
