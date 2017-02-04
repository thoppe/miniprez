---- .align-center .wrap  
@background(url="https://webslides.tv/static/images/nature.jpg")

.text-data  @h4 **miniprez**
@h4 Beautiful presentations in minimalist format <br>

@p 
 @button(href="https://github.com/thoppe/miniprez") .ghost ::github:: Project repo
 @button(href="https://twitter.com/metasemantic") .ghost ::twitter:: @metasemantic

@p .text-intro 
  miniprez is a static mobile friendly version of [webslides](https://github.com/jlantunez/webslides)

---- .align-left .bg-apple
.text-landing _Slide 2_
@h2 _simple markdown support_
@line
.wrap
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
@line
@h3
  Font-awesome  `::plug::` -> ::plug:: <br>
  Emoji  `:battery:` -> :battery:

---- .bg-apple .align-left
.text-landing Slide 4
@h2 _math support_
@line
@h3
  $$P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$$
<br>
`$$P(x)=\frac{1}{\sigma\sqrt{2\pi}}e^{-\frac{(x-\mu)^2}{2\sigma ^2}}$$`

---- .align-left 
.text-landing Slide 5
@h2 _pretty code blocks_
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
    @p Travis is the most popular travel app in the world. It collects reviews from travellers about hotels, restaurants and attractions. We partnered with various divisions to create a campaign for Travis Pro.

----- .bg-apple

@h1 FIN.