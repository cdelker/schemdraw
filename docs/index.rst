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
    
creates a new schemdraw drawing. Then,

.. code-block:: python

    d.add(elm.Resistor().right().label('1Ω'))

will add a resistor, going to the right with a label of "1Ω".
The next element added to the drawing will start at the endpoint of the resistor.
Display the results using the `draw` method.

.. jupyter-execute::

    d = schemdraw.Drawing()
    d.add(elm.Resistor().right().label('1Ω'))
    d.add(elm.Capacitor().down().label('10μF'))
    d.add(elm.Line().left())
    d.add(elm.SourceSin().up().label('10V'))
    d.draw()



.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage/start
   usage/placement   
   usage/customizing   
   elements/electrical
   elements/intcircuits
   elements/connectors
   elements/compound
   elements/logic 
   elements/dsp
   elements/flow
   classes/index   
   gallery/index
   changes



