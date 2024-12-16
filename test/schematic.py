''' Test for using schemdraw in a script with interactive pyplot window  '''
import schemdraw
import schemdraw.elements as elm

import matplotlib.pyplot as plt

with schemdraw.Drawing(file='cap.svg') as d:
    d.add(elm.Resistor().label('1K'))
    d.add(elm.Capacitor().down())

with schemdraw.Drawing(file='res.svg', transparent=True) as d2:
    d2.add(elm.Diode().fill(True))

fig, ax = plt.subplots()
ax.plot([0, 1, 2, 3], [1, 2, 1, 0], marker='o', ls='')
with schemdraw.Drawing(canvas=ax) as d3:
    d3 += elm.Resistor().label('1M')
plt.show()
