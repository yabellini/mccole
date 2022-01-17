"""Testing fixtures."""

import pytest
from mistletoe import Document


@pytest.fixture
def a_md():
    return {
        "action": "transform",
        "from": "a/index.md",
        "raw": "",
        "header": {},
        "doc": Document([]),
    }


@pytest.fixture
def b_md():
    return {
        "action": "transform",
        "from": "b/index.md",
        "raw": "",
        "header": {},
        "doc": Document([]),
    }
