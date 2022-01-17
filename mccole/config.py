"""Manage program configuration."""

import os
import yaml

from .util import McColeExc


# Main filename for each chapter.
MAIN_SRC_FILE = "index.md"
MAIN_DST_FILE = "index.html"

# Where to look for configuration.
DEFAULT_CONFIG_FILE = "mccole.yml"

# Default configuration settings.
DEFAULTS = {
    "src": os.curdir,  # Process current directory.
    "dst": "_site",  # Write HTML to `_site`.
    "exclude": [  # Don't copy these.
        DEFAULT_CONFIG_FILE,
        ".git",
        "*~",
    ],
}


def get_config(filename):
    """Read configuration file."""
    try:
        with open(filename, "r") as reader:
            loaded = yaml.safe_load(reader) or {}
        return DEFAULTS | loaded

    except OSError as exc:
        raise McColeExc(str(exc))
