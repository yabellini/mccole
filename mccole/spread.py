"""Spread information back across files."""

from .util import visit


def spread_data(config, files):
    """Spread data across every file that is being transformed."""
    for info in files:
        visit(info["from"], info["doc"], rewrite, config)


def rewrite(path, node, config):
    """Rewrite special values in this node."""
    pass
