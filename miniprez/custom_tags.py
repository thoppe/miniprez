import bs4

def background(tagline, soup):
    info = tagline.tag
    assert(info[0] == 'background')
    
    tag = soup.new_tag("span")
    tag["class"] = ["background",]
    tag["style"] = '''background-image:url('{url}')'''. format(**info[1])

    del info[1]["url"]
    
    return tag

def line(tagline, soup):
    info = tagline.tag
    assert(info[0] == 'line')
    
    return soup.new_tag("hr")

def button(tagline, soup):
    info = tagline.tag
    assert(info[0] == 'button')

    tag = soup.new_tag("a")
    tag["class"] = ["button",]

    for key in ["url", "href"]:
        if key in info[1]:
            tag["href"] = info[1][key]
            del info[1][key]

    return tag
    #p = soup.new_tag('p', {})
    #p.append(tag)
    #return p

