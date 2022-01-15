"""Section cross-references."""

import pytest

from mccole.fileio import md_to_doc
from mccole.gather import gather_data
from mccole.html import md_to_html
from mccole.config import DEFAULTS, McColeExc


def test_sec_ref_with_key_in_doc(a_md):
    text = "# @sec{t:Title}\n\npara @s{t}"
    a_md["doc"] = md_to_doc(text)
    xref = gather_data(DEFAULTS, [a_md])
    html = md_to_html(DEFAULTS, xref, text)
    assert '<a href="#t">Chapter&nbsp;1</a>' in html


def test_sec_ref_with_forward_key_in_doc(a_md):
    text = "# Title\n\npara @s{fwd}\n\n## @sec{fwd:Section}"
    a_md["doc"] = md_to_doc(text)
    xref = gather_data(DEFAULTS, [a_md])
    html = md_to_html(DEFAULTS, xref, text)
    assert '<a href="#fwd">Section&nbsp;1.1</a>' in html


def test_sec_ref_with_missing_key(a_md):
    text = "para @s{fwd}\n\n## @sec{something:Section}"
    a_md["doc"] = md_to_doc(text)
    xref = gather_data(DEFAULTS, [a_md])
    with pytest.raises(McColeExc):
        md_to_html(DEFAULTS, xref, text)
