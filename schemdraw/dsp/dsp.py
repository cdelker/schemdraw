''' Signal processing elements '''

from __future__ import annotations
import math
from typing import Optional, Sequence, Literal

from ..util import linspace, Point
from ..segments import Segment, SegmentCircle, SegmentText, SegmentArc
from ..elements import Element
from ..types import XY


FilterType = Literal['lp', 'bp', 'hp', 'notch']


class Square(Element):
    ''' Empty square element

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, .5), (1, .5),
                                      (1, -.5), (0, -0.5), (0, 0)]))
        self.elmparams['lblloc'] = 'center'
        self.elmparams['lblofst'] = 0
        self.anchors['N'] = (0.5, 0.5)
        self.anchors['S'] = (0.5, -0.5)
        self.anchors['E'] = (1, 0)
        self.anchors['W'] = (0, 0)
        self.elmparams['drop'] = (1, 0)


class Circle(Element):
    ''' Empty circle element

        Anchors:
            * N
            * S
            * E
            * W
            * NW
            * NE
            * SW
            * SE
    '''
    _element_defaults = {
        'radius': 0.5
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        rad = self.params['radius']
        k = rad*math.sqrt(2)/2  # Diagonal distance
        self.segments.append(SegmentCircle((rad, 0), rad))
        self.elmparams['lblloc'] = 'center'
        self.elmparams['lblofst'] = 0
        self.elmparams['drop'] = (2*rad, 0)
        self.anchors['N'] = (rad, rad)
        self.anchors['S'] = (rad, -rad)
        self.anchors['E'] = (2*rad, 0)
        self.anchors['W'] = (0, 0)
        self.anchors['NW'] = (rad-k, k)
        self.anchors['NE'] = (rad+k, k)
        self.anchors['SW'] = (rad-k, -k)
        self.anchors['SE'] = (rad+k, -k)
        self.anchors['center'] = (rad, 0)


class Sum(Circle):
    ''' Summation element (+ symbol)

        Anchors:
            * N
            * S
            * E
            * W
            * NW
            * NE
            * SW
            * SE
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.5, .2), (.5, -.2)]))
        self.segments.append(Segment([(.3, 0), (.7, 0)]))


class SumSigma(Circle):
    ''' Summation element (Greek Sigma symbol)

        Anchors:
            * N
            * S
            * E
            * W
            * NW
            * NE
            * SW
            * SE
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentText(label=r'$\Sigma$',
                                         pos=(0.45, 0),
                                         align=('center', 'center')))


class Mixer(Circle):
    ''' Mixer

        Args:
            N: text in North sector
            S: text in South sector
            E: text in East sector
            W: text in West sector
            font: Font family/name
            fontsize: Point size of label font

        Anchors:
            * N
            * S
            * E
            * W
            * NW
            * NE
            * SW
            * SE
    '''
    def __init__(self, N: Optional[str] = None, E: Optional[str] = None, S: Optional[str] = None, W: Optional[str] = None,
                 font: Optional[str] = None, fontsize: float = 10, **kwargs):
        super().__init__(**kwargs)
        rad = .5
        k = rad*math.sqrt(2)/2  # Diagonal distance
        self.segments.append(Segment([(rad+k, k), (rad-k, -k)], lw=1))
        self.segments.append(Segment([(rad+k, -k), (rad-k, k)], lw=1))
        self.elmparams['lblloc'] = 'top'
        self.elmparams['lblofst'] = 0.2
        if N:
            self.segments.append(SegmentText(
                (rad, rad/2+0.01), N,
                font=font, fontsize=fontsize))
        if S:
            self.segments.append(SegmentText(
                (rad, -rad/2-0.065), S,
                font=font, fontsize=fontsize))
        if E:
            self.segments.append(SegmentText(
                (rad*1.5+0.05, 0), E,
                font=font, fontsize=fontsize))
        if W:
            self.segments.append(SegmentText(
                (rad/2-0.05, 0), W,
                font=font, fontsize=fontsize))


class Speaker(Element):
    ''' Speaker with only one terminal '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, 0.25), (0.25, 0.25),
                                      (0.25, -.25), (0, -.25), (0, 0)]))
        self.segments.append(Segment([(0.25, 0.25), (0.5, 0.5), (0.5, -0.5),
                                      (0.25, -0.25), (.25, .25)]))


