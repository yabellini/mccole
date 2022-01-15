"""Glossary cross-references."""

import pytest

from mccole.html import md_to_html
from mccole.config import DEFAULTS, McColeExc


def test_gloss_ref_correctly_formatted():
    html = md_to_html(DEFAULTS, {}, "@g{text:key}")
    assert html.strip() == '<p><a href="gloss.html#key">text</a></p>'


def test_gloss_ref_with_spaces():
    html = md_to_html(DEFAULTS, {}, "@g{ text   :\tkey }")
    assert html.strip() == '<p><a href="gloss.html#key">text</a></p>'


def test_gloss_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@g{:key}")


def test_gloss_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@g{text:}")


def test_gloss_ref_missing_both():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@g{:}")


def test_gloss_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@g{first:second:third}")
