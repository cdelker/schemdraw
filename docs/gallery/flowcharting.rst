
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
        flow.Start().label('START')
        flow.Arrow().down(d.unit/3)
        h = flow.Decision(w=5.5, h=4, S='YES').label('Hey, wait,\nthis flowchart\nis a trap!')
        flow.Line().down(d.unit/4)
        flow.Wire('c', k=3.5, arrow='->').to(h.E)


Flowchart for flowcharts
^^^^^^^^^^^^^^^^^^^^^^^^

Recreation of `XKCD 518 <https://xkcd.com/518/>`_.

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d.config(fontsize=11)
        b = flow.Start().label('START')
        flow.Arrow().down(d.unit/2)
        d1 = flow.Decision(w=5, h=3.9, E='YES', S='NO').label('DO YOU\nUNDERSTAND\nFLOW CHARTS?')
        flow.Arrow().length(d.unit/2)
        d2 = flow.Decision(w=5, h=3.9, E='YES', S='NO').label('OKAY,\nYOU SEE THE\nLINE LABELED\n"YES"?')
        flow.Arrow().length(d.unit/2)
        d3 = flow.Decision(w=5.2, h=3.9, E='YES', S='NO').label('BUT YOU\nSEE THE ONES\nLABELED "NO".')

        flow.Arrow().right(d.unit/2).at(d3.E)
        flow.Box(w=2, h=1.25).anchor('W').label('WAIT,\nWHAT?')
        flow.Arrow().down(d.unit/2).at(d3.S)
        listen = flow.Box(w=2, h=1).label('LISTEN.')
        flow.Arrow().right(d.unit/2).at(listen.E)
        hate = flow.Box(w=2, h=1.25).anchor('W').label('I HATE\nYOU.')

        flow.Arrow().right(d.unit*3.5).at(d1.E)
        good = flow.Box(w=2, h=1).anchor('W').label('GOOD')
        flow.Arrow().right(d.unit*1.5).at(d2.E)
        d4 = flow.Decision(w=5.3, h=4.0, E='YES', S='NO').anchor('W').label('...AND YOU CAN\nSEE THE ONES\nLABELED "NO"?')

        flow.Wire('-|', arrow='->').at(d4.E).to(good.S)
        flow.Arrow().down(d.unit/2).at(d4.S)
        d5 = flow.Decision(w=5, h=3.6, E='YES', S='NO').label('BUT YOU\nJUST FOLLOWED\nTHEM TWICE!')
        flow.Arrow().right().at(d5.E)
        question = flow.Box(w=3.5, h=1.75).anchor('W').label("(THAT WASN'T\nA QUESTION.)")
        flow.Wire('n', k=-1, arrow='->').at(d5.S).to(question.S)

        flow.Line().at(good.E).tox(question.S)
        flow.Arrow().down()
        drink = flow.Box(w=2.5, h=1.5).label("LET'S GO\nDRINK.")
        flow.Arrow().right().at(drink.E).label('6 DRINKS')
        flow.Box(w=3.7, h=2).anchor('W').label('HEY, I SHOULD\nTRY INSTALLING\nFREEBSD!')
        flow.Arrow().up(d.unit*.75).at(question.N)
        screw = flow.Box(w=2.5, h=1).anchor('S').label('SCREW IT.')
        flow.Arrow().at(screw.N).toy(drink.S)


State Machine Acceptor
^^^^^^^^^^^^^^^^^^^^^^

`Source <https://en.wikipedia.org/wiki/Finite-state_machine#/media/File:DFAexample.svg>`_

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        elm.Arrow().length(1)
        s1 = flow.StateEnd().anchor('W').label('$S_1$')
        elm.Arc2(arrow='<-').at(s1.NE).label('0')
        s2 = flow.State().anchor('NW').label('$S_2$')
        elm.Arc2(arrow='<-').at(s2.SW).to(s1.SE).label('0')
        elm.ArcLoop(arrow='<-').at(s2.NE).to(s2.E).label('1')
        elm.ArcLoop(arrow='<-').at(s1.NW).to(s1.N).label('1')


Door Controller
^^^^^^^^^^^^^^^

`Diagram Source <https://en.wikipedia.org/wiki/Finite-state_machine#/media/File:Fsm_Moore_model_door_control.svg>`_

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
        delta = 4
        c4 = flow.Circle(r=1).label('4\nopening')
        c1 = flow.Circle(r=1).at((delta, delta)).label('1\nopened')
        c2 = flow.Circle(r=1).at((2*delta, 0)).label('2\nclosing')
        c3 = flow.Circle(r=1).at((delta, -delta)).label('3\nclosed')
        elm.Arc2(arrow='->', k=.3).at(c4.NNE).to(c1.WSW).label('sensor\nopened')
        elm.Arc2(arrow='->', k=.3).at(c1.ESE).to(c2.NNW).label('close')
        elm.Arc2(arrow='->', k=.3).at(c2.SSW).to(c3.ENE).label('sensor\nclosed')
        elm.Arc2(arrow='->', k=.3).at(c3.WNW).to(c4.SSE).label('open')
        elm.Arc2(arrow='<-', k=.3).at(c4.ENE).to(c2.WNW).label('open')
        elm.Arc2(arrow='<-', k=.3).at(c2.WSW).to(c4.ESE).label('close')


