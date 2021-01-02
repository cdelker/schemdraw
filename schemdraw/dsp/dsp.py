''' Signal processing elements '''

import math
from typing import Literal, Sequence

from ..util import linspace
from ..segments import Segment, SegmentCircle, SegmentText
from ..elements import Element
from ..types import XY


class Square(Element):
    ''' Empty square element

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        self.segments.append(Segment([[0, 0], [0, .5], [1, .5],
                                      [1, -.5], [0, -0.5], [0, 0]]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.anchors['N'] = [0.5, 0.5]
        self.anchors['S'] = [0.5, -0.5]
        self.anchors['E'] = [1, 0]
        self.anchors['W'] = [0, 0]
        self.params['drop'] = [1, 0]


class Circle(Element):
    ''' Empty circle element

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        rad = .5
        k = rad*math.sqrt(2)/2  # Diagonal distance
        self.segments.append(SegmentCircle([rad, 0], rad))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['drop'] = [2*rad, 0]
        self.anchors['N'] = [rad, rad]
        self.anchors['S'] = [rad, -rad]
        self.anchors['E'] = [2*rad, 0]
        self.anchors['W'] = [0, 0]
        self.anchors['NW'] = [rad-k, k]
        self.anchors['NE'] = [rad+k, k]
        self.anchors['SW'] = [rad-k, k]
        self.anchors['SE'] = [rad+k, k]
        self.anchors['center'] = [rad, 0]


class Sum(Circle):
    ''' Summation element (+ symbol)

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        self.segments.append(Segment([[.5, .2], [.5, -.2]]))
        self.segments.append(Segment([[.3, 0], [.7, 0]]))


class SumSigma(Circle):
    ''' Summation element (Greek Sigma symbol)

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentText(label=r'$\Sigma$',
                                         pos=[0.45, 0],
                                         align=('center', 'center')))


class Mixer(Circle):
    ''' Mixer

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        rad = .5
        k = rad*math.sqrt(2)/2  # Diagonal distance
        self.segments.append(Segment([[rad+k, k], [rad-k, -k]]))
        self.segments.append(Segment([[rad+k, -k], [rad-k, k]]))
        self.params['lblloc'] = 'top'
        self.params['lblofst'] = 0.2


class Speaker(Element):
    ''' Speaker with only one terminal '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        self.segments.append(Segment([[0, 0], [0, 0.25], [0.25, 0.25],
                                      [0.25, -.25], [0, -.25], [0, 0]]))
        self.segments.append(Segment([[0.25, 0.25], [0.5, 0.5], [0.5, -0.5],
                                      [0.25, -0.25], [.25, .25]]))


class Amp(Element):
    ''' Amplifier

        Anchors:
            in
            out
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        amph = 1.
        ampl = .75
        self.segments.append(Segment([[0, 0], [0, -amph/2], [ampl, 0],
                                      [0, amph/2], [0, 0]]))
        self.params['drop'] = [ampl, 0]
        self.anchors['in'] = [0, 0]
        self.anchors['out'] = [ampl, 0]


def _makesine() -> Sequence[XY]:
    sinx = linspace(-math.pi, math.pi, num=20)
    siny = [-math.sin(x)/10 for x in sinx]
    sinx = [x / math.pi * .3 + .5 for x in sinx]
    path = list(zip(sinx, siny))
    return path


class OscillatorBox(Square):
    ''' Oscillator in a square

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        path = _makesine()
        self.segments.append(Segment(path))


class Oscillator(Circle):
    ''' Oscillator in a circle

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        path = _makesine()
        self.segments.append(Segment(path))


class Filter(Square):
    ''' Filter

        Args:
            response: Filter response ('lp', 'bp', 'hp', or 'notch') for
                low-pass, band-pass, high-pass, and notch/band-stop filters

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, d=None, response: Literal['lp', 'bp', 'hp', 'notch']=None, **kwargs):
        super().__init__(d, **kwargs)
        path = _makesine()
        path1 = [[p[0], p[1]+.25] for p in path]
        path2 = [[p[0], p[1]-.25] for p in path]
        self.segments.append(Segment(path))
        self.segments.append(Segment(path1))
        self.segments.append(Segment(path2))

        if response:
            if response.lower() in ['bp', 'lp']:
                # Slash through high f
                self.segments.append(Segment([[.45, .17], [.55, .33]]))
            if response.lower() in ['bp', 'hp']:
                # Slash through low f
                self.segments.append(Segment([[.45, -.33], [.55, -.17]]))
            if response.lower() in ['lp', 'hp', 'notch']:
                # Slash through mid f
                self.segments.append(Segment([[.45, -.08], [.55, .08]]))


class Adc(Element):
    ''' Analog to digital converter

        Anchors:
            in
            out
            E (same as in)
            W (same as out)
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        self.segments.append(Segment([[0, 0], [.22, .5], [1.4, .5], [1.4, -.5],
                                      [.22, -.5], [0, 0]]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['drop'] = [1.4, 0]
        self.anchors['in'] = [0, 0]
        self.anchors['out'] = [1.4, 0]
        self.anchors['E'] = [1.4, 0]
        self.anchors['W'] = [0, 0]


class Dac(Element):
    ''' Digital to analog converter

        Anchors:
            in
            out
            E (same as in)
            W (same as out)
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        self.segments.append(Segment([[0, 0], [0, .5], [1.18, .5], [1.4, 0],
                                      [1.18, -.5], [0, -.5], [0, 0]]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['drop'] = [1.4, 0]
        self.anchors['in'] = [0, 0]
        self.anchors['out'] = [1.4, 0]
        self.anchors['E'] = [1.4, 0]
        self.anchors['W'] = [0, 0]


class Demod(Square):
    ''' Demodulator (box with a diode in it)

        Anchors:
            N
            S
            E
            W
    '''
    def __init__(self, d=None, **kwargs):
        super().__init__(d, **kwargs)
        self.segments.append(Segment([[.15, 0], [.3, 0]]))
        self.segments.append(Segment([[.3, .25], [.7, 0], [.3, -.25], [.3, .25]]))
        self.segments.append(Segment([[.7, .25], [.7, -.25]]))
        self.segments.append(Segment([[.7, 0], [.85, 0]]))
