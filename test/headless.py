''' Test for using schemdraw in a script WITHOUT interactive pyplot window  '''
import schemdraw
import schemdraw.elements as elm

schemdraw.use('svg')

with schemdraw.Drawing(file='testcircuit.svg', show=False) as d:
    d.add(elm.Resistor().label('1K'))
    d.add(elm.Capacitor().down())
print(d.get_imagedata('svg'))
