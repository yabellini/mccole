"""File transformation tools."""

from mistletoe import Document
from mistletoe.ast_renderer import ASTRenderer


def md_to_doc(md):
    """Convert Markdown to mistletoe Document."""
    with ASTRenderer() as renderer:  # noqa F841
        return Document(md)


def transform_files(config, files):
    """Convert to HTML."""
    for info in files:
        info["cooked"] = info["raw"]
