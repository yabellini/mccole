"""Patterns in input files."""

import re

FIGURE_REF = re.compile(r'<a\s+figure="(.+?)"\s*/>')
SECTION_REF = re.compile(r'<a\s+section="(.+?)"\s*/>')
TABLE_REF = re.compile(r'<a\s+table="(.+?)"\s*/>')

GLOSS_DEF = re.compile(r'<span\s+g="(.+?)">')
INDEX_DEF = re.compile(r'<span\s+i="(.+?)">')
GLOSS_INDEX_DEF = re.compile(r'<span\s+g="(.+?)"\s+i="(.+?)">')

HEADING_KEY = re.compile(r"\{\#(.+?)\}")

BIBLIOGRAPHY = re.compile(r'<div\s+class="bibliography"\s*/>')

FIGURE = re.compile(r'<figure\s+id="(.+?)"\s*>\s*.+?</figure>', re.DOTALL)
FIGURE_SRC = re.compile(r'<img\b.+?src="(.+?)".+?>')
FIGURE_ALT = re.compile(r'<img\b.+?src="(.+?)".+?>')
FIGURE_CAP = re.compile(r"<figcaption>(.+?)</figcaption>")

TABLE_START = re.compile(r'<div.+?class="table"')
TABLE_LBL = re.compile(r'id="(.+?)"')
TABLE_CAP = re.compile(r'cap="(.+?)"')
TABLE_BODY = re.compile(r"<div.+?>\n(.+)\n</div>", re.DOTALL)
