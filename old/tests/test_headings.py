"""Heading enumeration."""

from textwrap import dedent

import pytest

from mccole.config import DEFAULTS
from mccole.fileio import md_to_doc
from mccole.gather import gather_data
from mccole.util import McColeExc


def test_label_no_headings(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md])
    assert xref["sec_lbl_to_seq"] == {}


def test_label_badly_formatted(a_md):
    a_md["doc"] = md_to_doc("# @sec{Title}")
    with pytest.raises(McColeExc):
        gather_data(DEFAULTS, [a_md])


def test_label_single_heading(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # @sec{title:Title}
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md])
    assert xref["sec_lbl_to_seq"] == {"title": (1,)}


def test_label_sub_heading(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # @sec{title:Title}
        ## @sec{section:Section}
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md])
    assert xref["sec_lbl_to_seq"] == {"title": (1,), "section": (1, 1)}


def test_label_multiple_headings(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # @sec{t:Title}
        ## @sec{a:Section A}
        ### @sec{a1:Section A.1}
        ### @sec{a2:Section A.2}
        ## @sec{b:Section B}
        ## @sec{c:Section C}
        ### @sec{c1:Section C.1}
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md])
    assert xref["sec_lbl_to_seq"] == {
        "t": (1,),
        "a": (1, 1),
        "a1": (1, 1, 1),
        "a2": (1, 1, 2),
        "b": (1, 2),
        "c": (1, 3),
        "c1": (1, 3, 1),
    }


def test_label_headings_with_filler(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # @sec{t:Title}

        para

        ## @sec{a:Section A}

        para

        ### @sec{a1:Section A.1}

        para

        ## @sec{b:Section B}

        para

        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md])
    assert xref["sec_lbl_to_seq"] == {
        "t": (1,),
        "a": (1, 1),
        "a1": (1, 1, 1),
        "b": (1, 2),
    }


def test_label_headings_multiple_docs(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # @sec{a-t:Title A}
        ## @sec{a-1:Section B}
        ## @sec{a-2:Section C}
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        # @sec{b-t:Title X}
        ## @sec{b-1:Section Y}
        ## @sec{b-2:Section Z}
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md, b_md])
    assert xref["sec_lbl_to_seq"] == {
        "a-t": (1,),
        "a-1": (1, 1),
        "a-2": (1, 2),
        "b-t": (2,),
        "b-1": (2, 1),
        "b-2": (2, 2),
    }


def test_label_headings_fails_out_of_order(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title
        ### Section A.1
        """
        )
    )
    with pytest.raises(McColeExc):
        gather_data(DEFAULTS, [a_md])


def test_label_headings_with_appendix(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
            # @sec{a:Title A}
            ## @sec{a-s:Section A1}
            """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
            # @sec{b:Title B}
            ## @sec{b-s:Section B1}
            """
        )
    )
    config = DEFAULTS | {"appendix": "b", "entries": ["a", "b"]}
    xref = gather_data(config, [a_md, b_md])
    print("XREF", xref["sec_lbl_to_seq"])
    assert xref["sec_lbl_to_seq"] == {
        "a": (1,),
        "a-s": (1, 1),
        "b": ("A",),
        "b-s": ("A", 1),
    }
