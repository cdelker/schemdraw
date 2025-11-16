''' Sources, meters, and lamp elements '''

from __future__ import annotations
import math

from .elements import Element, Element2Term, LabelHint, gap
from .twoterm import resheight
from ..segments import Segment, SegmentCircle, SegmentText, SegmentPoly, SegmentPath
from .. import util


class Source(Element2Term):
    ''' Generic source element '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, 0), gap, (1, 0), (1, 0)]))
        self.segments.append(SegmentCircle((0.5, 0), 0.5,))
        self.elmparams['theta'] = 90


class SourceV(Source):
    ''' Voltage source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        plus_len = .2
        self.segments.append(Segment([(.25, -plus_len/2),
                                      (.25, plus_len/2)]))    # '-' sign
        self.segments.append(Segment([(.75-plus_len/2, 0),
                                      (.75+plus_len/2, 0)]))  # '+' sign
        self.segments.append(Segment([(.75, -plus_len/2),
                                      (.75, plus_len/2)]))     # '+' sign


class SourceI(Source):
    ''' Current source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.25, 0), (.75, 0)], arrow='->'))


class SourceSin(Source):
    ''' Source with sine '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sin_y = util.linspace(-.25, .25, num=25)
        sin_x = [.2 * math.sin((sy-.25)*math.pi*2/.5) + 0.5 for sy in sin_y]
        self.segments.append(Segment(list(zip(sin_x, sin_y))))


class SourcePulse(Source):
    ''' Pulse source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sq = .15
        x = .4
        self.segments.append(Segment(
            [(x, sq*2), (x, sq), (x+sq, sq), (x+sq, -sq),
             (x, -sq), (x, -sq*2)]))


class SourceTriangle(Source):
    ''' Triangle source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.4, .25), (.7, 0), (.4, -.25)]))


class SourceRamp(Source):
    ''' Ramp/sawtooth source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.4, .25), (.8, -.2), (.4, -.2)]))


class SourceSquare(Source):
    ''' Square wave source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.5, .25), (.7, .25), (.7, 0),
                                      (.3, 0), (.3, -.25), (.5, -.25)]))


class SourceControlled(Element2Term):
    ''' Generic controlled source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (.5, .5), (1, 0),
                                      (.5, -.5), (0, 0), gap, (1, 0)]))
        self.params['theta'] = 90


class SourceControlledV(SourceControlled):
    ''' Controlled voltage source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        plus_len = .2
        self.segments.append(Segment([(.25, -plus_len/2),
                                      (.25, plus_len/2)]))  # '-' sign
        self.segments.append(Segment([(.75-plus_len/2, 0),
                                      (.75+plus_len/2, 0)]))  # '+' sign
        self.segments.append(Segment([(.75, -plus_len/2),
                                      (.75, plus_len/2)]))  # '+' sign


class SourceControlledI(SourceControlled):
    ''' Controlled current source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.25, 0), (.75, 0)], arrow='->'))


batw = resheight*.75
bat1 = resheight*1.5
bat2 = resheight*.75


class BatteryCell(Element2Term):
    ''' Cell '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), gap, (batw, 0)]))
        self.segments.append(Segment([(0, bat1), (0, -bat1)]))
        self.segments.append(Segment([(batw, bat2), (batw, -bat2)]))


