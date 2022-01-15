"""File I/O, including Markdown-to-Document conversion."""

from pathlib import Path
from textwrap import dedent

import pytest
from mistletoe import Document

from mccole.config import DEFAULTS, McColeExc
from mccole.fileio import read_files, write_files

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


def test_output_fails_with_unknown_action():
    with pytest.raises(McColeExc):
        write_files(DEFAULTS, {}, [{"action": "unknown"}])


def test_copy_fails_with_forbidden_directory(fs):
    fs.create_dir("dst", perm_bits=0o000)
    files = [{"action": "copy", "from": Path("a.txt"), "to": Path("dst/a.txt")}]
    with pytest.raises(McColeExc):
        write_files(DEFAULTS, {}, files)


def test_copy_single_file_successful(fs):
    fs.create_file("a.txt", contents="contents")
    fs.create_dir(DEFAULTS["dst"])
    dst = Path(DEFAULTS["dst"]) / "a.txt"
    files = [{"action": "copy", "from": Path("a.txt"), "to": dst}]
    write_files(DEFAULTS, {}, files)
    assert dst.is_file()
    assert dst.read_text() == "contents"


def test_copy_single_file_fails_if_no_src_file(fs):
    fs.create_dir(DEFAULTS["dst"])
    files = [
        {"action": "copy", "from": Path("a.txt"), "to": Path(DEFAULTS["dst"]) / "a.txt"}
    ]
    with pytest.raises(McColeExc):
        write_files(DEFAULTS, {}, files)


def test_write_single_file_successful(fs):
    fs.create_dir(DEFAULTS["dst"])
    dst = Path(DEFAULTS["dst"]) / "a.html"
    files = [{"action": "transform", "from": "a.md", "to": dst, "raw": "# Title"}]
    write_files(DEFAULTS, {}, files)
    assert dst.read_text().rstrip() == "<h1>Title</h1>"


def test_write_fails_with_forbidden_directory(fs):
    fs.create_dir("dst", perm_bits=0o000)
    files = [
        {
            "action": "transform",
            "from": "a.md",
            "to": Path("dst/a.html"),
            "raw": "content",
        }
    ]
    with pytest.raises(McColeExc):
        write_files(DEFAULTS, {}, files)
