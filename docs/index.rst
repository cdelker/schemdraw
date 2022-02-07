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

    with schemdraw.Drawing() as d:
        d += elm.Resistor().right().label('1Ω')
    
creates a new schemdraw drawing with a resistor going to the right with a label of "1Ω".
The next element added to the drawing will start at the endpoint of the resistor.

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d += elm.Resistor().right().label('1Ω')
        d += elm.Capacitor().down().label('10μF')
        d += elm.Line().left()
        d += elm.SourceSin().up().label('10V')



.. toctree::
   :maxdepth: 3
   :caption: Contents:

   usage/start
   usage/index
   elements/elements
   gallery/index
   usage/customizing
   classes/index   
   changes


----------

Want to support Schemdraw development? Need more circuit examples? Pick up the Schemdraw Examples Pack on buymeacoffee.com:

.. raw:: html

    <a href="https://www.buymeacoffee.com/cdelker/e/55648" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 60px !important;width: 217px !important;" ></a>
