Circuit Gallery
===============

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import SchemDraw
    from SchemDraw import elements as elm
    from SchemDraw import logic
    from SchemDraw import dsp
    from SchemDraw import flow


Analog Circuits
---------------

Discharging capacitor
^^^^^^^^^^^^^^^^^^^^^

Shows how to connect to a switch with anchors.

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    V1 = d.add(elm.SOURCE_V, label='5V')
    d.add(elm.LINE, d='right', l=d.unit*.75)
    S1 = d.add(elm.SWITCH_SPDT2_CLOSE, d='up', anchor='b', rgtlabel='$t=0$')
    d.add(elm.LINE, d='right', xy=S1.c,  l=d.unit*.75)
    d.add(elm.RES, d='down', label='$100\Omega$', botlabel=['+','$v_o$','-'])
    d.add(elm.LINE, to=V1.start)
    d.add(elm.CAP, xy=S1.a, d='down', toy=V1.start, label='1$\mu$F')
    d.add(elm.DOT)
    d.draw()


Capacitor Network
^^^^^^^^^^^^^^^^^

Shows how to use endpoints to specify exact start and end placement.

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing()
    A  = d.add(elm.DOT, label='a')
    C1 = d.add(elm.CAP, label='8nF')
    C2 = d.add(elm.CAP, label='18nF')
    C3 = d.add(elm.CAP, botlabel='8nF', d='down')
    C4 = d.add(elm.CAP, botlabel='32nF', d='left')
    C5 = d.add(elm.CAP, botlabel='40nF')
    B  = d.add(elm.DOT, label='b')
    C6 = d.add(elm.CAP, label='2.8nF', endpts=[C1.end,C5.start])
    C7 = d.add(elm.CAP, endpts=[C2.end,C5.start])
    C7.add_label('5.6nF', loc='center', ofst=[-.3,-.1], align=('right','bottom'))
    d.draw()



ECE201-Style Circuit
^^^^^^^^^^^^^^^^^^^^

This example demonstrate use of `push()` and `pop()` and using the 'tox' and 'toy' keywords.

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing(unit=2)  # unit=2 makes elements have shorter than normal leads
    d.push()
    R1 = d.add(elm.RES, d='down', label='20$\Omega$')
    V1 = d.add(elm.SOURCE_V, d='down', reverse=True, label='120V')
    d.add(elm.LINE, d='right', l=3)
    d.add(elm.DOT)
    d.pop()
    d.add(elm.LINE, d='right', l=3)
    d.add(elm.DOT)
    d.add(elm.SOURCE_V, d='down', label='60V', reverse=True)
    d.add(elm.RES, label='5$\Omega$')
    d.add(elm.DOT)
    d.add(elm.LINE, d='right', l=3)
    d.add(elm.SOURCE_I, d='up', label='36A')
    d.add(elm.RES, label='10$\Omega$')
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', l=3, move_cur=False)
    d.add(elm.LINE, d='right', l=3)
    d.add(elm.DOT)
    R6 = d.add(elm.RES, d='down', toy=V1.end, label='6$\Omega$')
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', l=3, move_cur=False)
    d.add(elm.RES, d='right', xy=R6.start, label='1.6$\Omega$')
    d.add(elm.DOT, label='a')
    d.add(elm.LINE, d='right', xy=R6.end)
    d.add(elm.DOT, label='b')
    d.draw()


Loop Currents
^^^^^^^^^^^^^

Using the :py:meth:`Drawing.loopI` method to add loop currents, and rotating a label to make it fit.

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing(unit=5)
    V1 = d.add(elm.SOURCE_V, label='$20V$')
    R1 = d.add(elm.RES, d='right', label='400$\Omega$')
    d.add(elm.DOT)
    d.push()
    R2 = d.add(elm.RES, d='down', botlabel='100$\Omega$', lblrotate=True)
    d.add(elm.DOT)
    d.pop()
    L1 = d.add(elm.LINE)
    I1 = d.add(elm.SOURCE_I, d='down', botlabel='1A')
    L2 = d.add(elm.LINE, d='left', tox=V1.start)
    d.loopI([R1,R2,L2,V1], '$I_1$', pad=1.25)
    d.loopI([R1,I1,L2,R2], '$I_2$', pad=1.25)  # Use R1 as top element for both so they get the same height
    d.draw()


AC Loop Analysis
^^^^^^^^^^^^^^^^

Another good problem for ECE students...

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    I1 = d.add(elm.SOURCE_I, label=r'$5\angle 0^{\circ}$A')
    d.add(elm.DOT)
    d.push()
    d.add(elm.CAP, d='right', label=r'$-j3\Omega$')
    d.add(elm.DOT)
    d.push()
    d.add(elm.INDUCTOR, d='down', label=r'$j2\Omega$')
    d.add(elm.DOT)
    d.pop()
    d.add(elm.RES, d='right', label=r'$5\Omega$')
    d.add(elm.DOT)
    V1 = d.add(elm.SOURCE_V, d='down', reverse=True, botlabel=r'$5\angle -90^{\circ}$V')
    d.add(elm.LINE, d='left', tox=I1.start)
    d.pop()
    d.add(elm.LINE, d='up', l=d.unit*.8)
    L1 = d.add(elm.INDUCTOR, d='right', label=r'$j3\Omega$', tox=V1.start)
    d.add(elm.LINE, d='down', l=d.unit*.8)
    d.labelI(L1, '$i_g$', top=False)
    d.draw()

Infinite Transmission Line
^^^^^^^^^^^^^^^^^^^^^^^^^^

Elements can be added inside for-loops if you need multiples.
The ellipsis is just another circuit element.
This also demonstrates the :py:func:`group_elements` function to merge multiple elements into a single definition.

.. jupyter-execute::
    :code-below:
    
    d1 = SchemDraw.Drawing()
    d1.add(elm.RES)
    d1.push()
    d1.add(elm.CAP, d='down')
    d1.add(elm.LINE, d='left')
    d1.pop()
    RC = SchemDraw.group_elements(d1)

    d2 = SchemDraw.Drawing()
    for i in range(3):
        d2.add(RC)

    d2.push()
    d2.add(elm.LINE, l=d2.unit/6)
    d2.add(elm.ELLIPSIS)
    d2.add(RC)
    d2.pop()
    d2.here = [d2.here[0], d2.here[1]-d2.unit]
    d2.add(elm.LINE, d='right', l=d2.unit/6)
    d2.add(elm.ELLIPSIS)
    d2.draw()


Power supply
^^^^^^^^^^^^

