import copy, re
from mistune import Renderer, InlineGrammar, InlineLexer, Markdown
from mistune import BlockGrammar, BlockLexer, Markdown


def get_classnames(class_string):
    s = " ".join(class_string.strip().lstrip(".").split("."))
    return s if s else None


class DivClassRenderer(Renderer):
    def OpenBlockClass(self, names):
        return f"<div class='{names}'>"

    def CloseBlockClass(self):
        return f"</div>"

    def LineBlockClass(self, names, remaining):
        remaining = remaining.lstrip()
        return f"<span class='{names}'>{remaining}</span>"

    def SectionBlockClass(self, names):
        return f"<meta data-slide-classes='{names}'/>"

    def EmojiBlockClass(self, name):
        return f"<emoji data-emoji-alias='{name}'/></emoji>"


class DivClassInlineLexer(InlineLexer):
    def enable(self):

        self.default_rules.remove("escape")
        self.default_rules.remove("linebreak")

        # def enable_OpenBlockClass(self):
        # Matching pattern, three dots then valid class names dot separated
        grammar = r"\.\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"
        self.rules.SectionBlockClass = re.compile(grammar)
        self.default_rules.insert(0, "SectionBlockClass")

        # def enable_OpenBlockClass(self):
        # Matching pattern, two dots then valid class names dot separated
        grammar = r"\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"
        self.rules.OpenBlockClass = re.compile(grammar)
        self.default_rules.insert(1, "OpenBlockClass")

        # def enable_CloseBlockClass(self):
        # Matching pattern, two dots, but no triple dot
        grammar = r"[^\\]\.\."
        self.rules.CloseBlockClass = re.compile(grammar)
        self.default_rules.insert(2, "CloseBlockClass")

        # def enable_LineBlockClass(self):
        # Matching pattern, one dots and a space. Do a lookahead here
        grammar = r"\.([\-\w\d]+[\.[\-\w\d]+]?)(.*)"
        self.rules.LineBlockClass = re.compile(grammar)
        self.default_rules.insert(3, "LineBlockClass")

        # def enable_emoji(self):
        # Matching pattern, :stuck_out_tongue_closed_eyes:
        grammar = r"(:[\w\_]+:)(?!:)"
        self.rules.EmojiBlockClass = re.compile(grammar)
        self.default_rules.insert(4, "EmojiBlockClass")

        # Fix slashdot escape
        grammar = r"\\\."
        self.rules.SlashDotEscape = re.compile(grammar)
        self.default_rules.insert(-1, "SlashDotEscape")

        # def enable_AlmostText(self):
        # Anything BUT a prefixed dot or @ pattern
        grammar = r"^[\s\S]+?(?=[\\<!\[_*`~@.:]|https?://| {2,}\n|$)"
        self.rules.AlmostText = re.compile(grammar)
        self.default_rules.insert(-1, "AlmostText")

    def output_LineBlockClass(self, m):
        tags = get_classnames(m.group(1))

        # Run the parser over what's inside
        remaining = self.output(m.group(2))
        return self.renderer.LineBlockClass(tags, remaining)

    def output_SectionBlockClass(self, m):
        tags = get_classnames(m.group())
        return self.renderer.SectionBlockClass(tags)

    def output_OpenBlockClass(self, m):
        tags = get_classnames(m.group())
        return self.renderer.OpenBlockClass(tags)

    def output_CloseBlockClass(self, m):
        return self.renderer.CloseBlockClass()

    def output_EmojiBlockClass(self, m):
        return self.renderer.EmojiBlockClass(m.group(1))

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
    tx0 = """
...bg-black

..aligncenter.black
# fool.
the :smile:
words
on
the table 
.wtf Out *of* center
here *we* go
"""
    print(inline.default_rules)
    print(tx0)
    print("MARKDOWNED")
    tx1 = parser(tx0)
    print(tx1)
