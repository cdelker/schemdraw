
.. _gallery:

Circuit Gallery
===============

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import logic
    from schemdraw import dsp
    from schemdraw import flow


Analog Circuits
---------------

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
The ellipsis is just another circuit element.
This also demonstrates the :py:func:`group_elements` function to merge multiple elements into a single definition.

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


Opamp Circuits
--------------

Inverting Opamp
^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    op = d.add(elm.Opamp)
    d.add(elm.Line('left', xy=op.in2, l=d.unit/4))
    d.add(elm.Line('down', l=d.unit/5))
    d.add(elm.Ground)
    d.add(elm.Line('left', xy=op.in1, l=d.unit/6))
    d.add(elm.Dot)
    d.push()
    Rin = d.add(elm.Resistor('left', xy=op.in1-[d.unit/5,0], botlabel='$R_{in}$', lftlabel='$v_{in}$'))
    d.pop()
    d.add(elm.Line('up', l=d.unit/2))
    Rf = d.add(elm.Resistor('right', l=d.unit*1, label='$R_f$'))
    d.add(elm.Line('down', toy=op.out))
    d.add(elm.Dot)
    d.add(elm.Line('left', tox=op.out))
    d.add(elm.Line('right', l=d.unit/4, rgtlabel='$v_{o}$'))
    d.draw()


Non-inverting Opamp
^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    op = d.add(elm.Opamp)
    d.add(elm.Line(xy=op.out, l=.75))
    d.add(elm.Line('left', xy=op.in1, l=.75))
    d.add(elm.Line('up', l=1.5))
    d.add(elm.Dot)
    R1 = d.add(elm.Resistor('left', label='$R_1$'))
    d.add(elm.Ground)
    Rf = d.add(elm.Resistor('right', xy=R1.start, tox=op.out+.5, label='$R_f$'))
    d.add(elm.Line('down', toy=op.out))
    dot = d.add(elm.Dot)
    d.add(elm.Line('left', xy=op.in2, l=.75))
    d.add(elm.Dot)
    R3 = d.add(elm.Resistor('down', label='$R_3$'))
    d.add(elm.Dot)
    d.add(elm.Ground)
    R2 = d.add(elm.Resistor('left', xy=R3.start, label='$R_2$'))
    d.add(elm.SourceV('down', reverse=True, label='$v_{in}$'))
    d.add(elm.Line('right', tox=Rf.end))
    d.add(elm.Gap('down', xy=dot.start, toy=R3.end, label=['+','$v_o$','–']))
    d.draw()


Multi-stage amplifier
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    d.add(elm.Ground)
    d.add(elm.SourceV(label='500mV'))

    d.add(elm.Resistor('right', label='20k$\Omega$'))
    Vin = d.add(elm.Dot)
    d.add(elm.Line(l=.5))
    O1 = d.add(elm.Opamp(anchor='in1'))
    d.add(elm.Line('left', l=.75, xy=O1.in2))
    d.add(elm.Ground)
    d.add(elm.Line('up', xy=Vin.start, l=2))
    d.add(elm.Resistor('right', label='100k$\Omega$'))
    d.add(elm.Line('down', toy=O1.out))
    d.add(elm.Dot)
    d.add(elm.Line('right', xy=O1.out, l=5))
    O2 = d.add(elm.Opamp(anchor='in2'))
    Vin2 = d.add(elm.Line('left', l=.5, xy=O2.in1))
    d.add(elm.Dot)
    d.add(elm.Resistor('left', label='30k$\Omega$'))
    d.add(elm.Ground)
    d.add(elm.Line('up', xy=Vin2.end, l=1.5))
    d.add(elm.Resistor('right', label='90k$\Omega$'))
    d.add(elm.Line('down', toy=O2.out))
    d.add(elm.Dot)
    d.add(elm.Line('right', xy=O2.out, l=1, rgtlabel='$v_{out}$'))
    d.draw()



Opamp pin labeling
^^^^^^^^^^^^^^^^^^

