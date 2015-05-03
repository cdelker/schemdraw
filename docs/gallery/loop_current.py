import sys
sys.path.insert(0, '../../')
import SchemDraw as schem
import SchemDraw.elements as e

d = schem.Drawing(unit=5)
V1 = d.add( e.SOURCE_V, label='$20V$' )
R1 = d.add( e.RES, d='right', label='400$\Omega$' )
d.add( e.DOT )
d.push()
R2 = d.add( e.RES, d='down' )
R2.add_label( '100$\Omega$', loc='center', ofst=[-.9,.05] )
d.add( e.DOT )
d.pop()
L1 = d.add( e.LINE )
I1 = d.add( e.SOURCE_I, d='down', botlabel='1A' )
L2 = d.add( e.LINE, d='left', tox=V1.start )
d.loopI( [R1,R2,L2,V1], '$I_1$', pad=1.25 )
d.loopI( [R1,I1,L2,R2], '$I_2$', pad=1.25 )  # Use R1 as top element for both so they get the same height
d.draw(showplot=False)
d.save('loop_current.png')