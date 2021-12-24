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
    d += (op := elm.Opamp(leads=True))
    d += elm.Line().down().at(op.in2).length(d.unit/4)
    d += elm.Ground()
    d += elm.Dot().at(op.in1)
    d += (Rin := elm.Resistor().left().hold().label('$R_{in}$', loc='bot').label('$v_{in}$', loc='left'))
    d += elm.Line().up().length(d.unit/2)
    d += elm.Resistor().right().tox(op.out).label('$R_f$')
    d += elm.LineDot().down().toy(op.out)
    d += elm.Line().right().at(op.out).length(d.unit/4).label('$v_{o}$', loc='right')
    d.draw()


Non-inverting Opamp
^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    d += (op := elm.Opamp(leads=True))
    d += elm.Line(at=op.out).length(.75)
    d += elm.LineDot().up().at(op.in1).length(1.5)
    d.push()
    d += elm.Resistor().left().label('$R_1$')
    d += elm.Ground()
    d.pop()
    d += elm.Resistor().right().tox(op.out).label('$R_f$')
    d += elm.LineDot().down().toy(op.out)
    d += elm.Dot().at(op.in2)
    d += elm.Resistor().down().label('$R_3$')
    d.push()
    d += elm.Dot()
    d += elm.Ground()
    d += elm.Line().left()
    d += elm.SourceV().up().label('$v_{in}$')
    d += elm.Resistor().right().label('$R_2$')
    d.pop()
    d += elm.Line().right().tox(op.out.x+0.75)
    d += elm.Gap().up().toy(op.out).label(['–','$v_o$','+'])
    d.draw()


Multi-stage amplifier
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    d += elm.Ground()
    d += elm.SourceV().label('500mV')
    d += elm.Resistor().right().label('20k$\Omega$')
    d += (Vin := elm.Dot())
    d += (O1 := elm.Opamp(leads=True).anchor('in1'))
    d += elm.Ground().at(O1.in2)
    d += elm.Line().up().at(Vin.start).length(2)
    d += elm.Resistor().right().tox(O1.out).label('100k$\Omega$')
    d += elm.LineDot().down().toy(O1.out)
    d += elm.Line().right().at(O1.out).length(5)
    d += (O2 := elm.Opamp(leads=True).anchor('in2'))
    d += (Vin2 := elm.Dot().at(O2.in1))
    d += elm.Resistor().left().label('30k$\Omega$')
    d += elm.Ground()
    d += elm.Line().up().at(Vin2.end).length(1.5)
    d += elm.Resistor().right().tox(O2.out).label('90k$\Omega$')
    d += elm.LineDot().down().toy(O2.out)
    d += elm.Line().right().at(O2.out).length(1).label('$v_{out}$', loc='rgt')
    d.draw()



Opamp pin labeling
^^^^^^^^^^^^^^^^^^

This example shows how to label pin numbers on a 741 opamp, and connect to the offset anchors.
Pin labels are somewhat manually placed; without the `ofst` and `align` keywords they
will be drawn directly over the anchor position.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(fontsize=12)
    op = (elm.Opamp().label('741', loc='center', ofst=0)
                     .label('1', 'n1', fontsize=9, ofst=(-.1, -.25), halign='right', valign='top')
                     .label('5', 'n1a', fontsize=9, ofst=(-.1, -.25), halign='right', valign='top')
                     .label('4', 'vs', fontsize=9, ofst=(-.1, -.2), halign='right', valign='top')
                     .label('7', 'vd', fontsize=9, ofst=(-.1, .2), halign='right', valign='bottom')
                     .label('2', 'in1', fontsize=9, ofst=(-.1, .1), halign='right', valign='bottom')
                     .label('3', 'in2', fontsize=9, ofst=(-.1, .1), halign='right', valign='bottom')
                     .label('6', 'out', fontsize=9, ofst=(-.1, .1), halign='left', valign='bottom'))
    d += op
    d += elm.Line().left().at(op.in1).length(0.5)
    d += elm.Line().down().length(d.unit/2)
    d += elm.Ground()
    d += elm.Line().left().at(op.in2).length(0.5)
    d += elm.Line().right().at(op.out).length(0.5).label('$V_o$', 'right')
    d += elm.Line().up().at(op.vd).length(1).label('$+V_s$', 'right')
    d += (trim := elm.Potentiometer().down().at(op.n1).flip().scale(0.7))
    d += elm.Line().right().tox(op.n1a)
    d += elm.Line().up().to(op.n1a)
    d += elm.Line().left().at(trim.tap).tox(op.vs)
    d += elm.Dot()
    d.push()
    d += elm.Line().down().length(d.unit/3)
    d += elm.Ground()
    d.pop()
    d += elm.Line().up().toy(op.vs)
    d.draw()


Triaxial Cable Driver
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(fontsize=10)
    d += elm.Line().length(d.unit/5).label('V', 'left')
    d += (smu := elm.Opamp(sign=False).anchor('in2')
                      .label('SMU', 'center', ofst=[-.4, 0], halign='center', valign='center'))
    d += elm.Line().at(smu.out).length(d.unit/5)
    d.push()
    d += elm.Line().length(d.unit/4)
    d += (triax := elm.Triax(length=5, shieldofststart=.75))
    d.pop()
    d += elm.Dot()
    d += elm.Resistor().up().length(d.unit).scale(0.6)
    d += elm.Line().left()
    d += elm.Dot()
    d.push()
    d += elm.Line().down().toy(smu.in1)
    d += elm.Line().right().tox(smu.in1)
    d.pop()
    d += elm.Line().up().length(d.unit/5)
    d += elm.Line().right().length(d.unit/5)
    d += (buf := elm.Opamp(sign=False).anchor('in2').scale(0.6)
                         .label('BUF', 'center', ofst=(-.4, 0), halign='center', valign='center'))

    d += elm.Line().left().at(buf.in1).length(d.unit/5)
    d += elm.Line().up().length(d.unit/5)
    d += elm.Line().right()
    d += elm.Line().down().toy(buf.out)
    d += elm.Dot()
    d.push()
    d += elm.Line().left().tox(buf.out)
    d.pop()
    d += elm.Line().right().tox(triax.guardstart_top)
    d += elm.Line().down().toy(triax.guardstart_top)
    d += elm.GroundChassis().at(triax.shieldcenter)
    d.draw()
