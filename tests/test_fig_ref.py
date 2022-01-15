"""Figure cross-references."""

import pytest

from mccole.config import McColeExc
from mccole.html import md_to_html


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
