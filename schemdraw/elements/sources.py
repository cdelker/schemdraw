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
    ''' Current source

        Keyword Arguments:
            arrowwidth: Width of arrowhead
            arrowlength: length of arrowhead
            arrow_lw: Line width of arrow
            arrow_color: Color of arrow
    '''
    _element_defaults = {
        'arrowwidth': .15,
        'arrowlength': .25,
        'arrow_lw': None,
        'arrow_color': None,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.25, 0), (.75, 0)], arrow='->',
                                     arrowwidth=self.params['arrowwidth'],
                                     arrowlength=self.params['arrowlength'],
                                     lw=self.params['arrow_lw'],
                                     color=self.params['arrow_color']
                                     ))


class SourceSin(Source):
    ''' Source with sine

        Keyword Arguments:
            sin_lw: Line width of sine curve
            sin_color: Color of sine curve
    '''
    _element_defaults = {
        'sin_lw': None,
        'sin_color': None
        }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sin_y = util.linspace(-.25, .25, num=25)
        sin_x = [.2 * math.sin((sy-.25)*math.pi*2/.5) + 0.5 for sy in sin_y]
        self.segments.append(Segment(list(zip(sin_x, sin_y)),
                                     lw=self.params['sin_lw'],
                                     color=self.params['sin_color']
                                     ))


class SourcePulse(Source):
    ''' Pulse source

        Keyword Arguments:
            pulse_lw: Line width of pulse curve
            pulse_color: Color of pulse curve
    '''
    _element_defaults = {
        'pulse_lw': None,
        'pulse_color': None
        }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        sq = .15
        x = .4
        self.segments.append(Segment(
            [(x, sq*2), (x, sq), (x+sq, sq), (x+sq, -sq),
             (x, -sq), (x, -sq*2)],
            lw=self.params['pulse_lw'],
            color=self.params['pulse_color']
            ))


class SourceTriangle(Source):
    ''' Triangle source

        Keyword Arguments:
            tri_lw: Line width of triangle curve
            tri_color: Color of triangle curve
    '''
    _element_defaults = {
        'tri_lw': None,
        'tri_color': None
        }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.4, .25), (.7, 0), (.4, -.25)],
                                     lw=self.params['tri_lw'],
                                     color=self.params['tri_color']
                                     ))


class SourceRamp(Source):
    ''' Ramp/sawtooth source

        Keyword Arguments:
            ramp_lw: Line width of ramp curve
            ramp_color: Color of ramp curve
    '''
    _element_defaults = {
        'ramp_lw': None,
        'ramp_color': None
        }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.4, .25), (.8, -.2), (.4, -.2)],
                                     lw=self.params['ramp_lw'],
                                     color=self.params['ramp_color']
                                     ))


class SourceSquare(Source):
    ''' Square wave source

        Keyword Arguments:
            square_lw: Line width of square curve
            square_color: Color of square curve
    '''
    _element_defaults = {
        'square_lw': None,
        'square_color': None
        }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.5, .25), (.7, .25), (.7, 0),
                                      (.3, 0), (.3, -.25), (.5, -.25)],
                                    lw=self.params['square_lw'],
                                    color=self.params['square_color']))


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
    ''' Controlled current source

        Keyword Arguments:
            arrowwidth: Width of arrowhead
            arrowlength: length of arrowhead
            arrow_lw: Line width of arrow
            arrow_color: Color of arrow
    '''
    _element_defaults = {
        'arrowwidth': .15,
        'arrowlength': .25,
        'arrow_lw': None,
        'arrow_color': None,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.25, 0), (.75, 0)], arrow='->',
                                     arrowwidth=self.params['arrowwidth'],
                                     arrowlength=self.params['arrowlength'],
                                     lw=self.params['arrow_lw'],
                                     color=self.params['arrow_color']
                                     ))


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
    ''' Solar source

        Keyword Arguments:
            arrowwidth: Width of arrowhead
            arrowlength: length of arrowhead
            arrow_lw: Line width of arrow
            arrow_color: Color of arrow
    '''
    _element_defaults = {
        'arrowwidth': .15,
        'arrowlength': .25,
        'arrow_lw': None,
        'arrow_color': None,
        }
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

        hwidth = self.params['arrowwidth']
        hlength = self.params['arrowlength']
        lw = self.params['arrow_lw']
        color = self.params['arrow_color']
        self.segments.append(Segment([(1.1, .9), (.8, .6)],
                                     arrow='->', arrowwidth=hwidth, arrowlength=hlength,
                                     lw=lw, color=color))
        self.segments.append(Segment([(1.3, .7), (1, .4)],
                                     arrow='->', arrowwidth=hwidth, arrowlength=hlength,
                                     lw=lw, color=color))


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
    ''' Meter with diagonal arrow

        Keyword Arguments:
            arrowwidth: Width of arrowhead
            arrowlength: length of arrowhead
            arrow_lw: Line width of arrow
            arrow_color: Color of arrow
    '''
    _element_defaults = {
        'arrowwidth': .15,
        'arrowlength': .25,
        'arrow_lw': None,
        'arrow_color': None,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([ (.25, .16), (.75, -.16)], arrow='->',
                                     arrowwidth=self.params['arrowwidth'],
                                     arrowlength=self.params['arrowlength'],
                                     lw=self.params['arrow_lw'],
                                     color=self.params['arrow_color']
                                     ))


class Lamp(Source):
    ''' Incandescent Lamp

        Keyword Arguments:
            filament_lw: Line width of filament
            filament_color: Color of filament
    '''
    _element_defaults = {
        'filament_lw': None,
        'filament_color': None
    }
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
        self.segments.append(
            Segment(
                list(zip(x, y)),
                lw=self.params['filament_lw'],
                color=self.params['filament_color']))


class Lamp2(Source):
    ''' Incandescent Lamp (with X through a Source)

        Keyword Arguments:
            filament_lw: Line width of filament
            filament_color: Color of filament
    '''
    _element_defaults = {
        'filament_lw': None,
        'filament_color': None
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        r=0.5
        self.segments.append(Segment(
            [(r-r/2**.5, -r/2**.5),
             (r+r/2**.5,  r/2**.5)],
            lw=self.params['filament_lw'],
            color=self.params['filament_color']))

        self.segments.append(Segment(
            [(r-r/2**.5,  r/2**.5),
             (r+r/2**.5, -r/2**.5)],
            lw=self.params['filament_lw'],
            color=self.params['filament_color']))


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
    ''' Base class for square meter/scope boxes

        Keyword Arguments:
            width: Width and height of square box
            corner: Corner radius
            input_ofst: Distance from corner to input connections
            input_lw: line width of connector circles
            input_rad: radius of connector circles
            input_fill: Fill coloro of connector circles
    '''
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
