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
        V1 = elm.SourceV().label('5V')
        elm.Line().right(d.unit*.75)
        S1 = elm.SwitchSpdt2(action='close').up().anchor('b').label('$t=0$', loc='rgt')
        elm.Line().right(d.unit*.75).at(S1.c)
        elm.Resistor().down().label(r'$100\Omega$').label(['+','$v_o$','-'], loc='bot')
        elm.Line().to(V1.start)
        elm.Capacitor().at(S1.a).toy(V1.start).label(r'1$\mu$F').dot()


Capacitor Network
^^^^^^^^^^^^^^^^^

Shows how to use endpoints to specify exact start and end placement.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
        C1 = elm.Capacitor().label('8nF').idot().label('a', 'left')
        C2 = elm.Capacitor().label('18nF')
        C3 = elm.Capacitor().down().label('8nF', loc='bottom')
        C4 = elm.Capacitor().left().label('32nF')
        C5 = elm.Capacitor().label('40nF', loc='bottom').dot().label('b', 'left')
        C6 = elm.Capacitor().endpoints(C1.end, C5.start).label('2.8nF')
        C7 = (elm.Capacitor().endpoints(C2.end, C5.start)
                  .label('5.6nF', loc='center', ofst=(-.3, -.1), halign='right', valign='bottom'))


ECE201-Style Circuit
^^^^^^^^^^^^^^^^^^^^

This example demonstrate use of `push()` and `pop()` and using the 'tox' and 'toy' methods.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(unit=2)  # unit=2 makes elements have shorter than normal leads
        d.push()
        R1 = elm.Resistor().down().label('20Ω')
        V1 = elm.SourceV().down().reverse().label('120V')
        elm.Line().right(3).dot()
        d.pop()
        elm.Line().right(3).dot()
        elm.SourceV().down().reverse().label('60V')
        elm.Resistor().label('5Ω').dot()
        elm.Line().right(3).dot()
        elm.SourceI().up().label('36A')
        elm.Resistor().label('10Ω').dot()
        elm.Line().left(3).hold()
        elm.Line().right(3).dot()
        R6 = elm.Resistor().toy(V1.end).label('6Ω').dot()
        elm.Line().left(3).hold()
        elm.Resistor().right().at(R6.start).label('1.6Ω').dot(open=True).label('a', 'right')
        elm.Line().right().at(R6.end).dot(open=True).label('b', 'right')


Loop Currents
^^^^^^^^^^^^^

Using the :py:class:`schemdraw.elements.lines.LoopCurrent` element to add loop currents, and rotating a label to make it fit.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(unit=5)
        V1 = elm.SourceV().label('20V')
        R1 = elm.Resistor().right().label('400Ω')
        elm.Dot()
        d.push()
        R2 = elm.Resistor().down().label('100Ω', loc='bot', rotate=True)
        elm.Dot()
        d.pop()
        L1 = elm.Line()
        I1 = elm.SourceI().down().label('1A', loc='bot')
        L2 = elm.Line().tox(V1.start)
        elm.LoopCurrent([R1,R2,L2,V1], pad=1.25).label('$I_1$')
        elm.LoopCurrent([R1,I1,L2,R2], pad=1.25).label('$I_2$')    # Use R1 as top element for both so they get the same height


AC Loop Analysis
^^^^^^^^^^^^^^^^

Another good problem for ECE students...

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        I1 = elm.SourceI().label('5∠0° A').dot()
        d.push()
        elm.Capacitor().right().label('-j3Ω').dot()
        elm.Inductor().down().label('j2Ω').dot().hold()
        elm.Resistor().right().label('5Ω').dot()
        V1 = elm.SourceV().down().reverse().label('5∠-90° V', loc='bot')
        elm.Line().tox(I1.start)
        d.pop()
        elm.Line().up(d.unit*.8)
        L1 = elm.Inductor().tox(V1.start).label('j3Ω')
        elm.Line().down(d.unit*.8)
        elm.CurrentLabel(top=False, ofst=.3).at(L1).label('$i_g$')


Infinite Transmission Line
^^^^^^^^^^^^^^^^^^^^^^^^^^

