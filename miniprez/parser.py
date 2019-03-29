import mistune
import bs4
import re
from build_static import include_resource

# https://github.com/webslides/WebSlides
# https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md
# https://webslides.tv/demos/
# https://github.com/lepture/mistune

_global_class_pattern = re.compile("\.\.\.[\-\w\d]+[\.[\-\w\d]+]?")
_class_pattern = re.compile("\.\.[\-\w\d]+[\.[\-\w\d]+]?")
_end_class_pattern = re.compile("\.\.")
_tag_pattern = re.compile(".@([a-z]+)")

def class_tags(x):
    tokens = ' '.join(x.group().strip('.').split('.'))
    return f"<div class='{tokens}'>"

def miniprez_markdown(markdown_text):

    parser = mistune.Markdown(escape=False, use_xhtml=True, hard_wrap=False)
    html = parser(markdown_text)
    html = _tag_pattern.sub(r"<\1>", html)

    # Nest each block in a section div
    blocks = []
    strict_hr_tag = "<hr />"
    article = bs4.BeautifulSoup("", "html.parser").new_tag("article")
    article["id"] = "webslides"

    for slide_number, html in enumerate(html.split(strict_hr_tag)):

        # Note the globals and remove them
        section_classes = _global_class_pattern.findall(html)
        section_classes = ' '.join(
            [' '.join(x.strip('.').split('.')) for x in section_classes])

        html = _global_class_pattern.sub("", html)

        html = re.sub(_class_pattern, class_tags, html)
        html = _end_class_pattern.sub(r"<div>", html)

        # Parse with a error-correcting soup
        soup = bs4.BeautifulSoup(html, "html5lib")

        section = soup.new_tag("section")
        section["class"] = ' '.join(
            section_classes.strip('.').split('.'))
        
        section["data-slide-number"] = slide_number

        #section.extend(soup.body.contents)
        #print(soup.body.contents)
        #for x in soup.body.contents:
        #    print("HERE",x)
        #    section.append(x)
        section.append(soup)
        article.append(section)

    print(article)


    return str(article)


def add_script(soup, src):
    include_resource(src)

    tag = soup.new_tag("script", src=src)
    soup.body.append(tag)


def add_css(soup, src):
    include_resource(src)

    css_args = {"rel": "stylesheet", "type": "text/css", "media": "all"}
    tag = soup.new_tag("link", href=src, **css_args)
    soup.head.append(tag)


def build_body(html):
    soup = bs4.BeautifulSoup(html, "html5lib")

    add_css(soup, "static/css/webslides.css")
    add_css(soup, "static/css/miniprez.css")

    add_script(soup, "static/js/jquery-3.1.1.min.js")
    add_script(soup, "static/js/slider.js")

    # Remove empty paragraph tags
    for p in soup.find_all("p", text=None):
        if not p.contents:
            p.decompose()

    return soup


if __name__ == "__main__":
    text = "**hello** world."

    html = miniprez_markdown(text)
    soup = build_body(html)
    # with open('test.html', 'w') as FOUT:
    #    FOUT.write(str(soup))
    print(soup.prettify())