This example shows how to label pin numbers on a 741 opamp, and connect to the offset anchors.
Pin labels are somewhat manually placed; without the `ofst` and `align` keywords they
will be drawn directly over the anchor position. Also note the use of the `zoom` keyword
when placing the potentiometer to slightly reduce its size.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(fontsize=12)
    op = d.add(elm.Opamp(label='741', lblloc='center', lblofst=0))
    d.add(elm.Line('left', xy=op.in1, l=.5))
    d.add(elm.Line('down', l=d.unit/2))
    d.add(elm.Ground)
    d.add(elm.Line('left', xy=op.in2, l=.5))
    d.add(elm.Line('right', xy=op.out, l=.5, rgtlabel='$V_o$'))
    d.add(elm.Line('up', xy=op.vd, l=1, rgtlabel='$+V_s$'))
    trim = d.add(elm.Potentiometer('down', xy=op.n1, flip=True, zoom=.7))
    d.add(elm.Line('right', tox=op.n1a))
    d.add(elm.Line('up', to=op.n1a))
    d.add(elm.Line('left', xy=trim.tap, tox=op.vs))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Line('down', l=d.unit/3))
    d.add(elm.Ground)
    d.pop()
    d.add(elm.Line('up', toy=op.vs))
    op.add_label('1', loc='n1', size=9, ofst=[-.1, -.25], align=('right', 'top'))
    op.add_label('5', loc='n1a', size=9, ofst=[-.1, -.25], align=('right', 'top'))
    op.add_label('4', loc='vs', size=9, ofst=[-.1, -.2], align=('right', 'top'))
    op.add_label('7', loc='vd', size=9, ofst=[-.1, .2], align=('right', 'bottom'))
    op.add_label('2', loc='in1', size=9, ofst=[-.1, .1], align=('right', 'bottom'))
    op.add_label('3', loc='in2', size=9, ofst=[-.1, .1], align=('right', 'bottom'))
    op.add_label('6', loc='out', size=9, ofst=[-.1, .1], align=('left', 'bottom'))
    d.draw()



Triaxial Cable Driver
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(fontsize=10)
    d.add(elm.Line(lftlabel='V', l=d.unit/5))
    smu = d.add(elm.Opamp(sign=False, anchor='in2'))
    smu.add_label('SMU', ofst=[-.4, 0], loc='center', align=('center', 'center'))
    d.add(elm.Line(xy=smu.out, l=d.unit/5))
    d.push()
    d.add(elm.Line(l=d.unit/4))
    triax = d.add(elm.triax(length=5, shieldofststart=.75))
    d.pop()
    d.add(elm.Dot)
    d.add(elm.Resistor('up', l=d.unit, zoom=.6))
    d.add(elm.Line('left'))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Line('down', toy=smu.in1))
    d.add(elm.Line('right', tox=smu.in1))
    d.pop()
    d.add(elm.Line('up', l=d.unit/5))
    d.add(elm.Line('right', l=d.unit/5))
    buf = d.add(elm.Opamp(sign=False, zoom=.6, anchor='in2'))
    buf.add_label('BUF', ofst=[-.4, 0], loc='center', align=('center', 'center'))
    d.add(elm.Line('left', xy=buf.in1, l=d.unit/5))
    d.add(elm.Line('up', l=d.unit/5))
    d.add(elm.Line('right'))
    d.add(elm.Line('down', toy=buf.out))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Line('left', tox=buf.out))
    d.pop()
    d.add(elm.Line('right', tox=triax.guardstart_top))
    d.add(elm.Line('down', toy=triax.guardstart_top))
    d.add(elm.GroundChassis(xy=triax.shieldcenter))
    d.draw()


Logic Gates
-----------    

Logic gate definitions are in the :py:mod:`schemdraw.logic` module. Here it was imported with

.. code-block:: python

    import schemdraw.logic as l


Half Adder
^^^^^^^^^^

Notice the half and full adders set the drawing unit to 0.5 so the lines aren't quite as long and look better with logic gates.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=.5)
    S = d.add(logic.Xor(rgtlabel='$S$'))
    A = d.add(logic.Dot(xy=S.in1))
    d.add(logic.Line('left', l=d.unit*2, lftlabel='$A$'))
    d.add(logic.Line('left', xy=S.in2))
    B = d.add(logic.Dot)
    d.add(logic.Line('left', lftlabel='$B$'))

    d.add(logic.Line('down', xy=A.start, l=d.unit*3))
    C = d.add(logic.And('right', anchor='in1', rgtlabel='$C$'))
    d.add(logic.Line('down', xy=B.start, toy=C.in2))
    d.add(logic.Line(to=C.in2))
    d.draw()


Full Adder
^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(unit=.5)
    X1 = d.add(logic.Xor)
    d.add(logic.Dot)
    A = d.add(logic.Dot(xy=X1.in1))
    Ain = d.add(logic.Line('left', l=d.unit*2, lftlabel='$A$'))
    d.add(logic.Line('left', xy=X1.in2))
    B = d.add(logic.Dot)
    d.add(logic.Line('left', lftlabel='$B$'))

    d.add(logic.Line('right', xy=X1.out, l=d.unit))
    X2 = d.add(logic.Xor(anchor='in1'))
    C = d.add(logic.Line('down', xy=X2.in2, l=d.unit*2))
    d.push()
    d.add(logic.Dot(xy=C.center))
    d.add(logic.Line('left', tox=Ain.end, lftlabel='$C_{in}$'))
    d.pop()

    A1 = d.add(logic.And('right', anchor='in1'))
    d.add(logic.Line('left', xy=A1.in2, tox=X1.out))
    d.add(logic.Line('up', toy=X1.out))
    A2 = d.add(logic.And('right', anchor='in1', xy=[A1.in1[0],A1.in2[1]-d.unit*2]))
    d.add(logic.Line('left', xy=A2.in1, tox=A.start))
    d.add(logic.Line('up', toy=A.start))
    d.add(logic.Line('left', xy=A2.in2, tox=B.start))
    d.add(logic.Line('up', toy=B.start))

    O1 = d.add(logic.Or('right', xy=[A1.out[0],(A1.out[1]+A2.out[1])/2], rgtlabel='$C_{out}$'))
    d.add(logic.Line('down', xy=A1.out, toy=O1.in1))
    d.add(logic.Line('up', xy=A2.out, toy=O1.in2))
    d.add(logic.Line('right', xy=X2.out, tox=O1.out, rgtlabel='$S$'))
    d.draw()


