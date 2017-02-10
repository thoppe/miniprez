import itertools
import bs4
import pyparsing as pyp
from pyparsing import Word, Group, QuotedString
from pyparsing import ZeroOrMore, OneOrMore, Optional
from custom_tags import _registered_custom_tags
from inline_markdown import inline_markdown_parser

_soup = bs4.BeautifulSoup("","html.parser")

class tagline(object):
    '''
    Each line is parsed by tokens individually until no preprocessing 
    tokens are left.
    '''

    def __init__(self, line):
  
        self.line = line

        token = lambda c: pyp.Literal(c).suppress()

        g_name = Word(pyp.alphanums+'-_')
        g_quote = QuotedString('"')|QuotedString("'")
        g_header = Word('----')("name")+ZeroOrMore('-')
        
        g_option_token = Group( g_name("key") +
                                    token('=') +
                                    (g_name|g_quote)("value") )
        
        g_option = pyp.nestedExpr(content=g_option_token)

        g_tag   = (token('@') + g_name('name') +
                   Optional(g_option('options')))
                       
        g_class = token('.') + g_name('name')

        g_classlist = Group(ZeroOrMore(g_class))('classes')

        g_format_header = g_header + g_classlist
        g_format_named_tag = g_tag + g_classlist
        g_format_div_tag = Group(OneOrMore(g_class))('classes')

        g_format_tag = Group(g_format_named_tag | g_format_div_tag)
               
        g_format = Group(Group(g_format_header)|OneOrMore(g_format_tag))
        
        grammar = Optional(g_format)('format') + pyp.restOfLine('text')

        #self.tag_name = ""
        #self.classnames = []
        #self.tag_options = {}

        self.tags = None

        '''

        '''
        #g_format_header.setParseAction(set_tagname_section)        
        #g_format_tag.setParseAction(parse_format)

        try:
            res = grammar.parseString(line)
        except pyp.ParseException as Ex:
            print 'Failed parsing "{}"'.format(line)
            raise Ex

        #### STOP HERE
        self.text = res['text'].strip()
        self.tags = []

        if res.format:
            self.parse_format(res.format[0])

    def parse_format(self, res):
        
        for tag in res:
            
            if tag.name == '----':
                tag.name = 'section'

            # If classnames are used but name is empty
            # default to a div
            if not tag.name and tag.classes:
                tag.name = 'div'

            item = {}
            item = {"name":tag.name,
                    "classes":tag.classes.asList(),
                    "options":{}}

            if len(tag.options):
                for opt in tag.options[0]:
                    item["options"][opt.key] = opt.value

            self.tags.append(item)
    
    @property
    def indent(self):
        is_space = lambda x:x in ['\t',' ']
        return len(list(itertools.takewhile(is_space,self.line)))

    @property
    def empty(self):
        return not (self.text or self.tags)

    def __repr__(self):
        keys = ("tags", "text")
        vals = (getattr(self,x) for x in keys)
        return str(dict(zip(keys,vals)))

    def build(self, **kwargs):

        # Build the nested tags
        
        blocks = []
        for item in self.tags:
            name = item["name"]
            
            if name in _registered_custom_tags:
                tag = _registered_custom_tags[name](item, _soup)
            else:
                tag = _soup.new_tag(name)

            if item["classes"]:
                tag['class'] = tag.get('class',[]) + item["classes"]

            for key,val in item["options"].items():
                tag[key] = val

            blocks.append(tag)

        # Only insert items into the outermost tag
        for key,val in kwargs.items():
            blocks[0][key] = val

        # Insert text into the deepest tag
        if self.text:
            # Make any markdown modifications
            text = inline_markdown_parser(self.text)
            html_text = bs4.BeautifulSoup(text,'html.parser')
            blocks[-1].append(html_text)

        # Nest the blocks
        while len(blocks)>1:
            blocks[-2].append(blocks.pop(-1))

        return blocks[0]

if __name__ == "__main__":

    print tagline("---- .blue .purple")
    print tagline("----")
    print tagline("@h1(sky='orange' sun='set') .red .blue @h2 .dragons @h3(moon='blue') hi")
    print tagline("@h1 @h2 hi")

    print tagline(".blue .red moon")
    print tagline("hi")
    print tagline("").empty, tagline("hi").empty, tagline(".blue").empty
    print tagline("  .baby").indent, tagline("baby").indent

    T = tagline('@h1(sky="orange") @h2 @h3 hi')
    print T.build(indent=2)

    print tagline('@h2 @line').build()
    print tagline('@background(src="www") .blue @h2 text').build()

    

    
    
    
