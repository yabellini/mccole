"""Markdown conversion."""

from textwrap import dedent

from mccole.config import DEFAULTS
from mccole.html import md_to_html


def test_empty_doc_produces_no_html():
    assert md_to_html(DEFAULTS, {}, "") == ""


def test_h1_and_paragraph_becomes_html():
    md = dedent("# Title\nparagraph")
    html = md_to_html(DEFAULTS, {}, md)
    assert "<h1>Title</h1>" in html
    assert "<p>paragraph</p>" in html
