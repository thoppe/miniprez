import sys
import bs4
import os
import codecs
import argparse
from parser import file_iterator, section_iterator, section

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))

f_base_html = os.path.join(os.path.dirname(__location__),
                           "static", "minipres_base.html")

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--input",  type=str, help="Input miniprez file")
    parser.add_argument("--output", type=str,
                            help="Output html file, defaults to [input].html")
    parser.add_argument("f_input", type=str, help=argparse.SUPPRESS)
    
    
    args = parser.parse_args()
    f_md = args.input if args.input else args.f_input

    if args.output is None:
        args.output = '.'.join(os.path.basename(f_md).split('.')[:-1])+'.html'

    if not os.path.exists(f_md):
        raise SyntaxError("{} not found".format(f_md))
    
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

    with codecs.open(args.output,'w','utf-8') as FOUT:
        #output = unicode(base.prettify())
        output = unicode(base)

        FOUT.write(output)

    #print slides.prettify().encode('utf-8')