class Battery(Element2Term):
    ''' Battery '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), gap, (batw*3, 0)]))
        self.segments.append(Segment([(0, bat1), (0, -bat1)]))
        self.segments.append(Segment([(batw, bat2), (batw, -bat2)]))
        self.segments.append(Segment([(batw*2, bat1), (batw*2, -bat1)]))
        self.segments.append(Segment([(batw*3, bat2), (batw*3, -bat2)]))


class BatteryDouble(Element2Term):
    ''' Double-stack Battery '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), gap, (batw*9, 0)]))
        self.segments.append(Segment([(0, bat1), (0, -bat1)]))
        self.segments.append(Segment([(batw, bat2), (batw, -bat2)]))
        self.segments.append(Segment([(batw*2, bat1), (batw*2, -bat1)]))
        self.segments.append(Segment([(batw*3, bat2), (batw*3, -bat2)]))
        self.segments.append(Segment([(batw*4, bat1), (batw*4, -bat1)]))
        self.segments.append(Segment([(batw*5, bat2), (batw*5, -bat2)]))
        self.segments.append(Segment([(batw*6, bat1), (batw*6, -bat1)]))
        self.segments.append(Segment([(batw*7, bat2), (batw*7, -bat2)]))
        self.segments.append(Segment([(batw*8, bat1), (batw*8, -bat1)]))
        self.segments.append(Segment([(batw*9, bat2), (batw*9, -bat2)]))
        self.anchors['tap'] = (batw*4, bat1)

class Solar(Source):
    ''' Solar source '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cellw = resheight*.5
        cellw2 = cellw + .15
        cellx = .4
        self.segments.append(Segment([(cellx, cellw),
                                      (cellx, -cellw)]))
        self.segments.append(Segment([(cellx+.2, cellw2),
                                      (cellx+.2, -cellw2)]))
        self.segments.append(Segment([(0, 0), (cellx, 0), gap,
                                      (cellx+.2, 0), (1, 0)]))
        self.segments.append(Segment([(1.1, .9), (.8, .6)],
                                     arrow='->', arrowwidth=.16, arrowlength=.2))
        self.segments.append(Segment([(1.3, .7), (1, .4)],
                                     arrow='->', arrowwidth=.16, arrowlength=.2))


class MeterV(Source):
    ''' Volt meter '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentText((.5, 0), 'V'))


class MeterI(Source):
    ''' Current Meter (I) '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentText((.5, 0), 'I'))


class MeterA(Source):
    ''' Ammeter '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentText((.5, 0), 'A'))


class MeterOhm(Source):
    ''' Ohm meter '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentText((.5, 0), r'$\Omega$'))


class MeterArrow(Source):
    ''' Meter with diagonal arrow'''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([ (.25, .16), (.75, -.16)], arrow='->'))



class Lamp(Source):
    ''' Incandescent Lamp '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        a = .25
        b = .7
        t = util.linspace(1.4, 3.6*math.pi, 100)
        x = [a*t0 - b*math.sin(t0) for t0 in t]
        y = [a - b * math.cos(t0) for t0 in t]
        x = [xx - x[0] for xx in x]  # Scale to about the right size
        x = [xx / x[-1] for xx in x]
        y = [(yy - y[0]) * .25 for yy in y]
        self.segments.append(Segment(list(zip(x, y))))


class Lamp2(Source):
    ''' Incandescent Lamp (with X through a Source) '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        r=0.5
        self.segments.append(Segment(
            [(r-r/2**.5, -r/2**.5),
             (r+r/2**.5,  r/2**.5)]))
        self.segments.append(Segment(
            [(r-r/2**.5,  r/2**.5),
             (r+r/2**.5, -r/2**.5)]))


class Neon(Source):
    ''' Neon bulb '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        cellw = resheight
        cellx = .4
        self.segments.append(Segment([(cellx, cellw), (cellx, -cellw)]))
        self.segments.append(Segment([(cellx+.2, cellw), (cellx+.2, -cellw)]))
        self.segments.append(Segment([(0, 0), (cellx, 0), gap,
                                      (cellx+.2, 0), (1, 0)]))
        self.segments.append(SegmentCircle((cellx-.15, .2), .05, fill=True))


