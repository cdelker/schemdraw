
.. _galleryflow:

Flowcharting
------------

.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import flow    


Flowchart elements are defined in the :py:mod:`flow` module.

.. code-block:: python

    from schemdraw import flow

It's a Trap!
^^^^^^^^^^^^

Recreation of `XKCD 1195 <https://xkcd.com/1195/>`_.

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d += flow.Start().label('START')
        d += flow.Arrow().down(d.unit/3)
        d += (h := flow.Decision(w=5.5, h=4, S='YES').label('Hey, wait,\nthis flowchart\nis a trap!'))
        d += flow.Line().down(d.unit/4)
        d += flow.Wire('c', k=3.5, arrow='->').to(h.E)


Flowchart for flowcharts
^^^^^^^^^^^^^^^^^^^^^^^^

Recreation of `XKCD 518 <https://xkcd.com/518/>`_.

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d.config(fontsize=11)
        d += (b := flow.Start().label('START'))
        d += flow.Arrow().down(d.unit/2)
        d += (d1 := flow.Decision(w=5, h=3.9, E='YES', S='NO').label('DO YOU\nUNDERSTAND\nFLOW CHARTS?'))
        d += flow.Arrow().length(d.unit/2)
        d += (d2 := flow.Decision(w=5, h=3.9, E='YES', S='NO').label('OKAY,\nYOU SEE THE\nLINE LABELED\n"YES"?'))
        d += flow.Arrow().length(d.unit/2)
        d += (d3 := flow.Decision(w=5.2, h=3.9, E='YES', S='NO').label('BUT YOU\nSEE THE ONES\nLABELED "NO".'))

        d += flow.Arrow().right(d.unit/2).at(d3.E)
        d += flow.Box(w=2, h=1.25).anchor('W').label('WAIT,\nWHAT?')
        d += flow.Arrow().down(d.unit/2).at(d3.S)
        d += (listen := flow.Box(w=2, h=1).label('LISTEN.'))
        d += flow.Arrow().right(d.unit/2).at(listen.E)
        d += (hate := flow.Box(w=2, h=1.25).anchor('W').label('I HATE\nYOU.'))

        d += flow.Arrow().right(d.unit*3.5).at(d1.E)
        d += (good := flow.Box(w=2, h=1).anchor('W').label('GOOD'))
        d += flow.Arrow().right(d.unit*1.5).at(d2.E)
        d += (d4 := flow.Decision(w=5.3, h=4.0, E='YES', S='NO').anchor('W').label('...AND YOU CAN\nSEE THE ONES\nLABELED "NO"?'))

        d += flow.Wire('-|', arrow='->').at(d4.E).to(good.S)
        d += flow.Arrow().down(d.unit/2).at(d4.S)
        d += (d5 := flow.Decision(w=5, h=3.6, E='YES', S='NO').label('BUT YOU\nJUST FOLLOWED\nTHEM TWICE!'))
        d += flow.Arrow().right().at(d5.E)
        d += (question := flow.Box(w=3.5, h=1.75).anchor('W').label("(THAT WASN'T\nA QUESTION.)"))
        d += flow.Wire('n', k=-1, arrow='->').at(d5.S).to(question.S)

        d += flow.Line().at(good.E).tox(question.S)
        d += flow.Arrow().down()
        d += (drink := flow.Box(w=2.5, h=1.5).label("LET'S GO\nDRINK."))
        d += flow.Arrow().right().at(drink.E).label('6 DRINKS')
        d += flow.Box(w=3.7, h=2).anchor('W').label('HEY, I SHOULD\nTRY INSTALLING\nFREEBSD!')
        d += flow.Arrow().up(d.unit*.75).at(question.N)
        d += (screw := flow.Box(w=2.5, h=1).anchor('S').label('SCREW IT.'))
        d += flow.Arrow().at(screw.N).toy(drink.S)


State Machine Acceptor
^^^^^^^^^^^^^^^^^^^^^^

`Source <https://en.wikipedia.org/wiki/Finite-state_machine#/media/File:DFAexample.svg>`_

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d += elm.Arrow().length(1)
        d += (s1 := flow.StateEnd().anchor('W').label('$S_1$'))
        d += elm.Arc2(arrow='<-').at(s1.NE).label('0')
        d += (s2 := flow.State().anchor('NW').label('$S_2$'))
        d += elm.Arc2(arrow='<-').at(s2.SW).to(s1.SE).label('0')
        d += elm.ArcLoop(arrow='<-').at(s2.NE).to(s2.E).label('1')
        d += elm.ArcLoop(arrow='<-').at(s1.NW).to(s1.N).label('1')


Door Controller
^^^^^^^^^^^^^^^

