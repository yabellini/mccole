"""Generate a glossary."""

import re

import yaml

from .util import make_md

MULTISPACE = re.compile(r"\s+", re.DOTALL)


def gloss_keys(config):
    """Return all glossary entry keys."""
    return {entry["key"] for entry in config["gloss_data"]}


def gloss_to_html(config):
    """Convert glossary data to HTML."""
    lang = config["lang"]
    internal = {entry["key"]:entry[lang]["term"] for entry in config["gloss_data"]}
    entries = [_gloss_to_markdown(entry, lang, internal) for entry in config["gloss_data"]]
    text = "\n\n".join(entries)
    md = make_md()
    html = md.render(text)
    return html


def load_gloss(config):
    """Read glossary file if there is one."""
    if "gloss" in config:
        with open(config["gloss"], "r") as reader:
            config["gloss_data"] = yaml.safe_load(reader)
    else:
        config["gloss_data"] = {}


# ----------------------------------------------------------------------


def _gloss_to_markdown(entry, lang, internal):
    """Convert single glossary entry to Markdown."""
    first = f'<span class="glosskey" id="{entry["key"]}">{entry[lang]["term"]}</span>'

    if "acronym" in entry[lang]:
        first += f" ({entry[lang]['acronym']})"

    body = MULTISPACE.sub(entry[lang]["def"], " ")

    if "ref" in entry:
        refs = [f"[{internal[key]}](#{key})" for key in entry["ref"]]
        body += f"<br/>See also: {', '.join(refs)}."

    result = f"{first}\n:   {body}"
    return result
