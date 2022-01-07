Analog Circuits
---------------

.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    

Discharging capacitor
^^^^^^^^^^^^^^^^^^^^^

Shows how to connect to a switch with anchors.

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d += (V1 := elm.SourceV().label('5V'))
        d += elm.Line().right(d.unit*.75)
        d += (S1 := elm.SwitchSpdt2(action='close').up().anchor('b').label('$t=0$', loc='rgt'))
        d += elm.Line().right(d.unit*.75).at(S1.c)
        d += elm.Resistor().down().label('$100\Omega$').label(['+','$v_o$','-'], loc='bot')
        d += elm.Line().to(V1.start)
        d += elm.Capacitor().at(S1.a).toy(V1.start).label('1$\mu$F').dot()


Capacitor Network
^^^^^^^^^^^^^^^^^

Shows how to use endpoints to specify exact start and end placement.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
        d += (C1 := elm.Capacitor().label('8nF').idot().label('a', 'left'))
        d += (C2 := elm.Capacitor().label('18nF'))
        d += (C3 := elm.Capacitor().down().label('8nF', loc='bottom'))
        d += (C4 := elm.Capacitor().left().label('32nF'))
        d += (C5 := elm.Capacitor().label('40nF', loc='bottom').dot().label('b', 'left'))
        d += (C6 := elm.Capacitor().endpoints(C1.end, C5.start).label('2.8nF'))
        d += (C7 := elm.Capacitor().endpoints(C2.end, C5.start)
              .label('5.6nF', loc='center', ofst=(-.3, -.1), halign='right', valign='bottom'))


ECE201-Style Circuit
^^^^^^^^^^^^^^^^^^^^

This example demonstrate use of `push()` and `pop()` and using the 'tox' and 'toy' methods.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(unit=2)  # unit=2 makes elements have shorter than normal leads
        d.push()
        d += (R1 := elm.Resistor().down().label('20Ω'))
        d += (V1 := elm.SourceV().down().reverse().label('120V'))
        d += elm.Line().right(3).dot()
        d.pop()
        d += elm.Line().right(3).dot()
        d += elm.SourceV().down().reverse().label('60V')
        d += elm.Resistor().label('5Ω').dot()
        d += elm.Line().right(3).dot()
        d += elm.SourceI().up().label('36A')
        d += elm.Resistor().label('10Ω').dot()
        d += elm.Line().left(3).hold()
        d += elm.Line().right(3).dot()
        d += (R6 := elm.Resistor().toy(V1.end).label('6Ω').dot())
        d += elm.Line().left(3).hold()
        d += elm.Resistor().right().at(R6.start).label('1.6Ω').dot(open=True).label('a', 'right')
        d += elm.Line().right().at(R6.end).dot(open=True).label('b', 'right')


Loop Currents
^^^^^^^^^^^^^

Using the :py:class:`schemdraw.elements.lines.LoopCurrent` element to add loop currents, and rotating a label to make it fit.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(unit=5)
        d += (V1 := elm.SourceV().label('20V'))
        d += (R1 := elm.Resistor().right().label('400Ω'))
        d += elm.Dot()
        d.push()
        d += (R2 := elm.Resistor().down().label('100Ω', loc='bot', rotate=True))
        d += elm.Dot()
        d.pop()
        d += (L1 := elm.Line())
        d += (I1 := elm.SourceI().down().label('1A', loc='bot'))
        d += (L2 := elm.Line().tox(V1.start))
        d += elm.LoopCurrent([R1,R2,L2,V1], pad=1.25).label('$I_1$')
        d += elm.LoopCurrent([R1,I1,L2,R2], pad=1.25).label('$I_2$')    # Use R1 as top element for both so they get the same height


AC Loop Analysis
^^^^^^^^^^^^^^^^

Another good problem for ECE students...

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d += (I1 := elm.SourceI().label('5∠0° A').dot())
        d.push()
        d += elm.Capacitor().right().label('-j3Ω').dot()
        d += elm.Inductor().down().label('j2Ω').dot().hold()
        d += elm.Resistor().right().label('5Ω').dot()
        d += (V1 := elm.SourceV().down().reverse().label('5∠-90° V', loc='bot'))
        d += elm.Line().tox(I1.start)
        d.pop()
        d += elm.Line().up(d.unit*.8)
        d += (L1 := elm.Inductor().tox(V1.start).label('j3Ω'))
        d += elm.Line().down(d.unit*.8)
        d += elm.CurrentLabel(top=False, ofst=.3).at(L1).label('$i_g$')


