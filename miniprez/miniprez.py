import sys
import bs4
import os
import codecs
from parser import file_iterator, section_iterator, section

__location__ = os.path.realpath(os.path.join(
    os.getcwd(), os.path.dirname(__file__)))


if __name__ == "__main__":

    f_md = sys.argv[1]
    F = file_iterator(f_md)

    f_base = os.path.join(__location__, "base.html")

    with open(f_base) as FIN:
        raw = FIN.read()
        base = bs4.BeautifulSoup(raw,'lxml')
        slides = base.find("article",{"id":"minislides"})

    for k,x in enumerate(section_iterator(F)):
        soup = section(x).soup
        soup.section["slide-number"] = k+1
        slides.append(soup)

    with codecs.open('test.html','w','utf-8') as FOUT:
        output = unicode(base.prettify())
        FOUT.write(output)

    print slides.prettify()

