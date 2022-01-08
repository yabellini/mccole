from textwrap import dedent

import pytest

from mccole.config import get_config
from mccole.util import McColeExc


def test_config_file_not_found(fs):
    with pytest.raises(McColeExc):
        get_config("test.yml")


def test_empty_config_file_handled(fs):
    fs.create_file("test.yml")
    assert get_config("test.yml") == {}


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
    assert actual["first"] == "second"
    assert actual["third"] == [4, 5]
