
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
    d.add(flow.Start(w=2, h=1.5, label='START'))
    d.add(flow.Arrow('down', l=d.unit/3))
    h = d.add(flow.Decision(w=5.5, h=4, S='YES', label='Hey, wait,\nthis flowchart\nis a trap!'))
    d.add(flow.Line('down', l=d.unit/4))
    d.add(flow.Line('right', l=d.unit*1.1))
    d.add(flow.Line('up', toy=h.E))
    d.add(flow.Arrow('left', tox=h.E))
    d.draw()

Flowchart for flowcharts
^^^^^^^^^^^^^^^^^^^^^^^^

Recreation of `XKCD 518 <https://xkcd.com/518/>`_.

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(fontsize=11)
    b = d.add(flow.Start(w=2, h=1.5, label='START'))
    d.add(flow.Arrow('down', l=d.unit/2))
    d1 = d.add(flow.Decision(w=5, h=3.9, E='YES', S='NO', label='DO YOU\nUNDERSTAND\nFLOW CHARTS?'))
    d.add(flow.Arrow(l=d.unit/2))
    d2 = d.add(flow.Decision(w=5, h=3.9, E='YES', S='NO', label='OKAY,\nYOU SEE THE\nLINE LABELED\n"YES"?'))
    d.add(flow.Arrow(l=d.unit/2))
    d3 = d.add(flow.Decision(w=5.2, h=3.9, E='YES', S='NO', label='BUT YOU\nSEE THE ONES\nLABELED "NO".'))

    d.add(flow.Arrow('right', xy=d3.E, l=d.unit/2))
    d.add(flow.Box(w=2, h=1.25, label='WAIT,\nWHAT?', anchor='W'))
    d.add(flow.Arrow('down', xy=d3.S, l=d.unit/2))
    listen = d.add(flow.Box(w=2, h=1, label='LISTEN.'))
    d.add(flow.Arrow('right', xy=listen.E, l=d.unit/2))
    hate = d.add(flow.Box(w=2, h=1.25, label='I HATE\nYOU.', anchor='W'))

    d.add(flow.Arrow('right', xy=d1.E, l=d.unit*3.5))
    good = d.add(flow.Box(w=2, h=1, label='GOOD', anchor='W'))
    d.add(flow.Arrow('right', xy=d2.E, l=d.unit*1.5))
    d4 = d.add(flow.Decision(w=5.3, h=4.0, E='YES', S='NO', label='...AND YOU CAN\nSEE THE ONES\nLABELED "NO"?', anchor='W'))

    d.add(flow.Line('right', xy=d4.E, tox=good.S))
    d.add(flow.Arrow('up', toy=good.S))
    d.add(flow.Arrow('down', xy=d4.S, l=d.unit/2))
    d5 = d.add(flow.Decision(w=5, h=3.6, E='YES', S='NO', label='BUT YOU\nJUST FOLLOWED\nTHEM TWICE!'))
    d.add(flow.Arrow('right', xy=d5.E, l=d.unit))
    question = d.add(flow.Box(w=3.5, h=1.75, label="(THAT WASN'T\nA QUESTION.)", anchor='W'))
    d.add(flow.Line('down', xy=d5.S, l=d.unit/3))
    d.add(flow.Line('right', tox=question.S))
    d.add(flow.Arrow('up', toy=question.S))

    d.add(flow.Line('right', xy=good.E, tox=question.S))
    d.add(flow.Arrow('down', l=d.unit))
    drink = d.add(flow.Box(w=2.5, h=1.5, label="LET'S GO\nDRINK."))
    d.add(flow.Arrow('right', xy=drink.E, label='6 DRINKS'))
    d.add(flow.Box(w=3.7, h=2, label='HEY, I SHOULD\nTRY INSTALLING\nFREEBSD!', anchor='W'))
    d.add(flow.Arrow('up', xy=question.N, l=d.unit*.75))
    screw = d.add(flow.Box(w=2.5, h=1, label='SCREW IT.', anchor='S'))
    d.add(flow.Arrow('up', xy=screw.N, toy=drink.S))
    d.draw()
