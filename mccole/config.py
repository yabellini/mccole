"""Configuration."""

import os

import yaml

from .util import McColeExc

# Default configuration settings.
# Must use strings rather than Path objects for YAML persistence.
DEFAULTS = {
    "config": os.path.join(os.curdir, "mccole.yml"),
    "src": os.curdir,
    "dst": "_site",
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
