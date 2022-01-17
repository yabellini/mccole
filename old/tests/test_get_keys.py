"""Getting keys from cross-references."""

from textwrap import dedent

from mccole.config import DEFAULTS
from mccole.fileio import md_to_doc
from mccole.gather import gather_data


def test_get_bib_keys_none_in_document(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md])
    assert xref["bib_keys"] == {}


def test_get_bib_keys_in_one_document(a_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @b{key1:key2}

        **bold @b{key3}**
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md])
    assert xref["bib_keys"] == {
        "key1": {"a/index.md"},
        "key2": {"a/index.md"},
        "key3": {"a/index.md"},
    }


def test_get_bib_keys_in_multiple_documents(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @b{key1:key2}

        **bold @b{key3}**
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph @b{key3} and @b{key4}
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md, b_md])
    assert xref["bib_keys"] == {
        "key1": {"a/index.md"},
        "key2": {"a/index.md"},
        "key3": {"a/index.md", "b/index.md"},
        "key4": {"b/index.md"},
    }


def test_get_gloss_keys_in_multiple_documents(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @g{term:key1}

        **bold @g{term:key2}**
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph @g{term:key1} and @g{term:key3}
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md, b_md])
    assert xref["gloss_keys"] == {
        "key1": {"a/index.md", "b/index.md"},
        "key2": {"a/index.md"},
        "key3": {"b/index.md"},
    }


def test_get_index_keys_in_multiple_documents(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @i{term:key1}

        **bold @i{term:key2}**
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph @i{term:key1} and @i{term:key3}
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md, b_md])
    assert xref["index_keys"] == {
        "key1": {"a/index.md", "b/index.md"},
        "key2": {"a/index.md"},
        "key3": {"b/index.md"},
    }


def test_get_gloss_index_keys_in_multiple_documents(a_md, b_md):
    a_md["doc"] = md_to_doc(
        dedent(
            """\
        # Title

        paragraph @gi{term:gloss1:index1}

        **bold @gi{term:gloss2:index2}**
        """
        )
    )
    b_md["doc"] = md_to_doc(
        dedent(
            """\
        paragraph @gi{term:gloss1:index1} and @gi{term:gloss3:index3}
        """
        )
    )
    xref = gather_data(DEFAULTS, [a_md, b_md])
    assert xref["gloss_keys"] == {
        "gloss1": {"a/index.md", "b/index.md"},
        "gloss2": {"a/index.md"},
        "gloss3": {"b/index.md"},
    }
    assert xref["index_keys"] == {
        "index1": {"a/index.md", "b/index.md"},
        "index2": {"a/index.md"},
        "index3": {"b/index.md"},
    }
