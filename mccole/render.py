"""Convert token streams to HTML."""

from markdown_it.presets import commonmark
from markdown_it.renderer import RendererHTML
from markdown_it.utils import OptionsDict

from .bib import bib_to_html
from .gloss import gloss_to_html
from .include import inclusion_to_html
from .patterns import (
    BIBLIOGRAPHY,
    CITE,
    FIGURE,
    FIGURE_REF,
    GLOSS_DEF,
    GLOSS_INDEX_DEF,
    GLOSSARY,
    HEADING_AND_KEY,
    INDEX_DEF,
    INCLUSION,
    SECTION_REF,
    TABLE_BODY,
    TABLE_CAP,
    TABLE_LBL,
    TABLE_REF,
    TABLE_START,
    TOC,
)
from .util import err, make_md


def render(config, xref, seen, info):
    """Turn token stream into HTML."""
    options = OptionsDict(commonmark.make()["options"])
    renderer = McColeRenderer(config, xref, seen, info)
    return renderer.render(info["tokens"], options, {})


# ----------------------------------------------------------------------


class McColeRenderer(RendererHTML):
    """Translate token stream to HTML."""

    def __init__(self, config, xref, seen, info):
        """Remember settings and cross-reference information."""
        super().__init__(self)
        self.config = config
        self.xref = xref
        self.seen = seen
        self.info = info

    def heading_open(self, tokens, idx, options, env):
        """Add IDs to headings if requested."""
        inline = tokens[idx + 1]
        assert inline.type == "inline"
        for child in inline.children:
            if child.type == "text":
                match = HEADING_AND_KEY.search(child.content)
                if match:
                    heading_id = match.group(3)
                    child.content = child.content.replace(match.group(2), "")
                    tokens[idx].attrSet("id", heading_id)
        result = RendererHTML.renderToken(self, tokens, idx, options, env)
        return result

    def html_block(self, tokens, idx, options, env):
        """Look for special entries for bibliography, glossary, etc."""
        for (pat, method) in (
            (BIBLIOGRAPHY, self._bibliography),
            (FIGURE, self._figure),
            (GLOSSARY, self._glossary),
            (INCLUSION, self._inclusion),
            (TABLE_START, self._table),
            (TOC, self._toc),
        ):
            match = pat.search(tokens[idx].content)
            if match:
                return method(tokens, idx, options, env, match)
        return RendererHTML.renderToken(self, tokens, idx, options, env)

    def html_inline(self, tokens, idx, options, env):
        """Fill in span elements with cross-references."""
        for (pat, method) in (
            (CITE, self._cite),
            (FIGURE_REF, self._figure_ref),
            (GLOSS_DEF, self._gloss_def),
            (INDEX_DEF, self._index_def),
            (GLOSS_INDEX_DEF, self._gloss_index_def),
            (SECTION_REF, self._section_ref),
            (TABLE_REF, self._table_ref),
        ):
            match = pat.search(tokens[idx].content)
            if match:
                return method(tokens, idx, options, env, match)
        if tokens[idx].content == "</span>":
            return "</span>"
        return RendererHTML.renderToken(self, tokens, idx, options, env)

    def _bibliography(self, tokens, idx, options, env, match):
        """Generate a bibliography."""
        return bib_to_html(self.config)

    def _cite(self, tokens, idx, options, env, match):
        """Translate bibliographic citations."""
        assert tokens[idx + 1].type == "text"
        keys = [k.strip() for k in tokens[idx + 1].content.split(",")]
        self.seen["cite"].update(keys)
        refs = [f'<a href="../bibliography/#{k}">{k}</a>' for k in keys]
        # Get rid of `<cite>`, text, `</cite>`
        del tokens[idx : idx + 3]  # noqa e203
        return f"[{', '.join(refs)}]"

    def _figure(self, tokens, idx, options, env, match):
        """Generate a figure."""
        return tokens[idx].content

    def _figure_ref(self, tokens, idx, options, env, match):
        """Fill in figure reference."""
        key = match.group(1)
        self.seen["figure_ref"].add(key)
        label = self.xref["fig_lbl_to_index"].get(key, None)
        if label:
            label = ".".join(str(i) for i in label)
        else:
            label = "MISSING"
        return f'<a class="figref" href="{key}">Figure&nbsp;{label}</a>'

    def _glossary(self, tokens, idx, options, env, match):
        """Generate a glossary."""
        return gloss_to_html(self.config)

    def _gloss_def(self, tokens, idx, options, env, match):
        """Fill in glossary definition."""
        key = match.group(1)
        self.seen["gloss_ref"].add(key)
        return f'<span g="{key}">'

    def _gloss_index_def(self, tokens, idx, options, env, match):
        """Fill in glossary+index definition."""
        gloss_key = match.group(1)
        index_key = match.group(2)
        self.seen["gloss_ref"].add(gloss_key)
        self.seen["index_ref"].add(index_key)
        return f'<span g="{gloss_key}" i="{index_key}">'

    def _inclusion(self, tokens, idx, options, env, match):
        """Fill in file inclusion."""
        return inclusion_to_html(self.config, self.info, match.group(1))

    def _index_def(self, tokens, idx, options, env, match):
        """Fill in index definition."""
        key = match.group(1)
        return f'<span i="{key}">'

    def _section_ref(self, tokens, idx, options, env, match):
        """Fill in figure reference."""
        key = match.group(1)
        label = self.xref["heading_lbl_to_index"].get(key, None)
        if label:
            word = "Chapter" if label[0].isdigit() else "Appendix"
            label = ".".join(str(i) for i in label)
            fill = f"{word}&nbsp;{label}"
        else:
            fill = "MISSING"
        return f'<a class="secref" href="{key}">{fill}</a>'

    def _table(self, tokens, idx, options, env, match):
        """Parse a table nested inside a div."""
        content = tokens[idx].content
        lbl = TABLE_LBL.search(content).group(1)
        cap = TABLE_CAP.search(content).group(1)
        body = TABLE_BODY.search(content).group(1)
        opening = f'<table id="{lbl}">'
        closing = f"<caption>{cap}</caption>\n</table>"
        md = make_md()
        html = md.render(body)
        html = html.replace("<table>", opening).replace("</table>", closing)
        return html

    def _table_ref(self, tokens, idx, options, env, match):
        """Fill in table reference."""
        key = match.group(1)
        self.seen["table_ref"].add(key)
        label = self.xref["tbl_lbl_to_index"].get(key, None)
        if label:
            label = ".".join(str(i) for i in label)
        else:
            label = "MISSING"
        return f'<a class="tblref" href="{key}">Table&nbsp;{label}</a>'

    def _toc(self, tokens, idx, options, env, match):
        """Fill in table of contents."""
        level = int(match.group(1))
        if level == 1:
            slugs = [entry["slug"] for entry in self.config["pages"] if entry["major"] is not None]
            majors = [entry["major"] for entry in self.config["pages"]]
            titles = [self.xref["heading_lbl_to_title"][slug] for slug in slugs]
            combined = list(zip(slugs, majors, titles))
            refs = [f'<li value="{major}"><a href="./{slug}/">{title}</a></li>' for (slug, major, title) in combined]
            refs = "\n".join(refs)
            return f'<ol class="toc">\n{refs}\n</ol>'

        if level == 2:
            major = self.info["major"]
            indexes = [x for x in self.xref["heading_index_to_lbl"] if (x[0] == major) and (len(x) == 2)]
            labels = [self.xref["heading_index_to_lbl"][i] for i in indexes]
            titles = [self.xref["heading_lbl_to_title"][lbl] for lbl in labels]
            combined = list(zip(indexes, labels, titles))
            links = [f'<li><a href="#{label}">{title}</a></li>' for (index, label, title) in combined]
            links = "\n".join(links)
            html = f'<ol class="toc">\n{links}\n</ol>\n'
            return html

        err(config, f"Unknown table of contents level {level}.")
        return ""
