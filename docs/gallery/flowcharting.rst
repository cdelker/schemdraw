
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
    
    d = schemdraw.Drawing()
    d += flow.Start(w=2, h=1.5).label('START')
    d += flow.Arrow().down().length(d.unit/3)
    d += (h := flow.Decision(w=5.5, h=4, S='YES')
          .label('Hey, wait,\nthis flowchart\nis a trap!'))
    d += flow.Line().down().length(d.unit/4)
    d += flow.Line().right().length(d.unit*1.1)
    d += flow.Line().up().toy(h.E)
    d += flow.Arrow().left().tox(h.E)
    d.draw()


Flowchart for flowcharts
^^^^^^^^^^^^^^^^^^^^^^^^

Recreation of `XKCD 518 <https://xkcd.com/518/>`_.

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(fontsize=11)
    d += (b := flow.Start(w=2, h=1.5).label('START'))
    d += flow.Arrow().down().length(d.unit/2)
    d += (d1 := flow.Decision(w=5, h=3.9, E='YES', S='NO')
          .label('DO YOU\nUNDERSTAND\nFLOW CHARTS?'))
    d += flow.Arrow().length(d.unit/2)
    d += (d2 := flow.Decision(w=5, h=3.9, E='YES', S='NO')
          .label('OKAY,\nYOU SEE THE\nLINE LABELED\n"YES"?'))
    d += flow.Arrow().length(d.unit/2)
    d += (d3 := flow.Decision(w=5.2, h=3.9, E='YES', S='NO')
          .label('BUT YOU\nSEE THE ONES\nLABELED "NO".'))

    d += flow.Arrow().right().at(d3.E).length(d.unit/2)
    d += flow.Box(w=2, h=1.25).anchor('W').label('WAIT,\nWHAT?')
    d += flow.Arrow().down().at(d3.S).length(d.unit/2)
    d += (listen := flow.Box(w=2, h=1).label('LISTEN.'))
    d += flow.Arrow().right().at(listen.E).length(d.unit/2)
    d += (hate := flow.Box(w=2, h=1.25).anchor('W').label('I HATE\nYOU.'))

    d += flow.Arrow().right().at(d1.E).length(d.unit*3.5)
    d += (good := flow.Box(w=2, h=1).anchor('W').label('GOOD'))
    d += flow.Arrow().right().at(d2.E).length(d.unit*1.5)
    d += (d4 := flow.Decision(w=5.3, h=4.0, E='YES', S='NO').anchor('W')
          .label('...AND YOU CAN\nSEE THE ONES\nLABELED "NO"?'))

    d += flow.Line().right().at(d4.E).tox(good.S)
    d += flow.Arrow().up().toy(good.S)
    d += flow.Arrow().down().at(d4.S).length(d.unit/2)
    d += (d5 := flow.Decision(w=5, h=3.6, E='YES', S='NO')
          .label('BUT YOU\nJUST FOLLOWED\nTHEM TWICE!'))
    d += flow.Arrow().right().at(d5.E).length(d.unit)
    d += (question := flow.Box(w=3.5, h=1.75).anchor('W')
          .label("(THAT WASN'T\nA QUESTION.)"))
    d += flow.Line().down().at(d5.S).length(d.unit/3)
    d += flow.Line().right().tox(question.S)
    d += flow.Arrow().up().toy(question.S)

    d += flow.Line().right().at(good.E).tox(question.S)
    d += flow.Arrow().down().length(d.unit)
    d += (drink := flow.Box(w=2.5, h=1.5).label("LET'S GO\nDRINK."))
    d += flow.Arrow().right().at(drink.E).label('6 DRINKS')
    d += (flow.Box(w=3.7, h=2).anchor('W')
          .label('HEY, I SHOULD\nTRY INSTALLING\nFREEBSD!'))
    d += flow.Arrow().up().at(question.N).length(d.unit*.75)
    d += (screw := flow.Box(w=2.5, h=1).anchor('S').label('SCREW IT.'))
    d += flow.Arrow().up().at(screw.N).toy(drink.S)
    d.draw()
