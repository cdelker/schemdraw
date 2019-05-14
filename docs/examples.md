<link rel="stylesheet" href="css/codehilite.css">

## Examples

Following are examples of more complicated circuit diagrams. Most are useless circuits made for torturing ECE201 students. Further examples can be found in the Jupyter notebooks in the docs folder or the [gallery](gallery.html).


### Example 1

This example demonstrates use of `push()` and `pop()` and using 'tox' and 'toy' keywords.

    :::python
    d = schem.Drawing(unit=2)  # unit=2 makes elements with shorter than normal leads
    d.push()
    R1 = d.add(e.RES, d='down', label='20$\Omega$')
    V1 = d.add(e.SOURCE_V, d='down', reverse=True, label='120V')
    d.add(e.LINE, d='right', l=3)
    d.add(e.DOT)
    d.pop()
    d.add(e.LINE, d='right', l=3)
    d.add(e.DOT)
    d.add(e.SOURCE_V, d='down', label='60V', reverse=True)
    d.add(e.RES, label='5$\Omega$')
    d.add(e.DOT)
    d.add(e.LINE, d='right', l=3)
    d.add(e.SOURCE_I, d='up', label='36A')
    d.add(e.RES, label='10$\Omega$')
    d.add(e.DOT)
    d.add(e.LINE, d='left', l=3, move_cur=False)
    d.add(e.LINE, d='right', l=3)
    d.add(e.DOT)
    R6 = d.add(e.RES, d='down', toy=V1.start, label='6$\Omega$')
    d.add(e.DOT)
    d.add(e.LINE, d='left', l=3, move_cur=False)
    d.add(e.RES, d='right', xy=R6.start, label='1.6$\Omega$')
    d.add(e.DOT, label='a')
    d.add(e.LINE, d='right', xy=R6.end)
    d.add(e.DOT, label='b')
    d.draw()

![](img/ex01.svg)


### Capacitor discharging

Shows how to connect to a switch element anchors.

    :::python
    d = schem.Drawing()
    V1 = d.add(e.SOURCE_V, label='5V')
    d.add(e.LINE, d='right', l=d.unit*.75)
    S1 = d.add(e.SWITCH_SPDT2_CLOSE, d='up', anchor='b', rgtlabel='$t=0$')
    d.add(e.LINE, d='right', xy=S1.c,  l=d.unit*.75)
    d.add(e.RES, d='down', label='$100\Omega$', botlabel=['+','$v_o$','-'])
    d.add(e.LINE, to=V1.start)
    d.add(e.CAP, xy=S1.a, d='down', toy=V1.start, label='1$\mu$F')
    d.add(e.DOT)
    d.draw()

![](img/cap-charge.svg)


### Inverting Opamp

Shows how to connect to an opamp

    :::python
    d = schem.Drawing(inches_per_unit=.5)
    op = d.add(e.OPAMP)
    d.add(e.LINE, d='left', xy=op.in2, l=d.unit/4)
    d.add(e.LINE, d='down', l=d.unit/5)
    d.add(e.GND)
    d.add(e.LINE, d='left', xy=op.in1, l=d.unit/6)
    d.add(e.DOT)
    d.push()
    Rin = d.add(e.RES, d='left', xy=op.in1-[d.unit/5,0], botlabel='$R_{in}$', lftlabel='$v_{in}$')
    d.pop()
    d.add(e.LINE, d='up', l=d.unit/2)
    Rf = d.add(e.RES,  d='right', l=d.unit*1, label='$R_f$')
    d.add(e.LINE, d='down', toy=op.out)
    d.add(e.DOT)
    d.add(e.LINE, d='left', tox=op.out)
    d.add(e.LINE, d='right', l=d.unit/4, rgtlabel='$v_{o}$')
    d.draw()

![](img/inv_opamp.svg)


### Capacitor network

