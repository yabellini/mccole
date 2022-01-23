"""Manage program configuration."""

import os
from glob import glob

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
    "exclude": [DEFAULT_CONFIG_FILE, ".git", "*~", ".DS_Store"],  # Don't copy these.
}


def get_config(options):
    """Read configuration file."""
    try:
        with open(options.config, "r") as reader:
            config = yaml.safe_load(reader) or {}
            config = DEFAULTS | config

            if "dst" in options:
                config["dst"] = options.dst
            if "links" in config:
                config["links"] = _read_links(config["links"])
            if "src" in options:
                config["src"] = options.src

            return config

    except OSError as exc:
        raise McColeExc(str(exc))


def load_templates(config):
    """Load page templates."""
    config["template"] = {}
    for filename in glob("_template/*.html"):
        label = os.path.basename(filename)
        with open(filename, "r") as reader:
            config["template"][label] = reader.read()


def _read_links(filename):
    """Read YAML links file for later use."""
    with open(filename, "r") as reader:
        return yaml.safe_load(reader)
