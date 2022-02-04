from .dsp import Square, Circle, Sum, SumSigma, Mixer, Speaker, Amp, OscillatorBox, Oscillator, Filter, Adc, Dac, Demod, Circulator, Isolator, VGA
from ..elements import Arrowhead, Antenna, Dot, Arrow, Line, LineDot, Ic, IcPin, Multiplexer, Wire
from ..flow import Box

from . import legacy
import warnings

def __getattr__(name):
    e = getattr(legacy, name, None)
    if e is None:
        raise AttributeError('Element `{}` not found.'.format(name))
    warnings.warn('Dictionary-based elements are deprecated. Update to class-based elements or import from schemdraw.dsp.legacy.', DeprecationWarning)
    return e