"""Patching the document."""

import re
from textwrap import dedent

import pytest

from mccole.config import DEFAULTS
from mccole.html import md_to_html
from mccole.util import McColeExc


def test_div_with_no_content():
    md = dedent(
        """\
        <div>

        </div>
        """
    )
    html = md_to_html(DEFAULTS, {}, md)
    assert "<div>" in html
    assert "</div>" in html


def test_div_with_attributes():
    md = dedent(
        """\
        <div class="blue" size="large">

        </div>
        """
    )
    html = md_to_html(DEFAULTS, {}, md)
    assert re.match(r'<div\s+class="blue"\s+size="large"\s*>', html)


def test_div_with_paragraph():
    md = dedent(
        """\
        <div>

        paragraph

        </div>
        """
    )
    html = md_to_html(DEFAULTS, {}, md)
    assert re.match(r"^\s*<div>\s*<p>paragraph</p>\s*</div>$", html, re.DOTALL)


def test_div_with_nested_div():
    md = dedent(
        """\
        <div>

        <div>

        paragraph

        </div>

        </div>
        """
    )
    html = md_to_html(DEFAULTS, {}, md)
    assert re.match(
        r"^\s*<div>\s*<div>\s*<p>paragraph</p>\s*</div>\s*</div>$", html, re.DOTALL
    )


def test_opening_div_with_no_closing_div():
    md = dedent(
        """\
        <div>

        paragraph
        """
    )
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, md)


def test_closing_div_with_no_opening_div():
    md = dedent(
        """\
        <div>

        paragraph

        </div>

        </div>
        """
    )
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {}, md)