Another State Machine
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing():
        a = flow.Circle().label('a').fill('lightblue')
        b = flow.Circle().at((4, 0)).label('b').fill('lightblue')
        c = flow.Circle().at((8, 0)).label('c').fill('lightblue')
        f = flow.Circle().at((0, -4)).label('f').fill('lightblue')
        e = flow.Circle().at((4, -6)).label('e').fill('lightblue')
        d = flow.Circle().at((8, -4)).label('d').fill('lightblue')
        elm.ArcLoop(arrow='->').at(a.NW).to(a.NNE).label('00/0', fontsize=10)
        elm.ArcLoop(arrow='->').at(b.NNW).to(b.NE).label('01/0', fontsize=10)
        elm.ArcLoop(arrow='->').at(c.NNW).to(c.NE).label('11/0', fontsize=10)
        elm.ArcLoop(arrow='->').at(d.E).to(d.SE).label('10/0', fontsize=10)
        elm.ArcLoop(arrow='->').at(e.SSE).to(e.SW).label('11/1', fontsize=10)
        elm.ArcLoop(arrow='->').at(f.S).to(f.SW).label('01/1', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(a.ENE).to(b.WNW).label('01/0', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(b.W).to(a.E).label('00/0', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(b.ENE).to(c.WNW).label('11/0', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(c.W).to(b.E).label('01/0', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(a.ESE).to(d.NW).label('00/0', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(d.WNW).to(a.SE).label('10/0', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(f.ENE).to(e.NW).label('01/1', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(e.WNW).to(f.ESE).label('11/1', fontsize=10)
        elm.Arc2(k=.1, arrow='->').at(e.NE).to(d.WSW).label('11/1', fontsize=10)
        elm.Arc2(k=.1, arrow='->').at(d.SSW).to(e.ENE).label('10/0', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(f.NNW).to(a.SSW).label('00/0', fontsize=10)
        elm.Arc2(k=.1, arrow='<-').at(c.SSE).to(d.NNE).label('10/0', fontsize=10)


Logical Flow Diagram
^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing(unit=1) as dwg:
        a = flow.Circle(r=.5).label('a')
        x = flow.Decision(w=1.5, h=1.5).label('$X$').at(a.S).anchor('N')
        elm.RightLines(arrow='->').at(x.E).label(r'$\overline{X}$')
        y1 = flow.Decision(w=1.5, h=1.5).label('$Y$')
        dwg.move_from(y1.N, dx=-5)
        y2 = flow.Decision(w=1.5, h=1.5).label('$Y$')
        elm.RightLines(arrow='->').at(x.W).to(y2.N).label('$X$')
        elm.Arrow().at(y2.S).label('$Y$')
        b = flow.Circle(r=.5).label('b')
        dwg.move_from(b.N, dx=2)
        c = flow.Circle(r=.5).label('c')
        elm.RightLines(arrow='->').at(y2.E).to(c.N).label(r'$\overline{Y}$')
        elm.Arrow().at(y1.S).label('$Y$')
        d = flow.Circle(r=.5).label('d')
        dwg.move_from(d.N, dx=2)
        e = flow.Circle(r=.5).label('e')
        elm.RightLines(arrow='->').at(y1.E).to(e.N).label(r'$\overline{Y}$')


Prime Factorization
^^^^^^^^^^^^^^^^^^^

`Chart Source <https://commons.wikimedia.org/wiki/File:Factorization_flowchart.svg>`_
 

.. jupyter-execute::
    :code-below:

    # Set default flowchart box fill colors
    flow.Box.defaults['fill'] = '#eeffff'
    flow.Start.defaults['fill'] = '#ffeeee'
    flow.Decision.defaults['fill'] = '#ffffee'
    
    with schemdraw.Drawing() as d:
        d.config(unit=.75)
        flow.Start(h=1.5).label('Select\n$N>1$').drop('S')
        flow.Arrow().down()
        flow.Box().label('Let k=2\nLet $n=N$')
        flow.Arrow()
        k2 = flow.Decision(E='Yes', S='No').label('Is $k^2 < n$?').drop('E')
        flow.Arrow().length(1)
        flow.Box().label('Add final\nelement\nto dictionary').drop('S')
        flow.Arrow().down()
        flow.Start().label('Stop')
        flow.Arrow().at(k2.S)
        kn = flow.Decision(W='No', S='Yes').label('Is $k$ a\nfactor of $n$?').drop('W')
        flow.Arrow().left().length(1)
        flow.Box().label('Replace $k$\nby $k+1$').drop('N')
        flow.Arrow().toy(k2.W).dot(open=True)
        flow.Arrow().tox(k2.W)
    
        flow.Arrow().down().at(kn.S)
        flow.Box().label('Replace $n$\nby $n/k$')
        flow.Arrow()
        k3 = flow.Decision(E='No', W='Yes').label('Is $k$ in\ndictionary?').drop('E')
        
        flow.Arrow().left().at(k3.W).length(1)
        rep = flow.Box().label('Replace $v$\nby $v+1$')
        flow.Arrow()
        dot = flow.Arrow().up().toy(k2.W).dot(open=True)
        flow.Arrow().right().tox(rep.N)
    
        flow.Arrow().at(k3.E).right().length(1)
        flow.Box().label('Add $k$ to\ndictionary\nwith $v=1$').drop('S')
        flow.Arrow().down()
        flow.Arrow().left().to(rep.W, dx=-1.5)
        flow.Arrow().up().toy(k2.W)
        flow.Arrow().right().tox(dot.center)
