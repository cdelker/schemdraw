Integrated Circuits
-------------------

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


555 LED Blinker Circuit
^^^^^^^^^^^^^^^^^^^^^^^

Using the :py:class:`schemdraw.elements.intcircuits.Ic` class to define a custom integrated circuit.

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
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
                           pinspacing=1.5,
                           leadlen=1,
                           label='555')
        d += (T := IC555def)
        d += (BOT := elm.Ground().at(T.GND))
        d += elm.Dot()
        d += elm.Resistor().endpoints(T.DIS, T.THR).label('Rb').idot()
        d += elm.Resistor().up().at(T.DIS).label('Ra').label('+Vcc', 'right')
        d += elm.Line().endpoints(T.THR, T.TRG)
        d += elm.Capacitor().at(T.TRG).toy(BOT.start).label('C')
        d += elm.Line().tox(BOT.start)
        d += elm.Capacitor().at(T.CTL).toy(BOT.start).label('.01$\mu$F', 'bottom').dot()
        d += elm.Dot().at(T.DIS)
        d += elm.Dot().at(T.THR)
        d += elm.Dot().at(T.TRG)
        d += elm.Line().endpoints(T.RST,T.Vcc).dot()
        d += elm.Line().up(d.unit/4).label('+Vcc', 'right')
        d += elm.Resistor().right().at(T.OUT).label('330')
        d += elm.LED().flip().toy(BOT.start)
        d += elm.Line().tox(BOT.start)


Seven-Segment Display Counter
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
        d += (IC555 := elm.Ic555())
        d += (gnd := elm.Ground(xy=IC555.GND))
        d += elm.Dot()
        d += elm.Resistor().endpoints(IC555.DIS, IC555.THR).label('100 kΩ')
        d += elm.Resistor().up().at(IC555.DIS).label('1 kΩ').label('+Vcc', 'right')
        d += elm.Line().endpoints(IC555.THR, IC555.TRG)
        d += elm.Capacitor(polar=True).at(IC555.TRG).toy(gnd.start).label('10 μF')
        d += elm.Line().tox(gnd.start)
        d += elm.Capacitor().at(IC555.CTL).toy(gnd.start).label('.01 μF', 'bottom')
        d += elm.Line().tox(gnd.start)

        d += elm.Dot().at(IC555.DIS)
        d += elm.Dot().at(IC555.THR)
        d += elm.Dot().at(IC555.TRG)
        d += elm.Line().endpoints(IC555.RST,IC555.Vcc).dot()
        d += elm.Line().up(d.unit/4).label('+Vcc', 'right')

        IC4026 = elm.Ic(pins=[elm.IcPin('CLK', pin='1', side='left'),
                              elm.IcPin('INH', pin='2', side='left'), # Inhibit
                              elm.IcPin('RST', pin='15', side='left'),
                              elm.IcPin('DEI', pin='3', side='left'), # Display Enable In
                              elm.IcPin('Vss', pin='8', side='bot'),
                              elm.IcPin('Vdd', pin='16', side='top'),
                              elm.IcPin('UCS', pin='14', side='bot'), # Ungated C Segment
                              elm.IcPin('DEO', pin='4', side='bot'),  # Display Enable Out
                              elm.IcPin('Co', pin='4', side='bot'),   # Carry out
                              elm.IcPin('g', pin='7', side='right'),
                              elm.IcPin('f', pin='6', side='right'),                      
                              elm.IcPin('e', pin='11', side='right'),
                              elm.IcPin('d', pin='9', side='right'),
                              elm.IcPin('c', pin='13', side='right'),
                              elm.IcPin('b', pin='12', side='right'),
                              elm.IcPin('a', pin='10', side='right'),
                             ],
                       w=4, leadlen=.8).label('4026').right()

        d.move_from(IC555.OUT, dx=5, dy=-1)
        d += IC4026.anchor('center')
        d += elm.Wire('c').at(IC555.OUT).to(IC4026.CLK)
        d += elm.Line().endpoints(IC4026.INH, IC4026.RST).dot()
        d += elm.Line().left(d.unit/4)
        d += elm.Ground()
        d += elm.Wire('|-').at(IC4026.DEI).to(IC4026.Vdd).dot()
        d += elm.Line().up(d.unit/4).label('+Vcc', 'right')
        d += elm.Line().at(IC4026.Vss).tox(IC4026.UCS).dot()
        d += elm.Ground()
        d += elm.Line().tox(IC4026.DEO).dot()
        d += elm.Line().tox(IC4026.Co)

        d += elm.Resistor().right().at(IC4026.a)
        d += (disp := elm.SevenSegment(cathode=True).anchor('a'))
        d += elm.Resistor().at(IC4026.b)
        d += elm.Resistor().at(IC4026.c)
        d += elm.Resistor().at(IC4026.d)
        d += elm.Resistor().at(IC4026.e)
        d += elm.Resistor().at(IC4026.f)
        d += elm.Resistor().at(IC4026.g).label('7 x 330', loc='bottom')
        d += elm.Ground(lead=False).at(disp.cathode)


