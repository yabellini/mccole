#!/usr/bin/env python

"""Show token stream."""

import sys

from markdown_it import MarkdownIt
from mdit_py_plugins.deflist import deflist_plugin
from mdit_py_plugins.front_matter import front_matter_plugin


def make_parser():
    return (
        MarkdownIt("commonmark")
        .enable("table")
        .use(front_matter_plugin)
        .use(deflist_plugin)
    )


text = sys.stdin.read()
md = make_parser()
depth = 0

print("-" * 40)
for token in md.parse(text):
    if token.nesting < 0:
        depth += token.nesting
    content = token.content if token.content else "--empty--"
    children = None
    if token.children is not None:
        children = ", ".join(
            f"{child.type}[{child.content}]" for child in token.children
        )
    print(f"{'  ' * depth}{token.type}/{token.tag}: {content}: {children}")
    if token.nesting > 0:
        depth += token.nesting

print("-" * 40)
for token in md.parse(text):
    if token.type == "html_block":
        print(token.content)