J-K Flip Flop
^^^^^^^^^^^^^

Note the use of the LaTeX command **overline{Q}** in the label to draw a bar over the inverting output label.

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    # Two front gates (SR latch)
    G1 = d.add(logic.Nand(anchor='in1'))
    d.add(logic.Line(l=d.unit/6))
    Q1 = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/6))
    Q2 = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/3, rgtlabel='$Q$'))
    G2 = d.add(logic.Nand(anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5]))
    d.add(logic.Line(l=d.unit/6))
    Qb = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/3))
    Qb2 = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/6, rgtlabel='$\overline{Q}$'))
    S1 = d.add(logic.Line(xy=G2.in1, d='up', l=d.unit/6))
    d.add(logic.Line('down', xy=Q1.start, l=d.unit/6))
    d.add(logic.Line(to=S1.end))
    R1 = d.add(logic.Line('down', xy=G1.in2, l=d.unit/6))
    d.add(logic.Line('up', xy=Qb.start, l=d.unit/6))
    d.add(logic.Line(to=R1.end))

    # Two back gates
    d.add(logic.Line('left', xy=G1.in1, l=d.unit/6))
    J = d.add(logic.Nand(inputs=3, anchor='out', reverse=True))
    d.add(logic.Line('up', xy=J.in3, l=d.unit/6))
    d.add(logic.Line('right', tox=Qb2.start))
    d.add(logic.Line('down', toy=Qb2.start))
    d.add(logic.Line('left', xy=J.in2, l=d.unit/4, lftlabel='$J$'))
    d.add(logic.Line('left', xy=G2.in2, l=d.unit/6))
    K = d.add(logic.Nand(inputs=3, anchor='out', reverse=True))
    d.add(logic.Line('down', xy=K.in1, l=d.unit/6))
    d.add(logic.Line('right', tox=Q2.start))
    d.add(logic.Line('up', toy=Q2.start))
    d.add(logic.Line('left', xy=K.in2, l=d.unit/4, lftlabel='$K$'))
    C = d.add(logic.Line('down', xy=J.in1, toy=K.in3))
    d.add(logic.Dot(xy=C.center))
    d.add(logic.Line('left', xy=C.center, l=d.unit/4, lftlabel='$CLK$'))
    d.draw()



S-R Latch (Gates)
^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    d.add(logic.Line(l=d.unit/4, lftlabel='$R$'))
    G1 = d.add(logic.Nor(anchor='in1'))
    d.add(logic.Line(l=d.unit/4))
    Q = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/4, rgtlabel='$Q$'))

    G2 = d.add(logic.Nor(anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5]))
    d.add(logic.Line(l=d.unit/4))
    Qb = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/4, rgtlabel='$\overline{Q}$'))
    S1 = d.add(logic.Line('up', xy=G2.in1, l=d.unit/6))
    d.add(logic.Line('down', xy=Q.start, l=d.unit/6))
    d.add(logic.Line(to=S1.end))
    R1 = d.add(logic.Line('down', xy=G1.in2, l=d.unit/6))
    d.add(logic.Line('up', xy=Qb.start, l=d.unit/6))
    d.add(logic.Line(to=R1.end))
    d.add(logic.Line('left', xy=G2.in2, l=d.unit/4, lftlabel='$S$'))
    d.draw()



Solid State
-----------

S-R Latch (Transistors)
^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    Q1 = d.add(elm.BJT_NPN_C, reverse=True, lftlabel='Q1')
    Q2 = d.add(elm.BJT_NPN_C, xy=[d.unit*1.5, 0], label='Q2')
    d.add(elm.LINE, xy=Q1.collector, d='up', l=d.unit/2)

    R1 = d.add(elm.RES, d='up', label='R1', move_cur=False)
    d.add(elm.DOT, lftlabel='V1')
    d.add(elm.RES, d='right', botlabel='R3', l=d.unit*.75)
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='up', l=d.unit/8)
    d.add(elm.DOT_OPEN, label='Set')
    d.pop()
    d.add(elm.LINE, to=Q2.base)

    d.add(elm.LINE, xy=Q2.collector, d='up', l=d.unit/2)
    d.add(elm.DOT, rgtlabel='V2')
    R2 = d.add(elm.RES, d='up', botlabel='R2', move_cur=False)
    d.add(elm.RES, d='left', botlabel='R4', l=d.unit*.75)
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='up', l=d.unit/8)
    d.add(elm.DOT_OPEN, label='Reset')
    d.pop()
    d.add(elm.LINE, to=Q1.base)

    d.add(elm.LINE, xy=Q1.emitter, d='down', l=d.unit/4)
    BOT = d.add(elm.LINE, d='right', tox=Q2.emitter)
    d.add(elm.LINE, to=Q2.emitter)
    d.add(elm.DOT, xy=BOT.center)
    d.add(elm.GND, xy=BOT.center)

    TOP = d.add(elm.LINE, endpts=[R1.end,R2.end])
    d.add(elm.DOT, xy=TOP.center)
    d.add(elm.LINE, xy=TOP.center, d='up', l=d.unit/8, rgtlabel='Vcc')
    d.draw()


