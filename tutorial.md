---- .aligncenter
@background(url="https://webslides.tv/static/images/nature.jpg")
  
.text-data  @h4 **miniprez**
@h4 Beautiful presentations in minimalist format <br>

@p 
 @button(href="https://github.com/thoppe/miniprez") .ghost ::github:: Project repo
 @button(href="https://twitter.com/metasemantic") .ghost ::twitter:: @metasemantic

@p .text-intro 
  miniprez is a static mobile friendly version of [webslides](https://github.com/jlantunez/webslides)

---- .align-left .bg-white
@background(url="https://source.unsplash.com/aJTiW00qqtI/") .dark

.text-landing _Slide 2_
@h2 _simple markdown support_
@line
.wrap .bg-trans-dark
 .grid .wrap
  .column
    @h2 :fire: **bold**
    @p `**text**`
  .column
    @h2 :cloud: _emph_
    @p `_text_`
  .column
    @h2 :computer: `code`
    @p `&&&`code&&&`` 

---- .align-left
.text-landing Slide 3
@h2 _emoji_
Standard emoji and [font-awesome](http://fontawesome.io/)  
@line

.wrap .bg-trans-dark
 .grid .wrap
  .column `:battery:`
    @h1 :battery:
  .column `:heart_eyes:`
    @h1 :heart_eyes:
  .column `::plug::`
    @h1 ::plug:: 
  .column `::meetup::`
    @h1 ::meetup::
  .column `::ra::`
    @h1 ::ra:: 

---- .bg-apple .align-left
.text-landing Slide 4
@h2 _math support_
LaTeX rendered inline with [KaTex](https://github.com/Khan/KaTeX)  
@line
@h3
  $$P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$$
<br>
`$$P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$$`

---- .align-left 
.text-landing Slide 5
@h2 _pretty code blocks_
Syntax highlighting Google's [code prettify](https://github.com/google/code-prettify)  
@line
'''
sort [] = []
sort (x:xs) = sort lower ++ [x] ++ sort higher
    where
        lower = filter (< x) xs
        higher = filter (>= x) xs
'''
Code blocks are context-aware
'''
// to convert prefix to postfix
main() {
  char c = getchar();
  (c == '+' || c == '-' || c == '*' || c == '/') ? main(), main() : 0;
  putchar(c);
} 
'''

----- 

.card-50 .bg-white
  @figure(src="https://source.unsplash.com/BoBmrZ8epMA/800x600")
  
  .flex-content
    @h2 Side content!
    @p We live in a society exquisitely dependent on science and technology, in which hardly anyone knows anything about science and technology.

----- .bg-apple

@h1 FIN.