Another good problem to torture ECE201 students. Shows how to place an element using 'endpts' to cross a diagonal.

    :::python
    d = schem.Drawing()
    A  = d.add(e.DOT, label='a')
    C1 = d.add(e.CAP, label='8nF')
    C2 = d.add(e.CAP, label='18nF')
    C3 = d.add(e.CAP, botlabel='8nF', d='down')
    C4 = d.add(e.CAP, botlabel='32nF', d='left')
    C5 = d.add(e.CAP, botlabel='40nF')
    B  = d.add(e.DOT, label='b')
    C6 = d.add(e.CAP, label='2.8nF', endpts=[C1.end,C5.start])
    C7 = d.add(e.CAP, endpts=[C2.end,C5.start])
    C7.add_label('5.6nF', loc='center', ofst=[-.3,-.1], align=('right','bottom'))
    d.draw()

![](img/cap-net.svg)


### S-R Latch

Demonstrates using transistors

    :::python
    d = schem.Drawing()
    Q1 = d.add(e.BJT_NPN_C, reverse=True, lftlabel='Q1')
    Q2 = d.add(e.BJT_NPN_C, xy=[d.unit*2,0], label='Q2')
    d.add(e.LINE, xy=Q1.collector, d='up', l=d.unit/2)

    R1 = d.add(e.RES, d='up', label='R1', move_cur=False)
    d.add(e.DOT, lftlabel='V1')
    d.add(e.RES, d='right', botlabel='R3', l=d.unit*.75)
    d.add(e.DOT)
    d.push()
    d.add(e.LINE, d='up', l=d.unit/8)
    d.add(e.DOT_OPEN, label='Set')
    d.pop()
    d.add(e.LINE, to=Q2.base)

    d.add(e.LINE, xy=Q2.collector, d='up', l=d.unit/2)
    d.add(e.DOT, rgtlabel='V2')
    R2 = d.add(e.RES, d='up', botlabel='R2', move_cur=False)
    d.add(e.RES, d='left', botlabel='R4', l=d.unit*.75)
    d.add(e.DOT)
    d.push()
    d.add(e.LINE, d='up', l=d.unit/8)
    d.add(e.DOT_OPEN, label='Reset')
    d.pop()
    d.add(e.LINE, to=Q1.base)

    d.add(e.LINE, xy=Q1.emitter, d='down', l=d.unit/4)
    BOT = d.add(e.LINE, d='right', tox=Q2.emitter)
    d.add(e.LINE, to=Q2.emitter)
    d.add(e.DOT, xy=BOT.center)
    d.add(e.GND, xy=BOT.center)

    TOP = d.add(e.LINE, endpts=[R1.end,R2.end])
    d.add(e.DOT, xy=TOP.center)
    d.add(e.LINE, xy=TOP.center, d='up', l=d.unit/8, rgtlabel='Vcc')
    d.draw()

![](img/SR-Latch.svg)

### Half-adder

Demonstrate using logic gates

    :::python
    d = schem.Drawing(unit=.5)
    S = d.add(l.XOR2, rgtlabel='$S$')
    A = d.add(e.DOT, xy=S.in1)
    d.add(e.LINE, d='left', l=d.unit*2, lftlabel='$A$')
    d.add(e.LINE, d='left', xy=S.in2)
    B = d.add(e.DOT)
    d.add(e.LINE, d='left', lftlabel='$B$')
    d.add(e.LINE, d='down', xy=A.start, l=d.unit*3)
    C = d.add(l.AND2, d='right', anchor='in1', rgtlabel='$C$')
    d.add(e.LINE, d='down', xy=B.start, toy=C.in2)
    d.add(e.LINE, to=C.in2)
    d.draw()

![](img/half_add.svg)

### JK Flip-flop

