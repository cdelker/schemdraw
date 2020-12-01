''' Test for using schemdraw in a script with interactive pyplot window  '''
import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')

d = schemdraw.Drawing()
d.add(elm.Resistor(label='1K'))
d.add(elm.Capacitor('d'))
d.save('cap.svg')

d2 = schemdraw.Drawing()
d2.add(elm.Diode(fill=True))

d2.save('res.svg')
d2.draw()
d.draw()
