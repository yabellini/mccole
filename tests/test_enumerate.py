"""Flat enumerations within chapters."""

import pytest
from textwrap import dedent

from mccole.fileio import md_to_doc
from mccole.gather import gather_data
from mccole.config import DEFAULTS, McColeExc


def test_enumerate_fig_defs_no_figures(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title
        paragraph
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["fig_defs"] == {}


def test_enumerate_fig_defs_one_figure(a_md):
    a_md["doc"] = md_to_doc("@fig{label:file:alt:cap}")
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["fig_defs"] == {"label": (1, 1)}


def test_enumerate_fig_defs_multiple_files(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title
        @fig{first:file:alt:cap}
        @fig{second:file:alt:cap}
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        @fig{third:file:alt:cap}
        paragraph
        @fig{fourth:file:alt:cap}
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md, b_md])
    assert overall["fig_defs"] == {
        "first": (1, 1),
        "second": (1, 2),
        "third": (2, 1),
        "fourth": (2, 2),
    }


def test_enumerate_fig_defs_duplicate_label(a_md):
    a_md["doc"] = md_to_doc("@fig{label:a:b:c} @fig{label:d:e:f}")
    with pytest.raises(McColeExc):
        gather_data(DEFAULTS, [a_md])



def test_enumerate_tbl_defs_no_tables(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title
        paragraph
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["tbl_defs"] == {}


def test_enumerate_tbl_defs_one_table(a_md):
    a_md["doc"] = md_to_doc("@tbl{label:file:cap}")
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["tbl_defs"] == {"label": (1, 1)}


def test_enumerate_tbl_defs_multiple_files(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title
        @tbl{first:file:cap}
        @tbl{second:file:cap}
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        @tbl{third:file:cap}
        paragraph
        @tbl{fourth:file:cap}
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md, b_md])
    assert overall["tbl_defs"] == {
        "first": (1, 1),
        "second": (1, 2),
        "third": (2, 1),
        "fourth": (2, 2),
    }


def test_enumerate_tbl_defs_duplicate_label(a_md):
    a_md["doc"] = md_to_doc("@tbl{label:a:b:c} @tbl{label:d:e:f}")
    with pytest.raises(McColeExc):
        gather_data(DEFAULTS, [a_md])
