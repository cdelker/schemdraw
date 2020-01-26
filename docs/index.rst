SchemDraw documentation
=======================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import SchemDraw
    from SchemDraw import elements as e
    d = SchemDraw.Drawing()

SchemDraw is a Python package for producing high-quality electrical circuit schematic diagrams.
Circuit elements are added, one at a time, similar to how you might draw them by hand, using Python methods.

For example,

.. code-block:: python

    d.add(e.RES, d='right', label='1$\Omega$')

Will add a resistor, to Drawing `d`, going to the right with a label of "1Ω".
The next element added to the drawing will start at the endpoint of the resistor.
Display the results using the `draw` method.

.. jupyter-execute::

    d.add(e.RES, d='right', label='1$\Omega$')
    d.add(e.CAP, d='down', label='10$\mu$F')
    d.add(e.LINE, d='left')
    d.add(e.SOURCE_SIN, d='up', label='10V')
    d.draw()
    

.. TODO: add a changes page




.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage/start
   usage/placement
   usage/customizing
   elements/electrical
   elements/logic
   elements/dsp
   elements/flow
   gallery/gallery
