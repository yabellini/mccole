from textwrap import dedent

import pytest

from mccole.convert import doc_to_html, md_to_doc, md_to_html
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


# ----------------------------------------------------------------------


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


# ----------------------------------------------------------------------


def test_gloss_ref_correctly_formatted():
    html = md_to_html("@g{text:key}")
    assert html.strip() == '<p><a href="gloss.html#key">text</a></p>'


def test_gloss_ref_with_spaces():
    html = md_to_html("@g{ text   :\tkey }")
    assert html.strip() == '<p><a href="gloss.html#key">text</a></p>'


def test_gloss_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html("@g{:key}")


def test_gloss_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html("@g{text:}")


def test_gloss_ref_missing_both():
    with pytest.raises(McColeExc):
        md_to_html("@g{:}")


def test_gloss_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html("@g{first:second:third}")


# ----------------------------------------------------------------------


def test_index_ref_correctly_formatted():
    html = md_to_html("@i{text:key}")
    assert html.strip() == '<p><a href="index.html#key">text</a></p>'


def test_index_ref_with_spaces():
    html = md_to_html("@i{ text   :\tkey }")
    assert html.strip() == '<p><a href="index.html#key">text</a></p>'


def test_index_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html("@i{:key}")


def test_index_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html("@i{text:}")


def test_index_ref_missing_both():
    with pytest.raises(McColeExc):
        md_to_html("@i{:}")


def test_index_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html("@i{first:second:third}")


# ----------------------------------------------------------------------


def test_gloss_index_ref_correctly_formatted():
    html = md_to_html("@gi{text:gloss:index}")
    assert (
        html.strip()
        == '<p><a href="gloss.html#gloss" index="index.html#index">text</a></p>'
    )


def test_gloss_index_ref_with_spaces():
    html = md_to_html("@gi{text: gloss\t:   index}")
    assert (
        html.strip()
        == '<p><a href="gloss.html#gloss" index="index.html#index">text</a></p>'
    )


def test_gloss_index_ref_missing_text():
    with pytest.raises(McColeExc):
        md_to_html("@gi{:g:i}")


def test_gloss_index_ref_missing_gloss():
    with pytest.raises(McColeExc):
        md_to_html("@gi{t::i}")


def test_gloss_index_ref_missing_index():
    with pytest.raises(McColeExc):
        md_to_html("@gi{t:g:}")


def test_gloss_index_ref_too_few_fields():
    with pytest.raises(McColeExc):
        md_to_html("@gi{t:g}")


def test_gloss_index_ref_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html("@gi{t:g:i:x:y}")


# ----------------------------------------------------------------------


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


# ----------------------------------------------------------------------


def test_fig_ref_found():
    html = md_to_html("@f{key}", {"fig_defs": {"key": (2, 3)}})
    assert html.strip() == '<p><a href="#key">Figure&nbsp;2.3</a></p>'


def test_fig_ref_not_found():
    with pytest.raises(McColeExc):
        md_to_html("@f{other}", {"fig_defs": {"key": (2, 3)}})


def test_fig_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html("@f{}", {"fig_defs": {"key": (2, 3)}})


def test_fig_ref_multiple_keys():
    with pytest.raises(McColeExc):
        md_to_html("@f{one:two}", {"fig_defs": {"key": (2, 3)}})


# ----------------------------------------------------------------------


def test_tbl_def_correctly_formatted():
    html = md_to_html("@tbl{label:file:cap}")
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
    html = md_to_html("@tbl{ label\t:\tfile : cap  }")
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
        md_to_html("@tbl{:file:cap}")


def test_tbl_def_missing_file():
    with pytest.raises(McColeExc):
        md_to_html("@tbl{label::cap}")


def test_tbl_def_missing_cap():
    with pytest.raises(McColeExc):
        md_to_html("@tbl{label:file:}")


def test_tbl_def_too_many_fields():
    with pytest.raises(McColeExc):
        md_to_html("@tbl{label:file:cap:something}")


# ----------------------------------------------------------------------


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


# ----------------------------------------------------------------------


def test_two_stage_conversion():
    doc = md_to_doc("# Title")
    html = doc_to_html(doc)
    assert html.rstrip() == "<h1>Title</h1>"
