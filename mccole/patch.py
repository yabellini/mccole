"""Patch divs in the mistletoe parse tree."""

import re

from mistletoe.block_token import BlockToken, HTMLBlock

from .util import McColeExc


class Div(BlockToken):
    """Represent a div elements with attributes and children."""

    # Match a well-formed 'div' with attributes.
    DIV_PAT = re.compile(r'<div((\s+\w+=".+?"\s*)*)>')

    # Match an attribute within a 'div' tag.
    ATTR_PAT = re.compile(r'(\w+)="(.+?)"')

    def __init__(self, attributes, children):
        """Save data for later rendering."""
        self.attributes = attributes
        self.children = children


def patch_divs(node):
    """Patch <div> elements in document in-place."""
    stack = [[]]

    for child in node.children:
        if _is_div_start(child):
            stack.append([child])

        elif _is_div_end(child):
            if len(stack) <= 1:
                raise McColeExc("</div> without opening <div>")
            saved = stack.pop()
            stack[-1].append(_make_div(saved[0], saved[1:]))

        else:
            stack[-1].append(child)

    if len(stack) > 1:
        raise McColeExc("<div> without closing </div>")

    node.children = stack[0]
    return node


def _make_div(start, children):
    """Create a 'div' node with the given children."""
    match = Div.DIV_PAT.match(start.content)
    attributes = {x.group(1): x.group(2) for x in Div.ATTR_PAT.finditer(match.group(1))}
    return Div(attributes, children)


def _is_div_start(node):
    """Does this node start a div?"""
    return isinstance(node, HTMLBlock) and node.content.startswith("<div")


def _is_div_end(node):
    """Does this node end a div?"""
    return isinstance(node, HTMLBlock) and node.content.startswith("</div>")
