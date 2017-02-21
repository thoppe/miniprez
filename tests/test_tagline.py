from miniprez.tagline import tagline
from miniprez.custom_tags import _registered_custom_tags

from nose.tools import assert_equal


def test_empty_section():
    T = tagline("----")
    assert_equal(T.text, "")
    assert_equal(len(T.tags), 1)
    assert_equal(T.tags[0]["name"], "section")
    assert_equal(str(T), "<section></section>")


def test_extra_dashes_in_section_header():
    T1 = tagline("----")
    T2 = tagline("----------")
    assert_equal(T1, T2)


def test_simple_header():
    T1 = tagline("@h1 big dog")
    out = "<h1><text>big dog</text></h1>"
    assert_equal(str(T1), out)


def test_header_with_classes():
    T1 = tagline("@h1 .blue .red big dog")
    out = '<h1 class="blue red"><text>big dog</text></h1>'
    assert_equal(str(T1), out)


def test_text_only():
    T1 = tagline("big dog")
    out = '<text>big dog</text>'
    assert_equal(str(T1), out)


def test_text_with_markdown():
    T1 = tagline("This _is_ a **big** dog.")
    out = '<text>This <em>is</em> a <strong>big</strong> dog.</text>'
    assert_equal(str(T1), out)


def test_section_with_classes():
    T1 = tagline("---- .blue .red")
    out = '<section class="blue red"></section>'
    assert_equal(str(T1), out)


def test_indent():
    assert_equal(tagline("@h1 big dog").indent, 0)
    assert_equal(tagline("    @h1 big dog").indent, 4)
    assert_equal(str(tagline("@h1 big dog").build(indent=2)),
                 '<h1 indent="2"><text>big dog</text></h1>')


def test_automatic_div():
    T1 = tagline(".red .blue big dog")
    T2 = tagline("@div .red .blue big dog")
    assert_equal(T1, T2)


def test_nested_classes():
    T1 = tagline("@h1 .red @p .blue big dog")
    out = '<h1 class="red"><p class="blue"><text>big dog</text></p></h1>'
    assert_equal(str(T1), out)


def test_is_empty():
    assert_equal(tagline("").empty, True)
    assert_equal(tagline(".blue").empty, False)
    assert_equal(tagline("big dog").empty, False)


def test_markdown_style_header():
    T1 = tagline("### little dog")
    T2 = tagline("@h3 little dog")
    assert_equal(T1, T2)


def test_markdown_style_list():
    T1 = tagline("+ little dog")
    T2 = tagline("@li little dog")
    assert_equal(T1, T2)


def test_options():
    T1 = tagline('@h1(name="foo" class=bar)')
    out = '<h1 class="bar" name="foo"></h1>'
    assert_equal(str(T1), out)


def test_rebuild():
    # Building sometimes failed when run twice
    T1 = tagline('@background(foobar)')
    T1.build()
    T1.build()


def test_custom_function():
    T1 = tagline("@line")
    assert_equal(str(T1), "<hr/>")


def test_custom_background():
    T1 = tagline('@background(url="foobar")')
    T2 = tagline('@background(foobar)')
    out = (
        '<span class="background" '
        'style="background-image:url(\'foobar\')"></span>')

    assert_equal(str(T1), out)
    assert_equal(str(T1), str(T2))


def test_registered_custom_tags():
    # Test all tags that are registered
    line = '@{}(foobar) .red big dog'

    for name, func in _registered_custom_tags.items():
        tagline(line.format(name))


def test_nested_custom_tags_with_text():
    T1 = tagline('@background(src=foobar) @h2 big dogs')
    out = ('<span class="background" '
           'style="background-image:url(\'foobar\')"><h2><text>'
           'big dogs</text></h2></span>')

    assert_equal(str(T1), out)


def test_codeblock_with_text():
    T1 = tagline('@codeblock print x')
    out = '<pre class="prettyprint">print x</pre>'

    assert_equal(str(T1), out)
