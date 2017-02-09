'''
Custom tags. Make sure you register new custom tags at the bottom.
'''

import bs4

def _get_src(tagline):
    for key in ["url","href","src"]:
        if key in tagline.tag[1]:
            link = tagline.tag[1][key]
            del tagline.tag[1][key]
    return link

def background(tagline, soup):
    name,info = tagline.tag
    assert(name == 'background')

    tag = soup.new_tag("span")

    if tag.classnames:
        tag["class"]  = ["background",] + tag.classnames
    else:
        tag["class"] = ["background",]

    url = _get_src(tagline)   
    tag["style"] = '''background-image:url('{}')'''. format(url)
    
    return tag

def figure(tagline, soup):
    name,info = tagline.tag
    assert(name == 'figure')

    tag = soup.new_tag("figure")
    img = soup.new_tag("img")
    img['src'] = _get_src(tagline)

    # Potential to add figure caption here!
    tag.append(img)
    return tag
    

def line(tagline, soup):
    name,info = tagline.tag
    assert(name == 'line')
   
    return soup.new_tag("hr")

def button(tagline, soup):
    name,info = tagline.tag
    assert(name == 'button')

    tag = soup.new_tag("a")
    tag["class"] = ["button",]
    tag["href"] = _get_src(tagline)

    return tag

def codeblock(tagline, soup):
    name,info = tagline.tag
    assert(name == 'codeblock')

    tag = soup.new_tag("pre")
    tag["class"] = ["prettyprint",]
    tag.string = tagline.text.replace('__CODE_BLOCK_SPACE','\n').strip()
    tagline.text = ''
    
    return tag

#########################################################################

## Register new custom tags here

_registered_custom_tags = {
    "background" : background,
    "line" : line,
    "button" : button,
    "codeblock" : codeblock,
    "figure" : figure,
}


