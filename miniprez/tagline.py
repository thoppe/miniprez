import itertools
import bs4
import pyparsing as pyp
from pyparsing import Word, Group, QuotedString, Combine
from pyparsing import ZeroOrMore, OneOrMore, Optional, Literal
from custom_tags import _registered_custom_tags
from inline_markdown import inline_markdown_parser

_soup = bs4.BeautifulSoup("", "html.parser")


class tagline(object):

    '''
    Each line is parsed by tokens individually until no preprocessing
    tokens are left.
    '''

    def __init__(self, line):

        self.line = line

        def token(c):
            return Literal(c).suppress()

        name = Word(pyp.alphanums + '-_://.')
        quote = QuotedString('"') | QuotedString("'")
        header = Word('----')("name") + ZeroOrMore('-')

        named_option = name("key") + token('=') + (name | quote)("value")
        unnamed_option = (name | quote)("value")
        option_token = Group(named_option | unnamed_option)

        option = pyp.nestedExpr(content=option_token)

        tag = token('@') + name('name') + Optional(option('options'))

        MD_tags = OneOrMore('#') | Literal('+') | Literal('|')
        MD_tags = Combine(MD_tags)('name') + Optional(option('options'))

        cls = token('.') + name('name')

        classlist = Group(ZeroOrMore(cls))('classes')

        format_header = header + classlist
        format_named_tag = tag + classlist
        format_MD_tag = MD_tags + classlist
        format_div_tag = Group(OneOrMore(cls))('classes')

        format_tag = Group(format_named_tag |
                           format_div_tag |
                           format_MD_tag)

        g_format = Group(Group(format_header) | OneOrMore(format_tag))

        grammar = Optional(g_format)('format') + pyp.restOfLine('text')

        self.tags = None

        try:
            res = grammar.parseString(line)
        except pyp.ParseException as Ex:
            msg = 'Failed parsing "{}"'.format(line)
            raise Ex(msg)

        self.text = res['text'].strip()
        self.tags = []

        if res.format:
            self.parse_format(res.format[0])

    def parse_format(self, res):

        for tag in res:
            extra_classes = []

            if len(tag.name) >= 4 and tag.name[:4] == '----':
                tag.name = 'section'

            elif set(tag.name) == set('#'):
                tag.name = 'h{}'.format(len(tag.name))

            elif tag.name == '+':
                tag.name = 'li'

            elif tag.name == '|':
                tag.name = 'div'
                extra_classes += ['column']

            # If classnames are used but name is empty
            # default to a div
            if not tag.name and tag.classes:
                tag.name = 'div'

            item = {}
            item = {"name": tag.name,
                    "classes": tag.classes.asList() + extra_classes,
                    "options": {}}

            if len(tag.options):
                for opt in tag.options[0]:
                    item["options"][opt.key] = opt.value

            self.tags.append(item)

    @property
    def indent(self):
        def is_space(x):
            return x in ['\t', ' ']
        return len(list(itertools.takewhile(is_space, self.line)))

    @property
    def empty(self):
        return not (self.text or self.tags)

    @property
    def primary_name(self):
        if not self.tags:
            return "text"
        return self.tags[0]["name"]

    def is_header(self):
        return self.primary_name == "section"

    def __eq__(self, T2):
        if T2.text != self.text:
            return False
        if T2.indent != self.indent:
            return False
        return T2.tags == self.tags

    def __repr__(self):
        # keys = ("tags", "text", "indent")
        # vals = (getattr(self, x) for x in keys)
        # return str(dict(zip(keys, vals)))
        return str(self.build())

    def build(self, **kwargs):

        text = self.text

        # Build the nested tags
        blocks = []
        for k, item in enumerate(self.tags):
            name = item["name"]

            item["text"] = ""
            is_last_element = (k == len(self.tags) - 1)

            # Assign text to only the final element
            if is_last_element:
                item["text"] = text

            if name in _registered_custom_tags:
                tag = _registered_custom_tags[name](item)

                # Text may have changed, reflect this
                if is_last_element:
                    text = item["text"]

            else:
                tag = _soup.new_tag(name)

            if item["classes"]:
                tag['class'] = tag.get('class', []) + item["classes"]

            for key, val in item["options"].items():
                if key and key[0] == '_':
                    continue

                tag[key] = val

            blocks.append(tag)

        # Insert text into the deepest tag
        if text:
            # Make any markdown modifications
            MD_text = inline_markdown_parser(text)
            tag = _soup.new_tag("text")
            tag.append(bs4.BeautifulSoup(MD_text, 'html.parser'))

            if blocks:
                blocks[-1].append(tag)
            else:
                blocks.append(tag)

        # Only insert items into the outermost tag
        for key, val in kwargs.items():
            blocks[0][key] = val

        # Nest the blocks
        while len(blocks) > 1:
            blocks[-2].append(blocks.pop(-1))

        block = blocks[0]

        # If there aren't any inner sections, we are done
        if block.find() is None:
            return block

        # Othwerwise, fix punctuation errors
        punctuation = ".,!/;:%'\""

        for x in block.find():
            if not isinstance(x, bs4.element.NavigableString):
                continue
            if len(x) <= 1:
                continue
            if x[0] == ' ' and x[1] in punctuation:
                xs = bs4.element.NavigableString(x.string[1:])
                x.replace_with(xs)

        return block


if __name__ == "__main__":
    pass

    # print(tagline("----"))
    # print(tagline("-----"))

    # print(tagline("@h1 big dog"))
    # print(tagline("### little dog").build())
    # print(tagline("---- .blue .purple"))
    # print(tagline("hi"))
    # print(tagline("This is the **end**. People.").build())
    # print(tagline("  .baby").indent, tagline("baby").indent)
    # print(tagline(".blue .red moon"))
    # print(tagline("@h1 @h2 hi"))
    # print(tagline("+ list item").build())
    # print(T.build(indent=2))
    # print(tagline('@h2 @line').build())
    # T1 = tagline('@background(foobar)')
    # T = tagline('@background(src="www") .blue @h2 dogs')
    #print tagline('@figure(src="www" width=700) ')
    print tagline('@img(src="www" width=700) ')
