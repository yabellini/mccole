import pytest
from textwrap import dedent

from mccole.config import DEFAULTS
from mccole.files import md_to_doc
from mccole.gather import gather_data

from .util import dict_has_all


@pytest.fixture
def a_md():
    return {"action": "transform", "from": "a.md", "raw": "", "page": {}}


@pytest.fixture
def b_md():
    return {"action": "transform", "from": "b.md", "raw": "", "page": {}}


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
    expected = {
        "order": {"a.md": 1, "b.md": 2}
    }
    overall = gather_data(DEFAULTS, files)
    assert dict_has_all(expected, overall)


def test_find_bib_keys_none_in_document(a_md):
    md = dedent(
        """\
        # Title

        paragraph
        """
    )
    a_md["doc"] = md_to_doc(md)
    overall = gather_data(DEFAULTS, [a_md])
    assert overall["bibkeys"] == {}
