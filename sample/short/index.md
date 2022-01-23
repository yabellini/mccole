---
template: page.html
---

# Short {#short}

<div class="toc" level="2" />

Self-reference: <a section="short-section"/>.

Cross-references: <a section="file-backup"/> and <a section="unit-test-structure"/>.

Glossary: <span g="gloss_key">text</span>

Index: <span i="index term">text</span>

Glossary plus index: <span g="gloss_key" i="index term">text</span>

Index wrapping link: <span i="index term">[name][acorn]</span>

Citation: <cite>Oram2007</cite>.

> ### Blockquote
>
> This is a paragraph.
>
> So is this.

1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item
1. item

Long enough to wrap around.
Long enough to wrap around.
Long enough to wrap around.
Long enough to wrap around.
Long enough to wrap around.
Long enough to wrap around.
Long enough to wrap around.
Long enough to wrap around.

File inclusion:

<div class="include" file="test.py" />

Keep alpha:

<div class="include" file="test.txt" keep="alpha" />

Erase beta:

<div class="include" file="test.txt" erase="beta" />

Keep beta erase gamma:

<div class="include" file="test.txt" keep="beta" erase="gamma" />

Multi-inclusion of `.py` and `.out`

<div class="include" pat="multi.*" fill="py out" />

```python
for word in code:
    print f"{word} is formatted"
```

## Section heading {#short-section}

Figure reference: <a figure="short-figure"/>

<figure id="short-figure">
  <img src="figures/short.svg" alt="Short caption" />
  <figcaption>Long version of short caption.</figcaption>
</figure>

Table reference: <a table="short-table"/>

<div class="table" id="short-table" cap="Short table caption.">
| Meaning | Selector |
| ------- | -------- |
| Element with tag `"elt"` | `elt`    |
| Element with `class="cls"` | `.cls`   |
| Element with `id="ident"` | `#ident`   |
| `child` element inside a `parent` element | `parent child` |
</div>