Notice the diodes added with the `theta` parameter to point them in the right directions.
Also the use of newline characters inside resistor and capacitor labels.

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing(inches_per_unit=.5, unit=3)
    D1 = d.add(elm.DIODE, theta=-45)
    d.add(elm.DOT)
    D2 = d.add(elm.DIODE, theta=225, reverse=True)
    d.add(elm.DOT)
    D3 = d.add(elm.DIODE, theta=135, reverse=True)
    d.add(elm.DOT)
    D4 = d.add(elm.DIODE, theta=45)
    d.add(elm.DOT)

    d.add(elm.LINE, xy=D3.end, d='left', l=d.unit/2)
    d.add(elm.DOT_OPEN)
    G = d.add(elm.GAP, d='up', toy=D1.start, label='AC IN')
    d.add(elm.LINE, xy=D4.end, d='left', tox=G.start)
    d.add(elm.DOT_OPEN)

    top = d.add(elm.LINE, xy=D2.end, d='right', l=d.unit*3)
    Q2 = d.add(elm.BJT_NPN_C, anchor='collector', d='up', label='Q2\n2n3055')
    d.add(elm.LINE, xy=Q2.base, d='down', l=d.unit/2)
    Q2b = d.add(elm.DOT)
    d.add(elm.LINE, d='left', l=d.unit/3)
    Q1 = d.add(elm.BJT_NPN_C, anchor='emitter', d='up', label='Q1\n    2n3054')
    d.add(elm.LINE, d='up', xy=Q1.collector, toy=top.center)
    d.add(elm.DOT)

    d.add(elm.LINE, d='down', xy=Q1.base, l=d.unit/2)
    d.add(elm.DOT)
    d.add(elm.ZENER, d='down', reverse=True, botlabel='D2\n500mA')
    d.add(elm.DOT)
    G = d.add(elm.GND)
    d.add(elm.LINE, d='left')
    d.add(elm.DOT)
    d.add(elm.CAP_P, botlabel='C2\n100$\mu$F\n50V', d='up', reverse=True)
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='right')
    d.pop()
    d.add(elm.RES, d='up', toy=top.end, botlabel='R1\n2.2K\n50V')
    d.add(elm.DOT)

    d.here = [d.here[0]-d.unit, d.here[1]]
    d.add(elm.DOT)
    d.add(elm.CAP_P, d='down', toy=G.start, label='C1\n 1000$\mu$F\n50V', flip=True)
    d.add(elm.DOT)
    d.add(elm.LINE, xy=G.start, tox=D4.start, d='left')
    d.add(elm.LINE, d='up', toy=D4.start)

    d.add(elm.RES, d='right', xy=Q2b.center, label='R2', botlabel='56$\Omega$ 1W')
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='up', toy=top.start)
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', tox=Q2.emitter)
    d.pop()
    d.add(elm.CAP_P, d='down', toy=G.start, botlabel='C3\n470$\mu$F\n50V')
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', tox=G.start, move_cur=False)
    d.add(elm.LINE, d='right')
    d.add(elm.DOT)
    d.add(elm.RES, d='up', toy=top.center, botlabel='R3\n10K\n1W')
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', move_cur=False)
    d.add(elm.LINE, d='right')
    d.add(elm.DOT_OPEN)
    d.add(elm.GAP, d='down', toy=G.start, label='$V_{out}$')
    d.add(elm.DOT_OPEN)
    d.add(elm.LINE, d='left')
    d.draw()


Opamp Circuits
--------------

Inverting Opamp
^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    op = d.add(elm.OPAMP)
    d.add(elm.LINE, d='left', xy=op.in2, l=d.unit/4)
    d.add(elm.LINE, d='down', l=d.unit/5)
    d.add(elm.GND)
    d.add(elm.LINE, d='left', xy=op.in1, l=d.unit/6)
    d.add(elm.DOT)
    d.push()
    Rin = d.add(elm.RES, d='left', xy=op.in1-[d.unit/5,0], botlabel='$R_{in}$', lftlabel='$v_{in}$')
    d.pop()
    d.add(elm.LINE, d='up', l=d.unit/2)
    Rf = d.add(elm.RES,  d='right', l=d.unit*1, label='$R_f$')
    d.add(elm.LINE, d='down', toy=op.out)
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', tox=op.out)
    d.add(elm.LINE, d='right', l=d.unit/4, rgtlabel='$v_{o}$')
    d.draw()


Non-inverting Opamp
^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing()
    op = d.add(elm.OPAMP)
    d.add(elm.LINE, xy=op.out, l=.75)
    d.add(elm.LINE, xy=op.in1, d='left', l=.75)
    d.add(elm.LINE, d='up', l=1.5)
    d.add(elm.DOT)
    R1 = d.add(elm.RES, d='left', label='$R_1$')
    d.add(elm.GND)
    Rf = d.add(elm.RES, d='right', xy=R1.start, tox=op.out+.5, label='$R_f$')
    d.add(elm.LINE, d='down', toy=op.out)
    dot = d.add(elm.DOT)
    d.add(elm.LINE, d='left', xy=op.in2, l=.75)
    d.add(elm.DOT)
    R3 = d.add(elm.RES, d='down', label='$R_3$')
    d.add(elm.DOT)
    d.add(elm.GND)
    R2 = d.add(elm.RES, d='left', xy=R3.start, label='$R_2$')
    d.add(elm.SOURCE_V, d='down', reverse=True, label='$v_{in}$')
    d.add(elm.LINE, d='right', tox=Rf.end)
    d.add(elm.GAP_LABEL, d='down', xy=dot.start, toy=R3.end, label=['+','$v_o$','$-$'])
    d.draw()


Multi-stage amplifier
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    d.add(elm.GND)
    d.add(elm.SOURCE_V, label='$500mV$')

    d.add(elm.RES, d='right', label='20k$\Omega$')
    Vin = d.add(elm.DOT)
    d.add(elm.LINE, l=.5)
    O1 = d.add(elm.OPAMP, anchor='in1')
    d.add(elm.LINE, l=.75, d='left', xy=O1.in2)
    d.add(elm.GND)
    d.add(elm.LINE,xy=Vin.start,d='up',l=2)
    d.add(elm.RES,d='right',label='100k$\Omega$')
    d.add(elm.LINE,d='down',toy=O1.out)
    d.add(elm.DOT)
    d.add(elm.LINE,xy=O1.out,d='right',l=5)
    O2 = d.add(elm.OPAMP, anchor='in2')
    Vin2 = d.add(elm.LINE, l=.5, d='left', xy=O2.in1)
    d.add(elm.DOT)
    d.add(elm.RES, d='left', label='30k$\Omega$')
    d.add(elm.GND)
    d.add(elm.LINE,xy=Vin2.end,d='up',l=1.5)
    d.add(elm.RES,d='right',label='90k$\Omega$')
    d.add(elm.LINE,d='down',toy=O2.out)
    d.add(elm.DOT)
    d.add(elm.LINE, xy=O2.out,d='right',l=1, rgtlabel='$v_{out}$')
    d.draw()


