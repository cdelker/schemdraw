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
    d += (op := elm.Opamp())
    d += elm.Line().left().at(op.in2).length(d.unit/4)
    d += elm.Line().down().length(d.unit/5)
    d += elm.Ground()
    d += elm.Line().left().at(op.in1).length(d.unit/6)
    d += elm.Dot()
    d.push()
    d += (Rin := elm.Resistor().left().at((op.in1[0]-d.unit/5, op.in1[1]))
                              .label('$R_{in}$', loc='bot')
                              .label('$v_{in}$', loc='lft'))
    d.pop()
    d += elm.Line().up().length(d.unit/2)
    d += elm.Resistor().right().label('$R_f$')
    d += elm.Line().down().toy(op.out)
    d += elm.Dot()
    d += elm.Line().left().tox(op.out)
    d += elm.Line().right().length(d.unit/4).label('$v_{o}$', loc='rgt')
    d.draw()


Non-inverting Opamp
^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    d += (op := elm.Opamp())
    d += elm.Line(at=op.out).length(.75)
    d += elm.Line().left().at(op.in1).length(.75)
    d += elm.Line().up().length(1.5)
    d += elm.Dot()
    d += (R1 := elm.Resistor().left().label('$R_1$'))
    d += elm.Ground()
    d += (Rf := elm.Resistor().right().at(R1.start).tox(op.out+.5).label('$R_f$'))
    d += elm.Line().down().toy(op.out)
    d += (dot := elm.Dot())
    d += elm.Line().left().at(op.in2).length(.75)
    d += elm.Dot()
    d += (R3 := elm.Resistor().down().label('$R_3$'))
    d += elm.Dot()
    d += elm.Ground()
    d += (R2 := elm.Resistor().left().at(R3.start).label('$R_2$'))
    d += elm.SourceV().down().reverse().label('$v_{in}$')
    d += elm.Line().right().tox(Rf.end)
    d += elm.Gap().down().at(dot.start).toy(R3.end).label(['+','$v_o$','–'])
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
    d += elm.Line().length(.5)
    d += (O1 := elm.Opamp().anchor('in1'))
    d += elm.Line().left().length(0.75).at(O1.in2)
    d += elm.Ground()
    d += elm.Line().up().at(Vin.start).length(2)
    d += elm.Resistor().right().label('100k$\Omega$')
    d += elm.Line().down().toy(O1.out)
    d += elm.Dot()
    d += elm.Line().right().at(O1.out).length(5)
    d += (O2 := elm.Opamp().anchor('in2'))
    d += (Vin2 := elm.Line().left().at(O2.in1).length(0.5))
    d += elm.Dot()
    d += elm.Resistor().left().label('30k$\Omega$')
    d += elm.Ground()
    d += elm.Line().up().at(Vin2.end).length(1.5)
    d += elm.Resistor().right().label('90k$\Omega$')
    d += elm.Line().down().toy(O2.out)
    d += elm.Dot()
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
