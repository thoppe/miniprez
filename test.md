---- .aligncenter   
@background(url="https://webslides.tv/static/images/nature.jpg")

.text-data  @h4 **miniprez**
@h4 Beautiful presentations in minimalist format <br>

@p 
 @button(href="https://github.com/thoppe/miniprez") .ghost ::github:: Project repo
 @button(href="https://twitter.com/metasemantic") .ghost ::twitter:: @metasemantic

@p .text-intro 
  miniprez turns text into mobile friendly presentations.

---- .align-left .bg-apple
.text-landing _Slide 2_
@h2 _simple markdown support_
@line
@p
  **bold** text -> `**text**` <br>
  _emph_ text -> `_text_` <br>
  `code` text -> `\`code\`` 

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
_registered_custom_tags = {
    "background" : custom_tags.background,
    "line" : custom_tags.line,
    "button" : custom_tags.button,
}
'''

and more normal things with a test triple quote ''' here

'''
secondary code block!
'''

----- .wrap

@h2 .content-left We make interfaces and content strategy.
@p .content-left We are digital people by nature. When we develop a vision, it is based on knowledge, research and experience. Those images are for demo purposes only.

This should be one line: the **final** section _section_.
