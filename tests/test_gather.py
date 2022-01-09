import pytest

from mccole.config import DEFAULTS
from mccole.transform import gather_data


@pytest.fixture
def a_md():
    return {"action": "transform", "from": "a.md", "raw": "", "page": {}}


@pytest.fixture
def b_md():
    return {"action": "transform", "from": "b.md", "raw": "", "page": {}}


def test_gather_order_no_files():
    files = []
    overall = gather_data(DEFAULTS, files)
    assert overall == {
        "order": {}
    }


def test_gather_order_one_file(a_md):
    files = [a_md]
    overall = gather_data(DEFAULTS, files)
    assert overall == {
        "order": {"a.md": 1}
    }


def test_gather_order_multiple_files(a_md, b_md):
    files = [a_md, b_md]
    overall = gather_data(DEFAULTS, files)
    assert overall == {
        "order": {"a.md": 1, "b.md": 2}
    }
