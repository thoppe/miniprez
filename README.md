# MINIPREZ

Simple markup to web-friendly presentations that look great on mobile and on the big screen.
For a live demo see the tutorial [input](https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md) and the [slides](https://thoppe.github.io/miniprez/tutorial.html).

Miniprez is a command-line tool that turns special markup into slides.
Create a file called `hello.md` with the following examples to follow along.
Run `miniprez hello.md` to create a file named `hello.html`.
View `hello.html` in your web-browser and make sure to refresh each time you re-compile your slides!

### Installation

    pip install git+git://github.com/thoppe/miniprez.git

### Usage

miniprez is a command-line utility. If you've written a text file named `hello.md` with your presentation compile it with

    miniprez hello.md

and if everything works, `hello.html` should be ready to go! Follow the examples below and dig into [tutorial.md](https://raw.githubusercontent.com/thoppe/miniprez/develop/package/tutorial.md) for more syntax usage. To continuously rebuild every 3 seconds add the flag `--watch=3`.

### Tutorial

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

If all you want to do is create a div with a class you don't need to explicitly say `@div`, for example:

    .text-landing Hello.

gives `<div class="text-landing">Hello.</div>`.

Inline markdown shortcuts that work too,

    This is **bold**, this is _italic_, this is `code`, this is a [link](www.github.com/thoppe).

The markdown is enhanced with [emoji](http://www.webpagefx.com/tools/emoji-cheat-sheet/), [font-awesome](http://fontawesome.io/icons/) and [math](https://en.wikibooks.org/wiki/LaTeX/Mathematics),

    This is a :smile: and this is ::twitter:: and and equation $(a+b)^2$.

Lists can be made from either a combination of `@ul` and `@li` elements or simply

    + list item one
    + list item two
    + list item three

Columns can be built up from `.grid` and `.column` or use the shorthand for a column `|`

    .grid
        | # Big title
	| some text
    
Large code fences made from ` ``` ` and will be automatically code highlighted

    ```
    for x in A:
        print (x**2)
    ```

Element arguments can be added with like this

    @a(href="www.google.com" id="foo")

With this syntax there are some additional elements miniprez has added

| function name  | example | options
|---|---|---|
| `@background`  | @background(url="https://source.unsplash.com/4mta-DkJUAg") | `.light` `.dark` |
| `@unsplash`  | @unsplash(url=4mta-DkJUAg) | `.light` `.dark` |
| `@background_video`  | @background_video(url="https://cdn.shutterstock.com/...") | |
| `@button`  |  @button(href="https://github.com/thoppe/miniprez") | `.ghost` text after  |
| `@figure`  | @figure(src="images/1/image18.png" height=200px) | `height` caption text after  |
| `@line`  | Horizontal  | Shortcut for hr  |


### Libraries used:

+ [webslides](https://github.com/jlantunez/webslides): Custom CSS 
+ [KaTeX](https://github.com/Khan/KaTeX): JavaScript math rendering
+ [code prettify](https://github.com/google/code-prettify): Syntax highlighting 
+ [pyparsing](http://pyparsing.wikispaces.com/)
+ [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### (upcoming) features!

+ [x] Custom tags (background, background_video, line, button, figure)
+ [x] Code blocks
+ [x] Background videos examples!
+ [x] Nested divs
+ [x] List support
+ [ ] Support for command line compilation
+ [ ] Embedding tools (convert project to monolith html)
+ [ ] Global options (font?)
+ [ ] Selectively load libraries (e.g. font-awesome & KaTeX) on use
+ [ ] Slide number URL

### Presentations

First presented at [DC: Hack && Tell Round 41: Polka Sprockets](https://www.meetup.com/DC-Hack-and-Tell/events/236404104/).
