def create_files(fs, *names):
    for name in names:
        fs.create_file(name)
