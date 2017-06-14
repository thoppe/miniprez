import bs4
import os
import codecs

from parser import file_iterator, section_iterator, section
from build_env import build_environment
from _version import __version__

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


def build(args):

    lambda x: __version__

    if not args["--nocopy"]:
        if build_environment(**args):
            print("Created environment in ./static")

    f_base_html = os.path.join(__location__, "static", "minipres_base.html")

    with open(f_base_html) as FIN:
        raw = FIN.read()
        base = bs4.BeautifulSoup(raw, 'lxml')
        slides = base.find("article", {"id": "minislides"})

    F = file_iterator(args["INPUT"])

    for k, x in enumerate(section_iterator(F)):
        soup = section(x).soup
        soup.section["id"] = "slide-number-{}".format(k + 1)
        soup.section["class"] = soup.section.get('class', []) + ["slide", ]
        slides.append(soup)

    if args["--term"]:
        if args["--condense"]:
            print(slides.encode('utf-8'))
        else:
            print(slides.prettify().encode('utf-8'))
        return True

    with codecs.open(args["OUTPUT"], 'w', 'utf-8') as FOUT:
        if args["--condense"]:
            output = unicode(base)
        else:
            output = base.prettify()

        FOUT.write(output)
        print("Output written to {OUTPUT}".format(**args))
