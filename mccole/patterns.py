"""Patterns in input files."""

import re


FIG_REF = re.compile(r'<a\s+figref="(.+?)"\s*/>')
HEADING_KEY = re.compile(r'\{\#(.+?)\}')
SEC_REF = re.compile(r'<a\s+secref="(.+?)"\s*/>')
