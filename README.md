# miniprez

Dead simple markup to web-friendly presentations that look great on mobile and on the big screen.
For a live demo see the tutorial [input](https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md) and the [slides](https://thoppe.github.io/miniprez/tutorial.html).

### Usage

Miniprez is a command-line tool that turns special markup into slides.
All slides are separated by `----`. Hello world in miniprez looks like:

    ----
    Hello world.

Let's add some style to it!

    ----- 
    @h1 .text-landing Hello world.

The syntax to miniprez is pretty simple simple, each line is mostly independent of the others.
The `@` symbol creates a new html element and the `.` applies a class to that element, thus the first line becomes `<h1 class="text-landing">Hello world.</h1>`.

If you want tags to nest into each other, whitespace matters

    @h1
       This is big text.
       @strong This is big bold text.

If all you want to do is create a div with a class you don't need to explictly say `@div`, for example:

    .text-landing Hello.

gives `<div class="text-landing">Hello.</div>`.

Inline markdown shortcuts that work too,

    This is **bold**, this is _italic_, this is `code`, this is a [link](www.github.com/thoppe).

The markdown is enchanced with [emoji](http://www.webpagefx.com/tools/emoji-cheat-sheet/), [font-awesome](http://fontawesome.io/icons/) and [math](https://en.wikibooks.org/wiki/LaTeX/Mathematics),

    This is a :smile: and this is ::twitter:: and and equation $$(a+b)^2$$.

Lists can be made from either a combination of `@ul` and `@li` elements or simply

    + list item one
    + list item two
    + list item three
    
Large code blocks are made from fences of '```' and will be automatically highlighted.

    ```
    for x in A:
        print (x**2)
    ```

Element arguments can be added with like this

    @a(href="www.google.com" id="foo")

With this syntax there are some additional elements miniprez has added

| function name  | description  | example  |
|---|---|---|
| `@background`        | background image | ...  |
| `@background_video`  | full screen background video  | ...  |
| `@line`  | Horzontial  | Shortcut for hr  |
| `@figure`  | Image  | ...  |
| `@button`  | Pretty button  | ...  |



### Libraries used:

+ [webslides](https://github.com/jlantunez/webslides): Custom CSS 
+ [KaTeX](https://github.com/Khan/KaTeX): Javascript math rendering
+ [code prettify](https://github.com/google/code-prettify): Syntax highlighting 

+ [pyparsing](http://pyparsing.wikispaces.com/)
+ [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### (upcoming) features!

+ [x] Custom tags (background, background_video, line, button, figure)
+ [x] Code blocks
+ [x] BG videos examples!
+ [x] Nested divs
+ [x] List support
+ [ ] README documentation.
+ [ ] Support for command line compilation
+ [ ] Embedding tools (convert project to monolith html)
+ [ ] Global options (font?)
+ [ ] Selectively load libraries (eg. font-awesome & katex) on use
+ [ ] Slide number url