# Another example of grouping elements together. This one defines anchors within the group. 
import SchemDraw as schem
import SchemDraw.elements as e
import numpy as np

# Build a drawing of an SMU
smugp = schem.Drawing(unit=2.2)
smugp.add( e.LINE, d='right', l=smugp.unit/4 )
O1 = smugp.add( e.OPAMP_NOSIGN, anchor='in1' )
I = smugp.add( e.METER_I, d='right', xy=O1.out )
smugp.add( e.DOT )
smugp.push()
smugp.add( e.LINE, l=smugp.unit/2 )
F = smugp.add( e.DOT_OPEN, toplabel='F' )
smugp.pop()
Rs = smugp.add( e.RES, d='down' )
Rs.add_label('$R_s$', loc='center', ofst=[.5,-.3], align=('right','center'))
smugp.add( e.DOT )
smugp.push()
smugp.add( e.LINE, l=smugp.unit/2 )
S = smugp.add( e.DOT_OPEN, toplabel='S' )
smugp.pop()
smugp.add( e.LINE, d='left', tox=O1.in2[0]-smugp.unit/4 )
smugp.add( e.DOT )
smugp.push()
smugp.add( e.LINE, d='up', toy=O1.in2 )
smugp.add( e.LINE, d='right', tox=O1.in2 )
smugp.pop()
V = smugp.add( e.METER_V, d='down', l=smugp.unit*.75 )
GND = smugp.add( e.GND )

anchors = {
    'inpt':[0,0],
    'F':F.end,
    'S':S.end,
    'name':[I.center[0],GND.start[1]] }

#smugp.draw()  # Could draw the SMU by itself now.
gp = schem.group_elements(smugp, anchors=anchors)

def boxsmu(d, smu):
    ''' Draw a dotted box around the SMU element '''
    topleft = smu.inpt + np.array([-.5,1])
    d.add( e.LINE, xy=topleft, tox=topleft[0]+6, d='right', ls=':' )
    d.add( e.LINE, d='down', toy=topleft[1]-7, ls=':' )
    d.add( e.LINE, d='left', tox=topleft[0], ls=':' )
    d.add( e.LINE, d='up',   toy=topleft[1], ls=':' )


# Create a new drawing and add a couple SMUs to it.
d = schem.Drawing()
S1 = d.add( gp )
d.add( e.LABEL, xy=S1.name, label='SMU1' )
boxsmu(d, S1 )
d.add( e.RES, xy=S1.F, d='right', label='$R_c$' )
d.add( e.RES, d='down', label='$R_{ch}$', l=d.unit*3 )
d.add( e.RES, d='left', label='$R_c$' )
S2 = d.add( gp, anchor='F', d='right')
boxsmu(d, S2 )
d.add( e.LABEL, xy=S2.name, label='SMU2' )
d.draw(showplot=False)
d.save('smu.png')