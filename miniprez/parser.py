import mistune
import bs4
import re
import os
from importlib import resources
import logging

logger = logging.getLogger("miniprez")


# https://github.com/webslides/WebSlides
# https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md
# https://webslides.tv/demos/
# https://github.com/lepture/mistune

_global_class_pattern = re.compile("\.\.\.([a-z\-]+)")
_class_pattern = re.compile("\.\.([a-z\-]+)")
_end_class_pattern = re.compile("\.\.")
_tag_pattern = re.compile(".@([a-z]+)")


def miniprez_markdown(markdown_text):

    parser = mistune.Markdown(escape=False, use_xhtml=True, hard_wrap=True)
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
        html = _global_class_pattern.sub("", html)

        html = _class_pattern.sub(r'<div class="\1">', html)
        html = _end_class_pattern.sub(r"<div>", html)

        # Parse with a error-correcting soup
        soup = bs4.BeautifulSoup(html, "html5lib")

        section = soup.new_tag("section")
        section["class"] = section_classes
        section["data-slide-number"] = slide_number

        section.append(soup)
        article.append(section)

    return str(article)


def add_file(filename):

    if not os.path.exists(filename):
        logger.warning(f"Building {filename}")

        # Create the directory if we need to
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

        module_path = ".".join(os.path.split(directory))
        basename = os.path.basename(filename)

        # Read the file into the location
        res = resources.open_binary(module_path, basename)
        with res as FIN, open(filename, "wb") as FOUT:
            FOUT.write(res.read())


def add_script(soup, src):
    add_file(src)

    tag = soup.new_tag("script", src=src)
    soup.body.append(tag)


def add_css(soup, src):
    add_file(src)

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
        # pass
        p.decompose()

    return soup


if __name__ == "__main__":
    text = "**hello** world."

    html = miniprez_markdown(text)
    soup = build_body(html)
    # with open('test.html', 'w') as FOUT:
    #    FOUT.write(str(soup))
    print(soup.prettify())
