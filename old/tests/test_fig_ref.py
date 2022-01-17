"""Figure cross-references."""

import pytest

from mccole.config import DEFAULTS, McColeExc
from mccole.html import md_to_html


def test_fig_ref_found():
    html = md_to_html(DEFAULTS, {"fig_keys": {"key": (2, 3)}}, "@f{key}")
    assert html.strip() == '<p><a href="#key">Figure&nbsp;2.3</a></p>'


def test_fig_ref_not_found():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {"fig_keys": {"key": (2, 3)}}, "@f{other}")


def test_fig_ref_missing_key():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {"fig_keys": {"key": (2, 3)}}, "@f{}")


def test_fig_ref_multiple_keys():
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, {"fig_keys": {"key": (2, 3)}}, "@f{one:two}")
