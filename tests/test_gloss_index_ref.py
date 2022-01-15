"""Combined glossary+index references."""

import pytest

from mccole.html import md_to_html
from mccole.config import DEFAULTS, McColeExc


def test_gloss_index_ref_correctly_formatted():
    html = md_to_html(DEFAULTS, {}, "@gi{text:gloss:index}")
    assert (
        html.strip()
        == '<p><a href="gloss.html#gloss" index="index.html#index">text</a></p>'
    )


def test_gloss_index_ref_with_spaces():
    html = md_to_html(DEFAULTS, {}, "@gi{text: gloss\t:   index}")
    assert (
        html.strip()
        == '<p><a href="gloss.html#gloss" index="index.html#index">text</a></p>'
    )


def test_gloss_index_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@gi{:g:i}")


def test_gloss_index_ref_missing_gloss():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@gi{t::i}")


def test_gloss_index_ref_missing_index():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@gi{t:g:}")


def test_gloss_index_ref_too_few_fields():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@gi{t:g}")


def test_gloss_index_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, "@gi{t:g:i:x:y}")