Arduino Board
^^^^^^^^^^^^^

The Arduino board uses :py:class:`schemdraw.elements.connectors.OrthoLines` to easily add all connections between data bus and headers.

.. jupyter-execute::
    :code-below:

    class Atmega328(elm.Ic):
        def __init__(self, *args, **kwargs):
            pins=[elm.IcPin(name='PD0', pin='2', side='r', slot='1/22'),
                  elm.IcPin(name='PD1', pin='3', side='r', slot='2/22'),
                  elm.IcPin(name='PD2', pin='4', side='r', slot='3/22'),
                  elm.IcPin(name='PD3', pin='5', side='r', slot='4/22'),
                  elm.IcPin(name='PD4', pin='6', side='r', slot='5/22'),
                  elm.IcPin(name='PD5', pin='11', side='r', slot='6/22'),             
                  elm.IcPin(name='PD6', pin='12', side='r', slot='7/22'),             
                  elm.IcPin(name='PD7', pin='13', side='r', slot='8/22'),
                  elm.IcPin(name='PC0', pin='23', side='r', slot='10/22'),
                  elm.IcPin(name='PC1', pin='24', side='r', slot='11/22'),
                  elm.IcPin(name='PC2', pin='25', side='r', slot='12/22'),
                  elm.IcPin(name='PC3', pin='26', side='r', slot='13/22'),
                  elm.IcPin(name='PC4', pin='27', side='r', slot='14/22'),
                  elm.IcPin(name='PC5', pin='28', side='r', slot='15/22'),
                  elm.IcPin(name='PB0', pin='14', side='r', slot='17/22'),
                  elm.IcPin(name='PB1', pin='15', side='r', slot='18/22'),
                  elm.IcPin(name='PB2', pin='16', side='r', slot='19/22'),
                  elm.IcPin(name='PB3', pin='17', side='r', slot='20/22'),
                  elm.IcPin(name='PB4', pin='18', side='r', slot='21/22'),
                  elm.IcPin(name='PB5', pin='19', side='r', slot='22/22'),

                  elm.IcPin(name='RESET', side='l', slot='22/22', invert=True, pin='1'),
                  elm.IcPin(name='XTAL2', side='l', slot='19/22', pin='10'),
                  elm.IcPin(name='XTAL1', side='l', slot='17/22', pin='9'),
                  elm.IcPin(name='AREF', side='l', slot='15/22', pin='21'),
                  elm.IcPin(name='AVCC', side='l', slot='14/22', pin='20'),
                  elm.IcPin(name='AGND', side='l', slot='13/22', pin='22'),
                  elm.IcPin(name='VCC', side='l', slot='11/22', pin='7'),
                  elm.IcPin(name='GND', side='l', slot='10/22', pin='8')]
            super().__init__(pins=pins, w=5, plblofst=.05, botlabel='ATMEGA328', **kwargs)


    with schemdraw.Drawing() as d:
        d.config(fontsize=11, inches_per_unit=.4)
        d += (Q1 := Atmega328())
        d += (JP4 := elm.Header(rows=10, shownumber=True, pinsright=['D8', 'D9', 'D10', 'D11', 'D12', 'D13', '', '', '', ''], pinalignright='center')
                                .flip().at(Q1.PB5, dx=4, dy=1).anchor('pin6').label('JP4', fontsize=10))

        d += (JP3 := elm.Header(rows=6, shownumber=True, pinsright=['A0', 'A1', 'A2', 'A3', 'A4', 'A5'], pinalignright='center')
                            .flip().at(Q1.PC5, dx=4).anchor('pin6').label('JP3', fontsize=10))

        d += (JP2 := elm.Header(rows=8, shownumber=True, pinsright=['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'],
                                pinalignright='center')).at(Q1.PD7, dx=3).flip().anchor('pin8').label('JP2', fontsize=10)

        d += elm.OrthoLines(n=6).at(Q1.PB5).to(JP4.pin6)
        d += elm.OrthoLines(n=6).at(Q1.PC5).to(JP3.pin6)
        d += elm.OrthoLines(n=8).at(Q1.PD7).to(JP2.pin8)

        d += elm.Line().left(.9).at(JP4.pin7).label('GND', 'left')
        d += elm.Line().left(.9).at(JP4.pin8).label('AREF', 'left')
        d += elm.Line().left(.9).at(JP4.pin9).label('AD4/SDA', 'left')
        d += elm.Line().left(.9).at(JP4.pin10).label('AD5/SCL', 'left')

        d += (JP1 := elm.Header(rows=6, shownumber=True, pinsright=['VCC', 'RXD', 'TXD', 'DTR', 'RTS', 'GND'],
                                pinalignright='center').right().at(Q1.PD0, dx=4, dy=-2).anchor('pin1'))
        d += elm.Line().left(d.unit/2).at(JP1.pin1)
        d += elm.Vdd().label('+5V')
        d += elm.Line().left().at(JP1.pin2)
        d += elm.Line().toy(Q1.PD0).dot()
        d += elm.Line().left(d.unit+.6).at(JP1.pin3)
        d += elm.Line().toy(Q1.PD1).dot()
        d += elm.Line().left(d.unit/2).at(JP1.pin6)
        d += elm.Ground()

        d += elm.Line().left(d.unit*2).at(Q1.XTAL2).dot()
        d.push()
        d += elm.Capacitor().left(d.unit/2).scale(.75)
        d += elm.Line().toy(Q1.XTAL1).dot()
        d += elm.Ground()
        d += elm.Capacitor().right(d.unit/2).scale(.75).dot()
        d.pop()
        d += elm.Crystal().toy(Q1.XTAL1).label('16MHz', 'bottom')
        d += elm.Line().tox(Q1.XTAL1)

        d += elm.Line().left(d.unit/3).at(Q1.AREF).label('AREF', 'left')
        d += elm.Line().left(1.5*d.unit).at(Q1.AVCC)
        d += elm.Vdd().label('+5V')
        d += elm.Line().toy(Q1.VCC).dot().idot()
        d += elm.Line().tox(Q1.VCC).hold()
        d += elm.Capacitor().down().label('100n')
        d += (GND := elm.Ground())

        d += elm.Line().left().at(Q1.AGND)
        d += elm.Line().toy(Q1.GND).dot()
        d += elm.Line().tox(Q1.GND).hold()
        d += elm.Wire('|-').to(GND.center).dot()

        d += elm.Line().left().at(Q1.RESET).dot()
        d.push()
        d += elm.RBox().up().label('10K')
        d += elm.Vdd().label('+5V')
        d.pop()
        d += elm.Line().left().dot()
        d.push()
        d += (RST := elm.Button().up().label('Reset'))
        d += elm.Line().left(d.unit/2)
        d += elm.Ground()
        d.pop()

        d += elm.Capacitor().left().at(JP1.pin4).label('100n', 'bottom')
        d += elm.Wire('c', k=-16).to(RST.start)


.. _dip741:

741 Opamp, DIP Layout
^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d += (Q := elm.IcDIP(pins=8)
                     .label('Offset Null', loc='p1', fontsize=10)
                     .label('Inverting Input', loc='p2', fontsize=10)
                     .label('Non-inverting Input', loc='p3', fontsize=10)
                     .label('V-', loc='p4', fontsize=10)
                     .label('Offset Null', loc='p5', fontsize=10)
                     .label('Output', loc='p6', fontsize=10)
                     .label('V+', loc='p7', fontsize=10)
                     .label('NC', loc='p8', fontsize=10))
        d += elm.Line().at(Q.p2_in).length(d.unit/5)
        d += (op := elm.Opamp().anchor('in1').scale(.8))
        d += elm.Line().at(Q.p3_in).length(d.unit/5)
        d += elm.Wire('c', k=.3).at(op.out).to(Q.p6_in)
        d += elm.Wire('-|').at(Q.p4_in).to(op.n1)
        d += elm.Wire('-|').at(Q.p7_in).to(op.n2)