741 Opamp Internal Schematic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(fontsize=12, unit=2.5)
    Q1 = d.add(elm.BjtNpn(label='Q1', lftlabel='+IN'))
    Q3 = d.add(elm.BjtPnp('l', xy=Q1.emitter, anchor='emitter', lftlabel='Q3', flip=True))
    d.add(elm.Line('d', xy=Q3.collector))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Line('r', l=d.unit/4))
    Q7 = d.add(elm.BjtPnp(anchor='base', label='Q7'))
    d.pop()
    d.add(elm.Line('d', l=d.unit*1.25))
    Q5 = d.add(elm.BjtNpn('l', anchor='collector', flip=True, lftlabel='Q5'))
    d.add(elm.Line('l', xy=Q5.emitter, l=d.unit/2, lftlabel='OFST\nNULL', move_cur=False))
    d.add(elm.Resistor('d', xy=Q5.emitter, label='R1\n1K'))
    d.add(elm.Line('r', l=d.unit*.75))
    d.add(elm.Dot)
    R3 = d.add(elm.Resistor('u', label='R3\n50K'))
    d.add(elm.Line(toy=Q5.base))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Line('l', to=Q5.base))
    d.add(elm.Line('d', xy=Q7.emitter, toy=Q5.base))
    d.add(elm.DOT)
    d.pop()
    d.add(elm.Line('right', l=d.unit/4))
    Q6 = d.add(elm.BjtNpn(anchor='base', label='Q6'))
    d.add(elm.Line(xy=Q6.emitter, l=d.unit/3, rgtlabel='\nOFST\nNULL', move_cur=False))
    d.add(elm.Resistor('d', xy=Q6.emitter, label='R2\n1K'))
    d.add(elm.Dot)
    
    d.add(elm.Line('u', xy=Q6.collector, toy=Q3.collector))
    Q4 = d.add(elm.BjtPnp('r', anchor='collector', label='Q4'))
    d.add(elm.Line('l', xy=Q4.base, tox=Q3.base))
    d.add(elm.Line('u', xy=Q4.emitter, toy=Q1.emitter))
    Q2 = d.add(elm.BjtNpn('l', anchor='emitter', flip=True, lftlabel='Q2', rgtlabel='$-$IN'))
    d.add(elm.Line('u', xy=Q2.collector, l=d.unit/3))
    d.add(elm.Dot)
    Q8 = d.add(elm.BjtPnp('l', lftlabel='Q8', anchor='base', flip=True))
    d.add(elm.Line('d', xy=Q8.collector, toy=Q2.collector))
    d.add(elm.Dot)
    d.add(elm.Line('l', xy=Q2.collector, tox=Q1.collector))
    d.add(elm.Line('u', xy=Q8.emitter, l=d.unit/4))
    top = d.add(elm.Line('l', tox=Q7.collector))
    d.add(elm.Line('d', toy=Q7.collector))

    d.add(elm.Line('r', xy=top.start, l=d.unit*2))
    d.add(elm.Line('d', l=d.unit/4))
    Q9 = d.add(elm.BjtPnp('r', anchor='emitter', label='Q9', lblofst=-.1))
    d.add(elm.Line('l', xy=Q9.base, tox=Q8.base))
    d.add(elm.Dot(xy=Q4.base))
    d.add(elm.Line('d', xy=Q4.base, l=d.unit/2))
    d.add(elm.Line('r', tox=Q9.collector))
    d.add(elm.Dot)
    d.add(elm.Line('d', xy=Q9.collector, toy=Q6.collector))
    Q10 = d.add(elm.BjtNpn('l', anchor='collector', flip=True, lftlabel='Q10'))
    d.add(elm.Resistor('d', xy=Q10.emitter, toy=R3.start, label='R4\n5K'))
    d.add(elm.Dot)

    Q11 = d.add(elm.BjtNpn('r', xy=Q10.base, anchor='base', label='Q11'))
    d.add(elm.Dot(xy=Q11.base))
    d.add(elm.Line('u', l=d.unit/2))
    d.add(elm.Line('r', tox=Q11.collector))
    d.add(elm.Dot)
    d.add(elm.Line('d', xy=Q11.emitter, toy=R3.start))
    d.add(elm.Dot)
    d.add(elm.Line('u', xy=Q11.collector, l=d.unit*2))
    d.add(elm.Resistor(toy=Q9.collector, botlabel='R5\n39K'))
    Q12 = d.add(elm.BjtPnp('l', anchor='collector', flip=True, lftlabel='Q12', lblofst=-.1))
    d.add(elm.Line('u', xy=Q12.emitter, l=d.unit/4))
    d.add(elm.Dot)
    d.add(elm.Line('l', tox=Q9.emitter))
    d.add(elm.Dot)
    d.add(elm.Line('r', xy=Q12.base, l=d.unit/4))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Line('d', toy=Q12.collector))
    d.add(elm.Line('l', tox=Q12.collector))
    d.add(elm.Dot)
    d.pop()
    d.add(elm.Line('r', l=d.unit*1.5))
    Q13 = d.add(elm.BjtPnp(anchor='base', label='Q13'))
    d.add(elm.Line('u', l=d.unit/4))
    d.add(elm.Dot)
    d.add(elm.Line('l', tox=Q12.emitter))
    K = d.add(elm.Line('d', xy=Q13.collector, l=d.unit/5))
    d.add(elm.Dot)
    d.add(elm.Line('d'))
    Q16 = d.add(elm.BjtNpn('r', anchor='collector', label='Q16', lblofst=-.1))
    d.add(elm.Line('l', xy=Q16.base, l=d.unit/3))
    d.add(elm.Dot)
    R7 = d.add(elm.Resistor('u', toy=K.end, label='R7\n4.5K'))
    d.add(elm.Dot)
    d.add(elm.Line('r', tox=Q13.collector, move_cur=False))
    R8 = d.add(elm.Resistor('d', xy=R7.start, label='R8\n7.5K'))
    d.add(elm.Dot)
    d.add(elm.Line('r', tox=Q16.emitter))
    J = d.add(elm.Dot)
    d.add(elm.Line('u', toy=Q16.emitter))
    Q15 = d.add(elm.BjtNpn('r', anchor='collector', xy=R8.end, label='Q15'))
    d.add(elm.Line('l', xy=Q15.base, l=d.unit/2))
    d.add(elm.Dot)
    C1 = d.add(elm.Capacitor('u', toy=R7.end, label='C1\n30pF'))
    d.add(elm.Line('r', tox=Q13.collector))
    d.add(elm.Line('l', xy=C1.start, tox=Q6.collector))
    d.add(elm.Dot)
    d.add(elm.Line('d', xy=J.center, l=d.unit/2))
    Q19 = d.add(elm.BjtNpn('r', anchor='collector', label='Q19'))
    d.add(elm.Line('l', xy=Q19.base, tox=Q15.emitter))
    d.add(elm.Dot)
    d.add(elm.Line('u', toy=Q15.emitter, move_cur=False))
    d.add(elm.Line('d', xy=Q19.emitter, l=d.unit/4))
    d.add(elm.Dot)
    d.add(elm.Line('left'))
    Q22 = d.add(elm.BjtNpn('l', anchor='base', flip=True, lftlabel='Q22'))
    d.add(elm.Line('u', xy=Q22.collector, toy=Q15.base))
    d.add(elm.Dot)
    d.add(elm.Line('d', xy=Q22.emitter, toy=R3.start))
    d.add(elm.Dot)
    d.add(elm.Line('l', tox=R3.start, move_cur=False))
    d.add(elm.Line('r', tox=Q15.emitter))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Resistor('u', label='R12\n50K'))
    d.add(elm.Line(toy=Q19.base))
    d.pop()
    d.add(elm.Line(tox=Q19.emitter))
    d.add(elm.Dot)
    R11 = d.add(elm.Resistor('u', label='R11\n50'))
    d.add(elm.Line(toy=Q19.emitter))

    d.add(elm.Line('u', xy=Q13.emitter, l=d.unit/4))
    d.add(elm.Line('r', l=d.unit*1.5))
    d.add(elm.Dot)
    d.add(elm.Line(l=d.unit/4, rgtlabel='V+', move_cur=False))
    d.add(elm.Line('d', l=d.unit*.75))
    Q14 = d.add(elm.BjtNpn('r', anchor='collector', label='Q14'))
    d.add(elm.Line('l', xy=Q14.base, l=d.unit/2))
    d.push()
    d.add(elm.Dot)
    d.add(elm.Line('d', l=d.unit/2))
    Q17 = d.add(elm.BjtNpn('l', anchor='collector', flip=True, lftlabel='Q17', lblofst=-.1))
    d.add(elm.Line('r', xy=Q17.base, tox=Q14.emitter))
    d.add(elm.Dot)
    J = d.add(elm.Line('u', toy=Q14.emitter))
    d.pop()
    d.add(elm.Line(tox=Q13.collector))
    d.add(elm.Dot)
    d.add(elm.Resistor('d', xy=J.start, label='R9\n25'))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Line('l', tox=Q17.emitter))
    d.add(elm.Line('u', toy=Q17.emitter))
    d.pop()
    d.add(elm.Line('d', l=d.unit/4))
    d.add(elm.Dot)
    d.add(elm.Line('r', l=d.unit/4, rgtlabel='OUT', move_cur=False))
    d.add(elm.Resistor('d', label='R10\n50'))
    Q20 = d.add(elm.BjtPnp(d='r', anchor='emitter', label='Q20'))
    d.add(elm.Line('l', xy=Q20.base, l=d.unit/2))
    d.add(elm.Line('u', toy=Q15.collector))
    d.add(elm.Line('l', tox=Q15.collector))
    d.add(elm.Dot)
    d.add(elm.Line('d', xy=Q20.collector, toy=R3.start))
    d.add(elm.Dot)
    d.add(elm.Line('r', l=d.unit/4, rgtlabel='V-', move_cur=False))
    d.add(elm.Line('l', tox=R11.start))
    d.draw()


