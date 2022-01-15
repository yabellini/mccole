"""Bibliographic citations."""

import pytest

from mccole.config import McColeExc
from mccole.html import md_to_html


def test_bib_cite_with_no_keys():
    with pytest.raises(McColeExc):
        md_to_html("@b{}")


def test_bib_cite_with_one_key():
    html = md_to_html("@b{key}")
    assert html.strip() == '<p>[<a href="bib.html#key">key</a>]</p>'


def test_bib_cite_with_multiple_keys():
    html = md_to_html("@b{key1:key2}")
    assert (
        html.strip()
        == '<p>[<a href="bib.html#key1">key1</a>,<a href="bib.html#key2">key2</a>]</p>'
    )


def test_bib_cite_with_trailing_comma():
    with pytest.raises(McColeExc):
        md_to_html("@b{key:}")


def test_bib_cite_with_leading_comma():
    with pytest.raises(McColeExc):
        md_to_html("@b{:key}")
