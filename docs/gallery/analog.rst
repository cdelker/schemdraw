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
    V1 = d.add(elm.SourceV(label='5V'))
    d.add(elm.Line(d='right', l=d.unit*.75))
    S1 = d.add(elm.SwitchSpdt2(d='up', action='close', anchor='b', rgtlabel='$t=0$'))
    d.add(elm.Line(d='right', xy=S1.c,  l=d.unit*.75))
    d.add(elm.Resistor(d='down', label='$100\Omega$', botlabel=['+','$v_o$','-']))
    d.add(elm.Line(to=V1.start))
    d.add(elm.Capacitor(xy=S1.a, d='down', toy=V1.start, label='1$\mu$F'))
    d.add(elm.Dot())
    d.draw()


Capacitor Network
^^^^^^^^^^^^^^^^^

Shows how to use endpoints to specify exact start and end placement.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(fontsize=12)
    A  = d.add(elm.Dot(label='a'))
    C1 = d.add(elm.Capacitor(label='8nF'))
    C2 = d.add(elm.Capacitor(label='18nF'))
    C3 = d.add(elm.Capacitor(botlabel='8nF', d='down'))
    C4 = d.add(elm.Capacitor(botlabel='32nF', d='left'))
    C5 = d.add(elm.Capacitor(botlabel='40nF'))
    B  = d.add(elm.Dot(label='b'))
    C6 = d.add(elm.Capacitor(label='2.8nF', endpts=[C1.end,C5.start]))
    C7 = d.add(elm.Capacitor(endpts=[C2.end,C5.start]))
    C7.add_label('5.6nF', loc='center', ofst=[-.3,-.1], align=('right','bottom'))
    d.draw()



ECE201-Style Circuit
^^^^^^^^^^^^^^^^^^^^

This example demonstrate use of `push()` and `pop()` and using the 'tox' and 'toy' keywords.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=2)  # unit=2 makes elements have shorter than normal leads
    d.push()
    R1 = d.add(elm.Resistor(d='down', label='20$\Omega$'))
    V1 = d.add(elm.SourceV(d='down', reverse=True, label='120V'))
    d.add(elm.Line(d='right', l=3))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Line(d='right', l=3))
    d.add(elm.Dot())
    d.add(elm.SourceV(d='down', label='60V', reverse=True))
    d.add(elm.Resistor(label='5$\Omega$'))
    d.add(elm.DOT())
    d.add(elm.Line(d='right', l=3))
    d.add(elm.SourceI(d='up', label='36A'))
    d.add(elm.Resistor(label='10$\Omega$'))
    d.add(elm.DOT())
    d.add(elm.Line(d='left', l=3, move_cur=False))
    d.add(elm.Line(d='right', l=3))
    d.add(elm.DOT())
    R6 = d.add(elm.Resistor(d='down', toy=V1.end, label='6$\Omega$'))
    d.add(elm.DOT())
    d.add(elm.Line(d='left', l=3, move_cur=False))
    d.add(elm.Resistor(d='right', xy=R6.start, label='1.6$\Omega$'))
    d.add(elm.Dot(label='a'))
    d.add(elm.Line(d='right', xy=R6.end))
    d.add(elm.Dot(label='b'))
    d.draw()



Loop Currents
^^^^^^^^^^^^^

Using the :py:meth:`Drawing.loopI` method to add loop currents, and rotating a label to make it fit.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=5)
    V1 = d.add(elm.SourceV(label='$20V$'))
    R1 = d.add(elm.Resistor(d='right', label='400$\Omega$'))
    d.add(elm.Dot())
    d.push()
    R2 = d.add(elm.Resistor(d='down', botlabel='100$\Omega$', lblrotate=True))
    d.add(elm.Dot())
    d.pop()
    L1 = d.add(elm.Line())
    I1 = d.add(elm.SourceI(d='down', botlabel='1A'))
    L2 = d.add(elm.Line(d='left', tox=V1.start))
    d.loopI([R1,R2,L2,V1], '$I_1$', pad=1.25)
    d.loopI([R1,I1,L2,R2], '$I_2$', pad=1.25)  # Use R1 as top element for both so they get the same height
    d.draw()


AC Loop Analysis
^^^^^^^^^^^^^^^^

Another good problem for ECE students...

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    I1 = d.add(elm.SourceI(label=r'$5\angle 0^{\circ}$A'))
    d.add(elm.Dot())
    d.push()
    d.add(elm.Capacitor('right', label=r'$-j3\Omega$'))
    d.add(elm.Dot())
    d.push()
    d.add(elm.Inductor('down', label=r'$j2\Omega$'))
    d.add(elm.Dot())
    d.pop()
    d.add(elm.Resistor('right', label=r'$5\Omega$'))
    d.add(elm.Dot())
    V1 = d.add(elm.SourceV('down', reverse=True, botlabel=r'$5\angle -90^{\circ}$V'))
    d.add(elm.Line('left', tox=I1.start))
    d.pop()
    d.add(elm.Line('up', l=d.unit*.8))
    L1 = d.add(elm.Inductor('right', label=r'$j3\Omega$', tox=V1.start))
    d.add(elm.Line('down', l=d.unit*.8))
    l = d.labelI(L1, '$i_g$', top=False)
    d.draw()

