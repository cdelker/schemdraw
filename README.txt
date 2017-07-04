
SchemDraw is a python package for producing high-quality electrical circuit schematic diagrams. Typical usage::

        import SchemDraw as schem
        import SchemDraw.elements as e
        d = schem.Drawing()
        d.add( e.RES, label='100K$\Omega$' )
        d.add( e.CAP, d='down', botlabel='0.1$\mu$F' )
        d.draw()
        d.save( 'schematic.eps' )

Documentation is available in the docs folder or online:
http://cdelker.bitbucket.io/SchemDraw/SchemDraw.html

The most current version can be found in the source code git repository:
https://bitbucket.org/cdelker/schemdraw
