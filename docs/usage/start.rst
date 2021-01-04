Getting Started
===============

Installation
------------

schemdraw can be installed from pip using

.. code-block:: bash

    pip install schemdraw

or directly by downloading the source and running

.. code-block:: bash

    python setup.py install

Schemdraw requires Python 3.7+.
Python 3.8+ is recommended for its walrus operator (:=) that allows a
more compact notation of defining schematics.


Overview
---------

The :py:mod:`schemdraw` module allows for drawing circuit elements.
:py:mod:`schemdraw.elements` contains :ref:`electrical` pre-defined for
use in a drawing. A common import structure is:

.. jupyter-execute::

    import schemdraw
    import schemdraw.elements as elm

Schemdraw uses two main classes for creating circuit diagrams: :py:class:`schemdraw.elements.Element` and :py:class:`schemdraw.Drawing`.    
Element instances are created and added to a Drawing to make a complete schematic diagram.
All the different circuit elements subclass :py:class:`schemdraw.elements.Element` and have methods for defining the element's parameters and location within the drawing.
Individual elements can be viewed using the Jupyter representation of the element object:

.. jupyter-execute::

    elm.Resistor().label('R1')


To make a complete circuit diagram, a :py:class:`schemdraw.Drawing` is created and :py:class:`schemdraw.elements.Element` are added to it:

.. jupyter-execute::

    d = schemdraw.Drawing()
    d.add(elm.Resistor())
    d.add(elm.Capacitor())
    d.add(elm.Diode())
    d.draw()

The `+=` operator can also be used as shorthand notation to add elements to the drawing. This code is equivalent to the above:

.. code-block:: python

    d = schemdraw.Drawing()
    d += elm.Resistor()
    d += elm.Capacitor()
    d += elm.Diode()
    d.draw()

Element properties can be set using a chained method interface (new in version 0.9), for example:

.. jupyter-execute::

    d = schemdraw.Drawing()
    d += elm.Resistor().label('100KΩ')
    d += elm.Capacitor().down().label('0.1μF', loc='bottom')
    d += elm.Line().left()
    d += elm.Ground()
    d += elm.SourceV().up().label('10V')
    d.draw()

Methods `up`, `down`, `left`, `right` specify the drawing direction, and `label` adds text to the element.
If not specified, elements reuse the same direction from the previous element, and begin where
the previous element ended.

For full details of placing and stylizing elements, see :ref:`placement`.
and the :py:class:`schemdraw.elements.Element`.
In general, parameters that control **what** is drawn are passed to the element itself, and parameters that control **how** things are drawn are set using chained Element methods. For example, to make a polarized Capacitor, pass `polar=True` as an argument to `Capacitor`, but to change the Capacitor's color, use the `.color()` method: `elm.Capacitor(polar=True).color('red')`.

Calling `d.draw()` assembles the drawing. In Jupyter, this will show the schematic inline as the cell output.
If run as a script, the schematic will display in the interactive matplotlib window.
    
When saving, the image type is determined from the extension.
Options include `svg`, `eps`, `png`, `pdf`, and `jpg`.
A vector format, such as `svg` is recommended for best results.

.. code-block:: python

    d.save('basic_rc.svg')



Usage Modes
-----------

Jupyter Notebooks
*****************

Using a Jupyter Notebook in inline mode is recommended for the easy interactive creation of circuit diagrams. 
If your schematics pop up in an external window, set Matplotlib to inline mode before importing schemdraw:

.. code-block:: python

    %matplotlib inline

For best results when viewing circuits in the notebook, use a vector figure format, such as svg before importing schemdraw:

.. code-block:: python

    %config InlineBackend.figure_format = 'svg'


Python Scripts
**************

Code in a .py file can be run to generate figures, and by default, calling `d.draw()` will display a GUI window
for viewing the schematic.
Add the `show=False` option to `d.draw()` to suppress the window from appearing.

Rather than saving the schematic image to a file, the raw image data as a bytes array can be obtained
by calling `.get_imagedata()` with the desired image format.
This can be useful for integrating schemdraw into an existing GUI or web application.

.. code-block:: python

    from schemdraw import Drawing
    
    drawing = Drawing()
    ...
    image_bytes = drawing.get_imagedata('svg')


Server Side
***********

When running on a server, sometimes there is no display available. The code may attempt to open the GUI preview window and fail.
In these cases, try setting the Matplotlib backend to a non-gui option.
Before importing schemdraw, add these lines to use the Agg backend which does not have a GUI.
Then get the drawing using `d.get_imagedata()`, or `d.save()` rather than `d.draw()`.

.. code-block:: python

    import matplotlib
    matplotlib.use('Agg') # Set the backend here

Alternatively, use the SVG backend (see below).


Backends
--------

By default, all schematics are drawn on a Matplotlib axis. Starting in version 0.9, schematics can also be drawn on a new experimental
SVG image backend. Similar to Matplotlib's backend behavior, the SVG backend can be used for all drawings by calling:

.. code-block:: python

    schemdraw.use('svg')

Unlike Matplotlib, the backend can be changed at any time. Alternatively, the backend can be set at the time of drawing:

.. code-block:: 

    drawing.draw(backend='svg')
    
Reasons to choose the SVG backend include:

    - No Matplotlib or Numpy dependency required.
    - Speed. The SVG backend draws 4-10x faster than Matplotlib, depending on the circuit complexity.

Reasons to use Matplotlib backend:

    - To use complicated math formulas via Matplotlib's Mathtext. SVG backend only supports basic math symbols, superscripts, and subscripts
    - To customize the schematic after drawing it by using other Matplotlib functionality.
    - To render in other, non-SVG, image formats

