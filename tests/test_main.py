import pytest
import yaml

from mccole.config import DEFAULTS
from mccole.mccole import mccole


@pytest.fixture
def default_config(fs):
    with open(DEFAULTS["config"], "w") as writer:
        yaml.dump(DEFAULTS, writer)
    return DEFAULTS


def test_main_with_no_files(fs, default_config):
    fs.create_dir(DEFAULTS["dst"])
    mccole([])