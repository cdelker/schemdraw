Integrated Circuits
-------------------

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


555 LED Blinker Circuit
^^^^^^^^^^^^^^^^^^^^^^^

Using the `Ic` class to define a custom integrated circuit.

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


Arduino Board
^^^^^^^^^^^^^

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


    d = schemdraw.Drawing(fontsize=11, inches_per_unit=.4)
    Q1 = d.add(Atmega328())
    JP4 = d.add(elm.Header(rows=10, shownumber=True, flip=True, at=[Q1.PB5[0]+4, Q1.PB5[1]+1], anchor='p6', label='JP4', fontsize=10,
                           pinsright=['D8', 'D9', 'D10', 'D11', 'D12', 'D13', '', '', '', ''], pinalignright='center'))
    JP3 = d.add(elm.Header(rows=6, shownumber=True, flip=True, at=[Q1.PC5[0]+4, Q1.PC5[1]], anchor='p6', label='JP3', fontsize=10,
                           pinsright=['A0', 'A1', 'A2', 'A3', 'A4', 'A5'], pinalignright='center'))

    JP2 = d.add(elm.Header(rows=8, shownumber=True, flip=True, at=[Q1.PD7[0]+3, Q1.PD7[1]], anchor='p8', label='JP2', fontsize=10,
                           pinsright=['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'], pinalignright='center'))

    d.add(elm.OrthoLines(at=Q1.PB5, to=JP4.p6, n=6))
    d.add(elm.OrthoLines(at=Q1.PC5, to=JP3.p6, n=6))
    d.add(elm.OrthoLines(at=Q1.PD7, to=JP2.p8, n=8))

    d.add(elm.Line('l', at=JP4.p7, l=.9, lftlabel='GND'))
    d.add(elm.Line('l', at=JP4.p8, l=.9, lftlabel='AREF'))
    d.add(elm.Line('l', at=JP4.p9, l=.9, lftlabel='AD4/SDA'))
    d.add(elm.Line('l', at=JP4.p10, l=.9, lftlabel='AD5/SCL'))

    JP1 = d.add(elm.Header('r', at=[Q1.PD0[0]+4, Q1.PD0[1]-2], rows=6, anchor='p1', shownumber=True,
                           pinsright=['VCC', 'RXD', 'TXD', 'DTR', 'RTS', 'GND'], pinalignright='center'))
    d.add(elm.Line('l', at=JP1.p1, l=d.unit/2))
    d.add(elm.Vdd(label='+5V'))
    d.add(elm.Line('l', at=JP1.p2, l=d.unit))
    d.add(elm.Line('u', toy=Q1.PD0))
    d.add(elm.Dot)
    d.add(elm.Line('l', at=JP1.p3, l=d.unit+0.6))
    d.add(elm.Line('u', toy=Q1.PD1))
    d.add(elm.Dot)
    d.add(elm.Line('l', at=JP1.p6, l=d.unit/2))
    d.add(elm.Ground)

    d.add(elm.Line('l', at=Q1.XTAL2, l=d.unit*2))
    d.add(elm.Dot)
    d.push()
    d.add(elm.Capacitor('l', zoom=.75, l=d.unit/2))
    d.add(elm.Line('d', toy=Q1.XTAL1))
    d.add(elm.Dot)
    d.add(elm.Ground)
    d.add(elm.Capacitor('r', zoom=.75, l=d.unit/2))
    d.add(elm.Dot)
    d.pop()
    d.add(elm.Crystal('d', botlabel='16MHz', toy=Q1.XTAL1))
    d.add(elm.Line('r', tox=Q1.XTAL1))

    d.add(elm.Line('l', at=Q1.AREF, l=d.unit/3, lftlabel='AREF'))
    d.add(elm.Line('l', at=Q1.AVCC, l=1.5*d.unit))
    d.add(elm.Vdd(label='+5V'))
    d.add(elm.Dot)
    d.add(elm.Line('d', toy=Q1.VCC))
    d.add(elm.Dot)
    d.add(elm.Line('r', tox=Q1.VCC, move_cur=False))
    d.add(elm.Capacitor('d', label='100n'))
    GND = d.add(elm.Ground)

    d.add(elm.Line('l', at=Q1.AGND))
    d.add(elm.Line('d', toy=Q1.GND))
    d.add(elm.Dot)
    d.add(elm.Line('r', tox=Q1.GND, move_cur=False))
    d.add(elm.Line('d', toy=GND.xy))
    d.add(elm.Line('l', tox=GND.xy))
    d.add(elm.Dot)

    d.add(elm.Line('l', at=Q1.RESET))
    d.add(elm.Dot)
    d.push()
    d.add(elm.RBox('u', label='10K'))
    d.add(elm.Vdd(label='+5V'))
    d.pop()
    d.add(elm.Line('l'))
    d.push()
    d.add(elm.Dot)
    RST = d.add(elm.Button('up', label='Reset'))
    d.add(elm.Line('l', l=d.unit/2))
    d.add(elm.Ground)
    d.pop()

    d.add(elm.Capacitor('l', at=JP1.p4, botlabel='100n'))
    d.add(elm.Line('l', tox=RST.start[0]-2))
    d.add(elm.Line('u', toy=Q1.RESET))
    d.add(elm.Line('r', tox=RST.start))

    d.draw()

