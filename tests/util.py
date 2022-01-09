def create_files(fs, *names):
    """Create a bunch of files."""
    for name in names:
        fs.create_file(name)


def dict_has_all(expected, actual):
    return all(actual[k] == expected[k] for k in expected)
