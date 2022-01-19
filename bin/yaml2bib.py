#!/usr/bin/env python

import sys
import yaml

# ----------------------------------------------------------------------

def booktitle(entry):
    result = f"booktitle = {{{entry['booktitle']}}}"
    return result

def credits(entry, field="author"):
    names = entry[field]
    result = " and ".join(f"{n}" for n in names)
    return f"{field} = {{{result}}}"

def doi(entry):
    if "doi" not in entry:
        return None
    return f"doi = {{{entry['doi']}}}"

def isbn(entry):
    return f"isbn = {{{entry['isbn']}}}"

def month(entry):
    if "month" not in entry:
        return None
    return f"month = {{{entry['month']}}}"

def journal(entry):
    return f"journal = {{{entry['journal']}}}"

def number(entry):
    if "number" not in entry:
        return None
    return f"number = {{{entry['number']}}}"

def publisher(entry):
    if "publisher" not in entry:
        return None
    return f"publisher = {{{entry['publisher']}}}"

def title(entry):
    return f"title = {{{entry['title']}}}"

def url(entry):
    if "url" not in entry:
        return None
    return f"url = {{{entry['url']}}}"

def volume(entry):
    if "volume" not in entry:
        return None
    return f"volume = {{{entry['volume']}}}"

def year(entry):
    return f"year = {{{entry['year']}}}"

def show(*args):
    joined = ",\n".join([a for a in args if a])
    print(f"{joined}")
    print()

# ----------------------------------------------------------------------

def article(entry):
    show(
        f"@article{{{entry['key']},",
        credits(entry),
        title(entry),
        journal(entry),
        volume(entry),
        number(entry),
        month(entry),
        year(entry),
        publisher(entry),
        doi(entry),
        url(entry),
        "}"
    )

def book(entry):
    if "author" in entry:
        names = credits(entry)
    else:
        names = credits(entry, field="editor")
    show(
        f"@book{{{entry['key']}",
        names,
        title(entry),
        publisher(entry),
        year(entry),
        isbn(entry),
        "}"
    )

def incollection(entry):
    show(
        f"@incollection{{{entry['key']}",
        credits(entry),
        title(entry),
        credits(entry, field="editor"),
        booktitle(entry),
        year(entry),
        "}"
    )

def inproceedings(entry):
    show(
        f"@inproceedings{{{entry['key']}",
        credits(entry),
        title(entry),
        booktitle(entry),
        month(entry),
        year(entry),
        publisher(entry),
        doi(entry),
        url(entry),
        "}"
    )

def link(entry):
    show(
        f"@misc{{{entry['key']}",
        credits(entry),
        title(entry),
        year(entry),
        url(entry),
        "}"
    )

# ----------------------------------------------------------------------

if __name__ == "__main__":
    handlers = {    
        "article": article,
        "book": book,
        "incollection": incollection,
        "inproceedings": inproceedings,
        "link": link
    }
    for entry in yaml.safe_load(sys.stdin):
        try:
            handlers[entry["kind"]](entry)
        except Exception as exc:
            print("FAIL", entry, exc, file=sys.stderr)
            sys.exit(1)
