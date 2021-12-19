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
    
    d = schemdraw.Drawing()
    d += (V1 := elm.SourceV().label('5V'))
    d += elm.Line().right().length(d.unit*.75)
    d += (S1 := elm.SwitchSpdt2(action='close').up().anchor('b').label('$t=0$', loc='rgt'))
    d += elm.Line().right().at(S1.c).length(d.unit*.75)
    d += elm.Resistor().down().label('100 Ω').label(['+','$v_o$','-'], loc='bot')
    d += elm.Line().to(V1.start)
    d += elm.Capacitor().down().at(S1.a).toy(V1.start).label('1 μF')
    d += elm.Dot()
    d.draw()


Capacitor Network
^^^^^^^^^^^^^^^^^

Shows how to use endpoints to specify exact start and end placement.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(fontsize=12)
    d += (A := elm.Dot().label('a'))
    d += (C1 := elm.Capacitor().label('8nF'))
    d += (C2 := elm.Capacitor().label('18nF'))
    d += (C3 := elm.Capacitor().down().label('8nF', loc='bottom'))
    d += (C4 := elm.Capacitor().left().label('32nF'))
    d += (C5 := elm.Capacitor().label('40nF', loc='bottom'))
    d += (B := elm.Dot().label('b'))
    d += (C6 := elm.Capacitor().endpoints(C1.end, C5.start).label('2.8nF'))
    d += (C7 := elm.Capacitor().endpoints(C2.end, C5.start)
          .label('5.6nF', loc='center', ofst=(-.3, -.1), halign='right', valign='bottom'))
    d.draw()



ECE201-Style Circuit
^^^^^^^^^^^^^^^^^^^^

This example demonstrate use of `push()` and `pop()` and using the 'tox' and 'toy' methods.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=2)  # unit=2 makes elements have shorter than normal leads
    d.push()
    d += (R1 := elm.Resistor().down().label('20Ω'))
    d += (V1 := elm.SourceV().down().reverse().label('120V'))
    d += elm.Line().right().length(3)
    d += elm.Dot()
    d.pop()
    d += elm.Line().right().length(3)
    d += elm.Dot()
    d += elm.SourceV().down().reverse().label('60V')
    d += elm.Resistor().label('5Ω')
    d += elm.Dot()
    d += elm.LineDot().right().length(3)
    d += elm.SourceI().up().label('36A')
    d += elm.Resistor().label('10Ω')
    d += elm.Dot()
    d += elm.Line().left().length(3).hold()
    d += elm.Line().right().length(3)
    d += elm.Dot()
    d += (R6 := elm.Resistor().down().toy(V1.end).label('6Ω'))
    d += elm.Dot()
    d += elm.Line().left().length(3).hold()
    d += elm.Resistor().right().at(R6.start).label('1.6Ω')
    d += elm.Dot().label('a')
    d += elm.Line().right().at(R6.end)
    d += elm.Dot().label('b')
    d.draw()




Loop Currents
^^^^^^^^^^^^^

Using the :py:class:`schemdraw.elements.lines.LoopCurrent` element to add loop currents, and rotating a label to make it fit.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=5)
    d += (V1 := elm.SourceV().label('20V'))
    d += (R1 := elm.Resistor().right().label('400Ω'))
    d += elm.Dot()
    d.push()
    d += (R2 := elm.Resistor().down().label('100Ω', loc='bot', rotate=True))
    d += elm.Dot()
    d.pop()
    d += (L1 := elm.Line())
    d += (I1 := elm.SourceI().down().label('1A', loc='bot'))
    d += (L2 := elm.Line().left().tox(V1.start))
    d.loopI([R1,R2,L2,V1], '$I_1$', pad=1.25)
    d.loopI([R1,I1,L2,R2], '$I_2$', pad=1.25)  # Use R1 as top element for both so they get the same height
    d.draw()


AC Loop Analysis
^^^^^^^^^^^^^^^^

Another good problem for ECE students...

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    d += (I1 := elm.SourceI().label('5∠0° A'))
    d += elm.Dot()
    d.push()
    d += elm.Capacitor().right().label('-j3Ω')
    d += elm.Dot()
    d.push()
    d += elm.Inductor().down().label('j2Ω')
    d += elm.Dot()
    d.pop()
    d += elm.Resistor().right().label('5Ω')
    d += elm.Dot()
    d += (V1 := elm.SourceV().down().reverse().label('5∠-90° V', loc='bot'))
    d += elm.Line().left().tox(I1.start)
    d.pop()
    d += elm.Line().up().length(d.unit*.8)
    d += (L1 := elm.Inductor().right().tox(V1.start).label('j3Ω'))
    d += elm.Line().down().length(d.unit*.8)
    d.labelI(L1, '$i_g$', top=False)
    d.draw()


