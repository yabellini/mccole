"""Create cross-reference lookup."""

import logging


def cross_reference(config, chapters):
    """Create lookup tables for cross-references."""
    xref = {
        "heading_label_to_index": {},
        "heading_label_to_title": {},
        "heading_index_to_label": {},
        "figure_label_to_index": {},
        "table_label_to_index": {},
    }
    figure_refs = set()
    table_defs = set()

    for info in chapters:
        for token in info["tokens"]:
            _heading_definition(info, xref, token)
            _figure_definition(info, xref, token)
            _table_definition(info, xref, token)
            _figure_reference(figure_refs, token)
            _table_reference(table_refs, token)

    _check_defined_used("figures", xref["figure_label_to_index"], figure_refs)
    _check_defined_used("tables", xref["table_label_to_index"], table_refs)

    return xref


# ----------------------------------------------------------------------


def _check_defined_used(kind, defined, used):
    """Check that all labels are defined and used."""
    defined = set(defined.keys())
    for undefined in sorted(used - defined):
        logging.error(f"Undefined {kind} label {undefined}")
    for unused in sorted(defined - used):
        logging.warning(f"Unused {kind} label {unused}")


def _heading_definition(info, xref, token):
    pass


def _figure_definition(info, xref, token):
    pass


def _figure_reference(figure_refs, token):
    pass


def _table_definition(info, xref, token):
    pass


def _table_reference(table_refs, token):
    pass
