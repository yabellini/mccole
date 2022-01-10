from pathlib import Path
from textwrap import dedent

import pytest
from mistletoe import Document

from mccole.config import DEFAULTS, McColeExc
from mccole.fileio import read_files

from .util import create_files, dict_has_all


def test_find_nothing_when_nothing_present(fs):
    fs.create_dir("src")
    assert read_files(DEFAULTS, "src") == []


def test_collect_files(fs):
    create_files(fs, "src/a.png", "src/nested/b.md")
    files = read_files(DEFAULTS, "src")
    actual = {info["from"] for info in files}
    assert actual == {Path("src/a.png"), Path("src/nested/b.md")}


def test_exclude_unwanted_files(fs):
    create_files(fs, "src/a.md~", "src/nested/b.md")
    files = read_files(DEFAULTS, "src")
    actual = {info["from"] for info in files}
    assert actual == {Path("src/nested/b.md")}


def test_transform_filenames(fs):
    create_files(fs, "src/a.md", "src/b.jpg", "src/nested/c.md")
    config = DEFAULTS | {"dst": Path("/tmp/pages")}
    actual = read_files(config, "src")
    expected = [
        {
            "action": "transform",
            "from": Path("src/a.md"),
            "to": Path("/tmp/pages/src/a.html"),
        },
        {
            "action": "copy",
            "from": Path("src/b.jpg"),
            "to": Path("/tmp/pages/src/b.jpg"),
        },
        {
            "action": "transform",
            "from": Path("src/nested/c.md"),
            "to": Path("/tmp/pages/src/nested/c.html"),
        },
    ]
    assert len(actual) == len(expected)
    assert all(dict_has_all(e, a) for (e, a) in zip(expected, actual))


def test_get_no_frontmatter_for_copied_file(fs):
    contents = dedent(
        """\
        first line
        second line
        """
    )
    fs.create_file("src/a.png", contents=contents)
    actual = read_files(DEFAULTS, "src")
    assert len(actual) == 1
    assert "raw" not in actual[0]
    assert "headers" not in actual[0]
    assert "doc" not in actual[0]


def test_get_no_frontmatter_when_none_present(fs):
    contents = dedent(
        """\
        first line
        second line
        """
    )
    fs.create_file("src/a.md", contents=contents)
    actual = read_files(DEFAULTS, "src")
    assert len(actual) == 1
    assert actual[0]["raw"].rstrip() == contents.rstrip()
    assert actual[0]["header"] == {}
    assert isinstance(actual[0]["doc"], Document)
    assert len(actual[0]["doc"].children) > 0


def test_get_frontmatter_when_present(fs):
    contents = dedent(
        """\
        ---
        front: back
        ---
        first line
        second line
        """
    )
    fs.create_file("src/a.md", contents=contents)
    actual = read_files(DEFAULTS, "src")
    assert len(actual) == 1
    assert actual[0]["raw"].rstrip() == "first line\nsecond line"
    assert actual[0]["header"] == {"front": "back"}
    assert isinstance(actual[0]["doc"], Document)
    assert len(actual[0]["doc"].children) > 0


def test_get_no_frontmatter_when_absent(fs):
    contents = dedent(
        """\
        first line
        second line
        """
    )
    fs.create_file("src/a.md", contents=contents)
    actual = read_files(DEFAULTS, "src")
    assert len(actual) == 1
    assert actual[0]["raw"].rstrip() == "first line\nsecond line"
    assert actual[0]["header"] == {}
    assert isinstance(actual[0]["doc"], Document)
    assert len(actual[0]["doc"].children) > 0


def test_unreadable_file_to_convert(fs):
    fs.create_file("src/a.md", st_mode=0o000)
    with pytest.raises(McColeExc):
        read_files(DEFAULTS, "src")