class Amp(Element):
    ''' Amplifier

        Anchors:
            * in
            * out
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        amph = 1.
        ampl = .75
        self.segments.append(Segment([(0, 0), (0, -amph/2), (ampl, 0),
                                      (0, amph/2), (0, 0)]))
        self.elmparams['drop'] = (ampl, 0)
        self.anchors['input'] = (0, 0)
        self.anchors['out'] = (ampl, 0)


def _makesine() -> Sequence[XY]:
    sinx = linspace(-math.pi, math.pi, num=20)
    siny = [-math.sin(x)/10 for x in sinx]
    sinx = [x / math.pi * .3 + .5 for x in sinx]
    path = list(zip(sinx, siny))
    return path


class OscillatorBox(Square):
    ''' Oscillator in a square

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        path = _makesine()
        self.segments.append(Segment(path))


class Oscillator(Circle):
    ''' Oscillator in a circle

        Anchors:
            * N
            * S
            * E
            * W
            * NW
            * NE
            * SW
            * SE
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        path = _makesine()
        self.segments.append(Segment(path))


class Filter(Square):
    ''' Filter

        Args:
            response: Filter response ('lp', 'bp', 'hp', or 'notch') for
                low-pass, band-pass, high-pass, and notch/band-stop filters

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, response: Optional[FilterType] = None, **kwargs):
        super().__init__(**kwargs)
        path = _makesine()
        path1 = [Point((p[0], p[1]+.25)) for p in path]
        path2 = [Point((p[0], p[1]-.25)) for p in path]
        self.segments.append(Segment(path))
        self.segments.append(Segment(path1))
        self.segments.append(Segment(path2))

        if response:
            if response.lower() in ['bp', 'lp']:
                # Slash through high f
                self.segments.append(Segment([(.45, .17), (.55, .33)]))
            if response.lower() in ['bp', 'hp']:
                # Slash through low f
                self.segments.append(Segment([(.45, -.33), (.55, -.17)]))
            if response.lower() in ['lp', 'hp', 'notch']:
                # Slash through mid f
                self.segments.append(Segment([(.45, -.08), (.55, .08)]))


class Adc(Element):
    ''' Analog to digital converter

        Anchors:
            * in
            * out
            * E (same as in)
            * W (same as out)
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (.22, .5), (1.4, .5), (1.4, -.5),
                                      (.22, -.5), (0, 0)]))
        self.elmparams['lblloc'] = 'center'
        self.elmparams['lblofst'] = 0
        self.elmparams['drop'] = (1.4, 0)
        self.anchors['input'] = (0, 0)
        self.anchors['out'] = (1.4, 0)
        self.anchors['E'] = (1.4, 0)
        self.anchors['W'] = (0, 0)


class Dac(Element):
    ''' Digital to analog converter

        Anchors:
            * in
            * out
            * E (same as in)
            * W (same as out)
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, .5), (1.18, .5), (1.4, 0),
                                      (1.18, -.5), (0, -.5), (0, 0)]))
        self.elmparams['lblloc'] = 'center'
        self.elmparams['lblofst'] = 0
        self.elmparams['drop'] = (1.4, 0)
        self.anchors['input'] = (0, 0)
        self.anchors['out'] = (1.4, 0)
        self.anchors['E'] = (1.4, 0)
        self.anchors['W'] = (0, 0)


class Demod(Square):
    ''' Demodulator (box with a diode in it)

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.15, 0), (.3, 0)]))
        self.segments.append(Segment([(.3, .25), (.7, 0), (.3, -.25), (.3, .25)]))
        self.segments.append(Segment([(.7, .25), (.7, -.25)]))
        self.segments.append(Segment([(.7, 0), (.85, 0)]))


class Circulator(Circle):
    ''' Circulator (circle with an arrow in it)

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        radius = 0.5
        self.segments.append(
            SegmentArc((0.5, 0), 0.9 * radius, 0.9 * radius, 20, 200, "cw"))


class Isolator(Square):
    ''' Isolator (box with an arrow in it)

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        margin = 0.25
        path = ((margin, 0), (1 - margin, 0))
        self.segments.append(Segment(path, arrow="->"))


class VGA(Amp):
    ''' Variable Gain Amplifier (amplifier symbol with an arrow over it)

        Args:
            tuneup: Set tune above or below the symbol

        Anchors:
            * input
            * out
            * tune
    '''
    def __init__(self, tuneup: bool = True, **kwargs):
        super().__init__(**kwargs)
        path = ((-0.1, -0.5), (0.75, 0.5))
        self.segments.append(Segment(path, arrow="->"))
        self.anchors['tune'] = (0.325, 0.5 if tuneup else -0.5)