Opamp pin labeling
^^^^^^^^^^^^^^^^^^

This example shows how to label pin numbers on a 741 opamp, and connect to the offset anchors.
Pin labels are somewhat manually placed; without the `ofst` and `align` keywords they
will be drawn directly over the anchor position. Also note the use of the `zoom` keyword
when placing the potentiometer to slightly reduce its size.

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing(fontsize=12)
    op = d.add(elm.OPAMP, label='741', lblloc='center', lblofst=0)
    d.add(elm.LINE, xy=op.in1, d='left', l=.5)
    d.add(elm.LINE, d='down', l=d.unit/2)
    d.add(elm.GND)
    d.add(elm.LINE, xy=op.in2, d='left', l=.5)
    d.add(elm.LINE, xy=op.out, d='right', l=.5, rgtlabel='$V_o$')
    d.add(elm.LINE, xy=op.vd, d='up', l=1, rgtlabel='$+V_s$')
    trim = d.add(elm.POT, xy=op.n1, d='down', flip=True, zoom=.7)
    d.add(elm.LINE, d='right', tox=op.n1a)
    d.add(elm.LINE, d='up', to=op.n1a)
    d.add(elm.LINE, d='left', xy=trim.tap, tox=op.vs)
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='down', l=d.unit/3)
    d.add(elm.GND)
    d.pop()
    d.add(elm.LINE, d='up', toy=op.vs)    
    op.add_label('1', loc='n1', size=9, ofst=[-.1, -.25], align=('right', 'top'))
    op.add_label('5', loc='n1a', size=9, ofst=[-.1, -.25], align=('right', 'top'))
    op.add_label('4', loc='vs', size=9, ofst=[-.1, -.2], align=('right', 'top'))
    op.add_label('7', loc='vd', size=9, ofst=[-.1, .2], align=('right', 'bottom'))
    op.add_label('2', loc='in1', size=9, ofst=[-.1, .1], align=('right', 'bottom'))
    op.add_label('3', loc='in2', size=9, ofst=[-.1, .1], align=('right', 'bottom'))
    op.add_label('6', loc='out', size=9, ofst=[-.1, .1], align=('left', 'bottom'))
    d.draw()


Logic Gates
-----------    

Logic gate definitions are in the :py:mod:`SchemDraw.logic` module. Here it was imported with

.. code-block:: python

    import SchemDraw.logic as l


Half Adder
^^^^^^^^^^

Notice the half and full adders set the drawing unit to 0.5 so the lines aren't quite as long and look better with logic gates.

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing(unit=.5)
    S = d.add(logic.XOR2, rgtlabel='$S$')
    A = d.add(logic.DOT, xy=S.in1)
    d.add(logic.LINE, d='left', l=d.unit*2, lftlabel='$A$')
    d.add(logic.LINE, d='left', xy=S.in2)
    B = d.add(logic.DOT)
    d.add(logic.LINE, d='left', lftlabel='$B$')

    d.add(logic.LINE, d='down', xy=A.start, l=d.unit*3)
    C = d.add(logic.AND2, d='right', anchor='in1', rgtlabel='$C$')
    d.add(logic.LINE, d='down', xy=B.start, toy=C.in2)
    d.add(logic.LINE, to=C.in2)
    d.draw()


Full Adder
^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing(unit=.5)
    X1 = d.add(logic.XOR2)
    d.add(logic.DOT)
    A = d.add(logic.DOT, xy=X1.in1)
    Ain = d.add(logic.LINE, d='left', l=d.unit*2, lftlabel='$A$')
    d.add(logic.LINE, d='left', xy=X1.in2)
    B = d.add(logic.DOT)
    d.add(logic.LINE, d='left', lftlabel='$B$')

    d.add(logic.LINE, xy=X1.out, d='right', l=d.unit)
    X2 = d.add(logic.XOR2, anchor='in1')
    C = d.add(logic.LINE, d='down', xy=X2.in2, l=d.unit*2)
    d.push()
    d.add(logic.DOT, xy=C.center)
    d.add(logic.LINE, d='left', tox=Ain.end, lftlabel='$C_{in}$')
    d.pop()

    A1 = d.add(logic.AND2, d='right', anchor='in1')
    d.add(logic.LINE, d='left', xy=A1.in2, tox=X1.out)
    d.add(logic.LINE, d='up', toy=X1.out)
    A2 = d.add(logic.AND2, d='right', anchor='in1', xy=[A1.in1[0],A1.in2[1]-d.unit*2])
    d.add(logic.LINE, xy=A2.in1, d='left', tox=A.start)
    d.add(logic.LINE, d='up', toy=A.start)
    d.add(logic.LINE, xy=A2.in2, d='left', tox=B.start)
    d.add(logic.LINE, d='up', toy=B.start)

    O1 = d.add(logic.OR2, d='right', xy=[A1.out[0],(A1.out[1]+A2.out[1])/2], rgtlabel='$C_{out}$')
    d.add(logic.LINE, xy=A1.out,d='down', toy=O1.in1)
    d.add(logic.LINE, xy=A2.out,d='up', toy=O1.in2)
    d.add(logic.LINE, xy=X2.out, d='right', tox=O1.out, rgtlabel='$S$')
    d.draw()




J-K Flip Flop
^^^^^^^^^^^^^

