"""File transformation tools."""

from mccole.util import McColeExc


def gather_data(config, files):
    """Collect cross-reference data from ASTs."""
    pass


def parse_files(config, files):
    """Load Markdown."""
    for info in files:
        try:
            with open(info["from"], "r") as reader:
                info["raw"] = reader.read()
        except OSError as exc:
            raise McColeExc(str(exc))


def transform_files(config, files):
    """Convert to HTML."""
    for info in files:
        info["cooked"] = info["raw"]
