import pytest
from pathlib import Path

from mccole.util import DEFAULTS, McColeExc
from mccole.files import find_files

from .util import create_files


def test_find_nothing_when_nothing_present(fs):
    fs.create_dir('src')
    assert find_files(DEFAULTS, 'src') == ({}, {})


def test_collect_files_to_copy(fs):
    create_files(fs, 'src/a.png', 'src/nested/b.jpg')
    transform, copy = find_files(DEFAULTS, 'src')
    assert transform == {}
    assert set(copy.keys()) == {Path('src/a.png'), Path('src/nested/b.jpg')}


def test_collect_files_to_transform(fs):
    create_files(fs, 'src/a.md', 'src/nested/b.md')
    transform, copy = find_files(DEFAULTS, 'src')
    assert set(transform.keys()) == {Path('src/a.md'), Path('src/nested/b.md')}
    assert copy == {}


def test_exclude_unwanted_files(fs):
    create_files(fs, 'src/a.md~', 'src/nested/b.md')
    transform, copy = find_files(DEFAULTS, 'src')
    assert set(transform.keys()) == {Path('src/nested/b.md')}
    assert copy == {}


def test_sort_files(fs):
    create_files(fs, 'src/a.md~', 'src/nested/b.md', 'src/img/c.png')
    transform, copy = find_files(DEFAULTS, 'src')
    assert set(transform.keys()) == {Path('src/nested/b.md')}
    assert set(copy.keys()) == {Path('src/img/c.png')}
