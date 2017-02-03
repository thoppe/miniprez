import bs4

def background(tagline, soup):
    info = tagline.tag

    assert(info[0] == 'background')
    
    tag = soup.new_tag("span")
    tag["class"] = "background-"
    tag["style"] = '''background-image:url('{url}')'''. format(**info[1])

    del info[1]["url"]
    
    return tag

def line(tagline, soup):
    return soup.new_tag("hr")
