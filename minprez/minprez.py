import sys
import codecs
from parser import file_iterator, section_iterator

if __name__ == "__main__":

    f_md = sys.argv[1]
    F = file_iterator(f_md)

    with open("base.html") as FIN:
        raw = FIN.read()
        base = bs4.BeautifulSoup(raw,'lxml')
        slides = base.find("article",{"id":"webslidesX"})

    for x in section_iterator(F):
        slides.append( section(x).soup )

    with codecs.open('test.html','w','utf-8') as FOUT:
        FOUT.write( base.prettify() )

    print slides.prettify()

