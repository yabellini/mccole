from textwrap import dedent

import pytest

from mccole.convert import md_to_doc, md_to_html
from mccole.util import McColeExc


def test_empty_doc_produces_no_html():
    assert md_to_html("") == ""


def test_h1_and_paragraph_becomes_html():
    md = dedent(
        """\
        # Title
        paragraph
        """
    )
    html = md_to_html(md)
    assert "<h1>Title</h1>" in html
    assert "<p>paragraph</p>" in html


def test_bib_cite_with_no_keys():
    with pytest.raises(McColeExc):
        md_to_html("@b()")


def test_bib_cite_with_one_key():
    html = md_to_html("@b(key)")
    assert html.strip() == '<p>[<a href="bib.html#key">key</a>]</p>'


def test_bib_cite_with_multiple_keys():
    html = md_to_html("@b(key1:key2)")
    assert (
        html.strip()
        == '<p>[<a href="bib.html#key1">key1</a>,<a href="bib.html#key2">key2</a>]</p>'
    )


def test_bib_cite_with_trailing_comma():
    with pytest.raises(McColeExc):
        md_to_html("@b(key:)")


def test_bib_cite_with_leading_comma():
    with pytest.raises(McColeExc):
        md_to_html("@b(:key)")


def test_gloss_ref_correctly_formatted():
    html = md_to_html("@g(text:key)")
    assert html.strip() == '<p><a href="gloss.html#key">text</a></p>'


def test_gloss_ref_with_spaces():
    html = md_to_html("@g( text   :\tkey )")
    assert html.strip() == '<p><a href="gloss.html#key">text</a></p>'


def test_gloss_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html("@g(:key)")


def test_gloss_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html("@g(text:)")


def test_gloss_ref_missing_both():
    with pytest.raises(McColeExc):
        md_to_html("@g(:)")


def test_gloss_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html("@g(first:second:third)")


def test_index_ref_correctly_formatted():
    html = md_to_html("@i(text:key)")
    assert html.strip() == '<p><a href="index.html#key">text</a></p>'


def test_index_ref_with_spaces():
    html = md_to_html("@i( text   :\tkey )")
    assert html.strip() == '<p><a href="index.html#key">text</a></p>'


def test_index_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html("@i(:key)")


def test_index_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html("@i(text:)")


def test_index_ref_missing_both():
    with pytest.raises(McColeExc):
        md_to_html("@i(:)")


def test_index_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html("@i(first:second:third)")


def test_gloss_index_ref_correctly_formatted():
    html = md_to_html("@gi(text:gloss:index)")
    assert (
        html.strip()
        == '<p><a href="gloss.html#gloss" index="index.html#index">text</a></p>'
    )


def test_gloss_index_ref_with_spaces():
    html = md_to_html("@gi(text: gloss\t:   index)")
    assert (
        html.strip()
        == '<p><a href="gloss.html#gloss" index="index.html#index">text</a></p>'
    )


def test_gloss_index_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html("@gi(:g:i)")


def test_gloss_index_ref_missing_gloss():
    with pytest.raises(McColeExc):
        md_to_html("@gi(t::i)")


def test_gloss_index_ref_missing_index():
    with pytest.raises(McColeExc):
        md_to_html("@gi(t:g:)")


def test_gloss_index_ref_too_few_fields():
    with pytest.raises(McColeExc):
        md_to_html("@gi(t:g)")


def test_gloss_index_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html("@gi(t:g:i:x:y)")
