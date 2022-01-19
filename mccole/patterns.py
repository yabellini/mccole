"""Patterns in input files."""

import re


BIBLIOGRAPHY = re.compile(r'<div\s+class="bibliography"\s*/>')
FIG_REF = re.compile(r'<a\s+figref="(.+?)"\s*/>')
HEADING_KEY = re.compile(r'\{\#(.+?)\}')
SEC_REF = re.compile(r'<a\s+secref="(.+?)"\s*/>')