Note the use of the LaTeX command **overline{Q}** in the label to draw a bar over the inverting output label.

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    # Two front gates (SR latch)
    G1 = d.add(logic.NAND2, anchor='in1')
    d.add(logic.LINE, l=d.unit/6)
    Q1 = d.add(logic.DOT)
    d.add(logic.LINE, l=d.unit/6)
    Q2 = d.add(logic.DOT)
    d.add(logic.LINE, l=d.unit/3, rgtlabel='$Q$')
    G2 = d.add(logic.NAND2, anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5])
    d.add(logic.LINE, l=d.unit/6)
    Qb = d.add(logic.DOT)
    d.add(logic.LINE, l=d.unit/3)
    Qb2 = d.add(logic.DOT)
    d.add(logic.LINE, l=d.unit/6, rgtlabel='$\overline{Q}$')
    S1 = d.add(logic.LINE, xy=G2.in1, d='up', l=d.unit/6)
    d.add(logic.LINE, d='down', xy=Q1.start, l=d.unit/6)
    d.add(logic.LINE, to=S1.end)
    R1 = d.add(logic.LINE, xy=G1.in2, d='down', l=d.unit/6)
    d.add(logic.LINE, d='up', xy=Qb.start, l=d.unit/6)
    d.add(logic.LINE, to=R1.end)

    # Two back gates
    d.add(logic.LINE, xy=G1.in1, d='left', l=d.unit/6)
    J = d.add(logic.NAND3, anchor='out', reverse=True)
    d.add(logic.LINE, xy=J.in3, d='up', l=d.unit/6)
    d.add(logic.LINE, d='right', tox=Qb2.start)
    d.add(logic.LINE, d='down', toy=Qb2.start)
    d.add(logic.LINE, d='left', xy=J.in2, l=d.unit/4, lftlabel='$J$')
    d.add(logic.LINE, xy=G2.in2, d='left', l=d.unit/6)
    K = d.add(logic.NAND3, anchor='out', reverse=True)
    d.add(logic.LINE, xy=K.in1, d='down', l=d.unit/6)
    d.add(logic.LINE, d='right', tox=Q2.start)
    d.add(logic.LINE, d='up', toy=Q2.start)
    d.add(logic.LINE, d='left', xy=K.in2, l=d.unit/4, lftlabel='$K$')
    C = d.add(logic.LINE, d='down', xy=J.in1, toy=K.in3)
    d.add(logic.DOT, xy=C.center)
    d.add(logic.LINE, d='left', xy=C.center, l=d.unit/4, lftlabel='$CLK$')
    d.draw()


S-R Latch (Gates)
^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    d.add(logic.LINE, l=d.unit/4, lftlabel='$R$')
    G1 = d.add(logic.NOR2, anchor='in1')
    d.add(logic.LINE, l=d.unit/4)
    Q = d.add(logic.DOT)
    d.add(logic.LINE, l=d.unit/4, rgtlabel='$Q$')

    G2 = d.add(logic.NOR2, anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5])
    d.add(logic.LINE, l=d.unit/4)
    Qb = d.add(logic.DOT)
    d.add(logic.LINE, l=d.unit/4, rgtlabel='$\overline{Q}$')
    S1 = d.add(logic.LINE, xy=G2.in1, d='up', l=d.unit/6)
    d.add(logic.LINE, d='down', xy=Q.start, l=d.unit/6)
    d.add(logic.LINE, to=S1.end)
    R1 = d.add(logic.LINE, xy=G1.in2, d='down', l=d.unit/6)
    d.add(logic.LINE, d='up', xy=Qb.start, l=d.unit/6)
    d.add(logic.LINE, to=R1.end)
    d.add(logic.LINE, d='left', xy=G2.in2, l=d.unit/4, lftlabel='$S$')
    d.draw()



Solid State
-----------

