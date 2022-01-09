#!/usr/bin/env python

"""Show mistletoe AST for document."""

import sys

from mistletoe import Document
from mistletoe.ast_renderer import ASTRenderer

if len(sys.argv) == 1:
    with ASTRenderer() as renderer:
        print(renderer.render(Document(sys.stdin)))

else:
    for filename in sys.argv[1:]:
        if len(sys.argv) > 2:
            print(f"==== {filename}")
        with open(filename, 'r') as reader:
            with ASTRenderer() as renderer:
                print(renderer.render(Document(sys.stdin)))
