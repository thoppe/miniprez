'''
Custom tags. Make sure you register new custom tags at the bottom.
'''

import bs4
from inline_markdown import inline_markdown_parser, soup

def _get_src(tagline):
    opts = tagline["options"]
    for key in ["url","href","src"]:
        if key in opts:
            link = opts[key]
            del opts[key]
    return link

def background_video(tagline):
    tag = soup.new_tag("video")
    tag["autoplay"] = None
    tag["loop"] = None
    tag["class"] = ["background-video"]
    source = soup.new_tag("source")
    source['src'] = _get_src(tagline)
    tag.append(source)
    return tag

def background(tagline):
    tag = soup.new_tag("span")
    tag["class"]  = ["background",]
    url = _get_src(tagline)
    tag["style"] = '''background-image:url('{}')'''. format(url)
    return tag

def unsplash(tagline):
    key = _get_src(tagline)
    tagline['options']["url"] = "https://source.unsplash.com/{}".format(key)
    return background(tagline)


def figure(tagline):
    tag = soup.new_tag("figure")
    img = soup.new_tag("img")
    img['src'] = _get_src(tagline)

    img['style'] = []

    if 'height' in tagline["options"]:
        opt = "height:{}".format(tagline["options"].pop('height'))
        img['style'].append(opt)

    if 'width' in tagline["options"]:
        opt = "width:{}".format(tagline["options"].pop('width'))
        img['style'].append(opt)

    tag.append(img)
    
    # Potential to add figure caption here!
    if tagline["text"]:
        caption = soup.new_tag("figcaption")
        text = inline_markdown_parser(tagline["text"])
        caption.append(bs4.BeautifulSoup(text,'lxml'))
        tagline["text"] = ""
        tag.append(caption)
        
    return tag
    

def line(tagline):
    return soup.new_tag("hr")

def button(tagline):
    tag = soup.new_tag("a")
    tag["class"] = ["button",]
    tag["href"] = _get_src(tagline)

    return tag

def codeblock(tagline):
    tag = soup.new_tag("pre")
    tag["class"] = ["prettyprint",]

    tag.string = tagline["text"].replace('__CODE_BLOCK_SPACE','\n').strip()
    tagline["text"] = None
    
    return tag

#########################################################################

## Register new custom tags here

_registered_custom_tags = {
    "background" : background,
    "unsplash" : unsplash,
    "background_video" : background_video,
    "line" : line,
    "button" : button,
    "codeblock" : codeblock,
    "figure" : figure,
}


