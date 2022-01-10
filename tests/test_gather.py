from textwrap import dedent

import pytest
from mistletoe import Document

from mccole.config import DEFAULTS, McColeExc
from mccole.gather import gather_data
from mccole.convert import md_to_doc

from .util import dict_has_all


@pytest.fixture
def a_md():
    return {
        "action": "transform",
        "from": "a.md",
        "raw": "",
        "header": {},
        "doc": Document([]),
    }


@pytest.fixture
def b_md():
    return {
        "action": "transform",
        "from": "b.md",
        "raw": "",
        "header": {},
        "doc": Document([]),
    }


def test_gather_order_no_files():
    files = []
    overall = gather_data(DEFAULTS, files)
    assert dict_has_all({"order": {}}, overall)


def test_gather_order_one_file(a_md):
    files = [a_md]
    overall = gather_data(DEFAULTS, files)
    assert dict_has_all({"order": {"a.md": 1}}, overall)


def test_gather_order_multiple_files(a_md, b_md):
    files = [a_md, b_md]
    expected = {"order": {"a.md": 1, "b.md": 2}}
    overall = gather_data(DEFAULTS, files)
    assert dict_has_all(expected, overall)


def test_find_bib_keys_none_in_document(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["bib_keys"] == {}


def test_find_bib_keys_several_in_document(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @b(key1:key2)

        **bold @b(key3)**
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["bib_keys"] == {"key1": {"a.md"}, "key2": {"a.md"}, "key3": {"a.md"}}


def test_find_bib_keys_in_multiple_documents(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @b(key1:key2)

        **bold @b(key3)**
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph @b(key3) and @b(key4)
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md, b_md])
    assert overall["bib_keys"] == {
        "key1": {"a.md"},
        "key2": {"a.md"},
        "key3": {"a.md", "b.md"},
        "key4": {"b.md"},
    }


def test_find_gloss_keys_in_multiple_documents(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @g(term:key1)

        **bold @g(term:key2)**
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph @g(term:key1) and @g(term:key3)
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md, b_md])
    assert overall["gloss_keys"] == {
        "key1": {"a.md", "b.md"},
        "key2": {"a.md"},
        "key3": {"b.md"},
    }


def test_find_index_keys_in_multiple_documents(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @i(term:key1)

        **bold @i(term:key2)**
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph @i(term:key1) and @i(term:key3)
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md, b_md])
    assert overall["index_keys"] == {
        "key1": {"a.md", "b.md"},
        "key2": {"a.md"},
        "key3": {"b.md"},
    }


def test_find_gloss_index_keys_in_multiple_documents(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @gi(term:gloss1:index1)

        **bold @gi(term:gloss2:index2)**
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph @gi(term:gloss1:index1) and @gi(term:gloss3:index3)
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md, b_md])
    assert overall["gloss_keys"] == {
        "gloss1": {"a.md", "b.md"},
        "gloss2": {"a.md"},
        "gloss3": {"b.md"},
    }
    assert overall["index_keys"] == {
        "index1": {"a.md", "b.md"},
        "index2": {"a.md"},
        "index3": {"b.md"},
    }


def test_enumerate_no_headings(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["labels"] == {"a.md": {}}


def test_enumerate_single_heading(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["labels"] == {"a.md": {(1,): "Title"}}


def test_enumerate_sub_heading(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title
        ## Section
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["labels"] == {"a.md": {(1,): "Title", (1,1): "Section"}}


def test_enumerate_multiple_headings(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title
        ## Section A
        ### Section A.1
        ### Section A.2
        ## Section B
        ## Section C
        ### Section C.1
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["labels"] == {"a.md": {
        (1,): "Title",
        (1,1): "Section A",
        (1,1,1): "Section A.1",
        (1,1,2): "Section A.2",
        (1,2): "Section B",
        (1,3): "Section C",
        (1,3,1): "Section C.1",
    }}


def test_enumerate_headings_with_filler(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        para

        ## Section A

        para

        ### Section A.1

        para

        ## Section B

        para

        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["labels"] == {"a.md": {
        (1,): "Title",
        (1,1): "Section A",
        (1,1,1): "Section A.1",
        (1,2): "Section B",
    }}


def test_enumerate_headings_multiple_docs(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title A
        ## Section B
        ## Section C
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title X
        ## Section Y
        ## Section Z
        """
        )
    )
    overall = gather_data(DEFAULTS, [a_md, b_md])
    assert overall["labels"] == {
        "a.md": {
            (1,): "Title A",
            (1,1): "Section B",
            (1,2): "Section C",
        },
        "b.md": {
            (2,): "Title X",
            (2,1): "Section Y",
            (2,2): "Section Z",
        }
    }


def test_enumerate_headings_fails_out_of_order(a_md):
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
