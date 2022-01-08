"""Configuration."""

import os
from pathlib import Path

import yaml

from mccole.util import McColeExc

# Default configuration settings.
DEFAULTS = {
    "config": Path(os.curdir) / "mccole.yml",
    "dst": Path("_site"),
    "src": Path(os.curdir),
    "transform": ["*.md"],
    "exclude": ["*~"],
}


def get_config(filename):
    """Load configuration file."""
    try:
        with open(filename, "r") as reader:
            result = yaml.safe_load(reader)
            return {} if (result is None) else result
    except OSError as exc:
        raise McColeExc(str(exc))