Elements can be added inside for-loops if you need multiples.
The ellipsis is just another circuit element, called `DotDotDot` since Ellipsis is a reserved keyword in Python.
This also demonstrates the :py:class:`schemdraw.elements.ElementDrawing` class to merge multiple elements into a single definition.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing(show=False) as d1:
        elm.Resistor()
        d1.push()
        elm.Capacitor().down()
        elm.Line().left()
        d1.pop()

    with schemdraw.Drawing() as d2:
        for i in range(3):
            elm.ElementDrawing(d1)

        d2.push()
        elm.Line().length(d2.unit/6)
        elm.DotDotDot()
        elm.ElementDrawing(d1)
        d2.pop()
        d2.here = (d2.here[0], d2.here[1]-d2.unit)
        elm.Line().right().length(d2.unit/6)
        elm.DotDotDot()


Power supply
^^^^^^^^^^^^

Notice the diodes could be added individually, but here the built-in `Rectifier` element is used instead.
Also note the use of newline characters inside resistor and capacitor labels.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(inches_per_unit=.5, unit=3)
        D = elm.Rectifier()
        elm.Line().left(d.unit*1.5).at(D.N).dot(open=True).idot()
        elm.Line().left(d.unit*1.5).at(D.S).dot(open=True).idot()
        G = elm.Gap().toy(D.N).label(['–', 'AC IN', '+'])

        top = elm.Line().right(d.unit*3).at(D.E).idot()
        Q2 = elm.BjtNpn(circle=True).up().anchor('collector').label('Q2\n2n3055')
        elm.Line().down(d.unit/2).at(Q2.base)
        Q2b = elm.Dot()
        elm.Line().left(d.unit/3)
        Q1 = elm.BjtNpn(circle=True).up().anchor('emitter').label('Q1\n    2n3054')
        elm.Line().at(Q1.collector).toy(top.center).dot()

        elm.Line().down(d.unit/2).at(Q1.base).dot()
        elm.Zener().down().reverse().label('D2\n500mA', loc='bot').dot()
        G = elm.Ground()
        elm.Line().left().dot()
        elm.Capacitor(polar=True).up().reverse().label('C2\n100$\\mu$F\n50V', loc='bot').dot()
        elm.Line().right().hold()
        elm.Resistor().toy(top.end).label('R1\n2.2K\n50V', loc='bot').dot()

        d.move(dx=-d.unit, dy=0)
        elm.Capacitor(polar=True).toy(G.start).flip().label('C1\n 1000$\\mu$F\n50V').dot().idot()
        elm.Line().at(G.start).tox(D.W)
        elm.Line().toy(D.W).dot()

        elm.Resistor().right().at(Q2b.center).label('R2').label('56$\\Omega$ 1W', loc='bot').dot()
        d.push()
        elm.Line().toy(top.start).dot()
        elm.Line().tox(Q2.emitter)
        d.pop()
        elm.Capacitor(polar=True).toy(G.start).label('C3\n470$\\mu$F\n50V', loc='bot').dot()
        elm.Line().tox(G.start).hold()
        elm.Line().right().dot()
        elm.Resistor().toy(top.center).label('R3\n10K\n1W', loc='bot').dot()
        elm.Line().left().hold()
        elm.Line().right()
        elm.Dot(open=True)
        elm.Gap().toy(G.start).label(['+', '$V_{out}$', '–'])
        elm.Dot(open=True)
        elm.Line().left()

