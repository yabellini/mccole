# McCole: A Very Simple Publishing System

The authors of technical books often use an unholy combination of
a [static site generator][ssg],
[Pandoc][pandoc],
[LaTeX][latex],
and some home-brewed scripts to create both web and print versions of their work.
McCole is an attempt to create something simpler:
it doesn't do nearly as much as any of the tools just mentioned,
but it's smaller and less brittle.

## Setup

1.  Make sure you have Python 3.9 or higher.
    -   [optional] [Install conda][conda-install]
        and create a conda environment with `conda create -n mccole python=3.9`.
1.  Clone <https://github.com/gvwilson/mccole/> and go into the `mccole` directory.
1.  Install dependencies with `pip install -r requirements.txt`.
1.  Build the test project using `python -m mccole -C sample.
    -   You can now examine the generated files in `sample/_site`.
1.  Preview the test project using `python -m mccole -C sample -r 4000`.
    -   You can view the generated files on <http://localhost:4000>.
    -   Note: these files are *not* automatically regenerated as you edit them.
        If you make changes to the package or the source files,
	you must stop the server with <kbd>Ctrl-C</kdb> and restart it.
1.  To build and preview a project of your own, use
    <code>python -m mccole -s <em>/path/to/source</em> -d <em>/path/to/output</em> -r <em>port</em></code>
    (filling in the italicized portions).

## Command-Line Options

-   `-C` *dir* / `--chdir` *dir*: change working directory before running.
    -   All other paths are interpreted relative to this directory.

-   `-d` *dir* / `--dst` *dir*: specify destination (output) directory.

-   `-g` *file* / `--config` *file*: specify configuration file.
    -    The default is `mccole.yml` in the current working directory.

-   `-k` / `--keep`: keep pre-existing output files.
    -    By default McCole deletes the output directory and its contents at startup.

-   `-L` *level* / `--logging` *level*: set logging level to ``debug`, ``info`, ``warning`, ``error`, or `critical`.

-   `-r` *port* / `--run` *port*: run a server on the specified port after building the site.
    -    Use <kbd>Ctrl-C</kbd> to stop the server.

-   `-s` *dir* / `--src` *dir*: specify source (input) directory.

-   `-u` / `--unused`: warn about unused items (i.e., unreferenced figures or tables).

## Configuration File Options

The sample configuration file is:

```
copyrightyear: 2022
author: "Greg Wilson"
repo: https://github.com/gvwilson/mccole
tool: McCole

src: .
dst: _site
links: _data/links.yml
bib: _data/bibliography.bib
gloss: _data/glossary.yml
lang: en

copy:
- "*/figures/*.svg"
- "*/figures/*.pdf"
- "static/*.*"
- "favicon.ico"

root: index.md
chapters:
- slug: "short"
- slug: "file-backup"
- slug: "unit-test"
- slug: "pattern-matching"
- slug: "bibliography"
  appendix: true
- slug: "glossary"
```

Its fields are:

-   `copyrightyear` [int]: The year to display in the copyright notice.

-   `author` [str]: The author name to display in the copyright notice.

-   `repo` [url]: Where to find the source of the project.

-   `tool` [str]: The name of the tool used to create the site (usually "McCole").

-   `src` [path]: The source directory relative to the current working directory.

-   `dst` [path]: The destination directory relative to the current working directory.

-   `links` [path]: The file containing links to be added to Markdown files (discussed below).

-   `bib` [path]: The file containing the [BibTeX][bibtex] bibliography for the book (discussed below).

-   `gloss` [path]: The file containing the [Glosario][glosario] glossary for the book (discussed below).

-   `lang` [str]: An [ISO 639-1][iso-lang-codes] language identifier.

-   `copy` [list of pattern]: A list of filename patterns identifying files to copy verbatim.

-   `root` [path]: The path to the book's home page (typically "index.md").

-   `chapters` [list of object]: Descriptions of the chapters and appendices to include:
    -   `slug` [str]: The key identifying the chapter or appendix.
        McCole process a file called <code><em>slug</em>/index.md</code> for the chapter or appendix.
    -   `appendix` [optional bool]: `true` if this is the first appendix, absent otherwise.

-   `exclude` [optional list of pattern]: A list of filename patterns identifying files that are *not* copied.
    -   The default ignores `.git`, `.DS_Store`, and common editor backup files.

## Syntax

McCole uses [CommonMark][commonmark] with extensions.
(In our defense, *everyone* adds extensions…)

### Page Structure, Headings, and References

Chapters and appendices should start with:

-   YAML front-matter, which must specify the page template in the `_template` directory.
-   A level-1 heading with an ID that matches the chapter slug.
-   Optionally, a table of contents.
    `level="2"` specifies that only level-2 headings within this page are to be shown.

```
---
template: page.html
---