Infinite Transmission Line
^^^^^^^^^^^^^^^^^^^^^^^^^^

Elements can be added inside for-loops if you need multiples.
The ellipsis is just another circuit element, called `DotDotDot` since Ellipsis is a reserved keyword in Python.
This also demonstrates the :py:class:`schemdraw.elements.ElementDrawing` class to merge multiple elements into a single definition.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing(show=False) as d1:
        d1 += elm.Resistor()
        d1.push()
        d1 += elm.Capacitor().down()
        d1 += elm.Line().left()
        d1.pop()

    with schemdraw.Drawing() as d2:
        for i in range(3):
            d2 += elm.ElementDrawing(d1)

        d2.push()
        d2 += elm.Line().length(d2.unit/6)
        d2 += elm.DotDotDot()
        d2 += elm.ElementDrawing(d1)
        d2.pop()
        d2.here = (d2.here[0], d2.here[1]-d2.unit)
        d2 += elm.Line().right().length(d2.unit/6)
        d2 += elm.DotDotDot()


Power supply
^^^^^^^^^^^^

Notice the diodes could be added individually, but here the built-in `Rectifier` element is used instead.
Also note the use of newline characters inside resistor and capacitor labels.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(inches_per_unit=.5, unit=3)
        d += (D := elm.Rectifier())
        d += elm.Line().left(d.unit*1.5).at(D.N).dot(open=True).idot()
        d += elm.Line().left(d.unit*1.5).at(D.S).dot(open=True).idot()
        d += (G := elm.Gap().toy(D.N).label(['–', 'AC IN', '+']))

        d += (top := elm.Line().right(d.unit*3).at(D.E).idot())
        d += (Q2 := elm.BjtNpn(circle=True).up().anchor('collector').label('Q2\n2n3055'))
        d += elm.Line().down(d.unit/2).at(Q2.base)
        d += (Q2b := elm.Dot())
        d += elm.Line().left(d.unit/3)
        d += (Q1 := elm.BjtNpn(circle=True).up().anchor('emitter').label('Q1\n    2n3054'))
        d += elm.Line().at(Q1.collector).toy(top.center).dot()

        d += elm.Line().down(d.unit/2).at(Q1.base).dot()
        d += elm.Zener().down().reverse().label('D2\n500mA', loc='bot').dot()
        d += (G := elm.Ground())
        d += elm.Line().left().dot()
        d += elm.Capacitor(polar=True).up().reverse().label('C2\n100$\mu$F\n50V', loc='bot').dot()
        d += elm.Line().right().hold()
        d += elm.Resistor().toy(top.end).label('R1\n2.2K\n50V', loc='bot').dot()

        d.move(dx=-d.unit, dy=0)
        d += elm.Capacitor(polar=True).toy(G.start).flip().label('C1\n 1000$\mu$F\n50V').dot().idot()
        d += elm.Line().at(G.start).tox(D.W)
        d += elm.Line().toy(D.W).dot()

        d += elm.Resistor().right().at(Q2b.center).label('R2').label('56$\Omega$ 1W', loc='bot').dot()
        d.push()
        d += elm.Line().toy(top.start).dot()
        d += elm.Line().tox(Q2.emitter)
        d.pop()
        d += elm.Capacitor(polar=True).toy(G.start).label('C3\n470$\mu$F\n50V', loc='bot').dot()
        d += elm.Line().tox(G.start).hold()
        d += elm.Line().right().dot()
        d += elm.Resistor().toy(top.center).label('R3\n10K\n1W', loc='bot').dot()
        d += elm.Line().left().hold()
        d += elm.Line().right()
        d += elm.Dot(open=True)
        d += elm.Gap().toy(G.start).label(['+', '$V_{out}$', '–'])
        d += elm.Dot(open=True)
        d += elm.Line().left()