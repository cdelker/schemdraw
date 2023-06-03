.. _backends:

Backends
--------

The backend is the "canvas" on which a schematic is drawn. Schemdraw supports two backends: Matplotlib, and SVG.


Matplotlib Backend
******************

By default, all schematics are drawn on a Matplotlib axis.
A new Matplotlib Figure and Axis will be created, with no frame or borders.
A schematic may be added to an existing Axis by using the :py:meth:`schemdraw.Drawing.draw` method and setting
the `canvas` parameter to an existing Axis instance.

The Matplotlib backend renders text labels as primative lines and arcs rather than text elements by default.
This has the downside that SVG editors, such as Inkscape, cannot perform textual searches on the SVGs.
The upside is that there is no dependence on installed fonts on the hosts that open the SVGs.

To configure Matplotlib to render labels as SVG text elements:

.. code-block:: python

    import matplotlib
    matplotlib.rcParams['svg.fonttype'] = 'none'


SVG Backend
***********

Schematics can also be drawn on directly to an SVG image backend.
The SVG backend can be enabled for all drawings by calling:

.. code-block:: python

    schemdraw.use('svg')

The backend can be changed at any time. Alternatively, the backend can be set individually on each Drawing using the `canvas` parameter:

.. code-block:: 

    with schemdraw.Drawing(canvas='svg') as d:
        ...

Use additional Python libraries, such as `pycairo <https://cairosvg.org/>`_, to convert the SVG output into other image formats.

Math Text
^^^^^^^^^

The SVG backend has basic math text support, including greek symbols, subscripts, and superscripts.
However, if `ziamath <https://ziamath.readthedocs.io>`_ and `latex2mathml <https://pypi.org/project/latex2mathml/>`_ packages are installed, they will be used for full Latex math support.

The SVG backend can produce searchable-text SVGs by setting:

.. code-block:: python

    schemdraw.svgconfig.text = 'text'

However, text mode does not support full Latex compatibility.
To switch back to rendering text as SVG paths:

.. code-block:: python

    schemdraw.svgconfig.text = 'path'

Some SVG renderers are not fully compatible with SVG2.0. For better compatibility with SVG1.x, use

.. code-block:: python

    schemdraw.svgconfig.svg2 = False

The decimal precision of SVG elements can be set using

.. code-block:: python

    schemdraw.svgconfig.precision = 2



Backend Comparison
******************

Reasons to choose the SVG backend include:

    - No Matplotlib/Numpy dependency required (huge file size savings if bundling an executable).
    - Speed. The SVG backend draws 4-10x faster than Matplotlib, depending on the circuit complexity.

Reasons to use Matplotlib backend:

    - To customize the schematic after drawing it by using other Matplotlib functionality.
    - To render directly in other, non-SVG, image formats, with no additional code.
