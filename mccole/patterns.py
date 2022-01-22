"""Patterns in input."""

import re

# Cross-references are `<a type="key"/>`
FIGURE_REF = re.compile(r'<a\s+figure="(.+?)"\s*/>')
SECTION_REF = re.compile(r'<a\s+section="(.+?)"\s*/>')
TABLE_REF = re.compile(r'<a\s+table="(.+?)"\s*/>')

# Bibliographic citations are `<cite>key,key</cite>`.
CITE = re.compile(r"<cite>")

# Definitions are `<span g="key">text</span>` for glossary terms,
# `<span i="key">text</span>` for indexing terms,
# and `<span g="key" i="other_key">text</span>` for both.
GLOSS_DEF = re.compile(r'<span\s+g="(.+?)">')
INDEX_DEF = re.compile(r'<span\s+i="(.+?)">')
GLOSS_INDEX_DEF = re.compile(r'<span\s+g="(.+?)"\s+i="(.+?)">')

# Headings are `## Text {#key}`.
HEADING_KEY = re.compile(r"\s*(.+?)\s*\{\#(.+?)\}")

# `<div class="bibliography"/>` and `<div class="glossary"/>`
# show where the bibliography and glossary should go.
BIBLIOGRAPHY = re.compile(r'<div\s+class="bibliography"\s*/>')
GLOSSARY = re.compile(r'<div\s+class="glossary"\s*/>')

# `<div class="include" ...parameters... />`
INCLUSION = re.compile(r'<div\s+class="include"(.*?)/>')

# Figures are:
# <figure id="key">
#   <img src="file" alt="short"/>
#   <figcaption>long</figcaption>
# </figure>
FIGURE = re.compile(r'<figure\s+id="(.+?)"\s*>\s*.+?</figure>', re.DOTALL)
FIGURE_SRC = re.compile(r'<img\b.+?src="(.+?)".+?>')
FIGURE_ALT = re.compile(r'<img\b.+?alt="(.+?)".+?>')
FIGURE_CAP = re.compile(r"<figcaption>(.+?)</figcaption>")

# Since there isn't a way to add an ID to a Markdown table, they are:
# <div class="table" id="key" cap="caption">
# ...Markdown table...
# </div>
TABLE_START = re.compile(r'<div.+?class="table"')
TABLE_LBL = re.compile(r'id="(.+?)"')
TABLE_CAP = re.compile(r'cap="(.+?)"')
TABLE_BODY = re.compile(r"<div.+?>\n(.+)\n</div>", re.DOTALL)