555 LED Blinker Circuit
^^^^^^^^^^^^^^^^^^^^^^^

Using the `IC` function to generate a custom IC.

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    IC555def = elm.Ic(pins=[elm.IcPin(name='TRG', side='left', pin='2'),
                            elm.IcPin(name='THR', side='left', pin='6'),
                            elm.IcPin(name='DIS', side='left', pin='7'),
                            elm.IcPin(name='CTL', side='right', pin='5'),
                            elm.IcPin(name='OUT', side='right', pin='3'),
                            elm.IcPin(name='RST', side='top', pin='4'),
                            elm.IcPin(name='Vcc', side='top', pin='8'),
                            elm.IcPin(name='GND', side='bot', pin='1'),],
                       edgepadW=.5,
                       edgepadH=1,
                       pinspacing=2,
                       leadlen=1,
                       label='555')
    T = d.add(IC555def)
    BOT = d.add(elm.Ground(xy=T.GND))
    d.add(elm.Dot)
    d.add(elm.Resistor(endpts=[T.DIS, T.THR], label='Rb'))
    d.add(elm.Resistor('u', xy=T.DIS, label='Ra', rgtlabel='+Vcc'))
    d.add(elm.Line(endpts=[T.THR, T.TRG]))
    d.add(elm.Capacitor('d', xy=T.TRG, toy=BOT.start, label='C', l=d.unit/2))
    d.add(elm.Line('r', tox=BOT.start))
    d.add(elm.Capacitor('d', xy=T.CTL, toy=BOT.start, botlabel='.01$\mu$F'))
    d.add(elm.Dot(xy=T.DIS))
    d.add(elm.Dot(xy=T.THR))
    d.add(elm.Dot(xy=T.TRG))
    d.add(elm.Line(endpts=[T.RST,T.Vcc]))
    d.add(elm.Dot)
    d.add(elm.Line('u', l=d.unit/4, rgtlabel='+Vcc'))
    d.add(elm.Resistor('r', xy=T.OUT, label='330'))
    d.add(elm.LED(flip=True, d='down', toy=BOT.start))
    d.add(elm.Line('l', tox=BOT.start))
    d.draw()


