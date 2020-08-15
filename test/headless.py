''' Test for using schemdraw in a script WITHOUT interactive pyplot window  '''
import schemdraw
import schemdraw.elements as elm

d = schemdraw.Drawing()
d.add(elm.Resistor(label='1K'))
d.add(elm.Capacitor('d'))
d.save('testcircuit.png')
print(d.get_imagedata('svg'))
