"""Cross-references to tables."""

import pytest

from mccole.config import McColeExc
from mccole.html import md_to_html


def test_tbl_ref_found():
    html = md_to_html("@t{key}", {"tbl_defs": {"key": (2, 3)}})
    assert html.strip() == '<p><a href="#key">Table&nbsp;2.3</a></p>'


def test_tbl_ref_not_found():
    with pytest.raises(McColeExc):
        md_to_html("@t{other}", {"tbl_defs": {"key": (2, 3)}})


def test_tbl_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html("@t{}", {"tbl_defs": {"key": (2, 3)}})


def test_tbl_ref_multiple_keys():
    with pytest.raises(McColeExc):
        md_to_html("@t{one:two}", {"tbl_defs": {"key": (2, 3)}})
