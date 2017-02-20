from miniprez.tagline import tagline
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

def test_markdown_style_header():
    T1 = tagline("### little dog")
    T2 = tagline("@h3 little dog")
    assert_equal(T1,T2)


    
