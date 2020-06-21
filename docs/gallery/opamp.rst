Opamp Circuits
--------------

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


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
