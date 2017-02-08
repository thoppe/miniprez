# miniprez

Dead simple markup to web-friendly presentations that look great on mobile and on the big screen. Adapted from [webslides](https://github.com/jlantunez/webslides) by jlantunez.

Note: This is a live work-in-progress!

For a tutorial see the [input](https://raw.githubusercontent.com/thoppe/miniprez/gh-pages/tutorial.md) and the [slides](https://thoppe.github.io/miniprez/tutorial.html).

### (upcoming) features!

+ [x] Basic inline markdown support (*, _, **, backticks)
+ [x] Basic emoji markdown usage (:smile:)
+ [x] Direct SVG Font awesome usage through emoji syntax
+ [x] Buttons
+ [x] More advanced markdown support (links, images)
+ [x] [KaTeX](https://github.com/Khan/KaTeX) equations!
+ [x] Code blocks
+ [ ] support for command line compilation
+ [ ] Embedding tools (convert project to monolith html)
+ [ ] Global options (font?)
+ [~] Fix meta info to this project
+ [ ] Selectively load libraries (eg. font-awesome & katex) on use
+ [ ] Slide number url

### known bugs and problems
+ [ ] Extra space after markdown, ex. `*BOLD*!` becomes `BOLD !`
+ [x] remove webkit animations from webslides
+ [x] animation bug on mobile
+ [x] support for page down and up
+ [x] `<hr>` on `.bgapple` is the wrong color
+ [x] Using inline markdown on first slide
+ [x] `home` and `end` work properly