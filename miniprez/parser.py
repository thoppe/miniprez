import mistune
import bs4
import re
from build_static import add_css, add_script

# https://github.com/webslides/WebSlides
# https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md
# https://webslides.tv/demos/
# https://github.com/lepture/mistune

_slide_class_pattern = re.compile("\.\.\.[\-\w\d]+[\.[\-\w\d]+]?")
_open_class_pattern = re.compile("\.\.[\-\w\d]+[\.[\-\w\d]+]?")
_close_class_pattern = re.compile("\.\.")

# Must start the line
#_line_class_pattern = re.compile("^\s*\.([\-\w\d]+[\.[\-\w\d]+]?)(.*)")
#_tag_pattern = re.compile(".@([a-z]+)")



def process_open_class_tags(x):
    tokens = " ".join(x.group().strip(".").split("."))
    return f"<div class='{tokens}'>"


def process_line_class_tags(x):
    tokens = " ".join(x.group(1).strip().strip(".").split("."))
    return f"<div class='{tokens}'>{x.group(2)}</div>"

def get_classnames(class_string):
    return ' '.join(class_string.lstrip('.').split('.'))

line_class_pattern = re.compile("\.([\-\w\d]+[\.[\-\w\d]+]?)")
open_class_pattern = re.compile("\.\.[\-\w\d]+[\.[\-\w\d]+]?")
close_class_pattern = re.compile("\.\.")
def line_parser(line):
    tokens = line.split()

    if not tokens:
        return None

    if re.match(line_class_pattern, tokens[0]):        
        names = get_classnames(tokens[0])
        remaining = ' '.join(tokens[1:])
        return f"<div class='{names}'>{remaining}</div>"
    
    if re.match(open_class_pattern, tokens[0]):        
        names = get_classnames(tokens[0])
        remaining = ' '.join(tokens[1:])
        return f"<div class='{names}'>{remaining}"

    if re.match(close_class_pattern, tokens[0]):
        remaining = ' '.join(tokens[1:])
        return f"</div>"
        

    return None


def slide_parser(html):
    '''
    Takes a single slide after being markdown parsed and split by ----
    Returns the slide after parsing the class_patterns.
    '''

    # Note the slide-level classes and remove them
    section_classes = _slide_class_pattern.findall(html)
    section_classes = " ".join(
        [" ".join(x.strip(".").split(".")) for x in section_classes]
    )
    html = _slide_class_pattern.sub("", html)
    
    # Parse with a error-correcting soup
    soup = bs4.BeautifulSoup(html, "html5lib")

    # Create a new section and the slide-level classes in
    section = soup.new_tag("section")
    section["class"] = section_classes

    # Only parse the text elements. Tricky since we can't directly
    # put in html to bs4.strings (they get escaped)
    replace_patterns = {}

    for text_element in soup.find_all(text=True):
        new_text = line_parser(str(text_element))

        # Replacing is expensive, skip if we can
        if new_text is None:
            continue

        key = f"MINIPREZ_{len(replace_patterns)}"
        replace_patterns[key] = new_text
        text_element.replace_with(key)


    # Unwrap paragraph tags
    for p in soup.find_all("p", text=None):
        p.unwrap()

    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")

    # For good measure, reparse with an error-correcting soup
    #article = bs4.BeautifulSoup("", "html.parser").new_tag("article")
    #soup = bs4.BeautifulSoup(soup, "html.parser")
    
    # Do this so we remove the head.body parts of the tag
    for ele in soup.body.find_all():
        section.append(ele)
        
    if replace_patterns:
        section = str(section)
        for key, val in replace_patterns.items():
            section = section.replace(key, val)
            
    print(section)

    exit()
    exit()


    for text in soup.find_all(text=True):
        new_text = line_parser(text)


        if text == new_text:
            continue


    return section



def miniprez_markdown(markdown_text):

    parser = mistune.Markdown(escape=False, use_xhtml=False, hard_wrap=False)
    html = parser(markdown_text)
    html = _tag_pattern.sub(r"<\1>", html)

    # Nest each block in a section div
    blocks = []
    strict_hr_tag = "<hr />"
    article = bs4.BeautifulSoup("", "html.parser").new_tag("article")
    article["id"] = "webslides"

    for slide_number, html in enumerate(html.split(strict_hr_tag)):
        section = slide_parser(html)
        
        # Give each slide a sequential number
        section["data-slide-number"] = slide_number

        article.append(section)

    return str(article)



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
    text = """..aligncenter 
### ..text-data **miniprez** .."""

    parser = mistune.Markdown(escape=False, use_xhtml=True, hard_wrap=False)
    html = parser(text)
    print("MARKDOWN")
    print(html)

    print("SLIDE")
    print(slide_parser(html))
    exit()
    
    #html = miniprez_markdown(text)

    print("****************************")

    soup = build_body(html)
    # with open('test.html', 'w') as FOUT:
    #    FOUT.write(str(soup))
    print(soup.prettify())
