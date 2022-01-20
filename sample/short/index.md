---
---

# Short {#short}

Self-reference: <a secref="short"/>.

Glossary: <span g="gloss_key">text</span>

Index: <span i="index term">text</span>

Glossary plus index: <span g="gloss_key" i="index term">text</span>

Index wrapping link: <span i="index term">[name][acorn]</span>

Citation: <cite>Oram2007</cite>.

## Section heading {#short-section}

Figure reference: <a figref="short-figure"/>

<figure id="short-figure">
  <img src="figures/short.svg" alt="Short caption" />
  <figcaption>Long version of short caption.</figcaption>
</figure>

Table reference: <span t="short-table"/>

<div class="table" id="short-table" cap="Short table caption.">
| Meaning | Selector |
| ------- | -------- |
| Element with tag `"elt"` | `elt`    |
| Element with `class="cls"` | `.cls`   |
| Element with `id="ident"` | `#ident`   |
| `child` element inside a `parent` element | `parent child` |
</div>