`Diagram Source <https://en.wikipedia.org/wiki/Finite-state_machine#/media/File:Fsm_Moore_model_door_control.svg>`_

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
        delta = 4
        d += (c4 := flow.Circle(r=1).label('4\nopening'))
        d += (c1 := flow.Circle(r=1).at((delta, delta)).label('1\nopened'))
        d += (c2 := flow.Circle(r=1).at((2*delta, 0)).label('2\nclosing'))
        d += (c3 := flow.Circle(r=1).at((delta, -delta)).label('3\nclosed'))
        d += elm.Arc2(arrow='->', k=.3).at(c4.NNE).to(c1.WSW).label('sensor\nopened')
        d += elm.Arc2(arrow='->', k=.3).at(c1.ESE).to(c2.NNW).label('close')
        d += elm.Arc2(arrow='->', k=.3).at(c2.SSW).to(c3.ENE).label('sensor\nclosed')
        d += elm.Arc2(arrow='->', k=.3).at(c3.WNW).to(c4.SSE).label('open')
        d += elm.Arc2(arrow='<-', k=.3).at(c4.ENE).to(c2.WNW).label('open')
        d += elm.Arc2(arrow='<-', k=.3).at(c2.WSW).to(c4.ESE).label('close')


Another State Machine
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as dwg:
        dwg += (a := flow.Circle().label('a').fill('lightblue'))
        dwg += (b := flow.Circle().at((4, 0)).label('b').fill('lightblue'))
        dwg += (c := flow.Circle().at((8, 0)).label('c').fill('lightblue'))
        dwg += (f := flow.Circle().at((0, -4)).label('f').fill('lightblue'))
        dwg += (e := flow.Circle().at((4, -6)).label('e').fill('lightblue'))
        dwg += (d := flow.Circle().at((8, -4)).label('d').fill('lightblue'))
        dwg += elm.ArcLoop(arrow='->').at(a.NW).to(a.NNE).label('00/0', fontsize=10)
        dwg += elm.ArcLoop(arrow='->').at(b.NNW).to(b.NE).label('01/0', fontsize=10)
        dwg += elm.ArcLoop(arrow='->').at(c.NNW).to(c.NE).label('11/0', fontsize=10)
        dwg += elm.ArcLoop(arrow='->').at(d.E).to(d.SE).label('10/0', fontsize=10)
        dwg += elm.ArcLoop(arrow='->').at(e.SSE).to(e.SW).label('11/1', fontsize=10)
        dwg += elm.ArcLoop(arrow='->').at(f.S).to(f.SW).label('01/1', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(a.ENE).to(b.WNW).label('01/0', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(b.W).to(a.E).label('00/0', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(b.ENE).to(c.WNW).label('11/0', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(c.W).to(b.E).label('01/0', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(a.ESE).to(d.NW).label('00/0', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(d.WNW).to(a.SE).label('10/0', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(f.ENE).to(e.NW).label('01/1', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(e.WNW).to(f.ESE).label('11/1', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='->').at(e.NE).to(d.WSW).label('11/1', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='->').at(d.SSW).to(e.ENE).label('10/0', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(f.NNW).to(a.SSW).label('00/0', fontsize=10)
        dwg += elm.Arc2(k=.1, arrow='<-').at(c.SSE).to(d.NNE).label('10/0', fontsize=10)


Logical Flow Diagram
^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing(unit=1) as dwg:
        dwg += (a := flow.Circle(r=.5).label('a'))
        dwg += (x := flow.Decision(w=1.5, h=1.5).label('$X$').at(a.S).anchor('N'))
        dwg += elm.RightLines(arrow='->').at(x.E).label('$\overline{X}$')
        dwg += (y1 := flow.Decision(w=1.5, h=1.5).label('$Y$'))
        dwg.move_from(y1.N, dx=-5)
        dwg += (y2 := flow.Decision(w=1.5, h=1.5).label('$Y$'))
        dwg += elm.RightLines(arrow='->').at(x.W).to(y2.N).label('$X$')
        dwg += elm.Arrow().at(y2.S).label('$Y$')
        dwg += (b := flow.Circle(r=.5).label('b'))
        dwg.move_from(b.N, dx=2)
        dwg += (c := flow.Circle(r=.5).label('c'))
        dwg += elm.RightLines(arrow='->').at(y2.E).to(c.N).label('$\overline{Y}$')
        dwg += elm.Arrow().at(y1.S).label('$Y$')
        dwg += (d := flow.Circle(r=.5).label('d'))
        dwg.move_from(d.N, dx=2)
        dwg += (e := flow.Circle(r=.5).label('e'))
        dwg += elm.RightLines(arrow='->').at(y1.E).to(e.N).label('$\overline{Y}$')