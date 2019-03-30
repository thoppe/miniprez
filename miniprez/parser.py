import mistune
import bs4
import re
from build_static import include_resource

# https://github.com/webslides/WebSlides
# https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md
# https://webslides.tv/demos/
# https://github.com/lepture/mistune

_slide_class_pattern = re.compile("\.\.\.[\-\w\d]+[\.[\-\w\d]+]?")
_open_class_pattern = re.compile("\.\.[\-\w\d]+[\.[\-\w\d]+]?")
_close_class_pattern = re.compile("\.\.")

# Must start the line
_line_class_pattern = re.compile("^\s*\.([\-\w\d]+[\.[\-\w\d]+]?)(.*)")
_tag_pattern = re.compile(".@([a-z]+)")


def process_open_class_tags(x):
    tokens = " ".join(x.group().strip(".").split("."))
    return f"<div class='{tokens}'>"


def process_line_class_tags(x):
    tokens = " ".join(x.group(1).strip().strip(".").split("."))
    return f"<div class='{tokens}'>{x.group(2)}</div>"


def line_parser(line):
    line = re.sub(_open_class_pattern, process_open_class_tags, line)
    line = _close_class_pattern.sub(r"</div>", line)
    line = re.sub(_line_class_pattern, process_line_class_tags, line)

    return line


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

        # Note the slide-level classes and remove them
        section_classes = _slide_class_pattern.findall(html)
        section_classes = " ".join(
            [" ".join(x.strip(".").split(".")) for x in section_classes]
        )
        html = _slide_class_pattern.sub("", html)

        # Parse with a error-correcting soup
        soup = bs4.BeautifulSoup(html, "html5lib")

        # Create a new section and give a sequential slide number
        section = soup.new_tag("section")
        section["data-slide-number"] = slide_number

        # Add the slide-level classes in
        section["class"] = " ".join(section_classes.strip(".").split("."))

        # Only parse the text elements
        replace_patterns = {}

        for text in soup.find_all(text=True):
            new_text = line_parser(text)

            # Replacing is expensive, skip if we can
            if text == new_text:
                continue

            key = f"MINIPREZ_ESCAPED_REPLACEMENT{len(replace_patterns)}"
            replace_patterns[key] = new_text
            text.replace_with(key)

        # Make the replacements
        if replace_patterns:
            soup = str(soup)
            for key, val in replace_patterns.items():
                soup = soup.replace(key, val)

            # For good measure, reparse with an error-correcting soup
            soup = bs4.BeautifulSoup(soup, "html5lib")

        # Do this so we remove the head.body parts of the tag
        for ele in soup.body.find_all():
            section.append(ele)

        article.append(section)

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
    text = """...bg-white.dark

..aligncenter 

### ..text-data **miniprez** ..
#### Beautiful presentations in minimalist format

..text-intro miniprez is a static, mobile-friendly version of [webslides](https://github.com/jlantunez/webslides)
"""
    html = miniprez_markdown(text)

    print("****************************")

    soup = build_body(html)
    # with open('test.html', 'w') as FOUT:
    #    FOUT.write(str(soup))
    print(soup.prettify())
