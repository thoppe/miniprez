from miniprez import inline_markdown
from nose.tools import assert_equal

P = inline_markdown.Inline_Markdown_Paser()


def test_bold():
    a = "This is **bold** text"
    b = "This is <strong>bold</strong> text"
    assert_equal(P(a), b)


def test_emph():
    a = "This is _italic_ text"
    b = "This is <em>italic</em> text"
    assert_equal(P(a), b)


def test_code():
    P = inline_markdown.Inline_Markdown_Paser()
    a = "This is `code` text"
    b = "This is <code>code</code> text"
    assert_equal(P(a), b)


def test_strongred():
    P = inline_markdown.Inline_Markdown_Paser()
    a = "This is *strongred* text"
    b = 'This is <strong style="color:#c23">strongred</strong> text'
    assert_equal(P(a), b)


def test_link():
    a = "This is a [link](https://www.google.com)"
    b = 'This is a <a href="https://www.google.com">link</a>'
    assert_equal(P(a), b)


def test_emoji():
    a = "This is :coffee:"
    b = u'This is \u2615'
    assert_equal(P(a), b)


def test_fontawesome():
    a = "This is ::coffee::"
    b = 'This is <i aria-hidden="true" class="fa fa-coffee"></i>'
    assert_equal(P(a), b)


def test_equation():
    a = "This, $\frac{x^2}{y}$ is math."
    b = u'This, <div class="equation" data-expr="\x0crac{x^2}{y}"></div> is math.'
    assert_equal(P(a), b)
