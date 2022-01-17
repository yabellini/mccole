"""Program configuration."""

from textwrap import dedent

import pytest

from mccole.config import DEFAULTS, MULTI_KEYS, SCALAR_KEYS, get_config
from mccole.util import McColeExc


def test_config_file_not_found(fs):
    with pytest.raises(McColeExc):
        get_config("test.yml")


def test_empty_config_file_handled(fs):
    fs.create_file("test.yml")
    actual = get_config("test.yml")
    assert all(actual[k] == DEFAULTS[k] for k in SCALAR_KEYS)
    assert all(actual[k] == set(DEFAULTS[k]) for k in MULTI_KEYS)


def test_config_file_parsed(fs):
    text = dedent(
        """
        first: second
        third:
        - 4
        - 5
        """
    )
    fs.create_file("test.yml", contents=text)
    actual = get_config("test.yml")
    assert all(actual[k] == DEFAULTS[k] for k in SCALAR_KEYS)
    assert all(actual[k] == set(DEFAULTS[k]) for k in MULTI_KEYS)
    assert actual["first"] == "second"
    assert actual["third"] == {4, 5}


def test_config_file_overlay(fs):
    text = dedent(
        """
    src: changed
    transform:
    - "*.md"
    - "*.markdown"
    """
    )
    fs.create_file("test.yml", contents=text)
    actual = get_config("test.yml")
    assert actual["src"] == "changed"
    assert actual["transform"] == {"*.md", "*.markdown"}
