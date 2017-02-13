#! /usr/bin/env python
"""
Usage: miniprez.py INPUT [-o OUTPUT|-t] [--condense] [--nocopy] [--verbose]

-h --help     Show this help
-o, --output  FILE specify output file [default: INPUT.html]
-t, --term    Output just the slides to stdout 
--condense    Don't pretty-print the output [default: False]
--nocopy      Don't copy the static files: css, js, etc [default: False]
--verbose     Print more text [default: False]
"""

import sys
import bs4
import os
import codecs
from docopt import docopt
from parser import file_iterator, section_iterator, section
from build_env import build_environment

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

    if not args["--nocopy"]:
        if build_environment(**args):
            print("Created environment in ./static")

    with open(f_base_html) as FIN:
        raw = FIN.read()
        base = bs4.BeautifulSoup(raw,'lxml')
        slides = base.find("article",{"id":"minislides"})

    for k,x in enumerate(section_iterator(F)):
        soup = section(x).soup
        soup.section["id"] = "slide-number-{}".format(k+1)
        soup.section["class"] = soup.section.get('class',[]) + ["slide",]
        slides.append(soup)
    
    if args["--term"]:
        if args["--condense"]:
            print (slides.encode('utf-8'))
        else:
            print (slides.prettify().encode('utf-8'))
        exit()
        
    with codecs.open(args["OUTPUT"],'w','utf-8') as FOUT:
        if args["--condense"]:
            output = unicode(base)
        else:
            output = base.prettify()
        
        FOUT.write(output)
        print ("Output written to {OUTPUT}".format(**args))