class MeterBox(Element):
    ''' Base class for square meter/scope boxes '''
    _element_defaults = {
        'width': 1.5,
        'corner': .2,
        'input_ofst': (.4, .3),
        'input_lw': 1,
        'input_rad': 0.1,
        'input_fill': 'none'
    }
    def __init__(self, inputs: bool = True, **kwargs):
        super().__init__(**kwargs)
        w = self.params['width']
        corner = self.params['corner']
        input_ofst = self.params['input_ofst']
        input_lw = self.params['input_lw']
        input_rad = self.params['input_rad']
        center = w/2

        # Box
        self.segments.append(SegmentPoly([(0, 0), (0, w), (w, w), (w, 0)],
                                         closed=True, cornerradius=corner
                                         ))
        # Inputs
        if inputs:
            self.segments.append(SegmentCircle((input_ofst[0], input_ofst[1]), input_rad, lw=input_lw, fill=self.params['input_fill'], zorder=4))
            self.segments.append(SegmentCircle((w-input_ofst[0], input_ofst[1]), input_rad, lw=input_lw, fill=self.params['input_fill'], zorder=4))

        self.anchors['N'] = (w/2, w)
        self.anchors['S'] = (w/2, 0)
        self.anchors['E'] = (w, w/2)
        self.anchors['W'] = (0, w/2)
        self.anchors['NE'] = (w, w)
        self.anchors['SE'] = (w, 0)
        self.anchors['NW'] = (0, w)
        self.anchors['SW'] = (0, 0)
        self.anchors['in1'] = (input_ofst[0], input_ofst[1])
        self.anchors['in2'] = (w-input_ofst[0], input_ofst[1])
        self.anchors['name'] = (w/2, 0)
        self._labelhints['name'] = LabelHint((0, .1), halign='center', valign='base')
        self._labelhints['in1'] = LabelHint((0, input_rad+.1), halign='center', valign='base')
        self._labelhints['in2'] = LabelHint((0, input_rad+.1), halign='center', valign='base')
        self.elmparams['drop'] = self.anchors['in2']


class MeterAnalog(MeterBox):
    ''' Analog meter drawn as a box

        Args:
            inputs: Show input connections
            needle_percent: Position of the needle along the window from 0 to 100
            needle_color: Color of the needle
            needle_width: Line width of the needle
            window_fill: Fill color for window area
            input_ofst: (x, y) offset of input connectors
            input_lw: Line width of input connector circles
            input_rad: Radius of input connector circles
            input_fill: Fill color of input connector circles
    '''
    _element_defaults = {
        'needle_color': 'black',
        'needle_width': 1.5,
        'window_fill': 'none',
    }
    def __init__(self, inputs: bool = True, needle_percent: float = 70, **kwargs):
        super().__init__(inputs=inputs, **kwargs)
        w = self.params['width']
        center = w/2

        # Window
        arcy = 1.2
        arcy2 = .86
        arch = .2
        self.segments.append(
            SegmentPath(('M', (center-w/3, arcy),
                         'Q', (center, arcy+arch), (center+w/3, arcy),
                         'L', (center+w/4, arcy2),
                         'Q', (center, arcy2+arch*.7), (center-w/4, arcy2),
                         'Z'
                        ), color='black', fill=self.params['window_fill'], lw=1)
        )

        # Needle
        needle1, needle2 = .94, 1.2
        angle = math.radians(112 - 45 * needle_percent / 100)
        needle_start = center + needle1 * math.cos(angle), 0 + needle1 * math.sin(angle)
        needle_end = center + needle2 * math.cos(angle), 0 + needle2 * math.sin(angle)
        self.segments.append(
            Segment((needle_start, needle_end), lw=self.params['needle_width'], color=self.params['needle_color']))


