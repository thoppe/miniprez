import itertools
import bs4
import string
import pyparsing as pyp
import custom_tags
from emoji import emojize

_registered_custom_tags = {
    "background" : custom_tags.background
}

_section_header_token = '----'
_comment_marker_token = '//'

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

        #line = '''@p(foo="bar back" poo='goodfs ' dog=3) @h1 @p @h1 .text-intro Good karma and productivity.'''
        #line = '''@background(url="https://webslides.tv/static/images/nature.jpg")'''
  
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
                           
        g_classname = pyp.Literal(".").suppress() + g_name.setResultsName('name')

        g_format_text = pyp.ZeroOrMore(pyp.Group(g_tag | g_classname | g_header))
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
        
        if len(tags)>1:
            msg = 'Only one tag allowed per line, "{}"'.format(line)
            raise SyntaxError(msg)

        # Select only the first tag
        self.tag = tags[0] if tags else None

        # If classnames are used but tag is None, default to a div
        if self.tag is None and self.classnames:
            self.tag = ('div',{})

        # Otherwise set the tag to text
        elif self.tag is None:
            self.tag = ('text',{})

        self.primary_name = self.tag[0]

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
            tag['class'] = self.classnames

        options = self.tag[1]
        for key,val in options.items():
            tag[key] = val

        for key,val in kwargs.items():
            tag[key] = val

        if self.text:
            # Make any markdown modifications
            text = _INLINE_MARKDOWN_PARSER(self.text)
            html_text = bs4.BeautifulSoup(text,'lxml').p
            html_text["id"] = "_remove"
            tag.append(html_text)
            tag.find('p',{"id":"_remove"}).unwrap()

        return tag


class section(object):

    def __init__(self, lines):
        
        # Parse and filter for blank lines
        self.lines = [x for x in map(tagline,lines) if not x.is_empty]

        # Section shouldn't be empty
        assert(self.lines)

        # Section should start with a header
        assert(self.lines[0].is_section_header)

        soup  = bs4.BeautifulSoup("",'lxml')
        lines = iter(self)
        
        # Parse the header
        z = lines.next().build_tag(soup, indent=-2)
        soup.append(z)
        
        for x in lines:

            assert(x.has_tag)
            tag = x.build_tag(soup, indent=x.indent)

            if x.primary_name == "background":
                assert(z.name == "section")
                z.append(tag)
                tag = soup.new_tag("div",indent=-1)
                tag["class"] = "wrap"
                z.append(tag)
            
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
            
                
        # Remove all the indent tags
        for tag in soup.findAll(True, {"indent":True}):
            del tag["indent"]

        # Remove all the text tags and replace with a string
        for tag in soup.findAll("text"):
            tag.unwrap()

        self.soup = soup

    def __iter__(self):
        for line in self.lines:
            yield line

    def __repr__(self):
        return self.soup.prettify()
    
########################################################################


class inline_markdown_paser(object):

    def __init__(self):
        strong  = pyp.QuotedString("**")
        strong.setParseAction(lambda x:"<strong>{}</strong>".format(x[0]))

        strong2  = pyp.QuotedString("*")
        strong2.setParseAction(lambda x:"<strong>{}</strong>".format(x[0]))

        italic  = pyp.QuotedString("_")
        italic  = italic.setParseAction(lambda x:"<em>{}</em>".format(x[0]))

        code  = pyp.QuotedString("`")
        code  = code.setParseAction(lambda x:"<code>{}</code>".format(x[0]))

        emoji = pyp.QuotedString(":")
        func = lambda x: emojize(":{}:".format(x[0]), use_aliases=True)
        emoji = emoji.setParseAction(func)
        
        self.grammar = strong|strong2|italic|code|emoji


    def __call__(self, text):
        return self.grammar.transformString(text)

_INLINE_MARKDOWN_PARSER = inline_markdown_paser()
            
########################################################################

if __name__ == "__main__":
    T = tagline("This is **bold** _text_ with `code`.")
    P = inline_markdown_paser()
    
    print P(T.text)
