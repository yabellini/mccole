"""Gathering data across files."""

import pytest

from mccole.config import DEFAULTS
from mccole.gather import gather_data

from .util import dict_has_all


def test_gather_order_no_files():
    files = []
    overall = gather_data(DEFAULTS, files)
    assert dict_has_all({"order": {}}, overall)


def test_gather_order_one_file(a_md):
    files = [a_md]
    overall = gather_data(DEFAULTS, files)
    assert dict_has_all({"order": {"a.md": 1}}, overall)


def test_gather_order_multiple_files(a_md, b_md):
    files = [a_md, b_md]
    expected = {"order": {"a.md": 1, "b.md": 2}}
    overall = gather_data(DEFAULTS, files)
    assert dict_has_all(expected, overall)
