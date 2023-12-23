Opamp Circuits
--------------

.. jupyter-execute::
    :hide-code:

    import schemdraw
    from schemdraw import elements as elm


Inverting Opamp
^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        op = elm.Opamp(leads=True)
        elm.Line().down(d.unit/4).at(op.in2)
        elm.Ground(lead=False)
        Rin = elm.Resistor().at(op.in1).left().idot().label('$R_{in}$', loc='bot').label('$v_{in}$', loc='left')
        elm.Line().up(d.unit/2).at(op.in1)
        elm.Resistor().tox(op.out).label('$R_f$')
        elm.Line().toy(op.out).dot()
        elm.Line().right(d.unit/4).at(op.out).label('$v_{o}$', loc='right')


Non-inverting Opamp
^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        op = elm.Opamp(leads=True)
        out = elm.Line().at(op.out).length(.75)
        elm.Line().up().at(op.in1).length(1.5).dot()
        d.push()
        elm.Resistor().left().label('$R_1$')
        elm.Ground()
        d.pop()
        elm.Resistor().tox(op.out).label('$R_f$')
        elm.Line().toy(op.out).dot()
        elm.Resistor().left().at(op.in2).idot().label('$R_2$')
        elm.SourceV().down().reverse().label('$v_{in}$')
        elm.Line().right().dot()
        elm.Resistor().up().label('$R_3$').hold()
        elm.Line().tox(out.end)
        elm.Gap().toy(op.out).label(['–','$v_o$','+'])


Multi-stage amplifier
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        elm.Ground(lead=False)
        elm.SourceV().label('500mV')
        elm.Resistor().right().label(r'20k$\Omega$').dot()
        O1 = elm.Opamp(leads=True).anchor('in1')
        elm.Ground().at(O1.in2)
        elm.Line().up(2).at(O1.in1)
        elm.Resistor().tox(O1.out).label(r'100k$\Omega$')
        elm.Line().toy(O1.out).dot()
        elm.Line().right(5).at(O1.out)
        O2 = elm.Opamp(leads=True).anchor('in2')
        elm.Resistor().left().at(O2.in1).idot().label(r'30k$\Omega$')
        elm.Ground()
        elm.Line().up(1.5).at(O2.in1)
        elm.Resistor().tox(O2.out).label(r'90k$\Omega$')
        elm.Line().toy(O2.out).dot()
        elm.Line().right(1).at(O2.out).label('$v_{out}$', loc='rgt')


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
        elm.Line().left(.5).at(op.in1)
        elm.Line().down(d.unit/2)
        elm.Ground(lead=False)
        elm.Line().left(.5).at(op.in2)
        elm.Line().right(.5).at(op.out).label('$V_o$', 'right')
        elm.Line().up(1).at(op.vd).label('$+V_s$', 'right')
        trim = elm.Potentiometer().down().at(op.n1).flip().scale(0.7)
        elm.Line().tox(op.n1a)
        elm.Line().up().to(op.n1a)
        elm.Line().at(trim.tap).tox(op.vs).dot()
        d.push()
        elm.Line().down(d.unit/3)
        elm.Ground()
        d.pop()
        elm.Line().toy(op.vs)


Triaxial Cable Driver
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d.config(fontsize=10)
        elm.Line().length(d.unit/5).label('V', 'left')
        smu = (elm.Opamp(sign=False).anchor('in2')
                          .label('SMU', 'center', ofst=[-.4, 0], halign='center', valign='center'))
        elm.Line().at(smu.out).length(.3)
        d.push()
        elm.Line().length(d.unit/4)
        triax = elm.Triax(length=5, shieldofststart=.75)
        d.pop()
        elm.Resistor().up().scale(0.6).idot()
        elm.Line().left().dot()
        elm.Wire('|-').to(smu.in1).hold()
        elm.Wire('|-').delta(d.unit/5, d.unit/5)
        buf = (elm.Opamp(sign=False).anchor('in2').scale(0.6)
                             .label('BUF', 'center', ofst=(-.4, 0), halign='center', valign='center'))

        elm.Line().left(d.unit/5).at(buf.in1)
        elm.Wire('n').to(buf.out, dx=.5).dot()
        elm.Wire('-|').at(buf.out).to(triax.guardstart_top)
        elm.GroundChassis().at(triax.shieldcenter)