S-R Latch (Transistors)
^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing()
    Q1 = d.add(elm.BJT_NPN_C, reverse=True, lftlabel='Q1')
    Q2 = d.add(elm.BJT_NPN_C, xy=[d.unit*2,0], label='Q2')
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

    d = SchemDraw.Drawing(fontsize=12, unit=2.5)
    Q1 = d.add(elm.BJT_NPN, label='Q1', lftlabel='+IN')
    Q3 = d.add(elm.BJT_PNP, xy=Q1.emitter, anchor='emitter', lftlabel='Q3', flip=True, d='left')
    d.add(elm.LINE, d='down', xy=Q3.collector)
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='right', l=d.unit/4)
    Q7 = d.add(elm.BJT_NPN, anchor='base', label='Q7')
    d.pop()
    d.add(elm.LINE, d='down', l=d.unit*1.25)
    Q5 = d.add(elm.BJT_NPN, anchor='collector', d='left', flip=True, lftlabel='Q5')
    d.add(elm.LINE, d='left', xy=Q5.emitter, l=d.unit/2, lftlabel='OFST\nNULL', move_cur=False)
    d.add(elm.RES, d='down', xy=Q5.emitter, label='R1\n1K')
    d.add(elm.LINE, d='right', l=d.unit*.75)
    d.add(elm.DOT)
    R3 = d.add(elm.RES, d='up', label='R3\n50K')
    d.add(elm.LINE, toy=Q5.base)
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='left', to=Q5.base)
    d.add(elm.LINE, xy=Q7.emitter, d='down', toy=Q5.base)
    d.add(elm.DOT)
    d.pop()
    d.add(elm.LINE, d='right', l=d.unit/4)
    Q6 = d.add(elm.BJT_NPN, anchor='base', label='Q6')
    d.add(elm.LINE, xy=Q6.emitter, l=d.unit/3, rgtlabel='\nOFST\nNULL', move_cur=False)
    d.add(elm.RES, xy=Q6.emitter, d='down', label='R2\n1K')
    d.add(elm.DOT)

    d.add(elm.LINE, xy=Q6.collector, d='up', toy=Q3.collector)
    Q4 = d.add(elm.BJT_PNP, anchor='collector', d='right', label='Q4')
    d.add(elm.LINE, xy=Q4.base, d='left', tox=Q3.base)
    d.add(elm.LINE, xy=Q4.emitter, d='up', toy=Q1.emitter)
    Q2 = d.add(elm.BJT_NPN, anchor='emitter', d='left', flip=True, lftlabel='Q2', rgtlabel='$-$IN')
    d.add(elm.LINE, xy=Q2.collector, d='up', l=d.unit/3)
    d.add(elm.DOT)
    Q8 = d.add(elm.BJT_PNP, lftlabel='Q8', anchor='base', d='left', flip=True)
    d.add(elm.LINE, xy=Q8.collector, d='down', toy=Q2.collector)
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', xy=Q2.collector, tox=Q1.collector)
    d.add(elm.LINE, d='up', xy=Q8.emitter, l=d.unit/4)
    top = d.add(elm.LINE, d='left', tox=Q7.collector)
    d.add(elm.LINE, d='down', toy=Q7.collector)

    d.add(elm.LINE, d='right', xy=top.start, l=d.unit*2)
    d.add(elm.LINE, d='down', l=d.unit/4)
    Q9 = d.add(elm.BJT_PNP, anchor='emitter', d='right', label='Q9', lblofst=-.1)
    d.add(elm.LINE, d='left', xy=Q9.base, tox=Q8.base)
    d.add(elm.DOT, xy=Q4.base)
    d.add(elm.LINE, xy=Q4.base, d='down', l=d.unit/2)
    d.add(elm.LINE, d='right', tox=Q9.collector)
    d.add(elm.DOT)
    d.add(elm.LINE, xy=Q9.collector, d='down', toy=Q6.collector)
    Q10 = d.add(elm.BJT_NPN, anchor='collector', d='left', flip=True, lftlabel='Q10')
    d.add(elm.RES, d='down', xy=Q10.emitter, toy=R3.start, label='R4\n5K')
    d.add(elm.DOT)

    Q11 = d.add(elm.BJT_NPN, xy=Q10.base, anchor='base', label='Q11')
    d.add(elm.DOT, xy=Q11.base)
    d.add(elm.LINE, d='up', l=d.unit/2)
    d.add(elm.LINE, d='right', tox=Q11.collector)
    d.add(elm.DOT)
    d.add(elm.LINE, d='down', xy=Q11.emitter, toy=R3.start)
    d.add(elm.DOT)
    d.add(elm.LINE, d='up', xy=Q11.collector, l=d.unit*2)
    d.add(elm.RES, toy=Q9.collector, botlabel='R5\n39K')
    Q12 = d.add(elm.BJT_PNP, anchor='collector', d='left', flip=True, lftlabel='Q12', lblofst=-.1)
    d.add(elm.LINE, d='up', xy=Q12.emitter, l=d.unit/4)
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', tox=Q9.emitter)
    d.add(elm.DOT)
    d.add(elm.LINE, d='right', xy=Q12.base, l=d.unit/4)
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='down', toy=Q12.collector)
    d.add(elm.LINE, d='left', tox=Q12.collector)
    d.add(elm.DOT)
    d.pop()
    d.add(elm.LINE, d='right', l=d.unit*1.5)
    Q13 = d.add(elm.BJT_PNP, anchor='base', label='Q13')
    d.add(elm.LINE, d='up', l=d.unit/4)
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', tox=Q12.emitter)
    K = d.add(elm.LINE, d='down', xy=Q13.collector, l=d.unit/5)
    d.add(elm.DOT)
    d.add(elm.LINE, d='down')
    Q16 = d.add(elm.BJT_NPN, anchor='collector', d='right', label='Q16', lblofst=-.1)
    d.add(elm.LINE, xy=Q16.base, d='left', l=d.unit/3)
    d.add(elm.DOT)
    R7 = d.add(elm.RES, d='up', toy=K.end, label='R7\n4.5K')
    d.add(elm.DOT)
    d.add(elm.LINE, d='right', tox=Q13.collector, move_cur=False)
    R8 = d.add(elm.RES, d='down', xy=R7.start, label='R8\n7.5K')
    d.add(elm.DOT)
    d.add(elm.LINE, d='right', tox=Q16.emitter)
    J = d.add(elm.DOT)
    d.add(elm.LINE, d='up', toy=Q16.emitter)
    Q15 = d.add(elm.BJT_NPN, anchor='collector', xy=R8.end, label='Q15', d='right')
    d.add(elm.LINE, xy=Q15.base, d='left', l=d.unit/2)
    d.add(elm.DOT)
    C1 = d.add(elm.CAP, d='up', toy=R7.end, label='C1\n30pF')
    d.add(elm.LINE, d='right', tox=Q13.collector)
    d.add(elm.LINE, d='left', xy=C1.start, tox=Q6.collector)
    d.add(elm.DOT)
    d.add(elm.LINE, d='down', xy=J.center, l=d.unit/2)
    Q19 = d.add(elm.BJT_NPN, anchor='collector', d='right', label='Q19')
    d.add(elm.LINE, xy=Q19.base, d='left', tox=Q15.emitter)
    d.add(elm.DOT)
    d.add(elm.LINE, d='up', toy=Q15.emitter, move_cur=False)
    d.add(elm.LINE, xy=Q19.emitter, d='down', l=d.unit/4)
    d.add(elm.DOT)
    d.add(elm.LINE, d='left')
    Q22 = d.add(elm.BJT_NPN, anchor='base', d='left', flip=True, lftlabel='Q22')
    d.add(elm.LINE, d='up', xy=Q22.collector, toy=Q15.base)
    d.add(elm.DOT)
    d.add(elm.LINE, d='down', xy=Q22.emitter, toy=R3.start)
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', tox=R3.start, move_cur=False)
    d.add(elm.LINE, d='right', tox=Q15.emitter)
    d.add(elm.DOT)
    d.push()
    d.add(elm.RES, d='up', label='R12\n50K')
    d.add(elm.LINE, toy=Q19.base)
    d.pop()
    d.add(elm.LINE, tox=Q19.emitter)
    d.add(elm.DOT)
    R11 = d.add(elm.RES, d='up', label='R11\n50')
    d.add(elm.LINE, toy=Q19.emitter)

    d.add(elm.LINE, xy=Q13.emitter, d='up', l=d.unit/4)
    d.add(elm.LINE, d='right', l=d.unit*1.5)
    d.add(elm.DOT)
    d.add(elm.LINE, l=d.unit/4, rgtlabel='V+', move_cur=False)
    d.add(elm.LINE, d='down', l=d.unit*.75)
    Q14 = d.add(elm.BJT_NPN, anchor='collector', d='right', label='Q14')
    d.add(elm.LINE, d='left', xy=Q14.base, l=d.unit/2)
    d.push()
    d.add(elm.DOT)
    d.add(elm.LINE, d='down', l=d.unit/2)
    Q17 = d.add(elm.BJT_NPN, anchor='collector', d='left', flip=True, lftlabel='Q17', lblofst=-.1)
    d.add(elm.LINE, xy=Q17.base, d='right', tox=Q14.emitter)
    d.add(elm.DOT)
    J = d.add(elm.LINE, d='up', toy=Q14.emitter)
    d.pop()
    d.add(elm.LINE, tox=Q13.collector)
    d.add(elm.DOT)
    d.add(elm.RES, xy=J.start, d='down', label='R9\n25')
    d.add(elm.DOT)
    d.push()
    d.add(elm.LINE, d='left', tox=Q17.emitter)
    d.add(elm.LINE, d='up', toy=Q17.emitter)
    d.pop()
    d.add(elm.LINE, d='down', l=d.unit/4)
    d.add(elm.DOT)
    d.add(elm.LINE, d='right', l=d.unit/4, rgtlabel='OUT', move_cur=False)
    d.add(elm.RES, d='down', label='R10\n50')
    Q20 = d.add(elm.BJT_PNP, d='right', anchor='emitter', label='Q20')
    d.add(elm.LINE, xy=Q20.base, d='left', l=d.unit/2)
    d.add(elm.LINE, d='up', toy=Q15.collector)
    d.add(elm.LINE, d='left', tox=Q15.collector)
    d.add(elm.DOT)
    d.add(elm.LINE, xy=Q20.collector, d='down', toy=R3.start)
    d.add(elm.DOT)
    d.add(elm.LINE, d='right', l=d.unit/4, rgtlabel='V-', move_cur=False)
    d.add(elm.LINE, d='left', tox=R11.start)
    d.draw()


555 LED Blinker Circuit
^^^^^^^^^^^^^^^^^^^^^^^

