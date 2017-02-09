import itertools
import bs4
import re
import string
import pyparsing as pyp
import custom_tags

from custom_tags import _registered_custom_tags
from inline_markdown import inline_markdown_parser

_section_header_token = '----'
_comment_marker_token = '//'
_code_block_marker = "```"

def is_section_header(line):
    if len(line)<4:
        return False
    return line[:4] == _section_header_token

def section_iterator(lines):
    section = []
    for line in lines:
        if is_section_header(line) and section:
            yield section
            section = [line,]
        else:
            section.append(line)

    yield section  
            
def file_iterator(f_md):

    # Read all the lines
    lines = []
    with open(f_md) as FIN:
        for line in FIN:
            if not line.strip():
                continue
            if len(line)>=2 and line.lstrip()[:2] == _comment_marker_token:
                continue
            yield line.rstrip()

########################################################################
    
class tagline(object):
    '''
    Each line is parsed by tokens individually until no preprocessing 
    tokens are left.
    '''

    def __init__(self, line):
  
        self.classnames = []
        self.line = line

        g_name = pyp.Word(pyp.alphanums+'-_')
        g_quote = pyp.QuotedString('"')|pyp.QuotedString("'")
        g_header = pyp.Literal('----')+pyp.ZeroOrMore('-')
        
        g_option_token = (g_name.setResultsName("key") +
                          pyp.Literal("=").suppress() +
                          (g_name|g_quote).setResultsName("value"))
        g_option = pyp.nestedExpr(content=pyp.Group(g_option_token))

        g_tag   = (pyp.Literal("@").suppress() +
                   g_name.setResultsName('name') +
                   pyp.Optional(g_option).setResultsName('options'))
                           
        g_classname = (pyp.Literal(".").suppress() +
                       g_name.setResultsName('name'))

        g_format_text = pyp.ZeroOrMore(pyp.Group(g_tag|g_classname|g_header))
        grammar = g_format_text + pyp.restOfLine.setResultsName('text')

        tags = []

        def parse_tag(tag):
            options = {}
            if "options" in tag:
                for item in tag["options"][0]:
                    options[item['key']] = item['value']
            tags.append((tag["name"],options))
        def parse_classname(item):
            self.classnames.append(item['name'])

        g_header.setParseAction(lambda _:tags.append(("section",{})))
        g_tag.setParseAction(parse_tag)
        g_classname.setParseAction(parse_classname)

        try:
            res = grammar.parseString(line)
        except pyp.ParseException as Ex:
            print 'Failed parsing "{}"'.format(line)
            raise Ex

        self.text = res['text'].strip()
        
        #if len(tags)>1:
        #    msg = 'Only one tag allowed per line, "{}"'.format(line)
        #    raise SyntaxError(msg)

        # Select only the first tag
        self.tag = tags[0] if tags else None

        # If classnames are used but tag is None, default to a div
        if self.tag is None and self.classnames:
            self.tag = ('div',{})

        # Otherwise set the tag to text
        elif self.tag is None:
            self.tag = ('text',{})

    @property
    def primary_name(self):
        return self.tag[0]

    @property
    def indent(self):
        is_space = lambda x:x in ['\t',' ']
        return len(list(itertools.takewhile(is_space,self.line)))

    @property
    def is_section_header(self):
        return self.primary_name == 'section'
    
    @property
    def is_empty(self):
        return not (self.text or self.classnames or self.tag)

    @property
    def has_tag(self):
        return (self.tag is not None)

    def __repr__(self):
        keys = ("text","tag","classnames")
        vals = (getattr(self,x) for x in keys)
        return str(dict(zip(keys,vals)))

    def build_tag(self, soup, **kwargs):

        name = self.primary_name
        if name in _registered_custom_tags:
            tag = _registered_custom_tags[name](self, soup)
            
        else:
            tag = soup.new_tag(name)
        
        if self.classnames:
            tag['class'] = tag.get('class',[]) + self.classnames

        options = self.tag[1]
        for key,val in options.items():
            tag[key] = val

        for key,val in kwargs.items():
            tag[key] = val

        if self.text:
            # Make any markdown modifications
            text = inline_markdown_parser(self.text)
            html_text = bs4.BeautifulSoup(text,'html.parser')
            tag.append(html_text)

        return tag


class section(object):

    def __init__(self, lines):

        self.lines = []

        # Custom work for a code block
        is_inside_code_block = False
        code_buffer = []
        code_block_indent = None
        for line in lines:

            is_code_block = _code_block_marker == line.lstrip()[:3]

            if is_code_block:
                is_inside_code_block = not is_inside_code_block

            if is_code_block or is_inside_code_block:
                code_buffer.append( line.rstrip() )
    
            if is_code_block and not is_inside_code_block:
                space_ITR = itertools.takewhile(lambda x:x==' ',line)
                code_block_indent = len(list(space_ITR))

                # Remove the code buffer lines
                code_buffer = code_buffer[1:-1]
                
                # Empty out the contents of the buffer
                code_block = '__CODE_BLOCK_SPACE'.join(code_buffer)
                header = code_block_indent*' ' + '@codeblock '
                block = header + code_block
                self.lines.append(block)
                
                code_buffer = []
            elif not is_inside_code_block:
                self.lines.append(line)

    
        # Parse and filter for blank lines
        self.lines = [x for x in map(tagline,self.lines) if not x.is_empty]

        # Section shouldn't be empty
        assert(self.lines)

        # Section should start with a header
        assert(self.lines[0].is_section_header)

        soup  = bs4.BeautifulSoup("",'html.parser')
        lines = iter(self)
        
        # Parse the header
        z = lines.next().build_tag(soup, indent=-5)
        soup.append(z)
        
        for x in lines:

            assert(x.has_tag)
            tag = x.build_tag(soup, indent=x.indent)

            if x.primary_name in ["background", "background_video"]:
                assert(z.name == "section")
                z.append(tag)
                tag = soup.new_tag("div",indent=-2)
                tag["class"] = ["wrap",]
                z.append(tag)

            elif x.primary_name == "footer":
                z.findParent('section').append(tag)
            
            elif x.indent > z["indent"]:
                z.append(tag)
            
            elif x.indent == z["indent"]:
                z.parent.append(tag)

            elif x.indent < z["indent"]:
                
                while x.indent < z["indent"]:
                    z = z.parent

                # Take one more step so we are on the parent
                z.parent.append(tag)
                
            z = tag

        # We need to resoup the pot
        soup = bs4.BeautifulSoup(unicode(soup),'html.parser')
    
        # Remove all the indent tags
        for tag in soup.find_all(True, indent=True):
            del tag.attrs["indent"]

        # Remove all the text tags and replace with a string
        #for tag in soup.find_all("text"):
        #    tag.unwrap()

        self.soup = soup

    def __iter__(self):
        for line in self.lines:
            yield line

    def __repr__(self):
        return self.soup.prettify()

            
########################################################################

if __name__ == "__main__":

    P = inline_markdown_paser()

    T = tagline("This is a [link](https://www.google.com)")    
    print P(T.text)
    
    T = tagline("This is **bold** _text_ with `code`.")    
    print P(T.text)

    T = tagline(r"This is $$\int_a^b a*b*c x^2 \frac{x}{y}$$ math.")
    print P(T.text)

    T = tagline(r"This is :coffee: and ::coffee:: emoji.")
    print P(T.text)

    print P.used
