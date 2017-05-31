import matplotlib.pyplot as plt
plt.xkcd()

import SchemDraw as schem
import SchemDraw.elements as e

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
d.draw(showplot=False)
d.save('SRxkcd.svg')