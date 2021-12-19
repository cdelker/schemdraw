Schemdraw documentation
=======================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm

Schemdraw is a Python package for producing high-quality electrical circuit schematic diagrams.
Circuit elements are added, one at a time, similar to how you might draw them by hand, using Python methods.

For example,

.. code-block:: python

    d = schemdraw.Drawing()
    
creates a new schemdraw drawing. Then using `+=` or the `d.add` method,

.. code-block:: python

    d += elm.Resistor().right().label('1Ω')

will add a resistor, going to the right with a label of "1Ω".
The next element added to the drawing will start at the endpoint of the resistor.
Display the results using the `draw` method.

.. jupyter-execute::

    d = schemdraw.Drawing()
    d += elm.Resistor().right().label('1Ω')
    d += elm.Capacitor().down().label('10μF')
    d += elm.Line().left()
    d += elm.SourceSin().up().label('10V')
    d.draw()



.. toctree::
   :maxdepth: 3
   :caption: Contents:

   usage/start
   usage/placement   
   elements/elements
   gallery/index
   usage/customizing
   classes/index   
   changes



