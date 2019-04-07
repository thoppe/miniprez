% Title: Miniprez tutorial
% Author: Travis Hoppe

!!(https://source.unsplash.com/4mta-DkJUAg class="light")

...bg-black
..aligncenter

### .text-data **miniprez** 
#### Beautiful presentations in minimalist format

..text-intro miniprez is a static, mobile-friendly version of [webslides](https://github.com/jlantunez/webslides)

-----

% Triple dots indicate a slide level class
...bg-black 

# .text-landing The problem

..text-intro
+ I want simple and beautiful presentations.
+ Presentations that compile from text to interactive webpages.
+ Presentations that seperate content from style like Markdown. 
+ Presentations that render mathematics and highlight code.

<br>
Oh, and it should work well* on mobile too.
..

<footer>
.alignright *just show me the content!
</footer>

--------
...align-right.bg-white 

..size-50.wrap

# .text-landing The solution: <br> miniprez

.line

A [python library](https://github.com/thoppe/miniprez) written using
[pyparsing](http://pyparsing.wikispaces.com/) and
[Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/).
Miniprez compiles [text](tutorial.md) into a single-page html presentation
 (like this one) with extra goodies. Emoji, font-awesome, LaTeX, and code
 highlighting are built in. Full-screen backgrounds and video can render behind
 the each screen. Slides are controlled with page-up and page-down and scrolled
easily on mobile.

--------
!!(https://source.unsplash.com/F1dSr7I4AmY class="dark")

...align-left.bg-black

# _markdown_
### Basic [Markdown](https://daringfireball.net/projects/markdown/syntax)
<br>

+ **bold** `**text**`
+ *fire* `*text*`
+ _emph_ `_text_`

-----
!!(https://source.unsplash.com/pmX9BkDDr_A class="dark")

...align-left.bg-black

# _emoji_
### standard emoji and [font-awesome](http://fontawesome.io/)
<br>

..text-intro
+ `:battery:` :battery:
+ `:heart_eyes:` :heart_eyes:
+ `::meetup::` ::meetup::
+ `::ra::` ::ra:: 

-----
!!(https://source.unsplash.com/5mZ_M06Fc9g class="dark")
...bg-apple ...align-left

# _math support_
LaTeX rendered inline with [KaTex](https://github.com/Khan/KaTeX)  

.line

### $P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$
<br>
`$P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$`

-----
!!(https://source.unsplash.com/7BiMECHFgFY)
...align-left.bg-black.fullscreen

..bg-white.wrap
# _pretty code blocks_
Syntax highlighting Google's [code prettify](https://github.com/google/code-prettify). Code blocks are context-aware.

```
sort [] = []
sort (x:xs) = sort lower ++ [x] ++ sort higher
    where
        lower = filter (< x) xs
        higher = filter (>= x) xs
```
<br>
```
// to convert prefix to postfix
main() {
  char c = getchar();
  (c == '+' || c == '-' || c == '*' || c == '/') ? main(), main() : 0;
  putchar(c);
} 
```

------
!!(https://cdn.shutterstock.com/shutterstock/videos/15778135/preview/stock-footage-office-chair-race-slow-motion-young-guys-have-fun-in-the-office-during-a-break-games-of-businessm.mp4)

..slide-top
## _looping background animations_
Embed/hotlink any video file (thanks [Shutterstock](https://www.shutterstock.com/)!)

-----

!!(https://source.unsplash.com/U5rMrSI7Pn4 class="light")

...slide-bottom.bg-black

..content-center.text-shadow
## .text-landing **A pug and an Equation**
### $$i \hbar \frac{\partial}{\partial t}\Psi(\mathbf{r},t) = \hat H \Psi(\mathbf{r},t)$$
  
this slide looks important right? It's not!

Oh look, an inline $x^2$ equation.

------

...bg-apple
..wrap

## .text-data Thanks, you!
#### Contribute at
## [https://github.com/thoppe/miniprez](https://github.com/thoppe/miniprez)

