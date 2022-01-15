"""Figure definitions."""

import pytest

from mccole.config import McColeExc
from mccole.html import md_to_html


def test_fig_def_correctly_formatted():
    html = md_to_html("@fig{label:file:alt:cap}")
    assert html.strip() == "".join(
        [
            "<p>",
            '<figure id="label">',
            '<img src="file" alt="alt"/>',
            "<figcaption>cap</figcaption>",
            "</figure>",
            "</p>",
        ]
    )


def test_fig_def_with_spaces():
    html = md_to_html("@fig{ label : file : \t alt \t : cap  }")
    assert all(
        x in html
        for x in [
            '<figure id="label">',
            '<img src="file" alt="alt"/>',
            "<figcaption>cap</figcaption>",
            "</figure>",
        ]
    )


def test_fig_def_missing_label():
    with pytest.raises(McColeExc):
        md_to_html("@fig{:file:alt:cap}")


def test_fig_def_missing_file():
    with pytest.raises(McColeExc):
        md_to_html("@fig{label::alt:cap}")


def test_fig_def_missing_alt():
    with pytest.raises(McColeExc):
        md_to_html("@fig{label:file::cap}")


def test_fig_def_missing_cap():
    with pytest.raises(McColeExc):
        md_to_html("@fig{label:file:alt:}")


def test_fig_def_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html("@fig{label:file:alt:cap:something}")
