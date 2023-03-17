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
    
    with schemdraw.Drawing() as d:
        d += (op := elm.Opamp(leads=True))
        d += elm.Line().down(d.unit/4).at(op.in2)
        d += elm.Ground(lead=False)
        d += (Rin := elm.Resistor().at(op.in1).left().idot().label('$R_{in}$', loc='bot').label('$v_{in}$', loc='left'))
        d += elm.Line().up(d.unit/2).at(op.in1)
        d += elm.Resistor().tox(op.out).label('$R_f$')
        d += elm.Line().toy(op.out).dot()
        d += elm.Line().right(d.unit/4).at(op.out).label('$v_{o}$', loc='right')


Non-inverting Opamp
^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d += (op := elm.Opamp(leads=True))
        d += (out := elm.Line(at=op.out).length(.75))
        d += elm.Line().up().at(op.in1).length(1.5).dot()
        d.push()
        d += elm.Resistor().left().label('$R_1$')
        d += elm.Ground()
        d.pop()
        d += elm.Resistor().tox(op.out).label('$R_f$')
        d += elm.Line().toy(op.out).dot()
        d += elm.Resistor().left().at(op.in2).idot().label('$R_2$')
        d += elm.SourceV().down().reverse().label('$v_{in}$')
        d += elm.Line().right().dot()
        d += elm.Resistor().up().label('$R_3$').hold()
        d += elm.Line().tox(out.end)
        d += elm.Gap().toy(op.out).label(['–','$v_o$','+'])


Multi-stage amplifier
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d += elm.Ground(lead=False)
        d += elm.SourceV().label('500mV')
        d += elm.Resistor().right().label('20k$\Omega$').dot()
        d += (O1 := elm.Opamp(leads=True).anchor('in1'))
        d += elm.Ground().at(O1.in2)
        d += elm.Line().up(2).at(O1.in1)
        d += elm.Resistor().tox(O1.out).label('100k$\Omega$')
        d += elm.Line().toy(O1.out).dot()
        d += elm.Line().right(5).at(O1.out)
        d += (O2 := elm.Opamp(leads=True).anchor('in2'))
        d += elm.Resistor().left().at(O2.in1).idot().label('30k$\Omega$')
        d += elm.Ground()
        d += elm.Line().up(1.5).at(O2.in1)
        d += elm.Resistor().tox(O2.out).label('90k$\Omega$')
        d += elm.Line().toy(O2.out).dot()
        d += elm.Line().right(1).at(O2.out).label('$v_{out}$', loc='rgt')


Opamp pin labeling
^^^^^^^^^^^^^^^^^^

This example shows how to label pin numbers on a 741 opamp, and connect to the offset anchors.
Pin labels are somewhat manually placed; without the `ofst` and `align` keywords they
will be drawn directly over the anchor position.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
        op = (elm.Opamp().label('741', loc='center', ofst=0)
                     .label('1', 'n1', fontsize=9, ofst=(-.1, -.25), halign='right', valign='top')
                     .label('5', 'n1a', fontsize=9, ofst=(-.1, -.25), halign='right', valign='top')
                     .label('4', 'vs', fontsize=9, ofst=(-.1, -.2), halign='right', valign='top')
                     .label('7', 'vd', fontsize=9, ofst=(-.1, .2), halign='right', valign='bottom')
                     .label('2', 'in1', fontsize=9, ofst=(-.1, .1), halign='right', valign='bottom')
                     .label('3', 'in2', fontsize=9, ofst=(-.1, .1), halign='right', valign='bottom')
                     .label('6', 'out', fontsize=9, ofst=(-.1, .1), halign='left', valign='bottom'))
        d += op
        d += elm.Line().left(.5).at(op.in1)
        d += elm.Line().down(d.unit/2)
        d += elm.Ground(lead=False)
        d += elm.Line().left(.5).at(op.in2)
        d += elm.Line().right(.5).at(op.out).label('$V_o$', 'right')
        d += elm.Line().up(1).at(op.vd).label('$+V_s$', 'right')
        d += (trim := elm.Potentiometer().down().at(op.n1).flip().scale(0.7))
        d += elm.Line().tox(op.n1a)
        d += elm.Line().up().to(op.n1a)
        d += elm.Line().at(trim.tap).tox(op.vs).dot()
        d.push()
        d += elm.Line().down(d.unit/3)
        d += elm.Ground()
        d.pop()
        d += elm.Line().toy(op.vs)


Triaxial Cable Driver
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d.config(fontsize=10)
        d += elm.Line().length(d.unit/5).label('V', 'left')
        d += (smu := elm.Opamp(sign=False).anchor('in2')
                          .label('SMU', 'center', ofst=[-.4, 0], halign='center', valign='center'))
        d += elm.Line().at(smu.out).length(.3)
        d.push()
        d += elm.Line().length(d.unit/4)
        d += (triax := elm.Triax(length=5, shieldofststart=.75))
        d.pop()
        d += elm.Resistor().up().scale(0.6).idot()
        d += elm.Line().left().dot()
        d += elm.Wire('|-').to(smu.in1).hold()
        d += elm.Wire('|-').delta(d.unit/5, d.unit/5)
        d += (buf := elm.Opamp(sign=False).anchor('in2').scale(0.6)
                             .label('BUF', 'center', ofst=(-.4, 0), halign='center', valign='center'))

        d += elm.Line().left(d.unit/5).at(buf.in1)
        d += elm.Wire('n').to(buf.out, dx=.5).dot()
        d += elm.Wire('-|').at(buf.out).to(triax.guardstart_top)
        d += elm.GroundChassis().at(triax.shieldcenter)
