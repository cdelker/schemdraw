Flowchart Symbols
=================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import flow


schemdraw provides basic flowcharting abilities. 
The :py:mod:`schemdraw.flow.flow` module contains a set of functions for defining
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


All flowchart symbols have four anchors named 'N', 'S', 'E', and 'W' for the
four directions. The :py:class:`schemdraw.elements.intcircuits.Ic` element can be used with the flowchart elements to create blocks with multiple inputs/outputs per side if needed.

Flowchart elements must be connected with `Line`, or `Arrow`, elements. The `w` and `h` parameters must be manually specified to size each block to fit any labels.


Decisions
---------

To label the decision branches, the :py:class:`schemdraw.flow.flow.Decision` element takes keyword
arguments for each cardinal direction. For example:


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12, unit=1)

.. jupyter-execute::

    decision = flow.Decision(W='Yes', E='No', S='Maybe').label('Question?')
    

.. jupyter-execute::
    :hide-code:
    
    dec = d.add(decision)
    d.add(flow.Line().at(dec.W).left())
    d.add(flow.Line().at(dec.E).right())
    d.add(flow.Line().at(dec.S).down())
    d.draw()


See the :ref:`galleryflow` Gallery for more examples.
