Pictorial Schematics
--------------------

.. jupyter-execute::
    :hide-code:

    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import pictorial


LED Blinker
***********

.. jupyter-execute::
    :code-below:

    elm.Line.defaults['lw'] = 4

    with schemdraw.Drawing():
        bb = pictorial.Breadboard().up()
        pictorial.DIP().up().at(bb.E5).label('555', color='#DDD')
        elm.Line().at(bb.A8).to(bb.L1_7)
        elm.Line().at(bb.J5).to(bb.R1_4)
        elm.Line().at(bb.A5).to(bb.L2_4).color('black')
        pictorial.Resistor(330).at(bb.B7).to(bb.B12)
        pictorial.LED(lead_length=.3*pictorial.INCH).at(bb.C12)
        elm.Line().at(bb.A13).to(bb.L2_13).color('black')
        pictorial.Resistor(520).at(bb.G6).to(bb.G3)
        pictorial.Resistor(520).at(bb.J6).to(bb.R1_10)
        elm.Line().at(bb.H3).to(bb.H7).color('green')
        elm.Wire('c').at(bb.G7).to(bb.D6).linewidth(4).color('green')
        elm.Line().at(bb.H8).to(bb.H12).color('green')
        elm.Line().at(bb.J13).to(bb.R2_14).color('black')
        pictorial.CapacitorMylar(lead_length=.2*pictorial.INCH).at(bb.I12)
        elm.Line().at(bb.C6).to(bb.C3).color('green')
        pictorial.CapacitorMylar(lead_length=.2*pictorial.INCH).at(bb.D2)
        elm.Line().at(bb.A2).to(bb.L2_1).color('black')
