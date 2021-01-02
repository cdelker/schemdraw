''' Test for using schemdraw in a script WITHOUT interactive pyplot window  '''
import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')

d = schemdraw.Drawing()
d.add(elm.Resistor().label('1K'))
d.add(elm.Capacitor().down())
d.save('testcircuit.png')
print(d.get_imagedata('svg'))