Signal Processing
-----------------

Signal processing elements are in the :py:mod:`schemdraw.dsp` module.

.. code-block:: python

    from schemdraw import dsp


Various Networks
^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    d.add(dsp.Line(l=d.unit/3, label='in'))
    inpt = d.add(dsp.Dot)
    d.add(dsp.Arrow(l=d.unit/3))
    delay = d.add(dsp.Box(w=2, h=2, label='Delay\nT', anchor='W'))
    d.add(dsp.Arrow('right', l=d.unit/2, xy=delay.E))
    sm = d.add(dsp.SumSigma)
    d.add(dsp.Arrow(xy=sm.E, l=d.unit/2))
    intg = d.add(dsp.Box(w=2, h=2, label='$\int$', anchor='W'))
    d.add(dsp.Line('r', xy=intg.E, l=d.unit/2))
    d.add(dsp.Arrowhead(label='out'))
    d.add(dsp.Line('down', xy=inpt.center, l=d.unit/2))
    d.add(dsp.Line('right', tox=sm.S))
    d.add(dsp.Line('up', toy=sm.S))
    d.add(dsp.Arrowhead(botlabel='+'))
    d.draw()


.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(fontsize=14)
    d.add(dsp.Line(l=d.unit/2, label='F(s)'))
    d.push()
    d.add(dsp.Dot)
    d.add(dsp.Line('up', l=d.unit/2))
    d.add(dsp.Arrow('right', l=d.unit/2))
    h1 = d.add(dsp.Box(w=2, h=2, label='$H_1(s)$', anchor='W'))
    d.pop()
    d.add(dsp.Line('down', l=d.unit/2))
    d.add(dsp.Arrow('right', l=d.unit/2))
    h2 = d.add(dsp.Box(w=2, h=2, label='$H_2(s)$', anchor='W'))
    sm = d.add(dsp.SumSigma('right', xy=[h1.E[0] + d.unit/2, 0], anchor='center'))
    d.add(dsp.Line('right', xy=h1.E, tox=sm.N))
    d.add(dsp.Arrow('down', toy=sm.N))
    d.add(dsp.Line('right', xy=h2.E, tox=sm.S))
    d.add(dsp.Arrow('up', toy=sm.S))
    d.add(dsp.Line('right', xy=sm.E, l=d.unit/3))
    d.add(dsp.Arrowhead(label='Y(s)'))
    d.draw()


