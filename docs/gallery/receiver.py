# Superheterodyne receiver, with color fill
# Source: https://www.electronicdesign.com/adc/high-speed-rf-sampling-adc-boosts-bandwidth-dynamic-range

import SchemDraw
from SchemDraw import dsp

d = SchemDraw.Drawing(fontsize=12)
d.add(dsp.ANT)
d.add(dsp.LINE, d='right', l=d.unit/4)
filt1 = d.add(dsp.FILT_BP, botlabel='RF filter\n#1', anchor='W', lblofst=.2, fill='thistle')
d.add(dsp.LINE, xy=filt1.E, l=d.unit/4)
d.add(dsp.AMP, label='LNA', fill='lightblue')
d.add(dsp.LINE, l=d.unit/4)
filt2 = d.add(dsp.FILT_BP, botlabel='RF filter\n#2', anchor='W', lblofst=.2, fill='thistle')
d.add(dsp.LINE, xy=filt2.E, d='right', l=d.unit/3)
mix = d.add(dsp.MIX, label='Mixer', fill='navajowhite')
d.add(dsp.LINE, xy=mix.S, d='down', l=d.unit/3)
d.add(dsp.OSC, rgtlabel='Local\nOscillator', d='right', lblofst=.2, anchor='N', fill='navajowhite')
d.add(dsp.LINE, xy=mix.E, d='right', l=d.unit/3)
filtIF = d.add(dsp.FILT_BP, anchor='W', botlabel='IF filter', lblofst=.2, fill='thistle')
d.add(dsp.LINE, xy=filtIF.E, d='right', l=d.unit/4)
d.add(dsp.AMP, label='IF\namplifier', fill='lightblue')
d.add(dsp.LINE, l=d.unit/4)
demod = d.add(dsp.DEMOD, anchor='W', botlabel='Demodulator', lblofst=.2, fill='navajowhite')
d.add(dsp.LINE, xy=demod.E, d='right', l=d.unit/3)
d.add(dsp.ARROWHEAD)
d.draw()
d.save('receiver.svg')