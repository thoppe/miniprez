import itertools
import bs4
import copy

from tagline import tagline

_section_header_token = '----'
_comment_marker_token = '//'
_code_block_marker = "```"


def is_section_header(line):
    if len(line) < 4:
        return False
    return line[:4] == _section_header_token


def section_iterator(lines):
    section = []
    for line in lines:
        if is_section_header(line) and section:
            yield section
            section = [line, ]
        else:
            section.append(line)

    yield section


def file_iterator(f_md):

    # Read all the lines
    with open(f_md) as FIN:
        for line in FIN:
            if not line.strip():
                continue
            if len(line) >= 2 and line.lstrip()[:2] == _comment_marker_token:
                continue
            yield line.rstrip()

#


class section(object):

    def __init__(self, lines):

        self.lines = []

        # Custom work for a code block
        is_inside_code_block = False
        code_buffer = []
        code_block_indent = None
        for line in lines:

            is_code_block = _code_block_marker == line.lstrip()[:3]

            if is_code_block:
                is_inside_code_block = not is_inside_code_block

            if is_code_block or is_inside_code_block:
                code_buffer.append(line.rstrip())

            if is_code_block and not is_inside_code_block:
                space_ITR = itertools.takewhile(lambda x: x == ' ', line)
                code_block_indent = len(list(space_ITR))

                # Remove the code buffer lines
                code_buffer = code_buffer[1:-1]

                # Empty out the contents of the buffer
                code_block = '__CODE_BLOCK_SPACE'.join(code_buffer)
                header = code_block_indent * ' ' + '@codeblock '
                block = header + code_block
                self.lines.append(block)

                code_buffer = []
            elif not is_inside_code_block:
                self.lines.append(line)

        # Parse and filter for blank lines
        self.lines = [x for x in map(tagline, self.lines) if not x.empty]

        # Section shouldn't be empty
        assert(self.lines)

        # Section should start with a header
        assert(self.lines[0].is_header())

        soup = bs4.BeautifulSoup("", 'html.parser')
        lines = iter(self)

        # Parse the header
        z = lines.next().build(indent=-5)
        soup.append(z)

        for x in lines:
            tag = x.build(indent=x.indent)
            name = x.primary_name
            if name in ["background", "background_video", "unsplash"]:
                assert(z.name == "section")
                z.append(tag)
                tag = soup.new_tag("div", indent=-2)
                tag["class"] = ["wrap", ]
                z.append(tag)

            elif name == "footer":
                z.findParent('section').append(tag)

            elif x.indent > z["indent"]:
                # Append to the deepest child
                children = z.find_all()
                if not children:
                    z.append(tag)
                else:
                    children[-1].append(tag)

            elif x.indent == z["indent"]:
                z.parent.append(tag)

            elif x.indent < z["indent"]:
                while "indent" not in z.attrs or x.indent < z["indent"]:
                    z = z.parent

                # Take one more step so we are on the parent
                z.parent.append(tag)

            z = tag

        # We need to resoup the pot
        soup = bs4.BeautifulSoup(unicode(soup), 'html.parser')

        # Remove all the indent tags
        for tag in soup.find_all(True, indent=True):
            del tag.attrs["indent"]

        # If there are any li elements without a proper parent ul,ol
        # wrap them in one
        for tag in soup.find_all('li'):
            parent = tag.parent

            if parent.name not in ['ol', 'ul']:
                ul = soup.new_tag('ul')
                ul['class'] = ['markdownlist', ]

                for x in tag.find_next_siblings('li'):
                    ul.append(x.extract())
                ul.insert(0, copy.copy(tag))

                tag.replaceWith(ul)

        # Remove all the text tags and replace with a string
        # for tag in soup.find_all("text"):
        #    tag.unwrap()

        self.soup = soup

    def __iter__(self):
        for line in self.lines:
            yield line

    def __repr__(self):
        return str(self.soup)  # .soup.prettify()


#

if __name__ == "__main__":
    section_text = '''----
This is a code block
```
print x
```
And we're done!
'''

    S = section(section_text.split('\n'))
    print(S.soup.prettify())
