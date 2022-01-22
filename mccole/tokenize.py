"""Turn chapters into tokens."""

import yaml

from .util import make_md


def tokenize(config):
    """Parse each file in turn."""
    md = make_md()
    links_table = _make_links_table(config)
    for info in config["pages"]:
        with open(info["src"], "r") as reader:
            text = reader.read()
            text += links_table
            info["tokens"] = md.parse(text)
            info["metadata"] = _get_metadata(info["tokens"])


# ----------------------------------------------------------------------


def _get_metadata(tokens):
    """Find and parse metadata (if present)."""
    for token in tokens:
        if token.type == "front_matter":
            return yaml.safe_load(token.content)
    return {}


def _make_links_table(config):
    """Make Markdown links table from configuration."""
    if "links" not in config:
        return ""

    return "\n\n" + "\n".join(f"[{ln['key']}]: {ln['url']}" for ln in config["links"])
