"""Patterns in input files."""

import re


BIBLIOGRAPHY = re.compile(r'<div\s+class="bibliography"\s*/>')
FIG_REF = re.compile(r'<a\s+figref="(.+?)"\s*/>')
HEADING_KEY = re.compile(r'\{\#(.+?)\}')
SEC_REF = re.compile(r'<a\s+secref="(.+?)"\s*/>')
TABLE_START = re.compile(r'<div.+?class="table"')

TABLE_LBL = re.compile(r'id="(.+?)"')
TABLE_CAP = re.compile(r'cap="(.+?)"')
TABLE_BODY = re.compile(r'<div.+?>\n(.+)\n</div>', re.DOTALL)
