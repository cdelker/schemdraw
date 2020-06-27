''' Test for using schemdraw in a script with interactive pyplot window  '''
import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()
d.add(elm.Resistor(label='1K'))
d.add(elm.Capacitor('d'))

d2 = schemdraw.Drawing()
d2.add(elm.Diode(fill=True))

d2.draw()
d.draw()

