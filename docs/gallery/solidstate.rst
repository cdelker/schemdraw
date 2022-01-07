Solid State
-----------

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


S-R Latch (Transistors)
^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d += (Q1 := elm.BjtNpn(circle=True).reverse().label('Q1', 'left'))
        d += (Q2 := elm.BjtNpn(circle=True).at((d.unit*2, 0)).label('Q2'))
        d += elm.Line().up(d.unit/2).at(Q1.collector)

        d += (R1 := elm.Resistor().up().label('R1').hold())
        d += elm.Dot().label('V1', 'left')
        d += elm.Resistor().right(d.unit*.75).label('R3', 'bottom').dot()
        d += elm.Line().up(d.unit/8).dot(open=True).label('Set', 'right').hold()
        d += elm.Line().to(Q2.base)

        d += elm.Line().up(d.unit/2).at(Q2.collector)
        d += elm.Dot().label('V2', 'right')
        d += (R2 := elm.Resistor().up().label('R2', 'bottom').hold())
        d += elm.Resistor().left(d.unit*.75).label('R4', 'bottom').dot()
        d += elm.Line().up(d.unit/8).dot(open=True).label('Reset', 'right').hold()
        d += elm.Line().to(Q1.base)

        d += elm.Line().down(d.unit/4).at(Q1.emitter)
        d += (BOT := elm.Line().tox(Q2.emitter))
        d += elm.Line().to(Q2.emitter)
        d += elm.Dot().at(BOT.center)
        d += elm.Ground().at(BOT.center)

        d += (TOP := elm.Line().endpoints(R1.end, R2.end))
        d += elm.Dot().at(TOP.center)
        d += elm.Vdd().at(TOP.center).label('+Vcc')