A slightly more complicated logic gate example. Note the use of the LaTeX command **\\overline{Q}** in the label to draw a bar over the output label.

    :::python
    d = schem.Drawing()
    # Two front gates (SR latch)
    G1 = d.add(l.NAND2, anchor='in1')
    d.add(e.LINE, l=d.unit/6)
    Q1 = d.add(e.DOT)
    d.add(e.LINE, l=d.unit/6)
    Q2 = d.add(e.DOT)
    d.add(e.LINE, l=d.unit/3, rgtlabel='$Q$')
    G2 = d.add(l.NAND2, anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5])
    d.add(e.LINE, l=d.unit/6)
    Qb = d.add(e.DOT)
    d.add(e.LINE, l=d.unit/3)
    Qb2 = d.add(e.DOT)
    d.add(e.LINE, l=d.unit/6, rgtlabel='$\overline{Q}$')
    S1 = d.add(e.LINE, xy=G2.in1, d='up', l=d.unit/6)
    d.add(e.LINE, d='down', xy=Q1.start, l=d.unit/6)
    d.add(e.LINE, to=S1.end)
    R1 = d.add(e.LINE, xy=G1.in2, d='down', l=d.unit/6)
    d.add(e.LINE, d='up', xy=Qb.start, l=d.unit/6)
    d.add(e.LINE, to=R1.end)

    # Two back gates
    d.add(e.LINE, xy=G1.in1, d='left', l=d.unit/6)
    J = d.add(l.NAND3, anchor='out', reverse=True)
    d.add(e.LINE, xy=J.in3, d='up', l=d.unit/6)
    d.add(e.LINE, d='right', tox=Qb2.start)
    d.add(e.LINE, d='down', toy=Qb2.start)
    d.add(e.LINE, d='left', xy=J.in2, l=d.unit/4, lftlabel='$J$')
    d.add(e.LINE, xy=G2.in2, d='left', l=d.unit/6)
    K = d.add(l.NAND3, anchor='out', reverse=True)
    d.add(e.LINE, xy=K.in1, d='down', l=d.unit/6)
    d.add(e.LINE, d='right', tox=Q2.start)
    d.add(e.LINE, d='up', toy=Q2.start)
    d.add(e.LINE, d='left', xy=K.in2, l=d.unit/4, lftlabel='$K$')
    C = d.add(e.LINE, d='down', xy=J.in1, toy=K.in3)
    d.add(e.DOT, xy=C.center)
    d.add(e.LINE, d='left', xy=C.center, l=d.unit/4, lftlabel='$CLK$')
    d.draw()

![](img/JK.svg)


### 555-timer circuit

This example shows use of the `blackbox()` function to draw a 555-timer integrated circuit.

    :::python
    d = schem.Drawing()
    left = {'cnt':3,
            'labels':['TRG','THR','DIS'],
            'plabels':['2','6','7'],
            'loc':[.2,.35,.75],
            'lblsize':12,
            }
    right = {'cnt':2,
             'labels':['CTL','OUT'],
             'plabels':['5','3'],
            'lblsize':12,
             }
    top = {'cnt':2,
           'labels':['RST','Vcc'],
           'plabels':['4','8'],
           'lblsize':12,
           }
    bot = {'cnt':1,
           'labels':['GND'],
           'plabels':['1'],
           'lblsize':12,
            }

    IC555 = e.blackbox(d.unit*1.5, d.unit*2.25, 
                       linputs=left, rinputs=right, tinputs=top, binputs=bot,
                       leadlen=1, mainlabel='555')
    T = d.add(IC555)
    BOT = d.add(e.GND, xy=T.GND)  # Note: Anchors named same as pin labels
    d.add(e.DOT)
    d.add(e.RES, endpts=[T.DIS, T.THR], label='Rb')
    d.add(e.RES, d='up', xy=T.DIS, label='Ra', rgtlabel='+Vcc')
    d.add(e.LINE, endpts=[T.THR, T.TRG])
    d.add(e.CAP, xy=T.TRG, d='down', toy=BOT.start, label='C', l=d.unit/2)
    d.add(e.LINE, d='right', tox=BOT.start)
    d.add(e.CAP, d='down', xy=T.CTL, toy=BOT.start, botlabel='.01$\mu$F')
    d.add(e.DOT)
    d.add(e.DOT, xy=T.DIS)
    d.add(e.DOT, xy=T.THR)
    d.add(e.DOT, xy=T.TRG)
    d.add(e.LINE, endpts=[T.RST,T.Vcc])
    d.add(e.DOT)
    d.add(e.LINE, d='up', l=d.unit/4, rgtlabel='+Vcc')
    d.add(e.RES, xy=T.OUT, d='right', label='330')
    d.add(e.LED, flip=True, d='down', toy=BOT.start)
    d.add(e.LINE, d='left', tox=BOT.start)
    d.draw()

![](img/555blinker.svg)


------------------------------------------------------
[Return to SchemDraw documentation index](index.html)