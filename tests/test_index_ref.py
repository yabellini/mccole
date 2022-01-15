"""Index references."""

import pytest

from mccole.html import md_to_html
from mccole.config import DEFAULTS, McColeExc


def test_index_ref_correctly_formatted():
    html = md_to_html(DEFAULTS, {}, "@i{text:key}")
    assert html.strip() == '<p><a href="index.html#key">text</a></p>'


def test_index_ref_with_spaces():
    html = md_to_html(DEFAULTS, {}, "@i{ text   :\tkey }")
    assert html.strip() == '<p><a href="index.html#key">text</a></p>'


def test_index_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@i{:key}")


def test_index_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@i{text:}")


def test_index_ref_missing_both():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@i{:}")


def test_index_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@i{first:second:third}")
