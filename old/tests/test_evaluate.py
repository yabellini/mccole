"""Expression evaluation."""

from types import SimpleNamespace as SN

import pytest

from mccole.evaluate import create_env
from mccole.html import md_to_html
from mccole.util import McColeExc


@pytest.fixture
def basic_env():
    return create_env({"site": {"domain": "example.org"}, "page": {"title": "TITLE"}})


def test_create_env_empty():
    assert create_env({}) == {"site": SN(), "page": SN()}


def test_create_env_structured():
    original = {
        "site": {
            "logical": True,
            "multi": [5, 7, 9],
            "text": "text",
            "nested": {"key": "value"},
        }
    }
    expected = SN(logical=True, multi=[5, 7, 9], text="text", nested=SN(key="value"))
    assert create_env(original) == {"site": expected, "page": SN()}


def test_expr_constant_num_correct():
    html = md_to_html({}, {}, "@x{1}")
    assert html.strip() == "<p>1</p>"


def test_expr_constant_str_correct():
    html = md_to_html({}, {}, "@x{'this'}")
    assert html.strip() == "<p>this</p>"


def test_expr_arithmetic_correct():
    html = md_to_html({}, {}, "@x{2+3}")
    assert html.strip() == "<p>5</p>"


def test_expr_site_variable_correct(basic_env):
    html = md_to_html(basic_env, {}, "@x{site.domain}")
    assert html.strip() == "<p>example.org</p>"


def test_expr_page_variable_correct(basic_env):
    html = md_to_html(basic_env, {}, "@x{page.title}")
    assert html.strip() == "<p>TITLE</p>"


def test_expr_multiple_variables_correct(basic_env):
    md = "# @x{page.title}\nFound at @x{site.domain}."
    html = md_to_html(basic_env, {}, md)
    assert "<h1>TITLE</h1>" in html
    assert "<p>Found at example.org.</p>" in html


def test_expr_global_variable_not_found(basic_env):
    with pytest.raises(McColeExc):
        md_to_html({}, basic_env, "@x{missing}")


def test_expr_site_variable_not_found(basic_env):
    with pytest.raises(McColeExc):
        md_to_html({}, basic_env, "@x{site.missing}")


def test_expr_page_variable_not_found(basic_env):
    with pytest.raises(McColeExc):
        md_to_html({}, basic_env, "@x{page.missing}")
