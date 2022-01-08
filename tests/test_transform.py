from mccole.config import DEFAULTS
from mccole.transform import parse_files

def test_parse_empty(fs):
    fs.create_file("a.md", contents="")
    files = [{"from": "a.md"}]
    parse_files(DEFAULTS, files)
    assert "raw" in files[0]
    assert files[0]["raw"] == ""
