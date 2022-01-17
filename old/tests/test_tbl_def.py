"""Table definitions."""

import pytest

from mccole.config import DEFAULTS, McColeExc
from mccole.html import md_to_html


def test_tbl_def_correctly_formatted():
    html = md_to_html(DEFAULTS, {}, "@tbl{label:file:cap}")
    assert all(
        x in html
        for x in [
            '<table id="label">',
            "file",
            "<caption>cap</caption>",
            "</table>",
        ]
    )


def test_tbl_def_with_spaces():
    html = md_to_html(DEFAULTS, {}, "@tbl{ label\t:\tfile : cap  }")
    assert all(
        x in html
        for x in [
            '<table id="label">',
            "file",
            "<caption>cap</caption>",
            "</table>",
        ]
    )


def test_tbl_def_missing_label():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@tbl{:file:cap}")


def test_tbl_def_missing_file():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@tbl{label::cap}")


def test_tbl_def_missing_cap():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@tbl{label:file:}")


def test_tbl_def_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@tbl{label:file:cap:something}")
