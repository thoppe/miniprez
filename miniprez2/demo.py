import mistune
import bs4
import re


_global_class_pattern = re.compile('\.\.\.([a-z\-]+)')
_class_pattern = re.compile('\.\.([a-z\-]+)')
_end_class_pattern = re.compile('\.\.')
_tag_pattern = re.compile('.@([a-z]+)')

def miniprez_markdown(markdown_text):

    parser = mistune.Markdown(
        escape=False, use_xhtml=True, hard_wrap=True)
    html = parser(markdown_text)
    html = _tag_pattern.sub(r'<\1>', html)

    # Nest each block in a section div
    blocks = []
    strict_hr_tag = '<hr />'
    article = bs4.BeautifulSoup("", 'html.parser').new_tag("article")
    article['id'] = 'webslides'
    
    for html in html.split(strict_hr_tag):

        # Note the globals and remove them
        section_classes = _global_class_pattern.findall(html)
        html = _global_class_pattern.sub('', html)

        html = _class_pattern.sub(r'<div class="\1">', html)
        html = _end_class_pattern.sub(r'<div>', html)
        
        # Parse with a error-correcting soup
        soup = bs4.BeautifulSoup(html, 'html5lib')

        section = soup.new_tag("section")
        section['class'] = section_classes
        
        section.append(soup)
        article.append(section)

    return str(article)

def build_body(html):
    soup = bs4.BeautifulSoup(html, 'html5lib')

    css_args = {
        'rel':"stylesheet",
        'type':"text/css",
        'media':"all",
    }
    
    css = soup.new_tag("link", href="static/css/webslides.css", **css_args,)
    soup.head.append(css)

    css = soup.new_tag("link", href="static/css/miniprez.css", **css_args,)
    soup.head.append(css)

    script = soup.new_tag('script', src="static/js/webslides.js")
    soup.body.append(script)

    # Remove empty paragraph tags
    for p in soup.find_all('p', text=None):
        #pass
        p.decompose()
    
    return soup

text = '''
# header 1 **so bold** 
## header 2

-----

inline `code`
For the win!

-----
 
$x^2$
'''

text = '''...bg-white ...dark
..aligncenter 

### ..text-data **miniprez** ..
#### Beautiful presentations in minimalist format

..text-intro miniprez is a static, mobile-friendly version of [webslides](https://github.com/jlantunez/webslides)

-----
...bg-black 

# ..text-landing The problem ..

..text-intro
+ I want simple and beautiful presentations.
+ Presentations that compile from text to interactive webpages.
+ Presentations that seperate content from style like Markdown. 
+ Presentations that render mathematics and highlight code.

..
Oh, and it should work well* on mobile too.

.@footer ..alignright *just show me the content!
'''
html = miniprez_markdown(text)


soup = build_body(html)
with open('test.html', 'w') as FOUT:
    FOUT.write(str(soup))

print(soup.prettify())
