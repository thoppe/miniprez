from miniprez.parser import section
from nose.tools import assert_equal

slide0 = '''
---- .alignright
@h1 .text-data Good morning
   @p Time to rise and shine!
'''
slide0_out = '''<section class="alignright"><h1 class="text-data"><text>Good morning<p><text>Time to rise and shine!</text></p></text></h1></section>'''

slide1 = '''
---- .aligncenter
.red Red dogs
   .big big red dogs
   .small small red dogs
       .fat small fat red dogs
'''
slide1_out = '''<section class="aligncenter"><div class="red"><text>Red dogs<div class="big"><text>big red dogs</text></div><div class="small"><text>small red dogs<div class="fat"><text>small fat red dogs</text></div></text></div></text></div></section>'''

slide2 = '''
----
@background(foobar)
@h1 big dogs
'''
slide2_out = '''<section><span class="background" style="background-image:url(\'foobar\')"></span><div class="wrap"><h1><text>big dogs</text></h1></div></section>'''


slide3 = '''
----
Below is a list
@h1
  + item one
  + item **two**
'''
slide3_out = '''<section><text>Below is a list</text><h1><ul class="markdownlist"><li><text>item one</text></li><li><text>item <strong>two</strong></text></li></ul></h1></section>'''

slide4 = '''
----
Below is some code
```
for x in range(20):
    print x
```
'''
slide4_out = '''<section><text>Below is some code</text><pre class="prettyprint">for x in range(20):\n    print x</pre></section>'''


def test_empty_section():
    empty_section = ["----"]
    S = section(empty_section)
    assert_equal(str(S), "<section></section>")


def test_simple_slide0():
    S = section(slide0.split('\n'))
    assert_equal(str(S), slide0_out)


def test_simple_slide1():
    S = section(slide1.split('\n'))
    assert_equal(str(S), slide1_out)


def test_background_div_wrap():
    S = section(slide2.split('\n'))
    assert_equal(str(S), slide2_out)


def test_markdownlist():
    S = section(slide3.split('\n'))
    assert_equal(str(S), slide3_out)


def test_codeblock():
    S = section(slide4.split('\n'))
    assert_equal(str(S), slide4_out)