5-transistor Operational Transconductance Amplifer (OTA)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Note the use of current labels to show the bias currents.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        # tail transistor
        Q1 = elm.AnalogNFet().anchor('source').theta(0).reverse()
        elm.Line().down().length(0.5)
        ground = d.here
        elm.Ground()

        # input pair
        elm.Line().left().length(1).at(Q1.drain)
        Q2 = elm.AnalogNFet().anchor('source').theta(0).reverse()

        elm.Dot().at(Q1.drain)
        elm.Line().right().length(1)
        Q3 = elm.AnalogNFet().anchor('source').theta(0)

        # current mirror
        Q4 = elm.AnalogPFet().anchor('drain').at(Q2.drain).theta(0)
        Q5 = elm.AnalogPFet().anchor('drain').at(Q3.drain).theta(0).reverse()

        elm.Line().right().at(Q4.gate).to(Q5.gate)

        elm.Dot().at(0.5*(Q4.gate + Q5.gate))
        elm.Line().down().toy(Q4.drain)
        elm.Line().left().tox(Q4.drain)
        elm.Dot()

        # vcc connection
        elm.Line().right().at(Q4.source).to(Q5.source)
        elm.Dot().at(0.5*(Q4.source + Q5.source))
        elm.Vdd()

        # bias source
        elm.Line().left().length(0.25).at(Q1.gate)
        elm.SourceV().down().toy(ground).reverse().scale(0.5).label("Bias")
        elm.Ground()

        # signal labels
        elm.Tag().at(Q2.gate).label("In+").left()
        elm.Tag().at(Q3.gate).label("In−").right()
        elm.Dot().at(Q3.drain)
        elm.Line().right().tox(Q3.gate)
        elm.Tag().right().label("Out").reverse()

        # bias currents
        elm.CurrentLabel(length=1.25, ofst=0.25).at(Q1).label("20µA")
        elm.CurrentLabel(length=1.25, ofst=0.25).at(Q4).label("10µA")
        elm.CurrentLabel(length=1.25, ofst=0.25).at(Q5).label("10µA")


Quadruple loop negative feedback amplifier
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        # place twoports
        N1 = elm.Nullor().anchor('center')
        T1 = elm.TransimpedanceTransactor(reverse_output=True).reverse().flip().anchor('center').at([0,-3]).label("B")
        T2 = elm.CurrentTransactor().reverse().flip().anchor('center').at([0,-6]).label("D")
        T3 = elm.VoltageTransactor().reverse().anchor('center').at([0,-9]).label("A")
        T4 = elm.TransadmittanceTransactor(reverse_output=True).reverse().anchor('center').at([0,-12]).label("C")

        ## make connections
        # right side
        elm.Line().at(N1.out_n).to(T1.in_n)
        elm.Line().at(T1.in_p).to(T2.in_n)
        elm.Line().at(T3.in_n).to(T4.in_n)

        elm.Line().right().length(1).at(N1.out_p)
        pre_out = d.here
        outline = elm.Line().right().length(1).dot(open=True)
        out = d.here
        elm.Gap().down().label(('+','$V_o$','–')).toy(N1.out_n)
        elm.Line().idot(open=True).down().toy(T4.in_n)
        elm.Line().left().to(T4.in_n)
        elm.Dot()
        elm.CurrentLabelInline(direction='in', ofst=-0.15).at(outline).label('$I_o$')

        elm.Line().at(T2.in_p).right().tox(out)
        elm.Dot()

        elm.Line().right().at(T4.in_p).tox(pre_out)
        elm.Line().up().toy(pre_out)
        elm.Dot()

        elm.Line().right().at(T3.in_p).tox(pre_out)
        elm.Dot()

        # left side
        elm.Line().down().at(N1.in_n).to(T1.out_n)

        elm.Line().up().at(T3.out_p).to(T1.out_p)

        elm.Line().left().at(N1.in_p).length(1)
        pre_in = d.here
        inline = elm.Line().length(1).dot(open=True).left()
        in_node = d.here
        elm.Gap().down().label(('+','$V_i$','–')).toy(N1.in_n)
        elm.Line().idot(open=True).down().toy(T4.out_n)
        elm.Line().right().to(T4.out_n)
        elm.CurrentLabelInline(direction='out', ofst=-0.15).at(inline).label('$I_i$')

        elm.Line().left().at(T2.out_p).tox(in_node)
        elm.Dot()
        elm.Line().left().at(T3.out_n).tox(in_node)
        elm.Dot()

        elm.Line().left().at(T4.out_p).tox(pre_in)
        elm.Line().up().toy(pre_in)
        elm.Dot()

        elm.Line().left().at(T2.out_n).tox(pre_in)
        elm.Dot()