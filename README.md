# schemdraw

Schemdraw is a python package for producing high-quality electrical circuit schematic diagrams. Typical usage:

```python
import schemdraw
import schemdraw.elements as elm
d = schemdraw.Drawing()
d += elm.Resistor().label('100KΩ')
d += elm.Capacitor().down().label('0.1μF', loc='bottom')
d += elm.Line().left()
d += elm.Ground()
d += elm.SourceV().up().label('10V'))
d.draw()
d.save('schematic.svg')
```

Included are symbols for basic electrical components (resistors, capacitors, diodes, transistors, etc.), opamps, logic gates, signal processing elements, and flowchart blocks.

Documentation is available at [readthedocs](https://schemdraw.readthedocs.io)

The most current version can be found in the [source code git repository](https://bitbucket.org/cdelker/schemdraw).
