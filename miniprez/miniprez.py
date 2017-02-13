"""
Usage: miniprez.py INPUT [-h] [-o OUTPUT|-t] [--pretty]

-h --help     show this help
-o, --output  FILE specify output file [default: INPUT.html]
-t, --term    Output just the slides to stdout 
--pretty      Pretty-print the html output with Beautiful Soup [default: True]
--quiet       print less text
--verbose     print more text
"""

import sys
import bs4
import os
import codecs
from docopt import docopt
from parser import file_iterator, section_iterator, section

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

f_base_html = os.path.join(os.path.dirname(__location__),
                           "static", "minipres_base.html")

if __name__ == "__main__":

    args = docopt(__doc__)
    f_md = args["INPUT"]

    if not os.path.exists(f_md):
        raise IOError("{} not found".format(f_md))
        
    if args["OUTPUT"] is None:
        f_base = os.path.basename(f_md)
        args["OUTPUT"] = '.'.join(f_base.split('.')[:-1])+'.html'

    F = file_iterator(f_md)

    with open(f_base_html) as FIN:
        raw = FIN.read()
        base = bs4.BeautifulSoup(raw,'lxml')
        slides = base.find("article",{"id":"minislides"})

    for k,x in enumerate(section_iterator(F)):
        soup = section(x).soup
        soup.section["id"] = "slide-number-{}".format(k+1)
        soup.section["class"] = soup.section.get('class',[]) + ["slide",]
        slides.append(soup)


    if args["--pretty"]:
        output = unicode(base.prettify())
    else:
        output = unicode(base)

    if args["--term"]:
        print (slides.prettify().encode('utf-8'))
        
    else:
        with codecs.open(args["OUTPUT"],'w','utf-8') as FOUT:
            FOUT.write(output)
        print ("Output written to {OUTPUT}.".format(**args))


