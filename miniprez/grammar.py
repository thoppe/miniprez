import copy, re, itertools
from mistune import Renderer, InlineGrammar, InlineLexer, Markdown
from mistune import BlockGrammar, BlockLexer, Markdown
from mistune import _pre_tags
import logging

logger = logging.getLogger("miniprez")


def get_classnames(class_string):
    s = " ".join(class_string.strip().lstrip(".").split("."))
    return s if s else None


class DivClassRenderer(Renderer):
    def OpenBlock(self, names):
        return f"<div class='{names}'>"

    def CloseBlock(self):
        return f"</div>"

    def LineBlock(self, names, remaining):
        remaining = remaining.lstrip()
        return f"<span class='{names}'>{remaining}</span>"

    def SectionTags(self, names):
        return f"<meta data-slide-classes='{names}'/>"

    def Emoji(self, name, spacing=""):
        return f"{spacing}<emoji data-emoji-alias='{name}'/></emoji>"

    def FontAwesome(self, name, spacing=""):
        return f"{spacing}<span class='fa fa-{name}' aria-hidden=true></i>"

    def InlineLaTeX(self, expression, spacing=""):
        return f'{spacing}<span class="inline-equation" data-expr="{expression}"></span>'

    def BlockLaTeX(self, expression):
        expression = " ".join(expression.strip().split())
        return f'<div class="block-equation" data-expr="{expression}"></div>'

    def ShortImageLink(self, src, arguments, spacing=""):
        arguments = " ".join(arguments)
        return f'{spacing}<img src="{src}" {arguments} />'

    def BackgroundImageLink(self, src, arguments):
        arguments = " ".join(arguments)
        return f'<span {arguments} data-bg-src="{src}" data-is-bg=true></span>'

    def MetaInformation(self, key, value):
        return f'<meta name="{key}" content="{value}" data-is-header=true>'

    def Comment(self, text):
        return ""


class DivClassInlineLexer(InlineLexer):
    def enable(self):

        self._parse_inline_html = True

        self.default_rules.remove("escape")
        self.default_rules.remove("linebreak")

        rule_n = itertools.count()

        # Meta information
        grammar = re.compile(r"^%\s*([A-Z]\w*):\s*(.+?)(\n|$)")
        self.rules.MetaInformation = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "MetaInformation")

        # Comment information
        grammar = re.compile(r"^%(.*)(\n|$)")
        self.rules.Comment = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "Comment")

        # SectionTags, ...align-center.bg-black
        grammar = r"[\s]*\.\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"
        self.rules.SectionTags = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "SectionTags")

        # OpenBlock, ..align-center.bg-black
        # Matching pattern, two dots then valid class names dot separated
        grammar = r"[\s]*\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"
        self.rules.OpenBlock = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "OpenBlock")

        # CloseBlock, ..
        grammar = r"[\s]*[^\\]\.\."
        self.rules.CloseBlock = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "CloseBlock")

        # LineBlock, .text-data
        grammar = r"[\s]*\.([\-\w\d]+[\.[\-\w\d]+]?)(.*)"
        self.rules.LineBlock = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "LineBlock")

        # Background image link, !!(myimage.jpg class="dark")
        grammar = r"(^[\s]*)\!\!\(([^\)]+)\)"
        self.rules.BackgroundImageLink = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "BackgroundImageLink")

        # Short image link, !(myimage.jpg class="dark")
        grammar = r"(^[\s]*)\!\(([^\)]+)\)"
        self.rules.ShortImageLink = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "ShortImageLink")

        # FontAwesome, ::github::
        grammar = r"([\s]*)::([\w\_]+)::"
        self.rules.FontAwesome = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "FontAwesome")

        # Emoji, :stuck_out_tongue_closed_eyes:
        grammar = r"([\s]*)(:[\w\_]+:)"
        self.rules.Emoji = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "Emoji")

        # Block LaTeX, $$\int_{-\infty}^\infty \n \hat \f\xi\,e^{2 \pi i \xi x} \,d\xi$$
        grammar = "[\s]*\$\$([^\$]*)\$\$"
        self.rules.BlockLaTeX = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "BlockLaTeX")

        # Single line LaTeX, $\int_{-\infty}^\infty \hat \f\xi\,e^{2 \pi i \xi x} \,d\xi$
        grammar = r"([\s]*)\$([^\n]+)\$"
        self.rules.InlineLaTeX = re.compile(grammar)
        self.default_rules.insert(next(rule_n), "InlineLaTeX")

        # SlashDotEscape, \.
        grammar = r"\\\."
        self.rules.SlashDotEscape = re.compile(grammar)
        self.default_rules.insert(-1, "SlashDotEscape")

        # AlmostText1 matches \w\d and then things with a token
        tokens = r"\\<!\[_*`~@.:\$\%"
        grammar = r"^[\s]*[a-zA-Z0-9.-][\w\d%s]+" % tokens
        self.rules.AlmostText1 = re.compile(grammar)
        self.default_rules.insert(-1, "AlmostText1")

        # AlmostText2 matches up to a special token
        grammar = r"^[\s\S]+?(?=[%s ]|$)" % tokens
        self.rules.AlmostText2 = re.compile(grammar)
        self.default_rules.insert(-1, "AlmostText2")

    def output_MetaInformation(self, m):
        key, value = m.group(1), m.group(2)
        return self.renderer.MetaInformation(key, value)

    def output_Comment(self, m):
        return self.renderer.Comment(m.group(1))

    def output_LineBlock(self, m):
        tags = get_classnames(m.group(1))

        # Run the parser over what's inside
        remaining = self.output(m.group(2))
        return self.renderer.LineBlock(tags, remaining)

    def output_SectionTags(self, m):
        tags = get_classnames(m.group())
        return self.renderer.SectionTags(tags)

    def output_OpenBlock(self, m):
        tags = get_classnames(m.group())
        return self.renderer.OpenBlock(tags)

    def output_CloseBlock(self, m):
        return self.renderer.CloseBlock()

    def output_Emoji(self, m):
        return self.renderer.Emoji(name=m.group(2), spacing=m.group(1))

    def output_FontAwesome(self, m):
        return self.renderer.FontAwesome(name=m.group(2), spacing=m.group(1))

    def output_InlineLaTeX(self, m):
        return self.renderer.InlineLaTeX(
            expression=m.group(2).strip(), spacing=m.group(1)
        )

    def output_BlockLaTeX(self, m):
        return self.renderer.BlockLaTeX(m.group(1).strip())

    def output_ShortImageLink(self, m):
        tokens = m.group(2).split()
        return self.renderer.ShortImageLink(
            tokens[0], tokens[1:], spacing=m.group(1)
        )

    def output_BackgroundImageLink(self, m):
        tokens = m.group(2).split()
        return self.renderer.BackgroundImageLink(tokens[0], tokens[1:])

    def output_SlashDotEscape(self, m):
        return "."

    def output_AlmostText1(self, m):
        # logger.debug(f"AlmostText1 {m.group(0)}")
        return m.group()

    def output_AlmostText2(self, m):
        # logger.debug(f"AlmostText1 {m.group(0)}")
        return m.group()

    def output_text(self, m):
        # We normally shouldn't be here, but return even if we do
        return m.group()


