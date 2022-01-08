"""Configuration."""

import os
from pathlib import Path

import yaml

from mccole.util import McColeExc

# Default configuration settings.
DEFAULTS = {
    "config": Path(os.curdir) / "mccole.yml",
    "src": Path(os.curdir),
    "dst": Path("_site"),
    "transform": ["*.md"],
    "exclude": ["*~"],
}


def get_config(filename):
    """Load configuration file."""
    try:
        with open(filename, "r") as reader:
            loaded = yaml.safe_load(reader) or {}
            return DEFAULTS | loaded
    except OSError as exc:
        raise McColeExc(str(exc))
