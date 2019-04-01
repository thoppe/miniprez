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
        return f"<div class='{names}'>{remaining}</div>"

    
class DivClassInlineLexer(InlineLexer):

    rule_num = 0

    def enable(self):

        self.default_rules.remove('escape')
        self.default_rules.remove('linebreak')

        # def enable_OpenBlockClass(self):
        # Matching pattern, two dots then valid class names dot separated
        grammar = r"[^\\]\.\.[\-\w\d]+[\.[\-\w\d]+]?\s"

        self.rules.OpenBlockClass = re.compile(grammar) 
        self.default_rules.insert(self.rule_num, "OpenBlockClass")

        # def enable_CloseBlockClass(self):
        # Matching pattern, two dots, but no triple dot
        grammar = r"[^\\]\.\."

        self.rules.CloseBlockClass = re.compile(grammar) 
        self.default_rules.insert(self.rule_num+1, "CloseBlockClass")

        # def enable_LineBlockClass(self):
        # Matching pattern, one dots and a space. Do a lookahead here
        #grammar = r"\.([\-\w\d]+[\.[\-\w\d]+]?)(?=(.*))"
        grammar = r"[^\\]\.([\-\w\d]+[\.[\-\w\d]+]?)(.*)"

        self.rules.LineBlockClass = re.compile(grammar) 
        self.default_rules.insert(self.rule_num+2, "LineBlockClass")

        # Fix slashdot escape
        grammar = r'\\\.'
        self.rules.SlashDotEscape = re.compile(grammar) 
        self.default_rules.insert(-1, "SlashDotEscape")

        # def enable_AlmostText(self):
        # Anything BUT a prefixed dot or @ pattern
        grammar = r'^[\s\S]+?(?=[\\<!\[_*`~@.]|https?://| {2,}\n|$)'
        self.rules.AlmostText = re.compile(grammar) 
        self.default_rules.insert(-1, "AlmostText")


    def output_LineBlockClass(self, m):
        tags = get_classnames(m.group(1))

        # Run the parser over what's inside
        remaining = self.output(m.group(2))
        
        return self.renderer.LineBlockClass(tags, remaining)

    def output_OpenBlockClass(self, m):
        tags = get_classnames(m.group())
        return self.renderer.OpenBlockClass(tags)

    def output_CloseBlockClass(self, m):
        return self.renderer.CloseBlockClass()

    def output_SlashDotEscape(self, m):
        return '.'
    
    def output_AlmostText(self, m):
        #print("ALMOST", m.group())
        return m.group()

    def output_text(self, m):
        print("TEXT", m.group())
        # We don't want to escape any text! Be gentle here.
        return m.group()
        

# Monkeypatch the paragraph
class Markdown_NP(Markdown):
    
    def output_paragraph(self):
        text = self.token['text'].strip()
        return self.inline(text+' ')
    
renderer = DivClassRenderer()
inline = DivClassInlineLexer(renderer)

# Enable the features
inline.enable()

print(inline.default_rules)
#exit()
        
markdown = Markdown_NP(renderer, parse_inline_html=True, inline=inline)
#markdown = Markdown(renderer, inline=inline)
#markdown = Markdown_NP()

tx0 = '''
..aligncenter.black
# fool.
the
words
on
the table 
\.wtf Out *of* center
here *we* go
'''



print(tx0)
print("MARKDOWNED")
tx1 = markdown(tx0)
print(tx1)
