Getting Started
===============

Installation
------------

SchemDraw can be installed from pip using

.. code-block:: bash

    pip install SchemDraw

or directly by downloading the source and running

.. code-block:: bash

    python setup.py install


Jupyter Notebooks
-----------------

Using a Jupyter Notebook in inline mode is recommended for the easy creation of circuit diagrams. 
If your schematics pop up in an external window, set Matplotlib to inline mode before importing SchemDraw:

.. code-block:: python

    %matplotlib inline

For best results when viewing circuits in the notebook, use a vector figure format, such as svg before importing SchemDraw:

.. code-block:: python

    %config InlineBackend.figure_format = 'svg'
    

Overview
---------

The :py:mod:`SchemDraw` module allows for drawing circuit elements.
:py:mod:`SchemDraw.elements` contains :ref:`electrical` pre-defined for
use in a drawing. A common import structure is:

.. jupyter-execute::

    import SchemDraw
    import SchemDraw.elements as elm

All schematics start by creating a `Drawing` object:

.. jupyter-execute::
    :hide-output:

    d = SchemDraw.Drawing()
    
Then, circuit elements can be added to the drawing, one at a time.
The `d` keyword specifies the drawing direction, either 'right', 'left', 'up', or 'down'.
When the next element is added, it will start at the endpoint of previous element.
If `d` is not supplied, the element will be drawn in the same direction as the previous element.

.. jupyter-execute::
    :hide-output:

    d.add(elm.RES, d='right', label='1$\Omega$')
    d.add(elm.CAP, d='down', label='10$\mu$F')
    d.add(elm.LINE, d='left')
    d.add(elm.SOURCE_SIN, d='up', label='10V')

Then display and optionally save the drawing to a file:

.. jupyter-execute::

    d.draw()
    d.save('basic_rc.svg')

When saving, the image type is determined from the extension.
Options include `svg`, `eps`, `png`, `pdf`, and `jpg`.
A vector format, such as `svg` is recommended for best results.

For full details of placing and stylizing elements, see :ref:`placement`.
