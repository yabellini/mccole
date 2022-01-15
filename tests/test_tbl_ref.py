"""Cross-references to tables."""

import pytest

from mccole.config import DEFAULTS, McColeExc
from mccole.html import md_to_html


def test_tbl_ref_found():
    xref = {"tbl_keys": {"key": (2, 3)}}
    html = md_to_html(DEFAULTS, xref, "@t{key}")
    assert html.strip() == '<p><a href="#key">Table&nbsp;2.3</a></p>'


def test_tbl_ref_not_found():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {"tbl_keys": {"key": (2, 3)}}, "@t{other}")


def test_tbl_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {"tbl_keys": {"key": (2, 3)}}, "@t{}")


def test_tbl_ref_multiple_keys():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {"tbl_keys": {"key": (2, 3)}}, "@t{one:two}")