class Oscilloscope(MeterBox):
    ''' Oscilloscope drawn as a box

        Args:
            signal: Type of signal to display on the screen. 'sine', 'square', or 'triangle'
            inputs: Show input connections
            screen_fill: Fill color for screen area
            screen_lw: Line width  of the screen
            grid: Whether to show grid over the screen
            grid_color: Color for the oscope grid
            grid_lw: Line width of the grid
            signal_lw: Line width of the displayed signal
            signal_color: Color of the displayed signal
            input_ofst: (x, y) offset of input connectors
            input_lw: Line width of input connector circles
            input_rad: Radius of input connector circles
            input_fill: Fill color of input connector circles
    '''
    _element_defaults = {
        'screen_fill': 'none',
        'screen_lw': 1,
        'grid': True,
        'grid_color': '#666666',
        'grid_lw': 0.3,
        'signal_lw': 2,
        'signal_color': '#e0213b',
    }
    def __init__(self, signal: str = 'none', inputs: bool = True, **kwargs):
        super().__init__(inputs=inputs, **kwargs)
        w = self.params['width']
        center = w/2

        # Window
        gridN = 4
        wleft = w*.15
        wright = w*.85
        wwidth = wright-wleft
        grid = wwidth/(gridN+1)
        wheight = grid*3
        wtop = w*.9
        wbot = wtop - wheight

        self.segments.append(
            SegmentPoly(((wleft, wbot), (wleft, wtop), (wright, wtop), (wright, wbot)), closed=True,
                         lw=self.params['screen_lw'], fill=self.params['screen_fill']))

        if self.params['grid']:
            for i in range(gridN):
                x = wleft + (i+1)*grid
                self.segments.append(Segment(((x, wbot), (x, wtop)), lw=self.params['grid_lw'], color=self.params['grid_color']))
            for i in range(2):
                y = wbot + (i+1)*grid
                self.segments.append(Segment(((wleft, y), (wright, y)), lw=self.params['grid_lw'], color=self.params['grid_color']))

        # Signal
        if signal == 'sine':
            xx = util.linspace(wleft, wright, 20)
            yy = [wbot + wheight/2 + math.sin((x-wleft)/wwidth*math.pi*2)*wheight/2*.75 for x in xx]
            self.segments.append(Segment(list(zip(xx, yy)), lw=self.params['signal_lw'], color=self.params['signal_color']))
        elif signal == 'square':
            sbot = wbot + wheight/4
            stop = wtop - wheight/4
            edge1 = wleft + wwidth/3 - .1
            edge2 = wleft + wwidth*2/3 - .1
            edge3 = wleft + wwidth - .1
            self.segments.append(Segment(((wleft, sbot), (edge1, sbot),
                                          (edge1, stop), (edge2, stop),
                                          (edge2, sbot), (edge3, sbot),
                                          (edge3, stop), (wright, stop)),
                                         lw=self.params['signal_lw'], color=self.params['signal_color']))
        elif signal == 'triangle':
            sbot = wbot + wheight/4
            stop = wtop - wheight/4
            edge1 = wleft + wwidth/3 - .1
            edge2 = wleft + wwidth*2/3 - .1
            edge3 = wleft + wwidth - .1
            self.segments.append(Segment(((wleft, sbot), (edge1, stop),
                                          (edge2, sbot), (edge3, stop),
                                          (wright, stop-.1)),
                                         lw=self.params['signal_lw'], color=self.params['signal_color']))


class MeterDigital(MeterBox):
    ''' Digital meter drawn as a box

        Args:
            inputs: Show input connections
            screen_fill: Fill color for screen area
            screen_lw: Line width  of the screen
            input_ofst: (x, y) offset of input connectors
            input_lw: Line width of input connector circles
            input_rad: Radius of input connector circles
            input_fill: Fill color of input connector circles
    '''
    _element_defaults = {
        'screen_fill': 'none',
        'screen_lw': 1,
    }
    def __init__(self, inputs: bool = True, **kwargs):
        super().__init__(inputs=inputs, **kwargs)
        w = self.params['width']
        center = w/2

        wleft = w*.1
        wright = w*.9
        wwidth = wright-wleft
        wheight = w/3
        wtop = w*.85
        wbot = wtop - wheight

        self.segments.append(
            SegmentPoly(((wleft, wbot), (wleft, wtop),
                         (wright, wtop), (wright, wbot)), closed=True,
                         lw=self.params['screen_lw'], fill=self.params['screen_fill']))

        self.anchors['display'] = ((wleft+wright)/2, wbot)
        self._labelhints['display'] = LabelHint((0, .1), halign='center', valign='base', fontsize=11)
