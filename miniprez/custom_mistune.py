import copy, re
from mistune import Renderer, InlineGrammar, InlineLexer, Markdown
from mistune import BlockGrammar, BlockLexer, Markdown


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

    def Emoji(self, name):
        return f"<emoji data-emoji-alias='{name}'/></emoji>"

    def FontAwesome(self, name):
        return f"<span class='fa fa-{name}' aria-hidden=true></i>"

    def KaTeX(self, expression):
        return f'<span class="equation" data-expr="{expression}">'


class DivClassInlineLexer(InlineLexer):
    def enable(self):

        self.default_rules.remove("escape")
        self.default_rules.remove("linebreak")

        # OpenBlock, ...align-center.bg-black
        grammar = r"\.\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"
        self.rules.SectionTags = re.compile(grammar)
        self.default_rules.insert(0, "SectionTags")

        # OpenBlock, ..align-center.bg-black
        # Matching pattern, two dots then valid class names dot separated
        grammar = r"\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"
        self.rules.OpenBlock = re.compile(grammar)
        self.default_rules.insert(1, "OpenBlock")

        # CloseBlock, ..
        grammar = r"[^\\]\.\."
        self.rules.CloseBlock = re.compile(grammar)
        self.default_rules.insert(2, "CloseBlock")

        # LineBlock, .text-data
        grammar = r"\.([\-\w\d]+[\.[\-\w\d]+]?)(.*)"
        self.rules.LineBlock = re.compile(grammar)
        self.default_rules.insert(3, "LineBlock")

        # Emoji, :stuck_out_tongue_closed_eyes:
        grammar = r"::([\w\_]+)::"
        self.rules.FontAwesome = re.compile(grammar)
        self.default_rules.insert(4, "FontAwesome")

        # Emoji, :stuck_out_tongue_closed_eyes:
        grammar = r"(:[\w\_]+:)"
        self.rules.Emoji = re.compile(grammar)
        self.default_rules.insert(5, "Emoji")

        # Single line KaTeX, $\int_{-\infty}^\infty \hat \f\xi\,e^{2 \pi i \xi x} \,d\xi$
        grammar = r"\$([^\n]+)\$"
        self.rules.KaTeX = re.compile(grammar)
        self.default_rules.insert(6, "KaTeX")

        # SlashDotEscape, \.
        grammar = r"\\\."
        self.rules.SlashDotEscape = re.compile(grammar)
        self.default_rules.insert(-1, "SlashDotEscape")

        # AlmostText, anything but a prefixed (:.@)
        grammar = r"^[\s\S]+?(?=[\\<!\[_*`~@.:]|https?://| {2,}\n|$)"
        self.rules.AlmostText = re.compile(grammar)
        self.default_rules.insert(-1, "AlmostText")

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
        return self.renderer.Emoji(m.group(1))

    def output_FontAwesome(self, m):
        return self.renderer.FontAwesome(m.group(1))

    def output_KaTeX(self, m):
        return self.renderer.KaTeX(m.group(1).strip())

    def output_SlashDotEscape(self, m):
        return "."

    def output_AlmostText(self, m):
        return m.group()

    def output_text(self, m):
        # We normally shouldn't be here, but return even if we do
        return m.group()


# Monkeypatch the paragraph
class Markdown_NP(Markdown):
    def output_paragraph(self):
        text = self.token["text"].strip()
        return self.inline(text + " ")


# Globally build the parser

renderer = DivClassRenderer()
inline = DivClassInlineLexer(renderer)

# Enable the features
inline.enable()

parser = Markdown_NP(renderer, inline=inline)


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

$ \int_{-\infty}^\infty \hat \f\xi\,e^{2 \pi i \xi x} \,d\xi $ dsdfsd

sdasdasd
"""
    print(inline.default_rules)
    print(tx0)
    print("MARKDOWNED")
    tx1 = parser(tx0)
    print(tx1)
