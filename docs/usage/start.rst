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

Starting with version 0.7, schemdraw requires Python 3.7+.
    

Overview
---------

The :py:mod:`schemdraw` module allows for drawing circuit elements.
:py:mod:`schemdraw.elements` contains :ref:`electrical` pre-defined for
use in a drawing. A common import structure is:

.. jupyter-execute::

    import schemdraw
    import schemdraw.elements as elm

Schemdraw uses two main classes for creating circuit diagrams: :py:class:`schemdraw.Element` and :py:class:`schemdraw.Drawing`.    
Element instances are created and added to a Drawing to make a complete schematic diagram.
All the different circuit elements subclass :py:class:`schemdraw.Element` and are instantiated with keyword arguments defining the element's parameters and location within the drawing.
Individual elements can be viewed using the Jupyter representation of the element object:

.. jupyter-execute::

    elm.Resistor(label='R1')


To make a complete circuit diagram, a :py:class:`schemdraw.Drawing` is created and :py:class:`schemdraw.Element` are added to it:

.. jupyter-execute::
    :hide-output:

    d = schemdraw.Drawing()
    d.add(elm.Resistor(d='right', label='1$\Omega$'))
    d.add(elm.Capacitor(d='down', label='10$\mu$F'))
    d.add(elm.Line(d='left'))
    d.add(elm.SourceSin(d='up', label='10V'))

The element classes take a number of keyword arguments that define their position, direction, color, and other parameters.
If any required argument is not provided, its value will be inherited from the :py:class:`schemdraw.Drawing` the element belongs to.

The `d` keyword specifies the drawing direction, either 'right', 'left', 'up', or 'down', or with their abbreviations 'r', 'l', 'u', and 'd'.
The `at` keyword specifies the exact coordinates for the starting point of the element.
If `d` is not supplied, the element will be drawn in the same direction as the previous element, and if `at` is not supplied, the element will start at the endpoint of the previously added element.

To display the schematic, call `d.draw()`. In Jupyter, this will show the schematic inline as the cell output.
If run as a script, the schematic will display in the interactive matplotlib window.

.. jupyter-execute::

    d.draw()
    
When saving, the image type is determined from the extension.
Options include `svg`, `eps`, `png`, `pdf`, and `jpg`.
A vector format, such as `svg` is recommended for best results.

.. code-block:: python

    d.save('basic_rc.svg')


For full details of placing and stylizing elements, see :ref:`placement`.


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
by calling `d.get_imagedata()` using the desired `ImageFormat`.
This can be useful for integrating schemdraw into an existing GUI or web application.

.. code-block:: python

    from schemdraw import Drawing, ImageFormat
    
    drawing = Drawing()
    ...
    image_bytes = drawing.get_imagedata(ImageFormat.SVG)

Server Side
***********

When running on a server, sometimes there is no display available. The code may attempt to open the GUI preview window and fail.
In these cases, try setting the Matplotlib backend to a non-gui option.
Before importing schemdraw, add these lines to use the Agg backend which does not have a GUI.
Then get the drawing using `d.get_imagedata()`, or `d.save()` rather than `d.draw()`.

.. code-block:: python

    import matplotlib
    matplotlib.use('Agg') # Set the backend here


Backends
--------

By default, all schematics are drawn on a Matplotlib axis. Starting in 0.9, schematics can also be drawn on a new experimental
SVG image backend. Similar to Matplotlib's backend behavior, the SVG backend can be used for all drawings:

.. code-block:: python

    schemdraw.use('svg')

Unlike Matplotlib, the backend can be changed at any time. Alternatively, the backend can be set at the time of drawing:

.. code-block:: 

    drawing.draw(backend='svg')
    
Reasons to choose the SVG backend include:

    - No Matplotlib dependency required.
    - Speed. The SVG backend draws 4-10x faster than Matplotlib, depending on the circuit complexity.

Reasons to use Matplotlib backend:

    - To use complicated math formulas via Matplotlib's Mathtext. SVG backend only supports basic math symbols, superscripts, and subscripts
    - To customize the schematic after drawing it by using other Matplotlib functionality.
    - To render in other, non-SVG, image formats

