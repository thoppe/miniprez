import copy, re
from mistune import Renderer, InlineGrammar, InlineLexer, Markdown
#from mistune import RBlockGrammar, BlockLexer, Markdown

    
def get_classnames(class_string):
    s = " ".join(class_string.lstrip(".").split("."))
    return s if s else None

class DivClassRenderer(Renderer):
    
    def OpenBlockClass(self, names):
        return f"<div class='{names}'>"

    def CloseBlockClass(self):
        return f"</div>"

class DivClassInlineLexer(InlineLexer):

    def enable_OpenBlockClass(self):
        # Matching pattern, two dots then valid class names dot separated
        grammar = r"\.\.[\-\w\d]+[\.[\-\w\d]+]?"

        self.rules.OpenBlockClass = re.compile(grammar) 
        self.default_rules.insert(10, "OpenBlockClass")

    
    def enable_CloseBlockClass(self):
        # Matching pattern, two dots and a space
        grammar = r"\.\."

        self.rules.CloseBlockClass = re.compile(grammar) 
        self.default_rules.insert(11, "CloseBlockClass")

    def output_OpenBlockClass(self, m):
        tags = get_classnames(m.group())
        return self.renderer.OpenBlockClass(tags)

    def output_CloseBlockClass(self, m):
        return self.renderer.CloseBlockClass()

renderer = DivClassRenderer()
inline = DivClassInlineLexer(renderer)
# enable the features
inline.enable_OpenBlockClass()
inline.enable_CloseBlockClass()

markdown = Markdown(renderer, parse_inline_html=False, inline=inline)

tx0 = "Here we go ..aligncenter.black fool."
tx0 = '''# ..aligncenter.black fool.
..
assaf

that
'''
tx1 = markdown(tx0)

print(tx0)
print(tx1)