741 Opamp Internal Schematic
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(fontsize=12, unit=2.5)
        d += (Q1 := elm.BjtNpn().label('Q1').label('+IN', 'left'))
        d += (Q3 := elm.BjtPnp().left().at(Q1.emitter).anchor('emitter').flip().label('Q3', 'left'))
        d += elm.Line().down().at(Q3.collector).dot()
        d.push()
        d += elm.Line().right(d.unit/4)
        d += (Q7 := elm.BjtNpn().anchor('base').label('Q7'))
        d.pop()
        d += elm.Line().down(d.unit*1.25)
        d += (Q5 := elm.BjtNpn().left().flip().anchor('collector').label('Q5', 'left'))
        d += elm.Line().left(d.unit/2).at(Q5.emitter).label('OFST\nNULL', 'left').flip()
        d += elm.Resistor().down().at(Q5.emitter).label('R1\n1K')
        d += elm.Line().right(d.unit*.75).dot()
        d += (R3 := elm.Resistor().up().label('R3\n50K'))
        d += elm.Line().toy(Q5.base).dot()
        d.push()
        d += elm.Line().left().to(Q5.base)
        d += elm.Line().at(Q7.emitter).toy(Q5.base).dot()
        d.pop()
        d += elm.Line().right(d.unit/4)
        d += (Q6 := elm.BjtNpn().anchor('base').label('Q6'))
        d += elm.Line().at(Q6.emitter).length(d.unit/3).label('\nOFST\nNULL', 'right').hold()
        d += elm.Resistor().down().at(Q6.emitter).label('R2\n1K').dot()

        d += elm.Line().at(Q6.collector).toy(Q3.collector)
        d += (Q4 := elm.BjtPnp().right().anchor('collector').label('Q4'))
        d += elm.Line().at(Q4.base).tox(Q3.base)
        d += elm.Line().at(Q4.emitter).toy(Q1.emitter)
        d += (Q2 := elm.BjtNpn().left().flip().anchor('emitter').label('Q2', 'left').label('$-$IN', 'right'))
        d += elm.Line().up(d.unit/3).at(Q2.collector).dot()
        d += (Q8 := elm.BjtPnp().left().flip().anchor('base').label('Q8', 'left'))
        d += elm.Line().at(Q8.collector).toy(Q2.collector).dot()
        d += elm.Line().at(Q2.collector).tox(Q1.collector)
        d += elm.Line().up(d.unit/4).at(Q8.emitter)
        d += (top := elm.Line().tox(Q7.collector))
        d += elm.Line().toy(Q7.collector)

        d += elm.Line().right(d.unit*2).at(top.start)
        d += elm.Line().down(d.unit/4)
        d += (Q9 := elm.BjtPnp().right().anchor('emitter').label('Q9', ofst=-.1))
        d += elm.Line().at(Q9.base).tox(Q8.base)
        d += elm.Dot().at(Q4.base)
        d += elm.Line().down(d.unit/2).at(Q4.base)
        d += elm.Line().tox(Q9.collector).dot()
        d += elm.Line().at(Q9.collector).toy(Q6.collector)
        d += (Q10 := elm.BjtNpn().left().flip().anchor('collector').label('Q10', 'left'))
        d += elm.Resistor().at(Q10.emitter).toy(R3.start).label('R4\n5K').dot()

        d += (Q11 := elm.BjtNpn().right().at(Q10.base).anchor('base').label('Q11'))
        d += elm.Dot().at(Q11.base)
        d += elm.Line().up(d.unit/2)
        d += elm.Line().tox(Q11.collector).dot()
        d += elm.Line().at(Q11.emitter).toy(R3.start).dot()
        d += elm.Line().up(d.unit*2).at(Q11.collector)
        d += elm.Resistor().toy(Q9.collector).label('R5\n39K')
        d += (Q12 := elm.BjtPnp().left().flip().anchor('collector').label('Q12', 'left', ofst=-.1))
        d += elm.Line().up(d.unit/4).at(Q12.emitter).dot()
        d += elm.Line().tox(Q9.emitter).dot()
        d += elm.Line().right(d.unit/4).at(Q12.base).dot()
        d += elm.Wire('|-').to(Q12.collector).dot().hold()
        d += elm.Line().right(d.unit*1.5)
        d += (Q13 := elm.BjtPnp().anchor('base').label('Q13'))
        d += elm.Line().up(d.unit/4).dot()
        d += elm.Line().tox(Q12.emitter)
        d += (K := elm.Line().down(d.unit/5).at(Q13.collector).dot())
        d += elm.Line().down()
        d += (Q16 := elm.BjtNpn().right().anchor('collector').label('Q16', ofst=-.1))
        d += elm.Line().left(d.unit/3).at(Q16.base).dot()
        d += (R7 := elm.Resistor().up().toy(K.end).label('R7\n4.5K').dot())
        d += elm.Line().tox(Q13.collector).hold()
        d += (R8 := elm.Resistor().down().at(R7.start).label('R8\n7.5K').dot())
        d += elm.Line().tox(Q16.emitter)
        d += (J := elm.Dot())
        d += elm.Line().toy(Q16.emitter)
        d += (Q15 := elm.BjtNpn().right().at(R8.end).anchor('collector').label('Q15'))
        d += elm.Line().left(d.unit/2).at(Q15.base).dot()
        d += (C1 := elm.Capacitor().toy(R7.end).label('C1\n30pF'))
        d += elm.Line().tox(Q13.collector)
        d += elm.Line().at(C1.start).tox(Q6.collector).dot()
        d += elm.Line().down(d.unit/2).at(J.center)
        d += (Q19 := elm.BjtNpn().right().anchor('collector').label('Q19'))
        d += elm.Line().at(Q19.base).tox(Q15.emitter).dot()
        d += elm.Line().toy(Q15.emitter).hold()
        d += elm.Line().down(d.unit/4).at(Q19.emitter).dot()
        d += elm.Line().left()
        d += (Q22 := elm.BjtNpn().left().anchor('base').flip().label('Q22', 'left'))
        d += elm.Line().at(Q22.collector).toy(Q15.base).dot()
        d += elm.Line().at(Q22.emitter).toy(R3.start).dot()
        d += elm.Line().tox(R3.start).hold()
        d += elm.Line().tox(Q15.emitter).dot()
        d.push()
        d += elm.Resistor().up().label('R12\n50K')
        d += elm.Line().toy(Q19.base)
        d.pop()
        d += elm.Line().tox(Q19.emitter).dot()
        d += (R11 := elm.Resistor().up().label('R11\n50'))
        d += elm.Line().toy(Q19.emitter)

        d += elm.Line().up(d.unit/4).at(Q13.emitter)
        d += elm.Line().right(d.unit*1.5).dot()
        d += elm.Line().length(d.unit/4).label('V+', 'right').hold()
        d += elm.Line().down(d.unit*.75)
        d += (Q14 := elm.BjtNpn().right().anchor('collector').label('Q14'))
        d += elm.Line().left(d.unit/2).at(Q14.base)
        d.push()
        d += elm.Line().down(d.unit/2).idot()
        d += (Q17 := elm.BjtNpn().left().anchor('collector').flip().label('Q17', 'left', ofst=-.1))
        d += elm.Line().at(Q17.base).tox(Q14.emitter).dot()
        d += (J := elm.Line().toy(Q14.emitter))
        d.pop()
        d += elm.Line().tox(Q13.collector).dot()
        d += elm.Resistor().down().at(J.start).label('R9\n25').dot()
        d += elm.Wire('-|').to(Q17.emitter).hold()
        d += elm.Line().down(d.unit/4).dot()
        d += elm.Line().right(d.unit/4).label('OUT', 'right').hold()
        d += elm.Resistor().down().label('R10\n50')
        d += (Q20 := elm.BjtPnp().right().anchor('emitter').label('Q20'))
        d += elm.Wire('c', k=-1).at(Q20.base).to(Q15.collector)
        d += elm.Line().at(Q20.collector).toy(R3.start).dot()
        d += elm.Line().right(d.unit/4).label('V-', 'right').hold()
        d += elm.Line().tox(R11.start)