Using the `IC` function to generate a custom IC.

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    IC555def = elm.ic({'name': 'TRG', 'side': 'left', 'pin': '2'},
                    {'name': 'THR', 'side': 'left', 'pin': '6'},
                    {'name': 'DIS', 'side': 'left', 'pin': '7'},
                    {'name': 'CTL', 'side': 'right', 'pin': '5'},
                    {'name': 'OUT', 'side': 'right', 'pin': '3'},
                    {'name': 'RST', 'side': 'top', 'pin': '4'},
                    {'name': 'Vcc', 'side': 'top', 'pin': '8'},
                    {'name': 'GND', 'side': 'bot', 'pin': '1'},
                    edgepadW=.5,
                    edgepadH=1,
                    pinspacing=2,
                    leadlen=1)
    T = d.add(IC555def, label='555')
    BOT = d.add(elm.GND, xy=T.GND)
    d.add(elm.DOT)
    d.add(elm.RES, endpts=[T.DIS, T.THR], label='Rb')
    d.add(elm.RES, d='up', xy=T.DIS, label='Ra', rgtlabel='+Vcc')
    d.add(elm.LINE, endpts=[T.THR, T.TRG])
    d.add(elm.CAP, xy=T.TRG, d='down', toy=BOT.start, label='C', l=d.unit/2)
    d.add(elm.LINE, d='right', tox=BOT.start)
    d.add(elm.CAP, d='down', xy=T.CTL, toy=BOT.start, botlabel='.01$\mu$F')
    d.add(elm.DOT)
    d.add(elm.DOT, xy=T.DIS)
    d.add(elm.DOT, xy=T.THR)
    d.add(elm.DOT, xy=T.TRG)
    d.add(elm.LINE, endpts=[T.RST,T.Vcc])
    d.add(elm.DOT)
    d.add(elm.LINE, d='up', l=d.unit/4, rgtlabel='+Vcc')
    d.add(elm.RES, xy=T.OUT, d='right', label='330')
    d.add(elm.LED, flip=True, d='down', toy=BOT.start)
    d.add(elm.LINE, d='left', tox=BOT.start)
    d.draw()


Signal Processing
-----------------

Signal processing elements are in the :py:mod:`SchemDraw.dsp` module.

.. code-block:: python

    from SchemDraw import dsp


Various Networks
^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    d.add(dsp.LINE, l=d.unit/3, label='in')
    inpt = d.add(dsp.DOT)
    d.add(dsp.LINE, l=d.unit/3)
    d.add(dsp.ARROWHEAD)
    delay = d.add(dsp.makebox(2,2), label='Delay\nT', anchor='W')
    d.add(dsp.LINE, l=d.unit/2, d='right', xy=delay.E)
    d.add(dsp.ARROWHEAD, label='–')
    sm = d.add(dsp.SUMSIGMA)
    d.add(dsp.LINE, xy=sm.E, l=d.unit/2)
    d.add(dsp.ARROWHEAD)
    intg = d.add(dsp.makebox(2, 2), label='$\int$', anchor='W')
    d.add(dsp.LINE, xy=intg.E, l=d.unit/2, d='right')
    d.add(dsp.ARROWHEAD, label='out')
    d.add(dsp.LINE, xy=inpt.center, d='down', l=d.unit/2)
    d.add(dsp.LINE, d='right', tox=sm.S)
    d.add(dsp.LINE, d='up', toy=sm.S)
    d.add(dsp.ARROWHEAD, botlabel='+')
    d.draw()

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing(fontsize=14)
    d.add(dsp.LINE, l=d.unit/2, label='F(s)')
    d.push()
    d.add(dsp.DOT)
    d.add(dsp.LINE, d='up', l=d.unit/2)
    d.add(dsp.LINE, d='right', l=d.unit/2)
    d.add(dsp.ARROWHEAD)
    h1 = d.add(dsp.makebox(2, 2), label='$H_1(s)$', anchor='W')
    d.pop()
    d.add(dsp.LINE, d='down', l=d.unit/2)
    d.add(dsp.LINE, d='right', l=d.unit/2)
    d.add(dsp.ARROWHEAD)
    h2 = d.add(dsp.makebox(2, 2), label='$H_2(s)$', anchor='W')
    sm = d.add(dsp.SUMSIGMA, xy=[h1.E[0] + d.unit/2, 0], anchor='center', d='right')
    d.add(dsp.LINE, xy=h1.E, d='right', tox=sm.N)
    d.add(dsp.LINE, d='down', toy=sm.N)
    d.add(dsp.ARROWHEAD)
    d.add(dsp.LINE, xy=h2.E, d='right', tox=sm.S)
    d.add(dsp.LINE, d='up', toy=sm.S)
    d.add(dsp.ARROWHEAD)
    d.add(dsp.LINE, xy=sm.E, l=d.unit/3, d='right')
    d.add(dsp.ARROWHEAD, label='Y(s)')
    d.draw()


Superheterodyne Receiver
^^^^^^^^^^^^^^^^^^^^^^^^

`Source <https://www.electronicdesign.com/adc/high-speed-rf-sampling-adc-boosts-bandwidth-dynamic-range>`_.

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing(fontsize=12)
    d.add(dsp.ANT)
    d.add(dsp.LINE, d='right', l=d.unit/4)
    filt1 = d.add(dsp.FILT_BP, botlabel='RF filter\n#1', anchor='W', lblofst=.2, fill='thistle')
    d.add(dsp.LINE, xy=filt1.E, l=d.unit/4)
    d.add(dsp.AMP, label='LNA', fill='lightblue')
    d.add(dsp.LINE, l=d.unit/4)
    filt2 = d.add(dsp.FILT_BP, botlabel='RF filter\n#2', anchor='W', lblofst=.2, fill='thistle')
    d.add(dsp.LINE, xy=filt2.E, d='right', l=d.unit/3)
    mix = d.add(dsp.MIX, label='Mixer', fill='navajowhite')
    d.add(dsp.LINE, xy=mix.S, d='down', l=d.unit/3)
    d.add(dsp.OSC, rgtlabel='Local\nOscillator', d='right', lblofst=.2, anchor='N', fill='navajowhite')
    d.add(dsp.LINE, xy=mix.E, d='right', l=d.unit/3)
    filtIF = d.add(dsp.FILT_BP, anchor='W', botlabel='IF filter', lblofst=.2, fill='thistle')
    d.add(dsp.LINE, xy=filtIF.E, d='right', l=d.unit/4)
    d.add(dsp.AMP, label='IF\namplifier', fill='lightblue')
    d.add(dsp.LINE, l=d.unit/4)
    demod = d.add(dsp.DEMOD, anchor='W', botlabel='Demodulator', lblofst=.2, fill='navajowhite')
    d.add(dsp.LINE, xy=demod.E, d='right', l=d.unit/3)
    d.add(dsp.ARROWHEAD)
    d.draw()

