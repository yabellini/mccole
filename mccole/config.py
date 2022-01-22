"""Manage program configuration."""

from glob import glob
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
        ".DS_Store"
    ],
}


def get_config(filename):
    """Read configuration file."""
    try:
        with open(filename, "r") as reader:
            config = yaml.safe_load(reader) or {}
            config = DEFAULTS | config
            if "links" in config:
                config["links"] = _read_links(config["links"])
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
