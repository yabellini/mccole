from textwrap import dedent

import pytest
from mistletoe import Document

from mccole.config import DEFAULTS
from mccole.gather import gather_data
from mccole.transform import md_to_doc

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
