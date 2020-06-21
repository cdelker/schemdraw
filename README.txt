# SchemDraw

SchemDraw is a python package for producing high-quality electrical circuit schematic diagrams. Typical usage::

        import SchemDraw
        import SchemDraw.elements as elm
        d = SchemDraw.Drawing()
        d.add(elm.Resistor(label='100K$\Omega$'))
        d.add(elm.Capacitor(d='down', botlabel='0.1$\mu$F'))
        d.add(elm.Line(d='left'))
        d.add(elm.Ground)
        d.add(elm.SourceV(d='up', label='10V'))
        d.draw()
        d.save('schematic.svg')

Included are symbols for basic electrical components (resistors, capacitors, diodes, transistors, etc.), opamps, logic gates, signal processing elements, and flowchart blocks.

Documentation is available at [readthedocs](https://schemdraw.readthedocs.io)

The most current version can be found in the [source code git repository](https://bitbucket.org/cdelker/schemdraw).
