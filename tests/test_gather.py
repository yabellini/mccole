"""Gathering data across files."""

from mccole.config import DEFAULTS
from mccole.gather import gather_data

from .util import dict_has_all


def test_gather_order_no_files():
    files = []
    xref = gather_data(DEFAULTS, files)
    assert dict_has_all({"order": {}}, xref)


def test_gather_order_one_file(a_md):
    files = [a_md]
    xref = gather_data(DEFAULTS, files)
    assert dict_has_all({"order": {"a.md": 1}}, xref)


def test_gather_order_multiple_files(a_md, b_md):
    files = [a_md, b_md]
    expected = {"order": {"a.md": 1, "b.md": 2}}
    xref = gather_data(DEFAULTS, files)
    assert dict_has_all(expected, xref)
