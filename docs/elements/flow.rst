Flowchart Symbols
=================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import SchemDraw
    from SchemDraw import flow


SchemDraw provides basic flowcharting abilities. 
The :py:mod:`SchemDraw.flow` module contains a set of functions for defining
flowchart blocks that can be added to SchemDraw Drawings.

.. code-block:: python

    from SchemDraw import flow

Flowchart blocks:

.. jupyter-execute::
    :hide-code:
    
    d = SchemDraw.Drawing(fontsize=10, unit=.5)
    d.add(flow.start(), label='start()')
    d.add(flow.LINE)
    d.add(flow.box(), label='box()')
    d.add(flow.LINE)
    d.add(flow.sub(), label='sub()')
    d.add(flow.LINE)
    d.add(flow.data(), label='data()')
    d.add(flow.LINE)
    d.add(flow.decision(), label='decision()')
    d.add(flow.LINE)
    d.add(flow.connect(1.5), label='connect()')
    d.draw()


.. function:: SchemDraw.flow.box(w=3, h=2)
   
   Flowchart box
   
   :param w: width
   :param h: height
   :rtype: dict
   :returns: element definition dictionary

.. function:: SchemDraw.flow.sub(w=3.5, h=2, s=.3)
   
   Flowchart subprocess box (box with extra vertical lines)
   
   :param w: width
   :param h: height
   :param s: spacing of side lines
   :rtype: dict
   :returns: element definition dictionary

.. function:: SchemDraw.flow.data(w=3, h=2, s=.5)
   
   Flowchart data or I/O block (parallelogram)
   
   :param w: width
   :param h: height
   :param s: slant of parallelogram
   :rtype: dict
   :returns: element definition dictionary

.. function:: SchemDraw.flow.start(w=3, h=2)
   
   Flowchart start block (oval)
   
   :param w: width
   :param h: height
   :rtype: dict
   :returns: element definition dictionary

.. function:: SchemDraw.flow.connect(r=0.75)
   
   Flowchart connect block (circle)
   
   :param r: radius
   :rtype: dict
   :returns: element definition dictionary

.. function:: SchemDraw.flow.decision(w=4, h=2, responses=None)
   
   Flowchart decision block (diamond)
   
   :param w: width
   :param h: height
   :param responses: Dictionary of responses to label at each point of diamond. Keys are 'N', 'S', 'E', 'W'. Example: {'E': 'Yes', 'W': 'No'}
   :rtype: dict
   :returns: element definition dictionary


All flowchart symbols have four anchors named 'N', 'S', 'E', and 'W' for the
four directions. The :py:func:`SchemDraw.elements.ic` function can be used with the flowchart elements
to create blocks with multiple inputs/outputs per side if needed.

Flowchart elements do not have "leads" like electrical elements, so they 
must be connected with LINE elements. The ARROWHEAD element can be used to
show flow direction. The `w` and `h` parameters must be manually specified to size each block to fit any labels.


Decisions
---------

To label the decision branches, the :py:func:`SchemDraw.flow.decision` function takes the
`responses` parameter, a dictionary of responses for each direction. For example:


.. jupyter-execute::
    :hide-code:
    
    d = SchemDraw.Drawing(fontsize=12, unit=1)

.. jupyter-execute::

    decision = flow.decision(responses={'W': 'Yes', 'E': 'No', 'S': 'Maybe'})
    

.. jupyter-execute::
    :hide-code:
    
    dec = d.add(decision, label='decision()')
    d.add(flow.LINE, xy=dec.W, d='left')
    d.add(flow.LINE, xy=dec.E, d='right')
    d.add(flow.LINE, xy=dec.S, d='down')    
    d.draw()


See the :ref:`galleryflow` Gallery for more examples.
