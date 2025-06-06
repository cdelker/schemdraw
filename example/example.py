import schemdraw
import schemdraw.elements as elm
schemdraw.use('svg')
schemdraw.svgconfig.text = 'text'
schemdraw.svgconfig.svg2 = False

with schemdraw.Drawing(file="example.svg"):
    elm.Resistor().label(r'$CLICk-ME$', href="#jump", color="blue")
    elm.Resistor().down().label(r'$RESET$', decoration="overline")

