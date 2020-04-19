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


.. function:: schemdraw.flow.box(w=3, h=2)
   
   Flowchart box
   
   :param w: width
   :param h: height
   :rtype: dict
   :returns: element definition dictionary

.. function:: schemdraw.flow.sub(w=3.5, h=2, s=.3)
   
   Flowchart subprocess box (box with extra vertical lines)
   
   :param w: width
   :param h: height
   :param s: spacing of side lines
   :rtype: dict
   :returns: element definition dictionary

.. function:: schemdraw.flow.data(w=3, h=2, s=.5)
   
   Flowchart data or I/O block (parallelogram)
   
   :param w: width
   :param h: height
   :param s: slant of parallelogram
   :rtype: dict
   :returns: element definition dictionary

.. function:: schemdraw.flow.start(w=3, h=2)
   
   Flowchart start block (oval)
   
   :param w: width
   :param h: height
   :rtype: dict
   :returns: element definition dictionary

.. function:: schemdraw.flow.connect(r=0.75)
   
   Flowchart connect block (circle)
   
   :param r: radius
   :rtype: dict
   :returns: element definition dictionary

.. function:: schemdraw.flow.decision(w=4, h=2, **kwargs)
   
   Flowchart decision block (diamond)
   
   :param w: width
   :param h: height
   
   :Keyword Arguments:
        * **N, S, E, W**: (string) Label for each point of diamond. Example: E='Yes', S='No'
   :rtype: dict
   :returns: element definition dictionary


All flowchart symbols have four anchors named 'N', 'S', 'E', and 'W' for the
four directions. The :py:func:`schemdraw.elements.ic` function can be used with the flowchart elements
to create blocks with multiple inputs/outputs per side if needed.

Flowchart elements do not have "leads" like electrical elements, so they 
must be connected with LINE, ARROW, or ARROW_DOUBLE elements. The `w` and `h` parameters must be manually specified to size each block to fit any labels.


Decisions
---------

To label the decision branches, the :py:func:`schemdraw.flow.decision` function takes keyword
arguments for each cardinal direction. For example:


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12, unit=1)

.. jupyter-execute::

    decision = flow.decision(W='Yes', E='No', S='Maybe')
    

.. jupyter-execute::
    :hide-code:
    
    dec = d.add(decision, label='decision()')
    d.add(flow.LINE, xy=dec.W, d='left')
    d.add(flow.LINE, xy=dec.E, d='right')
    d.add(flow.LINE, xy=dec.S, d='down')    
    d.draw()


See the :ref:`galleryflow` Gallery for more examples.
