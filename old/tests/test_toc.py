"""Generating tables of contents."""

import pytest

from mccole.config import DEFAULTS, McColeExc
from mccole.html import md_to_html


def test_toc_fails_when_spec_is_empty():
    with pytest.raises(McColeExc):
        md_to_html({}, {}, "@toc{}")


def test_toc_fails_when_spec_is_non_numeric():
    with pytest.raises(McColeExc):
        md_to_html({}, {}, "@toc{abc}")


def test_toc_fails_when_spec_missing_first_element():
    with pytest.raises(McColeExc):
        md_to_html({}, {}, "@toc{:3}")


def test_toc_fails_when_spec_missing_second_element():
    with pytest.raises(McColeExc):
        md_to_html({}, {}, "@toc{1:}")


def test_toc_fails_when_spec_has_too_many_elements():
    with pytest.raises(McColeExc):
        md_to_html({}, {}, "@toc{1:2:3}")


def test_toc_with_single_entry():
    xref = {"toc": {(1,): {"label": "title", "text": "Chapter"}}}
    xref = {"seq_to_sec_lbl": {(1,): "title"}, "seq_to_sec_title": {(1,): "Chapter"}}
    html = md_to_html(DEFAULTS, xref, "@toc{1}")
    assert '<ul class="toc">\n<li><a href="#title">Chapter</a></li>\n</ul>' in html


def test_toc_to_depth_2():
    xref = {
        "seq_to_sec_lbl": {
            (1,): "a-title",
            (1, 1): "a-section",
            (1, 1, 1): "a-subsection",
            (2,): "b-title",
            (2, 1): "b-section",
            (2, 1, 1): "b-subsection",
        },
        "seq_to_sec_title": {
            (1,): "A Title",
            (1, 1): "A Section",
            (1, 1, 1): "A Subsection",
            (2,): "B Title",
            (2, 1): "B Section",
            (2, 1, 1): "B Subsection",
        },
    }
    html = md_to_html(DEFAULTS, xref, "@toc{2}")

    expected = (
        ("a-title", "A Title"),
        ("a-section", "A Section"),
        ("b-title", "B Title"),
        ("b-section", "B Section"),
    )
    for (lbl, title) in expected:
        line = f'<a href="#{lbl}">{title}</a>'
        assert line in html

    not_expected = (
        ("a-subsection", "A Subsection"),
        ("b-subsection", "B Subsection"),
    )
    for (lbl, title) in not_expected:
        assert f'<a href="#{lbl}">{title}</a>' not in html


def test_toc_depth_2_3():
    xref = {
        "seq_to_sec_lbl": {
            (1,): "a-title",
            (1, 1): "a-section",
            (1, 1, 1): "a-subsection",
            (2,): "b-title",
            (2, 1): "b-section",
            (2, 1, 1): "b-subsection",
        },
        "seq_to_sec_title": {
            (1,): "A Title",
            (1, 1): "A Section",
            (1, 1, 1): "A Subsection",
            (2,): "B Title",
            (2, 1): "B Section",
            (2, 1, 1): "B Subsection",
        },
    }
    html = md_to_html(DEFAULTS, xref, "@toc{2:3}")

    expected = (
        ("a-section", "A Section"),
        ("a-subsection", "A Subsection"),
        ("b-section", "B Section"),
        ("b-subsection", "B Subsection"),
    )
    for (lbl, title) in expected:
        line = f'<a href="#{lbl}">{title}</a>'
        assert line in html

    not_expected = (
        ("a-title", "A Title"),
        ("b-title", "B Title"),
    )
    for (lbl, title) in not_expected:
        assert f'<a href="#{lbl}">{title}</a>' not in html


def test_toc_depth_1_2():
    xref = {
        "seq_to_sec_lbl": {
            (1,): "a-title",
            (1, 1): "a-section",
            (1, 1, 1): "a-subsection",
            (1, 1, 1, 1): "a-subsubsection",
        },
        "seq_to_sec_title": {
            (1,): "A Title",
            (1, 1): "A Section",
            (1, 1, 1): "A Subsection",
            (1, 1, 1, 1): "A Subsubsection",
        },
    }
    html = md_to_html(DEFAULTS, xref, "@toc{1:2}")

    expected = (
        ("a-title", "A Title"),
        ("a-section", "A Section"),
    )
    for (lbl, title) in expected:
        line = f'<a href="#{lbl}">{title}</a>'
        assert line in html

    not_expected = (
        ("a-subsection", "A Subsection"),
        ("a-subsubsection", "B Subsubsection"),
    )
    for (lbl, title) in not_expected:
        assert f'<a href="#{lbl}">{title}</a>' not in html
