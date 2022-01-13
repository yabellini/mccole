"""Configuration."""

import os

import yaml

from .util import McColeExc

# Default configuration file name.
DEFAULT_CONFIG_NAME = "mccole.yml"

# Default location of configuration file.
DEFAULT_CONFIG_PATH = os.path.join(os.curdir, DEFAULT_CONFIG_NAME)

# Default configuration settings.
# Must use strings rather than Path objects for YAML persistence.
DEFAULTS = {
    "src": os.curdir,
    "dst": "_site",
    "transform": ["*.md"],
    "exclude": [DEFAULT_CONFIG_NAME, "*~"],
}

# Single-valued keys.
SCALAR_KEYS = {"dst", "src"}

# Multi-valued keys.
MULTI_KEYS = {"exclude", "transform"}


def get_config(filename):
    """Load configuration file."""
    try:
        config = DEFAULTS.copy()
        for key in MULTI_KEYS:
            config[key] = set(config[key])
        with open(filename, "r") as reader:
            loaded = yaml.safe_load(reader) or {}
            for key in loaded:
                if key in MULTI_KEYS:
                    config[key] |= set(loaded[key])
                elif isinstance(loaded[key], list):
                    config[key] = set(loaded[key])
                else:
                    config[key] = loaded[key]
        return config
    except OSError as exc:
        raise McColeExc(str(exc))
