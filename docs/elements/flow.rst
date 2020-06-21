Flowchart Symbols
=================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import flow


schemdraw provides basic flowcharting abilities. 
The :py:mod:`schemdraw.flow` module contains a set of functions for defining
flowchart blocks that can be added to schemdraw Drawings.

.. code-block:: python

    from schemdraw import flow

Flowchart blocks:

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=10, unit=.5)
    d.add(flow.Start(label='Start()'))
    d.add(flow.Line())
    d.add(flow.Box(label='Box()'))
    d.add(flow.Line())
    d.add(flow.Subroutine(label='Subroutine()'))
    d.add(flow.Line())
    d.add(flow.Data(label='Data()'))
    d.add(flow.Line())
    d.add(flow.Decision(label='Decision()'))
    d.add(flow.LINE)
    d.add(flow.Connect(r=1, label='Connect()'))
    d.draw()


.. class:: schemdraw.flow.Square(w=3, h=2)
   
   Flowchart square
   
   :param w: width
   :param h: height

.. class:: schemdraw.flow.Subroutine(w=3.5, h=2, s=.3)
   
   Flowchart subprocess box (box with extra vertical lines)
   
   :param w: width
   :param h: height
   :param s: spacing of side lines

.. class:: schemdraw.flow.Data(w=3, h=2, s=.5)
   
   Flowchart data or I/O block (parallelogram)
   
   :param w: width
   :param h: height
   :param s: slant of parallelogram

.. class:: schemdraw.flow.Start(w=3, h=2)
   
   Flowchart start block (oval)
   
   :param w: width
   :param h: height

.. class:: schemdraw.flow.Connect(r=0.75)
   
   Flowchart connect block (circle)
   
   :param r: radius

.. class:: schemdraw.flow.Decision(w=4, h=2, **kwargs)
   
   Flowchart decision block (diamond)
   
   :param w: width
   :param h: height
   :param N: Label for North/Top point of diamond
   :param E: Label for East/Right point of diamond
   :param S: Label for South/Bottom point of diamond
   :param W: Label for West/Left point of diamond


All flowchart symbols have four anchors named 'N', 'S', 'E', and 'W' for the
four directions. The :py:class:`schemdraw.elements.intcircuits.Ic` element can be used with the flowchart elements to create blocks with multiple inputs/outputs per side if needed.

Flowchart elements must be connected with `Line`, or `Arrow`, elements. The `w` and `h` parameters must be manually specified to size each block to fit any labels.


Decisions
---------

To label the decision branches, the :py:class:`schemdraw.flow.Eecision` element takes keyword
arguments for each cardinal direction. For example:


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12, unit=1)

.. jupyter-execute::

    decision = flow.Decision(W='Yes', E='No', S='Maybe', label='Question?')
    

.. jupyter-execute::
    :hide-code:
    
    dec = d.add(decision)
    d.add(flow.Line, xy=dec.W, d='left')
    d.add(flow.Line, xy=dec.E, d='right')
    d.add(flow.Line, xy=dec.S, d='down')
    d.draw()


See the :ref:`galleryflow` Gallery for more examples.
