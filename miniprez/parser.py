import mistune
import bs4, os
from emoji import emojize
from build_static import add_css, add_script, include_resource
from grammar import markdown_parser
import logging

logger = logging.getLogger("miniprez")
_video_extensions = set(["mp4", "webm", "flac"])

# References
# https://github.com/webslides/WebSlides
# https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md
# https://webslides.tv/demos/
# https://github.com/lepture/mistune

CDN_KaTeX_css = {
    "src": "https://cdn.jsdelivr.net/npm/katex@0.10.1/dist/katex.min.css",
    "cdn": True,
    "integrity": "sha384-dbVIfZGuN1Yq7/1Ocstc1lUEm+AT+/rCkibIcC/OmWo5f0EA48Vf8CytHzGrSwbQ",
    "crossorigin": "anonymous",
}

CDN_KaTeX_js = {
    "src": "https://cdn.jsdelivr.net/npm/katex@0.10.1/dist/katex.min.js",
    "cdn": True,
    "integrity": "sha384-2BKqo+exmr9su6dir+qCw08N2ZKRucY4PrGQPPWU1A7FtlCGjmEGFqXCv5nyM5Ij",
    "crossorigin": "anonymous",
    # defer=None,
}

Roboto_FontLink = "https://fonts.googleapis.com/css?family=Roboto:100,100i,300,300i,400,400i,700,700i%7CMaitree:200,300,400,600,700&amp;subset=latin-ext"


def slide_parser(html):
    """
    Takes a single slide after being markdown parsed and split by ----
    Returns the slide after parsing the class_patterns.
    """

    # Parse with a error-correcting soup
    soup = bs4.BeautifulSoup(html, "html5lib")

    # Create a new section and the slide-level classes in
    section = soup.new_tag("section")
    section["class"] = ["slide"]
    # section['style'] = 'display: none;'

    # Note the slide-level classes and remove them
    for meta in soup.find_all("meta", attrs={"data-slide-classes": True}):
        section["class"].append(meta["data-slide-classes"])
        meta.decompose()

    # Replace the emoji with their targets
    for ele in soup.find_all("emoji"):
        symbol = emojize(ele["data-emoji-alias"], use_aliases=True)
        ele.replace_with(symbol)

    # For all the background spans, append the correct class
    bg = None
    for ele in soup.find_all("span", {"data-is-bg": True}):

        bg = ele.extract()
        src = bg["data-bg-src"]
        del bg["data-is-bg"]
        del bg["data-bg-src"]

        if "class" not in bg.attrs:
            bg["class"] = []

        src_ext = os.path.splitext(src)[-1].strip(".")
        bg["class"].append("background")

        if src_ext in _video_extensions:
            # Handle case for background videos (DOES NOT WORK YET)
            logger.error("bg videos not implemented yet. sorry")

            """
            video = soup.new_tag(
                'video', **{
                    "loop":None,
                    "muted":None, "autoplay":None, "poster":None,
                })
            
            source = soup.new_tag('source', **{"src":src, "type":"video/mp4"})
            video.append(source)
            bg.append(video)
            #bg.append(video)
            #section['class'].append('fullscreen')
            """
        else:
            bg["class"].append("background")
            bg["style"] = f"background-image:url('{src}')"

    # Add the parsed soup to the section and unwrap the body tags
    section.append(soup.body)
    section.body.unwrap()

    # For background add to the begining of the section; wrap everything else
    if bg is not None:
        wrap = soup.new_tag("div", attrs={"class": "wrap"})
        children = list(section.children)
        section.clear()
        section.append(bg)
        section.append(wrap)
        wrap.extend(children)

    return section


def miniprez_markdown(markdown_text):
    html = markdown_parser(markdown_text)
    # html = _tag_pattern.sub(r"<\1>", html)

    # Nest each block in a section div
    blocks = []
    strict_hr_tag = "<hr>"
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
    add_css(soup, Roboto_FontLink, cdn=True)

    add_script(soup, "static/js/jquery-3.1.1.min.js")
    add_script(soup, "static/js/slider.js")

    # If we used font-awesome, add the class and fonts
    if soup.find("span", class_="fa") is not None:
        add_css(soup, "static/css/font-awesome.min.css")
        include_resource("static/fonts/fontawesome-webfont.woff")
        include_resource("static/fonts/fontawesome-webfont.woff2")

    if soup.find("code"):
        has_found_code_block = False

        # Need to add the class tag
        for ele in soup.find_all("code"):
            if ele.parent.name == "pre":
                ele["class"] = "prettyprint"
                has_found_code_block = True

        if has_found_code_block:
            # Google's prettifier
            add_script(soup, "static/js/run_prettify.js")

    # If we have an equation, add the static information
    if soup.find(class_="inline-equation") or soup.find(
        class_="block-equation"
    ):
        # logger.warning("EQUATION DETECTED. Currently using CDN.")
        add_script(soup, **CDN_KaTeX_js)
        add_css(soup, **CDN_KaTeX_css)
        add_script(soup, "static/js/render_equations.js")

    # Move the markdown header information to the right place
    for meta in soup.find_all("meta", attrs={"data-is-header":True}):
        del meta['data-is-header']
        meta.extract()
        print(meta)
        exit()

    # Add the HTML doctype
    soup.insert(0, bs4.element.Doctype("HTML"))

    # Unwrap all useless p tags
    for ele in soup.find_all("p"):
        if isinstance(ele, bs4.element.Tag):
            if not ele.get_text().strip():
                ele.unwrap()

    # Wrap the parent element codes if needed
    for ele in soup.find_all("span"):
        if "class" not in ele.attrs:
            continue

        if "inline-equation" in ele["class"]:
            continue
        if "block-equation" in ele["class"]:
            continue

        parent = ele.parent
        if parent.name not in ["h1", "h2", "h3", "h4", "h5", "h6"]:
            continue

        if "class" not in parent.attrs:
            parent["class"] = []
        parent["class"].extend(ele["class"])
        ele.unwrap()


    return soup


if __name__ == "__main__":
    text = """...bg-black.foo
introduction
..aligncenter 
### .text-data **miniprez**
--------------------------
slide two
"""

    html = parser(text)
    html = miniprez_markdown(text)

    print("****************************")

    soup = build_body(html)
    # with open('test.html', 'w') as FOUT:
    #    FOUT.write(str(soup))
    print(soup.prettify())
