"""Convert Markdown to other formats."""

from mistletoe import Document
from mistletoe.ast_renderer import ASTRenderer
from mistletoe.span_token import SpanToken

from .evaluate import create_env
from .util import EXTENSIONS


def create_output(config, files, converter):
    """Create output file content."""
    create_env(config)
    for info in files:
        if info["action"] == "transform":
            info["html"] = converter(info["doc"], config)


def md_to_doc(md):
    """Convert Markdown to plain mistletoe Document.

    Need the plain Document in order to find uses of special tags.
    """
    with ASTRenderer() as renderer:  # noqa F841
        return Document(md)


def _make_parser(class_name, tag, *fields):
    """Make a mistletoe-compatible parsing class."""

    class result(SpanToken):
        pattern = EXTENSIONS[tag]["re"]

        def __init__(self, match):
            values = EXTENSIONS[tag]["func"](match)
            if (len(fields) == 1) and (fields[0][0] == "*"):
                field = fields[0][1:]
                setattr(self, field, values)
            else:
                for (i, name) in enumerate(fields):
                    setattr(self, name, values[i])

    result.__name__ = class_name

    return result


class Expression(SpanToken):
    """Parse an `@x(...)` inline expression."""

    pattern = EXTENSIONS["@x"]["re"]

    def __init__(self, match):
        """Fill in fields during construction."""
        self.expr = EXTENSIONS["@x"]["func"](match)[0]


PARSERS = [
    _make_parser("BibCite", "@b", "*cites"),
    _make_parser("FigRef", "@f", "label"),
    _make_parser("GlossRef", "@g", "text", "key"),
    _make_parser("IndexRef", "@i", "text", "key"),
    _make_parser("GlossIndexRef", "@gi", "text", "gloss_key", "index_key"),
    _make_parser("TblRef", "@t", "label"),
    _make_parser("FigDef", "@fig", "label", "file", "alt", "cap"),
    _make_parser("TblDef", "@tbl", "label", "file", "cap"),
    Expression,
]