# Monkeypatch the paragraph
class Markdown_NP(Markdown):
    def output_paragraph(self):
        text = self.token["text"].strip()
        result = self.inline(text + " ")
        return f"<p>{result}</p>"

    def output_open_html(self):
        """
        Override this, as we would like to always use our full inline parser
        """
        text = self.token["text"]
        tag = self.token["tag"]
        if self._parse_block_html and tag not in _pre_tags:
            text = self.inline(text)
        extra = self.token.get("extra") or ""
        html = "<%s%s>%s</%s>" % (tag, extra, text, tag)
        return self.renderer.block_html(html)


# Globally build the parser

renderer = DivClassRenderer()
inline = DivClassInlineLexer(renderer)

# Enable the features
inline.enable()

markdown_parser = Markdown_NP(renderer, inline=inline, parse_block_html=True)


if __name__ == "__main__":
    tx0 = r"""
...bg-black

..aligncenter.black
# fool.
the :smile: ::igloo::
words
on
the table 
.wtf Out *of* center
here *we* go

$$ \int_{-\infty}^\infty \hat \f\xi\,e^{2 \pi i \xi x} 
\,d\xi $$ 
"""
    tx0 = """
%Author: Travis Hoppe
%Author: Travis Hoppe
%Title: Miniprez tutorial

sdfsdf
% Foo bar

!!(https://source.unsplash.com/4mta-DkJUAg class="light")
"""

    # tx0 = "\n.alignright foobar"
    # tx0 = "Title: foo bar\nAuthor: dogs\nspaz\nTitle: foo bar"
    # tx0 = "www.google.com"
    # tx0 = "www.google.com \n <hr> sdfsdf"
    # tx0 = "The !(www.google.com foobar) "
    # tx0 = "The !!(www.google.com class='dark')"
    # tx0 = "The !(www.google.com height=300 width=400)"
    # tx0 = "The $x*x*x$"
    # tx0 = "The :smile:"
    # tx0 = ".text-landing **A pug and an Equation**"
    # import coloredlogs, logging
    # logger = logging.getLogger("miniprez")
    # fmt = "%(message)s"
    # coloredlogs.install(level="DEBUG", logger=logger, fmt=fmt)
    # logger.setLevel(logging.DEBUG)

    # Create a logger object.
    import coloredlogs

    logger = logging.getLogger("miniprez")
    fmt = "%(asctime)s %(levelname)s %(message)s"
    coloredlogs.install(level="DEBUG", logger=logger, fmt=fmt)

    print(inline.default_rules)
    print(tx0)
    print("MARKDOWNED")
    tx1 = markdown_parser(tx0)
    print(tx1)