# Short {#short}

<div class="toc" level="2" />
```

Level-2 headings should be written as shown below;
please use the chapter slug as the first part of the ID in `{#…}`.

```
## Section heading {#short-section}
```

To refer to a chapter, appendix, or section, use:

```
Cross-reference: <a section="short-section"/>.
```

Do *not* include `#` in the `section` attribute's value.

### Figures and Tables

Create figures like this:

```
<figure id="short-figure">
  <img src="figures/short.svg" alt="Short caption" />
  <figcaption>Long version of short caption.</figcaption>
</figure>
```

-   The `id` can be used in cross-references (discussed below).
    Please use the chapter slug as the first part.

-   The `src` specifies the relative path from the chapter directory to the image file.
    For consistency, please put figures in a `figures` sub-directory in each chapter,
    and please use SVG format.

-   The `alt` field should contain short alternative text to identify the figure.

-   The `figcaption` element should contain a longer caption.
    Do not include numbering: this is added automatically.

Create tables like this:

```
<div class="table" id="short-table" cap="Short table caption.">
| Meaning | Selector |
| ------- | -------- |
| Element with tag `"elt"` | `elt`    |
| Element with `class="cls"` | `.cls`   |
| Element with `id="ident"` | `#ident`   |
| `child` element inside a `parent` element | `parent child` |
</div>
```

-   The `id` can be used in cross-references (discussed below).
    Please use the chapter slug as the first part.

-   The `cap` attribute should contain a longer caption.
    Do not include numbering: this is added automatically.

-   The body of the table is written in Markdown, not HTML.

### Other References

-   Use <cite>Key1,Key2</cite> to create bibliographic citations.
    (This is an abuse of the `cite` tag,
    which is supposed to be used for the titles of works rather than references to them,
    but McCole cleans this up when generating HTML.)

-   Refer to a figure using `<a figure="short-figure"/>`
    (with the figure ID in place of `short-figure`).

-   Similarly, refer to a table using `<a table="short-table"/>`.

-   Use `<span g="gloss_key">text</span>` to link to a glossary entry,
    where `gloss_key` must be a key in the glossary (discussed below).

-   Use `<span i="index term">text</span>` to indicate text that should appear in the index
    (discussed below).

-   If a term is both a glossary entry and an index entry,
    use `<span g="gloss_key" i="index term">text</span>`.
    The `g` attribute must come before the `i` attribute.

-   Index and glossary indicators must go outside Markdown links,
    i.e., use `<span i="index term">[name][link-key]</span>`
    and *not* `[<span i="index term">name</span>][link-key]`.

### Callouts

Use a blockquote with a level-3 heading to create a callout:

```
> ### Callout Title
>
> This is a paragraph.
>
> So is this.
```

## File Inclusions

To include a text-file as a pre-formatted code block, use:

```
<div class="include" file="test.py" />
```

The `file` attribute specifies the path to the file to be included
relative to the chapter directory.

To include only a portion of a file, use:

<div class="include" file="test.txt" keep="alpha" />

where `alpha` identified the section of the file to keep;
the file must contain the markers `[alpha]` and `[/alpha]`.
For example, if the file is:

```
before alpha

[alpha]
alpha 1 of 2
alpha 2 of 2
[/alpha]

after alpha
```

then the displayed text will be:

```
alpha 1 of 2
alpha 2 of 2
```

If the file is a program, the markers can be placed in comments:

```
print("This is omitted")

# [selected]
print("This is kept")
# [/selected]

print("This is also omitted")
```

Note that only one marked section is kept (the first encountered).

To omit lines inside a marked section, use:

```
<div class="include" file="test.txt" erase="beta" />
```

The `keep` and `erase` attributes can be combined:
McCole will keep the lines indicated by the first attribute,
then erase lines within that section indicated by the second attribute.
For example, if the input file is:

```
before

[beta]
beta 1 before gamma

[gamma]
gamma 1 of 1
[/gamma]

beta 2 after gamma
[/beta]

after
```

then the directive:

<div class="include" file="test.txt" keep="beta" erase="gamma" />

will produce:

```
beta 1 before gamma


beta 2 after gamma
```

Finally, to include several files at once, use:

<div class="include" pat="multi.*" fill="py out" />

The `*` in the `pat` attribute is replaced with each fragment of `fill` in turn
to create actual filenames,
which are then included.
Multi-inclusion cannot be combined with `keep` or `erase`.

## The Bibliography

McCole expects a [BibTeX][bibtex] bibliography
because that's what users are most likely to have already
and because there is no open, widely-used alternative based on an easily-parsed format like YAML.
The BibTeX-to-HTML generator in `mccole/bib.py` only handles a subset of BibTeX at the moment.

## The Glossary

The glossary uses the [Glosario][glosario] format.

## Templates

McCole uses the files in `_template` as page templates.
Values are filled in using simple Python string formatting;
all of the HTML generated from a Markdown page is copied as one chunk.

## Links

All external links are defined in a YAML file (by default, `_data/links.yml`).
They are turned into a Markdown link table:

```
[key-1]: url-1
[key-2]: url-2
```

which is appended to every Markdown file during parsing.

## Implementation

McCole uses:

-   [markdown-it-py][markdown-it-py] to parse and render Markdown.

-   [bibtexparser][bibtexparser] to parse BibTeX bibliographies.

-   [paged.js][paged-js] for pagination (experimental).

The processing cycle is:

1.  Parse command-line options.

1.  Initialize logging and change working directory.

1.  Read the configuration file.
    -   Command-line options take precedence over configuration file values,
        which in turn take precedence over default values defined in `mccole/config.py`.

1.  Load the bibliography, glossary, and template files.

1.  Collect Markdown files to process based on the `root` and `chapters` fields of the configuration file.

1.  Turn each Markdown file into a markdown-it token stream.

1.  Search those token streams for cross-reference IDs (e.g., figure IDs)
    and give each a unique sequence number.

1.  Delete the output directory unless asked not to.

1.  Render the collected files by converting the markdown-it token streams back to HTML
    and filling in the page's template.
    -   As a side-effect, find figure and table IDs that aren't referenced anywhere.

1.  Copy non-Markdown files, such as figures and CSS style files.

1.  Display warnings and/or errors.

1.  Run a preview server if asked to.

## Colophon

This book is typeset in [Crimson][crimson-font].
McCole ("muh-COAL") is named after Robert McCole Wilson (1934-2015),
who taught me how to write
and that writing well is important.
Thanks, Dad.

<p align="center"><img src="./sample/static/mccole.jpg" alt="Robert McCole Wilson" /></p>

[bibtex]: http://www.bibtex.org/
[bibtexparser]: https://bibtexparser.readthedocs.io/
[commonmark]: https://commonmark.org/
[conda-install]: https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
[crimson-font]: https://www.1001fonts.com/crimson-font.html
[glosario]: https://glosario.carpentries.org/
[iso-lang-codes]: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
[latex]: https://www.latex-project.org/
[markdown-it-py]: https://markdown-it-py.readthedocs.io/
[paged-js]: https://www.pagedjs.org/
[pandoc]: https://pandoc.org/
[ssg]: https://jamstack.org/generators/
