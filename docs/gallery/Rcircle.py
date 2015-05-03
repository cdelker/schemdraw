import sys
sys.path.insert(0, '../../')
import SchemDraw as schem
import SchemDraw.elements as e

colors = ['red', 'orange', 'yellow', 'yellowgreen', 'green', 'blue', 'indigo', 'violet']
d = schem.Drawing()
for i in range(8):
    d.add(e.RES, label='R%d'%i, theta=45*i+20, color=colors[i] )
d.draw(showplot=False)
d.save('Rcircle.png')