Infinite Transmission Line
^^^^^^^^^^^^^^^^^^^^^^^^^^

Elements can be added inside for-loops if you need multiples.
The ellipsis is just another circuit element, called `DotDotDot` since Ellipsis is a reserved keyword in Python.
This also demonstrates the :py:class:`schemdraw.elements.ElementDrawing` class to merge multiple elements into a single definition.

.. jupyter-execute::
    :code-below:

    d1 = schemdraw.Drawing()
    d1 += elm.Resistor()
    d1.push()
    d1 += elm.Capacitor().down()
    d1 += elm.Line().left()
    d1.pop()

    d2 = schemdraw.Drawing()
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
    d2.draw()


Power supply
^^^^^^^^^^^^

Notice the diodes use the `theta` method to point them in the right directions.
Also the use of newline characters inside resistor and capacitor labels.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(inches_per_unit=.5, unit=3)
    d += (D1 := elm.Diode().theta(-45))
    d += elm.Dot()
    d += (D2 := elm.Diode().theta(225).reverse())
    d += elm.Dot()
    d += (D3 := elm.Diode().theta(135).reverse())
    d += elm.Dot()
    d += (D4 := elm.Diode().theta(45))
    d += elm.Dot()

    d += elm.Line().left().at(D3.start).length(d.unit*1.5)
    d += elm.Dot(open=True)
    d += (G := elm.Gap().up().toy(D1.start).label(['–', 'AC IN', '+']))
    d += elm.Line().left().at(D4.end).tox(G.start)
    d += elm.Dot(open=True)

    d += (top := elm.Line().right().at(D2.start).length(d.unit*3))
    d += (Q2 := elm.BjtNpn(circle=True).up().anchor('collector').label('Q2\n2n3055'))
    d += elm.Line().down().at(Q2.base).length(d.unit/2)
    d += (Q2b := elm.Dot())
    d += elm.Line().left().length(d.unit/3)
    d += (Q1 := elm.BjtNpn(circle=True).up().anchor('emitter').label('Q1\n    2n3054'))
    d += elm.Line().up().at(Q1.collector).toy(top.center)
    d += elm.Dot()

    d += elm.Line().down().at(Q1.base).length(d.unit/2)
    d += elm.Dot()
    d += elm.Zener().down().reverse().label('D2\n500mA', loc='bot')
    d += elm.Dot()
    d += (G := elm.Ground())
    d += elm.Line().left()
    d += elm.Dot()
    d += elm.Capacitor(polar=True).up().reverse().label('C2\n100$\mu$F\n50V', loc='bot')
    d += elm.Dot()
    d.push()
    d += elm.Line().right()
    d.pop()
    d += elm.Resistor().up().toy(top.end).label('R1\n2.2K\n50V', loc='bot')
    d += elm.Dot()

    d.move(dx=-d.unit, dy=0)
    d += elm.Dot()
    d += elm.Capacitor(polar=True).down().toy(G.start).flip().label('C1\n 1000$\mu$F\n50V')
    d += elm.Dot()
    d += elm.Line().left().at(G.start).tox(D4.start)
    d += elm.Line().up().toy(D4.start)

    d += elm.Resistor().right().at(Q2b.center).label('R2').label('56$\Omega$ 1W', loc='bot')
    d += elm.Dot()
    d.push()
    d += elm.Line().up().toy(top.start)
    d += elm.Dot()
    d += elm.Line().left().tox(Q2.emitter)
    d.pop()
    d += elm.Capacitor(polar=True).down().toy(G.start).label('C3\n470$\mu$F\n50V', loc='bot')
    d += elm.Dot()
    d += elm.Line().left().tox(G.start).hold()
    d += elm.Line().right()
    d += elm.Dot()
    d += elm.Resistor().up().toy(top.center).label('R3\n10K\n1W', loc='bot')
    d += elm.Dot()
    d += elm.Line().left().hold()
    d += elm.Line().right()
    d += elm.Dot(open=True)
    d += elm.Gap().down().toy(G.start).label(['+', '$V_{out}$', '–'])
    d += elm.Dot(open=True)
    d += elm.Line().left()
    d.draw()
