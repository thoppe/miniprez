# miniprez

Dead simple markup to web-friendly presentations that look great on mobile and on the big screen. Adapted from [webslides](https://github.com/jlantunez/webslides) by jlantunez.

Note: This is a live work-in-progress!

For a tutorial see the [input](https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md) and the [slides](https://thoppe.github.io/miniprez/tutorial.html).

### Usage

Write the docs here.

Miniprez is a command-line tool that turns special markup into slides. All slides are separated by `----`. Hello world in miniprez looks like:

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
       

### (upcoming) features!

+ [x] Basic inline markdown support (*, _, **, backticks, links)
+ [x] Emojis and font awesome  (:smile:)
+ [x] Custom tags (background, background_video, line, button, figure)
+ [x] [KaTeX](https://github.com/Khan/KaTeX) equations!
+ [x] Code blocks
+ [x] BG videos examples!
+ [x] Nested divs
+ [x] List support
+ [ ] Support for command line compilation
+ [ ] Embedding tools (convert project to monolith html)
+ [ ] Global options (font?)
+ [ ] Selectively load libraries (eg. font-awesome & katex) on use
+ [ ] Slide number url