"""Testing utilities."""


def create_files(fs, *names):
    """Create a bunch of files."""
    for name in names:
        fs.create_file(name)


def dict_has_all(required, actual):
    return all(actual[k] == required[k] for k in required)