Superheterodyne Receiver
^^^^^^^^^^^^^^^^^^^^^^^^

`Source <https://www.electronicdesign.com/adc/high-speed-rf-sampling-adc-boosts-bandwidth-dynamic-range>`_.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(fontsize=12)
    d.add(dsp.Antenna)
    d.add(dsp.Line('right', l=d.unit/4))
    filt1 = d.add(dsp.Filter(response='bp', botlabel='RF filter\n#1', anchor='W', lblofst=.2, fill='thistle'))
    d.add(dsp.Line(xy=filt1.E, l=d.unit/4))
    d.add(dsp.Amp(label='LNA', fill='lightblue'))
    d.add(dsp.Line(l=d.unit/4))
    filt2 = d.add(dsp.Filter(response='bp', botlabel='RF filter\n#2', anchor='W', lblofst=.2, fill='thistle'))
    d.add(dsp.Line('right', xy=filt2.E, l=d.unit/3))
    mix = d.add(dsp.Mixer(label='Mixer', fill='navajowhite'))
    d.add(dsp.Line('down', xy=mix.S, l=d.unit/3))
    d.add(dsp.Oscillator('right', rgtlabel='Local\nOscillator', lblofst=.2, anchor='N', fill='navajowhite'))
    d.add(dsp.Line('right', xy=mix.E, l=d.unit/3))
    filtIF = d.add(dsp.Filter(response='bp', anchor='W', botlabel='IF filter', lblofst=.2, fill='thistle'))
    d.add(dsp.Line('right', xy=filtIF.E, l=d.unit/4))
    d.add(dsp.Amp(label='IF\namplifier', fill='lightblue'))
    d.add(dsp.Line(l=d.unit/4))
    demod = d.add(dsp.Demod(anchor='W', botlabel='Demodulator', lblofst=.2, fill='navajowhite'))
    d.add(dsp.Arrow('right', xy=demod.E, l=d.unit/3))
    d.draw()

Direct Conversion Receiver
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    d.add(dsp.Antenna)
    d.add(dsp.Arrow('right', l=d.unit/2, botlabel='$f_{RF}$'))
    d.add(dsp.Amp(label='LNA'))
    d.add(dsp.Line('right', l=d.unit/5))
    d.add(dsp.Dot)
    d.push()
    d.add(dsp.Line(l=d.unit/4))
    mix1 = d.add(dsp.Mixer(label='Mixer', lblofst=0))
    d.add(dsp.Arrow(l=d.unit/2))
    lpf1 = d.add(dsp.Filter(response='lp', botlabel='LPF', lblofst=.2))
    d.add(dsp.Line(l=d.unit/6))
    adc1 = d.add(dsp.Adc(label='ADC'))
    d.add(dsp.Arrow(l=d.unit/3))
    dsp1 = d.add(dsp.Ic(pins=[dsp.IcPin(side='L'), dsp.IcPin(side='L'), dsp.IcPin(side='R')],
                        size=(2.75, 5), leadlen=0, anchor='inL2', label='DSP'))
    d.add(dsp.Arrow(xy=dsp1.inR1, l=d.unit/3))
    d.pop()

    d.add(dsp.Line('down', toy=dsp1.inL1))
    d.add(dsp.Arrow('right', tox=mix1.W))
    mix2 = d.add(dsp.Mixer(label='Mixer', lblofst=0))
    d.add(dsp.Arrow(tox=lpf1.W))
    d.add(dsp.Filter(response='lp', botlabel='LPF', lblofst=.2))
    d.add(dsp.Line(tox=adc1.W))
    d.add(dsp.Adc(label='ADC'))
    d.add(dsp.Arrow(to=dsp1.inL1))

    d.add(dsp.Arrowhead(xy=mix1.S, d='up'))
    d.add(dsp.Line('down', xy=mix1.S, l=d.unit/6))
    d.add(dsp.Line('left', l=d.unit*1.25))
    d.add(dsp.Line('down', l=d.unit*.75))
    flo = d.add(dsp.Dot(lftlabel='$f_{LO}$'))
    d.push()
    d.add(dsp.Line('down', l=d.unit/5))
    d.add(dsp.Oscillator('right', rgtlabel='LO', anchor='N', lblofst=.15))
    d.pop()
    d.add(dsp.Arrowhead('up', xy=mix2.S))
    d.add(dsp.Line('down', xy=mix2.S, l=d.unit/4))
    b1 = d.add(dsp.Square('right', label='90°', anchor='N'))
    d.add(dsp.Arrowhead('right', xy=b1.W))
    d.add(dsp.Line('left', xy=b1.W, l=d.unit/4))
    d.add(dsp.Line('up', toy=flo.center))
    d.add(dsp.Line('left', tox=flo.center))
    d.draw()


