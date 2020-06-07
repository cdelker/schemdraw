''' DEPRECATED element definitions, based on dictionaries instead of classes, translated
    into their newer class counterparts.
'''

from functools import partial

from .. import dsp
from ..elements.legacy import LINE, DOT, LINEDOT, LINE_DOT, ARROW, ARROWHEAD, ANT, ic, multiplexer
from ..flow import Box

def makebox(w, h):
    return partial(Box, w=w, h=h)

BOX = dsp.Square
CIRCLE = dsp.Circle
SUM = dsp.Sum
SUMSIGMA = dsp.SumSigma
MIX = dsp.Mixer
SPEAKER1 = dsp.Speaker
AMP = dsp.Amp
OSCBOX = dsp.OscillatorBox
OSC = dsp.Oscillator
FILT = dsp.Filter
FILT_BP = partial(dsp.Filter, response='bp')
FILT_LP = partial(dsp.Filter, response='lp')
FILT_HP = partial(dsp.Filter, response='hp')
ADC = dsp.Adc
DAC = dsp.Dac
DEMOD = dsp.Demod
