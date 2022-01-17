"""Test file reordering."""

import pytest

from mccole.config import DEFAULTS
from mccole.fileio import find_files
from mccole.util import McColeExc


@pytest.fixture
def dirs_and_files(fs):
    fs.create_dir("a")
    fs.create_file("a/index.md")
    fs.create_file("a/image.png")
    fs.create_dir("b")
    fs.create_file("b/index.md")
    fs.create_file("b/data.csv")


def test_reorder_with_no_ordering(fs, dirs_and_files):
    files = find_files(DEFAULTS, ".")
    expected = {"a/index.md", "a/image.png", "b/index.md", "b/data.csv"}
    assert {str(f["from"]) for f in files} == expected


def test_reorder_with_ordering(fs, dirs_and_files):
    config = DEFAULTS | {"entries": ["b", "a"]}
    files = find_files(config, ".")
    filenames = [str(f["from"]) for f in files]
    assert filenames[:2] == ["b/index.md", "a/index.md"]
    assert set(filenames[2:]) == {"a/image.png", "b/data.csv"}


def test_reorder_with_missing_files(fs, dirs_and_files):
    config = DEFAULTS | {"entries": ["b", "a", "c"]}
    with pytest.raises(McColeExc):
        find_files(config, ".")