Infinite Transmission Line
^^^^^^^^^^^^^^^^^^^^^^^^^^

Elements can be added inside for-loops if you need multiples.
The ellipsis is just another circuit element, called `DotDotDot` since Ellipsis is a reserved keyword in Python.
This also demonstrates the :py:class:`schemdraw.elements.ElementDrawing` class to merge multiple elements into a single definition.

.. jupyter-execute::
    :code-below:
    
    d1 = schemdraw.Drawing()
    d1.add(elm.Resistor())
    d1.push()
    d1.add(elm.Capacitor('down'))
    d1.add(elm.Line('left'))
    d1.pop()

    d2 = schemdraw.Drawing()
    for i in range(3):
        d2.add(elm.ElementDrawing(d1))

    d2.push()
    d2.add(elm.Line(l=d2.unit/6))
    d2.add(elm.DotDotDot)
    d2.add(elm.ElementDrawing(d1))
    d2.pop()
    d2.here = [d2.here[0], d2.here[1]-d2.unit]
    d2.add(elm.Line('right', l=d2.unit/6))
    d2.add(elm.DotDotDot)
    d2.draw()


Power supply
^^^^^^^^^^^^

Notice the diodes added with the `theta` parameter to point them in the right directions.
Also the use of newline characters inside resistor and capacitor labels.

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(inches_per_unit=.5, unit=3)
    D1 = d.add(elm.Diode(theta=-45))
    d.add(elm.Dot)
    D2 = d.add(elm.Diode(theta=225, reverse=True))
    d.add(elm.Dot)
    D3 = d.add(elm.Diode(theta=135, reverse=True))
    d.add(elm.Dot)
    D4 = d.add(elm.Diode(theta=45))
    d.add(elm.Dot)

    d.add(elm.Line('left', xy=D3.end, l=d.unit/2))
    d.add(elm.Dot(open=True))
    G = d.add(elm.Gap('up', toy=D1.start, label=['–', 'AC IN', '+']))
    d.add(elm.Line('left', xy=D4.end, tox=G.start))
    d.add(elm.Dot(open=True))

    top = d.add(elm.Line('right', xy=D2.end, l=d.unit*3))
    Q2 = d.add(elm.BjtNpn('up', circle=True, anchor='collector', label='Q2\n2n3055'))
    d.add(elm.Line('down', xy=Q2.base, l=d.unit/2))
    Q2b = d.add(elm.Dot)
    d.add(elm.Line('left', l=d.unit/3))
    Q1 = d.add(elm.BjtNpn('up', circle=True, anchor='emitter', label='Q1\n    2n3054'))
    d.add(elm.Line('up', xy=Q1.collector, toy=top.center))
    d.add(elm.Dot)

    d.add(elm.Line('down', xy=Q1.base, l=d.unit/2))
    d.add(elm.Dot)
    d.add(elm.Zener('down', reverse=True, botlabel='D2\n500mA'))
    d.add(elm.Dot)
    G = d.add(elm.Ground())
    d.add(elm.Line('left'))
    d.add(elm.Dot)
    d.add(elm.Capacitor('up', polar=True, botlabel='C2\n100$\mu$F\n50V', reverse=True))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Line('right'))
    d.pop()
    d.add(elm.Resistor('up', toy=top.end, botlabel='R1\n2.2K\n50V'))
    d.add(elm.Dot)

    d.here = [d.here[0]-d.unit, d.here[1]]
    d.add(elm.Dot)
    d.add(elm.Capacitor('down', polar=True, toy=G.start, label='C1\n 1000$\mu$F\n50V', flip=True))
    d.add(elm.Dot)
    d.add(elm.Line('left', xy=G.start, tox=D4.start))
    d.add(elm.Line('up', toy=D4.start))

    d.add(elm.Resistor('right', xy=Q2b.center, label='R2', botlabel='56$\Omega$ 1W'))
    d.add(elm.Dot())
    d.push()
    d.add(elm.Line('up', toy=top.start))
    d.add(elm.Dot())
    d.add(elm.Line('left', tox=Q2.emitter))
    d.pop()
    d.add(elm.Capacitor('down', polar=True, toy=G.start, botlabel='C3\n470$\mu$F\n50V'))
    d.add(elm.Dot)
    d.add(elm.Line('left', tox=G.start, move_cur=False))
    d.add(elm.Line('right'))
    d.add(elm.Dot)
    d.add(elm.Resistor('up', toy=top.center, botlabel='R3\n10K\n1W'))
    d.add(elm.Dot)
    d.add(elm.Line('left', move_cur=False))
    d.add(elm.Line('right'))
    d.add(elm.Dot(open=True))
    d.add(elm.Gap('down', toy=G.start, label=['+', '$V_{out}$', '–']))
    d.add(elm.Dot(open=True))
    d.add(elm.Line('left'))
    d.draw()
