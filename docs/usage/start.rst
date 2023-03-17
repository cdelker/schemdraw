Getting Started
===============

Installation
------------

schemdraw can be installed from pip using

.. code-block:: bash

    pip install schemdraw

or to include optional ``matplotlib`` backend dependencies:

.. code-block:: bash

    pip install schemdraw[matplotlib]

To allow the SVG drawing :ref:`backends` to render math expressions,
install the optional `ziamath <https://ziamath.readthedocs.io>`_ dependency with:

.. code-block:: bash

    pip install schemdraw[svgmath]


Alternatively, schemdraw can be installed directly by downloading the source and running

.. code-block:: bash

    python setup.py install

Schemdraw requires Python 3.7 or higher. Note that many of the examples and test notebooks still require 3.8+ to run due to their use of the walrus operator. The optional svgmath dependencies also require 3.8+.


Overview
---------

The :py:mod:`schemdraw` module allows for drawing circuit elements.
:py:mod:`schemdraw.elements` contains :ref:`electrical` pre-defined for
use in a drawing. A common import structure is:

.. jupyter-execute::

    import schemdraw
    import schemdraw.elements as elm

To make a circuit diagram, a :py:class:`schemdraw.Drawing` is created and :py:class:`schemdraw.elements.Element` instances are added to it:

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d.add(elm.Resistor())
        d.add(elm.Capacitor())
        d.add(elm.Diode())

The `+=` operator may be used as shorthand notation to add elements to the drawing.
This code is equivalent to the above:

.. code-block:: python

    with schemdraw.Drawing() as d:
        d += elm.Resistor()
        d += elm.Capacitor()
        d += elm.Diode()

Element placement and other properties and are set using a chained method interface, for example:

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d += elm.Resistor().label('100KΩ')
        d += elm.Capacitor().down().label('0.1μF', loc='bottom')
        d += elm.Line().left()
        d += elm.Ground()
        d += elm.SourceV().up().label('10V')

Methods `up`, `down`, `left`, `right` specify the drawing direction, and `label` adds text to the element.
If not specified, elements reuse the same direction from the previous element, and begin where
the previous element ended.

Using the `with` context manager is a convenience, letting the drawing be displayed and saved upon exiting the `with` block. Schematics may also be created simply by assinging a new Drawing instance, but this requires calling `draw()` and/or `save()` explicitly:

.. code-block:: python

    d = schemdraw.Drawing()
    d += elm.Resistor()
    ...
    d.draw()
    d.save('my_circuit.svg')


For full details of placing and stylizing elements, see :ref:`placement`.
and :py:class:`schemdraw.elements.Element`.

In general, parameters that control **what** is drawn are passed to the element itself, and parameters that control **how** things are drawn are set using chained Element methods. For example, to make a polarized Capacitor, pass `polar=True` as an argument to `Capacitor`, but to change the Capacitor's color, use the `.color()` method: `elm.Capacitor(polar=True).color('red')`.


Viewing the Drawing
-------------------

Jupyter
*******

When run in a Jupyter notebook, the schematic will be drawn to the cell output after the `with` block is exited.
If your schematics pop up in an external window, and you are using the Matplotlib backend, set Matplotlib to inline mode before importing schemdraw:

.. code-block:: python

    %matplotlib inline

For best results when viewing circuits in the notebook, use a vector figure format, such as svg before importing schemdraw:

.. code-block:: python

    %config InlineBackend.figure_format = 'svg'


Python Scripts and GUI/Web apps
*******************************

If run as a Python script, the schematic will be opened in a pop-up window after the `with` block exits.
Add the `show=False` option when creating the Drawing to suppress the window from appearing.

.. code-block:: python

    with schemdraw.Drawing(show=False) as d:
        ...

The raw image data as a bytes array can be obtained by calling `.get_imagedata()` with the after the `with` block exits.
This can be useful for integrating schemdraw into an existing GUI or web application.

.. code-block:: python

    with schemdraw.Drawing() as drawing:
        ...
    image_bytes = drawing.get_imagedata('svg')


Headless Servers
****************

When running on a server, sometimes there is no display available.
The code may attempt to open the GUI preview window and fail.
In these cases, try setting the Matplotlib backend to a non-GUI option.
Before importing schemdraw, add these lines to use the Agg backend which does not have a GUI.
Then get the drawing using `d.get_imagedata()`, or `d.save()` to get the image.

.. code-block:: python

    import matplotlib
    matplotlib.use('Agg') # Set Matplotlib's backend here

Alternatively, use Schemdraw's SVG backend (see :ref:`backends`).


Saving Drawings
---------------

To save the schematic to a file, add the `file` parameter when setting up the Drawing.
The image type is determined from the file extension.
Options include `svg`, `eps`, `png`, `pdf`, and `jpg` when using the Matplotlib backend, and `svg` when using the SVG backend.
A vector format such as `svg` is recommended for best image quality.

.. code-block:: python

    with schemdraw.Drawing(file='my_circuit.svg') as d:
        ...

The Drawing may also be saved using with the :py:meth:`schemdraw.Drawing.save` method.

