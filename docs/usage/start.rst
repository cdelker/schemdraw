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

    pip install ./

Schemdraw requires Python 3.8 or higher.


Overview
---------

The :py:mod:`schemdraw` module allows for drawing circuit elements.
:py:mod:`schemdraw.elements` contains :ref:`electrical` pre-defined for
use in a drawing. A common import structure is:

.. jupyter-execute::

    import schemdraw
    import schemdraw.elements as elm


To make a circuit diagram, use a context manager (`with` statement) on a :py:class:`schemdraw.Drawing`. Then any :py:class:`schemdraw.elements.Element` instances created within the `with` block added to the drawing:

.. jupyter-execute::

    with schemdraw.Drawing():
        elm.Resistor()
        elm.Capacitor()
        elm.Diode()

**New in version 0.18**: The context manager keeps track of the active drawing, so that using `drawing.add(element)` or `drawing += element` is no longer necessary.
These operators are still functional and are needed if drawing outside a `with` context manager:

.. code-block:: python

    with schemdraw.Drawing() as drawing:
        drawing += elm.Resistor()
        drawing += elm.Capacitor()
        drawing.add(elm.Diode())   # Same as `drawing +=`

Element placement and other properties are set using a chained method interface, for example:

.. jupyter-execute::

    with schemdraw.Drawing():
        elm.Resistor().label('100KΩ')
        elm.Capacitor().down().label('0.1μF', loc='bottom')
        elm.Line().left()
        elm.Ground()
        elm.SourceV().up().label('10V')

Methods `up`, `down`, `left`, `right` specify the drawing direction, and `label` adds text to the element.
If not specified, elements reuse the same direction from the previous element, and begin where
the previous element ended.

Using the `with` context manager is a convenience, letting the drawing be displayed and saved upon exiting the `with` block. Schematics may also be created simply by assinging a new Drawing instance, but this requires explicitly adding elements to the drawing with `d.add` or d +=`, and calling `draw()` and/or `save()` to show the drawing:

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

