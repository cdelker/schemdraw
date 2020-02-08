# SchemDraw

SchemDraw is a python package for producing high-quality electrical circuit schematic diagrams. Typical usage::

        import SchemDraw
        import SchemDraw.elements as e
        d = SchemDraw.Drawing()
        d.add(e.RES, label='100K$\Omega$')
        d.add(e.CAP, d='down', botlabel='0.1$\mu$F')
        d.add(e.LINE, d='left')
        d.add(e.GND)
        d.add(e.SOURCE_V, d='up', label='10V')
        d.draw()
        d.save('schematic.svg')

Included are symbols for basic electrical components (resistors, capacitors, diodes, transistors, etc.), opamps, logic gates, signal processing elements, and flowchart blocks.

Documentation is available in the docs folder or [online](http://cdelker.bitbucket.io/SchemDraw/).

The most current version can be found in the [source code git repository](https://bitbucket.org/cdelker/schemdraw).