Digital Filter
^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=1, fontsize=14)
    d.add(dsp.Line(lftlabel='x[n]', l=d.unit*2))
    d.add(dsp.Dot)

    d.push()
    d.add(dsp.Line('right'))
    d.add(dsp.Amp(botlabel='$b_0$'))
    d.add(dsp.ARROW)
    s0 = d.add(dsp.Sum(anchor='W'))
    d.pop()

    d.add(dsp.Arrow('down'))
    z1 = d.add(dsp.Square(label='$z^{-1}$'))
    d.add(dsp.Line(l=d.unit/2))
    d.add(dsp.DOT)

    d.push()
    d.add(dsp.Line('right'))
    d.add(dsp.Amp(botlabel='$b_1$'))
    d.add(dsp.Arrow)
    s1 = d.add(dsp.Sum(anchor='W'))
    d.pop()

    d.add(dsp.Arrow('down', l=d.unit*.75))
    d.add(dsp.Square(label='$z^{-1}$'))
    d.add(dsp.Line(l=d.unit*.75))
    d.add(dsp.Line('right'))
    d.add(dsp.Amp(botlabel='$b_2$'))
    d.add(dsp.Arrow)
    s2 = d.add(dsp.Sum(anchor='W'))

    d.add(dsp.Arrow('up', xy=s2.N, toy=s1.S))
    d.add(dsp.Arrow('up', xy=s1.N, toy=s0.S))

    d.add(dsp.LineDot('right', xy=s0.E, l=d.unit*2.75))
    d.push()
    d.add(dsp.Arrow('right', rgtlabel='y[n]'))
    d.pop()
    d.add(dsp.Arrow('down'))
    d.add(dsp.Square(label='$z^{-1}$'))
    d.add(dsp.Line(l=d.unit/2))
    d.add(dsp.Dot)
    d.push()
    d.add(dsp.Line('left'))
    a1 = d.add(dsp.Amp(botlabel='$-a_1$'))
    d.add(dsp.Arrow(xy=a1.out, tox=s1.E))
    d.pop()

    d.add(dsp.Arrow('down', l=d.unit*.75))
    d.add(dsp.Square(label='$z^{-1}$'))
    d.add(dsp.Line(l=d.unit*.75))
    d.add(dsp.Line('left'))
    a1 = d.add(dsp.Amp(botlabel='$-a_2$'))
    d.add(dsp.Arrow(xy=a1.out, tox=s2.E))
    d.draw()



.. _galleryflow:

Flowcharting
------------

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
    d.add(flow.Line('left', tox=h.E))
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


Styles
------

Circuit elements can be styled using Matplotlib colors, line-styles, and line widths.

Resistor circle
^^^^^^^^^^^^^^^

Uses named colors in a loop.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    for i, color in enumerate(['red', 'orange', 'yellow', 'yellowgreen', 'green', 'blue', 'indigo', 'violet']):
        d.add(elm.Resistor(label='R{}'.format(i), theta=45*i+20, color=color))
    d.draw()


Hand-drawn
^^^^^^^^^^

And for a change of pace, activate Matplotlib's XKCD mode for "hand-drawn" look!

.. jupyter-execute::
    :code-below:

    import matplotlib.pyplot as plt
    plt.xkcd()

    d = schemdraw.Drawing(inches_per_unit=.5)
    op = d.add(elm.Opamp)
    d.add(elm.Line('left', xy=op.in2, l=d.unit/4))
    d.add(elm.Line('down', l=d.unit/5))
    d.add(elm.Ground)
    d.add(elm.Line('left', xy=op.in1, l=d.unit/6))
    d.add(elm.Dot)
    d.push()
    Rin = d.add(elm.Resistor('left', xy=op.in1-[d.unit/5,0], botlabel='$R_{in}$', lftlabel='$v_{in}$'))
    d.pop()
    d.add(elm.Line('up', l=d.unit/2))
    Rf = d.add(elm.Resistor('right', l=d.unit*1, label='$R_f$'))
    d.add(elm.Line('down', toy=op.out))
    d.add(elm.Dot)
    d.add(elm.Line('left', tox=op.out))
    d.add(elm.Line('right', l=d.unit/4, rgtlabel='$v_{o}$'))
    d.draw()