Direct Conversion Receiver
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing()
    d.add(dsp.ANT)
    d.add(dsp.LINE, d='right', l=d.unit/2, botlabel='$f_{RF}$')
    d.add(dsp.ARROWHEAD)
    d.add(dsp.AMP, label='LNA')
    d.add(dsp.LINE, d='right', l=d.unit/5)
    d.add(dsp.DOT)
    d.push()
    d.add(dsp.LINE, l=d.unit/4)
    mix1 = d.add(dsp.MIX, label='Mixer')
    d.add(dsp.LINE, l=d.unit/2)
    d.add(dsp.ARROWHEAD)
    lpf1 = d.add(dsp.FILT_LP, botlabel='LPF', lblofst=.2)
    d.add(dsp.LINE, l=d.unit/6)
    adc1 = d.add(dsp.ADC, label='ADC')
    d.add(dsp.LINE, l=d.unit/3)
    d.add(dsp.ARROWHEAD)
    dsp1 = d.add(dsp.ic({'side': 'L'}, {'side': 'L'}, {'side': 'R'}, size=(2.75, 5), leadlen=0), anchor='inL2', label='DSP')
    d.add(dsp.LINE, xy=dsp1.inR1, l=d.unit/3)
    d.add(dsp.ARROWHEAD)
    d.pop()

    d.add(dsp.LINE, d='down', toy=dsp1.inL1)
    d.add(dsp.LINE, d='right', tox=mix1.W)
    d.add(dsp.ARROWHEAD)
    mix2 = d.add(dsp.MIX, label='Mixer')
    d.add(dsp.LINE, tox=lpf1.W)
    d.add(dsp.ARROWHEAD)
    d.add(dsp.FILT_LP, botlabel='LPF', lblofst=.2)
    d.add(dsp.LINE, tox=adc1.W)
    d.add(dsp.ADC, label='ADC')
    d.add(dsp.LINE, to=dsp1.inL1)
    d.add(dsp.ARROWHEAD)

    d.add(dsp.ARROWHEAD, xy=mix1.S, d='up')
    d.add(dsp.LINE, xy=mix1.S, d='down', l=d.unit/6)
    d.add(dsp.LINE, d='left', l=d.unit*1.25)
    d.add(dsp.LINE, d='down', l=d.unit*.75)
    flo = d.add(dsp.DOT, lftlabel='$f_{LO}$')
    d.push()
    d.add(dsp.LINE, d='down', l=d.unit/5)
    d.add(dsp.OSC, rgtlabel='LO', d='right', anchor='N', lblofst=.15)
    d.pop()
    d.add(dsp.ARROWHEAD, xy=mix2.S, d='up')
    d.add(dsp.LINE, xy=mix2.S, d='down', l=d.unit/4)
    b1 = d.add(dsp.BOX, label='90°', anchor='N', d='right')
    d.add(dsp.ARROWHEAD, xy=b1.W, d='right')
    d.add(dsp.LINE, xy=b1.W, d='left', l=d.unit/4)
    d.add(dsp.LINE, d='up', toy=flo.center)
    d.add(dsp.LINE, d='left', tox=flo.center)
    d.draw()

Digital Filter
^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing(unit=1, fontsize=14)
    d.add(dsp.LINE, lftlabel='x[n]', l=d.unit*2)
    d.add(dsp.DOT)

    d.push()
    d.add(dsp.LINE, d='right')
    d.add(dsp.AMP, botlabel='$b_0$')
    d.add(dsp.LINE)
    d.add(dsp.ARROWHEAD)
    s0 = d.add(dsp.SUM, anchor='W')
    d.pop()

    d.add(dsp.LINE, d='down')
    d.add(dsp.ARROWHEAD)
    z1 = d.add(dsp.BOX, label='$z^{-1}$')
    d.add(dsp.LINE, l=d.unit/2)
    d.add(dsp.DOT)

    d.push()
    d.add(dsp.LINE, d='right')
    d.add(dsp.AMP, botlabel='$b_1$')
    d.add(dsp.LINE)
    d.add(dsp.ARROWHEAD)
    s1 = d.add(dsp.SUM, anchor='W')
    d.pop()

    d.add(dsp.LINE, l=d.unit*.75, d='down')
    d.add(dsp.ARROWHEAD)
    d.add(dsp.BOX, label='$z^{-1}$')
    d.add(dsp.LINE, l=d.unit*.75)
    d.add(dsp.LINE, d='right')
    d.add(dsp.AMP, botlabel='$b_2$')
    d.add(dsp.LINE)
    d.add(dsp.ARROWHEAD)
    s2 = d.add(dsp.SUM, anchor='W')

    d.add(dsp.LINE, xy=s2.N, d='up', toy=s1.S)
    d.add(dsp.ARROWHEAD)
    d.add(dsp.LINE, xy=s1.N, d='up', toy=s0.S)
    d.add(dsp.ARROWHEAD)

    d.add(dsp.LINE, xy=s0.E, l=d.unit*2.75, d='right')
    d.add(dsp.DOT)
    d.push()
    d.add(dsp.LINE, d='right', rgtlabel='y[n]')
    d.add(dsp.ARROWHEAD)
    d.pop()
    d.add(dsp.LINE, d='down')
    d.add(dsp.ARROWHEAD)
    d.add(dsp.BOX, label='$z^{-1}$')
    d.add(dsp.LINE, l=d.unit/2)
    d.add(dsp.DOT)
    d.push()
    d.add(dsp.LINE, d='left')
    a1 = d.add(dsp.AMP, botlabel='$-a_1$')
    d.add(dsp.LINE, xy=a1.out, tox=s1.E)
    d.add(dsp.ARROWHEAD)
    d.pop()

    d.add(dsp.LINE, d='down', l=d.unit*.75)
    d.add(dsp.ARROWHEAD)
    d.add(dsp.BOX, label='$z^{-1}$')
    d.add(dsp.LINE, l=d.unit*.75)
    d.add(dsp.LINE, d='left')
    a1 = d.add(dsp.AMP, botlabel='$-a_2$')
    d.add(dsp.LINE, xy=a1.out, tox=s2.E)
    d.add(dsp.ARROWHEAD)
    d.draw()


.. _galleryflow:

Flowcharting
------------

Flowchart elements are defined in the :py:mod:`flow` module.

.. code-block:: python

    from SchemDraw import flow

It's a Trap!
^^^^^^^^^^^^

