Flowcharts and Diagrams
=======================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import flow


Schemdraw provides basic symbols for flowcharting and state diagrams. 
The :py:mod:`schemdraw.flow.flow` module contains a set of functions for defining
flowchart blocks and connecting lines that can be added to schemdraw Drawings.

.. code-block:: python

    from schemdraw import flow

Flowchart blocks:

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=10, unit=.5)
    d.add(flow.Start().label('Start').drop('E'))
    d.add(flow.Arrow())
    d.add(flow.Ellipse().label('Ellipse'))
    d.add(flow.Arrow())
    d.add(flow.Box(label='Box'))
    d.add(flow.Arrow())
    d.add(flow.RoundBox(label='RoundBox').drop('S'))
    d.add(flow.Arrow().down())
    d.add(flow.Subroutine(label='Subroutine').drop('W'))
    d.add(flow.Arrow().left())
    d.add(flow.Data(label='Data'))
    d.add(flow.Arrow())
    d.add(flow.Decision(label='Decision'))
    d.add(flow.Arrow())
    d.add(flow.Connect(label='Connect'))
    d.draw()

Some elements have been defined with multiple names, which can be used depending on the context or user preference:

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=10, unit=.5)
    d.add(flow.Terminal().label('Terminal').drop('E'))
    d.add(flow.Arrow())
    d.add(flow.Process().label('Process'))
    d.add(flow.Arrow())
    d.add(flow.RoundProcess().label('RoundProcess'))
    d.add(flow.Arrow())
    d.add(flow.Circle(label='Circle'))
    d.add(flow.Arrow())
    d.add(flow.State(label='State'))
    d.add(flow.Arrow())
    d.add(flow.StateEnd(label='StateEnd'))
    d.draw()


All flowchart symbols have 16 anchor positions named for the compass directions: 'N', 'S', 'E', 'W', 'NE', 'SE, 'NNE', etc., plus a 'center' anchor.

The :py:class:`schemdraw.elements.intcircuits.Ic` element can be used with the flowchart elements to create blocks with other inputs/outputs per side if needed.

The size of each block must be specified manually using `w` and `h` or `r` parameters to size each block to fit any labels.


Connecting Lines
----------------

Typical flowcharts will use `Line` or `Arrow` elements to connect the boxes. The line and arrow elements have been included in the `flow` module for convenience. 

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d.config(fontsize=10, unit=.5)
        d += flow.Terminal().label('Start')
        d += flow.Arrow()
        d += flow.Process().label('Do something').drop('E')
        d += flow.Arrow().right()
        d += flow.Process().label('Do something\nelse')


Some flow diagrams, such as State Machine diagrams, often use curved connectors between states. Several Arc connectors are available.
Each Arc element takes an `arrow` parameter, which may be '->', '<-', or '<->', to define the end(s) on which to draw arrowheads.

Arc2
^^^^

`Arc2` draws a symmetric quadratic Bezier curve between the endpoints, with curvature controlled by parameter `k`. Endpoints of the arc should be specified using `at()` and `to()` methods.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12, unit=1)

.. jupyter-execute::

    d += (a := flow.State().label('A'))
    d += (b := flow.State(arrow='->').label('B').at((4, 0)))
    d += flow.Arc2(arrow='->').at(a.NE).to(b.NW).color('deeppink').label('Arc2')
    d += flow.Arc2(k=.2, arrow='<->').at(b.SW).to(a.SE).color('mediumblue').label('Arc2')

.. jupyter-execute::
    :hide-code:

    d.draw()


ArcZ and ArcN
^^^^^^^^^^^^^

These draw symmetric cubic Bezier curves between the endpoints. The `ArcZ` curve approaches the endpoints horizontally, and `ArcN` approaches them vertically.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12, unit=1)

.. jupyter-execute::

    d += (a := flow.State().label('A'))
    d += (b := flow.State().label('B').at((4, 4)))
    d += (c := flow.State().label('C').at((8, 0)))
    d += flow.ArcN(arrow='<->').at(a.N).to(b.S).color('deeppink').label('ArcN')
    d += flow.ArcZ(arrow='<->').at(b.E).to(c.W).color('mediumblue').label('ArcZ')

.. jupyter-execute::
    :hide-code:

    d.draw()

Arc3
^^^^

The `Arc3` curve is an arbitrary cubic Bezier curve, defined by endpoints and angle of approach to each endpoint. `ArcZ` and `ArcN` are simply `Arc3` defined with the angles as 0 and 180, or 90 and 270, respectively.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12, unit=1)

.. jupyter-execute::

    d += (a := flow.State().label('A'))
    d += (b := flow.State().label('B').at((3, 3)))
    d += flow.Arc3(th1=75, th2=-45, arrow='<->').at(a.N).to(b.SE).color('deeppink').label('Arc3')

.. jupyter-execute::
    :hide-code:

    d.draw()


ArcLoop
^^^^^^^

The `ArcLoop` curve draws a partial circle that intersects the two endpoints, with the given radius. Often used in state machine diagrams to indicate cases where the state does not change.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12, unit=1)

.. jupyter-execute::

    d += (a := flow.State().label('A'))
    d += flow.ArcLoop(arrow='<-').at(a.NW).to(a.NNE).color('mediumblue').label('ArcLoop', halign='center')

.. jupyter-execute::
    :hide-code:

    d.draw()


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


Layout and Flow
---------------

Without any directions specified, boxes flow top to bottom (see left image).
If a direction is specified (right image), the flow will continue in that direction, starting the next arrow at an appropriate anchor.
Otherwise, the `drop` method is useful for specifing where to begin the next arrow.

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d.config(fontsize=10, unit=.5)
        d += flow.Terminal().label('Start')
        d += flow.Arrow()
        d += flow.Process().label('Step 1')
        d += flow.Arrow()
        d += flow.Process().label('Step 2').drop('E')
        d += flow.Arrow().right()
        d += flow.Connect().label('Next')

        d += flow.Terminal().label('Start').at((4, 0))
        d += flow.Arrow().theta(-45)
        d += flow.Process().label('Step 1')
        d += flow.Arrow()
        d += flow.Process().label('Step 2').drop('E')
        d += flow.Arrow().right()
        d += flow.Connect().label('Next')


See the :ref:`galleryflow` Gallery for more examples.
