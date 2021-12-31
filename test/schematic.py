''' Test for using schemdraw in a script with interactive pyplot window  '''
import schemdraw
import schemdraw.elements as elm

#schemdraw.use('svg')

with schemdraw.Drawing(file='cap.svg') as d:
    d.add(elm.Resistor().label('1K'))
    d.add(elm.Capacitor().down())

with schemdraw.Drawing(file='res.svg') as d2:
    d2.add(elm.Diode().fill(True))
