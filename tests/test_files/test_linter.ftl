-button-term = Test
button-test = Test
button-test-ref1 = Test { -button-term }
button-test-ref2 = Test { button-test }

short = Too short
wrong_character = Too short
# Wrong 'quotes' in comment
button-quote = Wrong ' quote
button-quote0 = Wrong quote's quote
button-quote1 = Wrong " quote
button-quote2 = Wrong 'quotes'
# Wrong "quotes" in comment
button-quote3 = Wrong "quotes"
button-quote4 = Wrong ' quote

html-link = Test with <a href="http">link</a>
html-link1 = Test with <a href="{ $link }">link</a>
html-link2 = Test with <a href="{ $link }" rel="test">link</a>
html-link3 = Test with <a id="123" href="{ $link }" rel="test">link</a>

button-with-var = This is a { $var }

button-test2 = {
    $var ->
        [t] Foo
       *[s] Bar
}

button-test2 =
    .tooltip = Test
