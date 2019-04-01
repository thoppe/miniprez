import copy, re
from mistune import Renderer, InlineGrammar, InlineLexer, Markdown

# from mistune import RBlockGrammar, BlockLexer, Markdown


def get_classnames(class_string):
    s = " ".join(class_string.lstrip(".").split("."))
    return s if s else None


class DivClassRenderer(Renderer):
    def OpenBlockClass(self, names):
        return f"<div class='{names}'>"

    def CloseBlockClass(self):
        return f"</div>"


class DivClassInlineLexer(InlineLexer):

    rule_num = 10

    def enable_OpenBlockClass(self):
        # Matching pattern, two dots then valid class names dot separated
        grammar = r"\.\.[\-\w\d]+[\.[\-\w\d]+]?"

        self.rules.OpenBlockClass = re.compile(grammar)
        self.default_rules.insert(self.rule_num, "OpenBlockClass")

    def enable_CloseBlockClass(self):
        # Matching pattern, two dots and a space
        grammar = r"\.\."

        self.rules.CloseBlockClass = re.compile(grammar)
        self.default_rules.insert(self.rule_num + 1, "CloseBlockClass")

    def output_OpenBlockClass(self, m):
        tags = get_classnames(m.group())
        return self.renderer.OpenBlockClass(tags)

    def output_CloseBlockClass(self, m):
        print("MATCH!!!", m)

        return self.renderer.CloseBlockClass()


renderer = DivClassRenderer()
inline = DivClassInlineLexer(renderer)

# Enable the features
inline.enable_OpenBlockClass()
inline.enable_CloseBlockClass()

# Monkeypatch the paragraph
class Markdown_NP(Markdown):
    def output_paragraph(self):
        text = self.token["text"].strip()
        print(self.token, self.tokens)
        return self.inline(text + " " + "\n" + "\n")
        return self.renderer.paragraph(self.inline(self.token["text"]))


# markdown = Markdown_NP(renderer, parse_inline_html=True, inline=inline)
markdown = Markdown_NP(renderer, inline=inline, hard_wrap=True)

tx0 = """
..aligncenter.black
# fool.
the
words
on
the table

Out of center
"""

tx0 = """
the words
on the

table
"""

tx1 = markdown(tx0)

print(tx0)
print("MARKDOWNED")
print(tx1)