Recreation of `XKCD 1195 <https://xkcd.com/1195/>`_.

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing()
    d.add(flow.start(2, 1.5), label='START')
    d.add(flow.LINE, d='down', l=d.unit/3)
    d.add(flow.ARROWHEAD)
    h = d.add(flow.decision(5.5, 4, responses={'S': 'YES'}), label='Hey, wait,\nthis flowchart\nis a trap!')
    d.add(flow.LINE, d='down', l=d.unit/4)
    d.add(flow.LINE, d='right', l=d.unit*1.1)
    d.add(flow.LINE, d='up', toy=h.E)
    d.add(flow.LINE, d='left', tox=h.E)
    d.add(flow.ARROWHEAD)
    d.draw()

Flowchart for flowcharts
^^^^^^^^^^^^^^^^^^^^^^^^

Recreation of `XKCD 518 <https://xkcd.com/518/>`_.

.. jupyter-execute::
    :code-below:
    
    d = SchemDraw.Drawing(fontsize=11)
    b = d.add(flow.start(2, 1.5), label='START')
    d.add(flow.LINE, d='down', l=d.unit/2)
    d.add(flow.ARROWHEAD)
    d1 = d.add(flow.decision(5, 3.9, responses={'E': 'YES', 'S': 'NO'}), label='DO YOU\nUNDERSTAND\nFLOW CHARTS?')
    d.add(flow.LINE, l=d.unit/2)
    d.add(flow.ARROWHEAD)
    d2 = d.add(flow.decision(5, 3.9, responses={'E': 'YES', 'S': 'NO'}), label='OKAY,\nYOU SEE THE\nLINE LABELED\n"YES"?')
    d.add(flow.LINE, l=d.unit/2)
    d.add(flow.ARROWHEAD)
    d3 = d.add(flow.decision(5.2, 3.9, responses={'E': 'YES', 'S': 'NO'}), label='BUT YOU\nSEE THE ONES\nLABELED "NO".')

    d.add(flow.LINE, xy=d3.E, d='right', l=d.unit/2)
    d.add(flow.ARROWHEAD)
    d.add(flow.box(2, 1.25), label='WAIT,\nWHAT?', anchor='W')
    d.add(flow.LINE, xy=d3.S, d='down', l=d.unit/2)
    d.add(flow.ARROWHEAD)
    listen = d.add(flow.box(2, 1), label='LISTEN.')
    d.add(flow.LINE, xy=listen.E, d='right', l=d.unit/2)
    d.add(flow.ARROWHEAD)
    hate = d.add(flow.box(2, 1.25), label='I HATE\nYOU.', anchor='W')

    d.add(flow.LINE, xy=d1.E, d='right', l=d.unit*3.5)
    d.add(flow.ARROWHEAD)
    good = d.add(flow.box(2, 1), label='GOOD', anchor='W')
    d.add(flow.LINE, xy=d2.E, d='right', l=d.unit*1.5)
    d.add(flow.ARROWHEAD)
    d4 = d.add(flow.decision(5.3, 4.0, responses={'E': 'YES', 'S': 'NO'}), label='...AND YOU CAN\nSEE THE ONES\nLABELED "NO"?', anchor='W')

    d.add(flow.LINE, xy=d4.E, d='right', tox=good.S)
    d.add(flow.LINE, d='up', toy=good.S)
    d.add(flow.ARROWHEAD)
    d.add(flow.LINE, xy=d4.S, d='down', l=d.unit/2)
    d.add(flow.ARROWHEAD)
    d5 = d.add(flow.decision(5, 3.6, responses={'E': 'YES', 'S': 'NO'}), label='BUT YOU\nJUST FOLLOWED\nTHEM TWICE!')
    d.add(flow.LINE, xy=d5.E, d='right', l=d.unit)
    d.add(flow.ARROWHEAD)
    question = d.add(flow.box(3.5, 1.75), label="(THAT WASN'T\nA QUESTION.)", anchor='W')
    d.add(flow.LINE, xy=d5.S, d='down', l=d.unit/3)
    d.add(flow.LINE, d='right', tox=question.S)
    d.add(flow.LINE, d='up', toy=question.S)
    d.add(flow.ARROWHEAD)

    d.add(flow.LINE, d='right', xy=good.E, tox=question.S)
    d.add(flow.LINE, d='down', l=d.unit)
    d.add(flow.ARROWHEAD)
    drink = d.add(flow.box(2.5, 1.5), label="LET'S GO\nDRINK.")
    d.add(flow.LINE, xy=drink.E, d='right', label='6 DRINKS')
    d.add(flow.ARROWHEAD)
    d.add(flow.box(3.7, 2), label='HEY, I SHOULD\nTRY INSTALLING\nFREEBSD!', anchor='W')
    d.add(flow.LINE, xy=question.N, d='up', l=d.unit*.75)
    d.add(flow.ARROWHEAD)
    screw = d.add(flow.box(2.5, 1), label='SCREW IT.', anchor='S')
    d.add(flow.LINE, xy=screw.N, d='up', toy=drink.S)
    d.add(flow.ARROWHEAD)
    d.draw()



Styles
------

Circuit elements can be styled using Matplotlib colors, line-styles, and line widths.

Resistor circle
^^^^^^^^^^^^^^^

Uses named colors in a loop.

.. jupyter-execute::
    :code-below:

    d = SchemDraw.Drawing()
    for i, color in enumerate(['red', 'orange', 'yellow', 'yellowgreen', 'green', 'blue', 'indigo', 'violet']):
        d.add(elm.RES, label='R{}'.format(i), theta=45*i+20, color=color)
    d.draw()


Hand-drawn
^^^^^^^^^^

And for a change of pace, activate Matplotlib's XKCD mode for "hand-drawn" look!

.. jupyter-execute::
    :code-below:

    import matplotlib.pyplot as plt
    plt.xkcd()

    d = SchemDraw.Drawing(inches_per_unit=.5)
    op = d.add(elm.OPAMP)
    d.add(elm.LINE, d='left', xy=op.in2, l=d.unit/4)
    d.add(elm.LINE, d='down', l=d.unit/5)
    d.add(elm.GND)
    d.add(elm.LINE, d='left', xy=op.in1, l=d.unit/6)
    d.add(elm.DOT)
    d.push()
    Rin = d.add(elm.RES, d='left', xy=op.in1-[d.unit/5,0], botlabel='$R_{in}$', lftlabel='$v_{in}$')
    d.pop()
    d.add(elm.LINE, d='up', l=d.unit/2)
    Rf = d.add(elm.RES,  d='right', l=d.unit*1, label='$R_f$')
    d.add(elm.LINE, d='down', toy=op.out)
    d.add(elm.DOT)
    d.add(elm.LINE, d='left', tox=op.out)
    d.add(elm.LINE, d='right', l=d.unit/4, rgtlabel='$v_{o}$')
    d.draw()
