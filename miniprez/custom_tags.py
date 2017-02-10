'''
Custom tags. Make sure you register new custom tags at the bottom.
'''

import bs4

def _get_src(tagline):
    opts = tagline["options"]
    for key in ["url","href","src"]:
        if key in opts:
            link = opts[key]
            del opts[key]
    return link

def background_video(tagline, soup):
    tag = soup.new_tag("video")
    tag["autoplay"] = None
    tag["loop"] = None
    tag["class"] = ["background-video"]
    source = soup.new_tag("source")
    source['src'] = _get_src(tagline)
    tag.append(source)
    return tag

def background(tagline, soup):
    tag = soup.new_tag("span")
    tag["class"]  = ["background",]
    url = _get_src(tagline)
    tag["style"] = '''background-image:url('{}')'''. format(url)
    return tag

def figure(tagline, soup):
    tag = soup.new_tag("figure")
    img = soup.new_tag("img")
    img['src'] = _get_src(tagline)

    # Potential to add figure caption here!
    tag.append(img)
    return tag
    

def line(tagline, soup):
    return soup.new_tag("hr")

def button(tagline, soup):
    tag = soup.new_tag("a")
    tag["class"] = ["button",]
    tag["href"] = _get_src(tagline)

    return tag

def codeblock(tagline, soup):
    tag = soup.new_tag("pre")
    tag["class"] = ["prettyprint",]
    tag.string = tagline.text.replace('__CODE_BLOCK_SPACE','\n').strip()
    tagline.text = ''
    
    return tag

#########################################################################

## Register new custom tags here

_registered_custom_tags = {
    "background" : background,
    "background_video" : background_video,
    "line" : line,
    "button" : button,
    "codeblock" : codeblock,
    "figure" : figure,
}


