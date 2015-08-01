import matplotlib.pyplot as plt

import SchemDraw as schem
import SchemDraw.elements as e

plt.xkcd()

d = schem.Drawing(inches_per_unit=.5)
op = d.add( e.OPAMP )
d.add( e.LINE, d='left', xy=op.in2, l=d.unit/4 )
d.add( e.LINE, d='down', l=d.unit/5 )
d.add( e.GND )
d.add( e.LINE, d='left', xy=op.in1, l=d.unit/6 )
d.add( e.DOT )
d.push()
Rin = d.add( e.RES, d='left', xy=op.in1-[d.unit/5,0], botlabel='$R_{in}$', lftlabel='$v_{in}$' )
d.pop()
d.add( e.LINE, d='up', l=d.unit/2 )
Rf = d.add( e.RES,  d='right', l=d.unit*1, label='$R_f$' )
d.add( e.LINE, d='down', toy=op.out )
d.add( e.DOT )
d.add( e.LINE, d='left', tox=op.out )
d.add( e.LINE, d='right', l=d.unit/4, rgtlabel='$v_{o}$' )

d.draw()

d.save('ex_xkcd.png')