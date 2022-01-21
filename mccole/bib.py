"""Handle bibliography."""

import re

import bibtexparser


def bib_keys(config):
    """Return all citation keys."""
    if "bib_data" not in config:
        return set()
    return {entry["ID"] for entry in config["bib_data"]}


def bib_to_html(config):
    """Create HTML version of bibliography data."""
    entries = [_bib_to_html(e) for e in config["bib_data"]]
    return "\n".join(['<div class="bibliography">', "\n".join(entries), "</div>"])


def load_bib(config):
    """Read bibliography file if there is one."""
    if "bib" in config:
        with open(config["bib"], "r") as reader:
            config["bib_data"] = bibtexparser.load(reader).entries
    else:
        config["bib_data"] = {}


# ----------------------------------------------------------------------


def _bib_to_html(entry):
    """Convert bibliography entry to HTML."""
    kind = entry["ENTRYTYPE"]
    key = entry["ID"]
    content = HANDLERS[kind](entry)
    content = "".join(c for c in content if c is not None)
    return f'<p id="{key}" class="bib"><span class="bib">{key}</span>: {content}</p>'


def _article(entry):
    return [
        _credits(entry),
        ": ",
        _title(entry, quote=True),
        " ",
        _journal(entry),
        _volnum(entry, prefix=", "),
        _date(entry),
        _publisher(entry),
        _doi(entry, prefix=", "),
        _url(entry, prefix=", "),
        ".",
    ]


def _book(entry):
    if "author" in entry:
        names = _credits(entry)
    else:
        names = _credits(entry, field="editor")
    return [
        names,
        ": ",
        _title(entry, emph=True),
        " ",
        _publisher(entry),
        ", ",
        _date(entry),
        ", ",
        _isbn(entry),
        ".",
    ]


def _incollection(entry):
    return [
        _credits(entry),
        ": ",
        _title(entry, quote=True),
        ". In ",
        _credits(entry, field="editor"),
        ", ",
        _booktitle(entry, emph=True),
        ", ",
        _publisher(entry),
        ", ",
        _date(entry),
        _isbn(entry, prefix=", "),
        ".",
    ]


def _inproceedings(entry):
    return [
        _credits(entry),
        ": ",
        _title(entry, quote=True),
        ". In ",
        _booktitle(entry, emph=True),
        ", ",
        _date(entry),
        _publisher(entry, prefix=", "),
        ", ",
        _doi(entry),
        _url(entry, prefix=", "),
        ".",
    ]


def _misc(entry):
    return [
        _credits(entry),
        ": ",
        _title(entry, quote=True),
        " ",
        _date(entry),
        ", ",
        _url(entry),
        ".",
    ]


HANDLERS = {
    "article": _article,
    "book": _book,
    "incollection": _incollection,
    "inproceedings": _inproceedings,
    "misc": _misc,
}


def _booktitle(entry, quote=False, emph=False):
    if quote:
        return f'"{entry["booktitle"]}"'
    if emph:
        return f"<cite>{entry['booktitle']}</cite>"
    return entry["booktitle"]


SPLIT_NAMES = re.compile(r"\band\b")


def _credits(entry, field="author"):
    names = [n.strip() for n in SPLIT_NAMES.split(entry[field])]
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f", and {names[-1]}"


MONTH = {
    "1": "Jan",
    "2": "Feb",
    "3": "Mar",
    "4": "Apr",
    "5": "May",
    "6": "Jun",
    "7": "Jul",
    "8": "Aug",
    "9": "Sep",
    "10": "Oct",
    "11": "Nov",
    "12": "Dec",
}


def _date(entry):
    if "year" not in entry:
        return None
    if "month" not in entry:
        return entry["year"]
    return f"{MONTH[entry['month']]} {entry['year']}"


def _doi(entry):
    return entry.get("doi", None)


def _isbn(entry, prefix=None):
    return _with_prefix(entry, "isbn", prefix)


def _journal(entry):
    return entry["journal"]


def _publisher(entry, prefix=None):
    return _with_prefix(entry, "publisher", prefix)


def _title(entry, quote=False, emph=False):
    if quote:
        return f'"{entry["title"]}"'
    if emph:
        return f"<cite>{entry['title']}</cite>"
    return entry["title"]


def _url(entry, prefix=None):
    return _with_prefix(entry, "url", prefix)


def _volnum(entry):
    if "volume" not in entry:
        return None
    if "number" not in entry:
        return entry["volume"]
    return f"{entry['volume']}({entry['number']})"


def _with_prefix(entry, key, prefix):
    result = entry.get(key, None)
    if result is None:
        return result
    elif prefix is None:
        return result
    else:
        return f"{prefix} {result}"
