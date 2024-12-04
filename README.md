# schemdraw

Schemdraw is a python package for producing high-quality electrical circuit schematic diagrams. Typical usage:

```python
import schemdraw
import schemdraw.elements as elm
with schemdraw.Drawing(file='schematic.svg') as d:
    elm.Resistor().label('100KΩ')
    elm.Capacitor().down().label('0.1μF', loc='bottom')
    elm.Line().left()
    elm.Ground()
    elm.SourceV().up().label('10V')
```

Included are symbols for basic electrical components (resistors, capacitors, diodes, transistors, etc.), opamps and signal processing elements. Additionally, Schemdraw can produce digital timing diagrams, state machine diagrams, and flowcharts.

Documentation is available at [readthedocs](https://schemdraw.readthedocs.io)

The most current version can be found in the [source code git repository](https://github.com/cdelker/schemdraw).
