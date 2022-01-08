from pathlib import Path

from mccole.config import DEFAULTS
from mccole.files import find_files

from .util import create_files


def test_find_nothing_when_nothing_present(fs):
    fs.create_dir("src")
    assert find_files(DEFAULTS, "src") == []


def test_collect_files(fs):
    create_files(fs, "src/a.png", "src/nested/b.md")
    files = find_files(DEFAULTS, "src")
    actual = {info["from"] for info in files}
    assert actual == {Path("src/a.png"), Path("src/nested/b.md")}


def test_exclude_unwanted_files(fs):
    create_files(fs, "src/a.md~", "src/nested/b.md")
    files = find_files(DEFAULTS, "src")
    actual = {info["from"] for info in files}
    assert actual == {Path("src/nested/b.md")}


def test_transform_filenames(fs):
    create_files(fs, "src/a.md", "src/b.jpg", "src/nested/c.md")
    config = DEFAULTS | {"dst": Path("/tmp/pages")}
    files = find_files(config, "src")
    assert files == [
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
