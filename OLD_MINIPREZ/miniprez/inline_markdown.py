import pyparsing as pyp
import bs4
from emoji import emojize

QS = pyp.QuotedString


class Inline_Markdown_Paser(object):

    def __init__(self):
        # Keep track of the tags that were used
        self.used = {
            "emoji": False,
            "font_awesome": False,
            "math": False,
        }

        strongred = QS("*").setParseAction(self._strongred)
        strong = QS("**").setParseAction(self._strong)
        italic = QS("_").setParseAction(self._italic)
        emoji = QS(":").setParseAction(self._emoji)
        font_awesome = QS("::").setParseAction(self._font_awesome)

        code = QS("`", escChar='&&&', convertWhitespaceEscapes=False)
        code.setParseAction(self._code)

        math = QS(quoteChar="$", convertWhitespaceEscapes=False)
        math.setParseAction(self._math)

        text = QS(quoteChar="[", endQuoteChar="]")
        href = QS(quoteChar="(", endQuoteChar=")")
        link = (text + href).setParseAction(self._link)

        text_transforms = strong | strongred | italic
        transforms = (math | text_transforms | code |
                      font_awesome | emoji | link)
        plain_text = pyp.Word(pyp.printables)
        whitespace = pyp.White(' ') | pyp.White('\t')
        self.grammar = pyp.OneOrMore(transforms | plain_text | whitespace)

    def _strongred(self, x):
        tag = self._strong(x)
        tag["style"] = "color:#c23"
        return tag

    def _strong(self, x):
        tag = soup.new_tag("strong")
        tag.string = x[0]
        return tag

    def _italic(self, x):
        tag = soup.new_tag("em")
        tag.string = x[0]
        return tag

    def _code(self, x):
        tag = soup.new_tag("code")
        tag.string = x[0]
        return tag

    def _link(self, x):
        tag = soup.new_tag("a", href=x[1])
        tag.string = x[0]
        return tag

    def _font_awesome(self, x):
        self.used['font_awesome'] = True

        tag = soup.new_tag("i")
        tag["class"] = ["fa", "fa-{}".format(x[0])]
        tag["aria-hidden"] = "true"
        return tag

    def _emoji(self, x):
        self.used['emoji'] = True
        return emojize(":{}:".format(x[0]), use_aliases=True)

    def _math(self, x):
        self.used['math'] = True

        tag = soup.new_tag("div")
        tag["class"] = ["equation", ]
        tag["data-expr"] = x[0]
        return tag

    def __call__(self, text):
        tags = self.grammar.parseString(text)
        return ' '.join(map(unicode, tags))


# Create one shared instance
inline_markdown_parser = Inline_Markdown_Paser()
soup = bs4.BeautifulSoup("<div></div>", 'html.parser')

if __name__ == "__main__":

    P = Inline_Markdown_Paser()

    text = "This is a [link](https://www.google.com)"
    print(P(text))

    text = "This is **bold** _text_ with `code`."
    print(P(text))

    text = "This is $$\int_a^b a*b*c x^2 \frac{x}{y}$$ math."
    print(P(text))

    text = "This is :coffee: and ::coffee:: emoji."
    print(P(text))

    print(P.used)
