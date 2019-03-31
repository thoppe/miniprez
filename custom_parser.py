import copy, re
from mistune import Renderer, InlineGrammar, InlineLexer, Markdown

    
def get_classnames(class_string):
    s = " ".join(class_string.lstrip(".").split("."))
    return s if s else None

class OpenBlockClassRenderer(Renderer):
    def OpenBlockClass(self, names):
        return f"<div class='{names}'>"

class OpenBlockClassInlineLexer(InlineLexer):
    name = "OpenBlockClass"

    def enable(self):
        # Matching pattern, two dots then valid class names dot separated
        grammar = r"\.\.[\-\w\d]+[\.[\-\w\d]+]?"

        setattr(self.rules, self.name, re.compile(grammar)) 
        self.default_rules.insert(10, self.name)

    def output_OpenBlockClass(self, m):
        tags = get_classnames(m.group())
        return getattr(self.renderer, self.name)(tags)

renderer = OpenBlockClassRenderer()
inline = OpenBlockClassInlineLexer(renderer)
# enable the feature
inline.enable()

markdown = Markdown(renderer, inline=inline)

tx0 = "Here we go ..aligncenter.black fool."
tx0 = "# ..aligncenter.black fool."
tx1 = markdown(tx0)

print(tx0)
print(tx1)
