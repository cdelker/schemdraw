''' Switches and buttons '''

from __future__ import annotations
from typing import Optional, Sequence
import math

from .elements import Element, Element2Term, LabelHint, gap
from ..segments import Segment, SegmentCircle, SegmentArc, SegmentPoly
from ..types import Point, ActionType
from ..util import linspace

sw_dot_r = .12


class Switch(Element2Term):
    ''' Toggle Switch

        Args:
            action: action arrow ('open' or 'close')
            contacts: Draw contacts as open circles
            nc: Draw normally closed contact line
            arrowwidth: Width of arrowhead
            arrowlength: Length of arrowhead
            arrow_lw: line width of arrow
            arrow_color: Color of arrow
    '''
    _element_defaults = {
        'arrowwidth': .15,
        'arrowlength': .25,
        'arrow_lw': None,
        'arrow_color': None,
    }
    def __init__(self,
                 action: Optional[ActionType] = None,
                 contacts: bool = True,
                 nc: bool = False,
                 **kwargs):
        super().__init__(**kwargs)
        if contacts:
            if nc:
                self.segments.append(Segment(
                    [(0, 0), gap, (sw_dot_r*2, 0), (.9, sw_dot_r+.05), gap, (1, 0)]
                    ))
            else:
                self.segments.append(Segment(
                [(0, 0), gap, (sw_dot_r*2, .1), (.8, .45), gap, (1, 0)]))
            self.segments.append(SegmentCircle((sw_dot_r, 0), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, 0), sw_dot_r, fill='bg', zorder=3))

        else:

            if nc:
                self.segments.append(Segment([(0, 0), (1.15, .45), gap, (1, 0)]))
                self.segments.append(Segment([(1, 0), (1, .55)]))
            else:
                self.segments.append(Segment([(0, 0), (.85, .45), gap, (1, 0)]))


        if action == 'open':
            self.segments.append(SegmentArc((.4, .1), width=.5, height=.75,
                                            theta1=-10, theta2=70, arrow='ccw',
                                            lw=self.params['arrow_lw'], color=self.params['arrow_color'],
                                            arrowwidth=self.params['arrowwidth'], arrowlength=self.params['arrowlength']
                                            ))
        if action == 'close':
            self.segments.append(SegmentArc((.4, .25), width=.5, height=.75,
                                            theta1=-10, theta2=70, arrow='cw',
                                            lw=self.params['arrow_lw'], color=self.params['arrow_color'],
                                            arrowwidth=self.params['arrowwidth'], arrowlength=self.params['arrowlength'],
                                            ))


class SwitchSpdt(Switch):
    ''' Single-pole double throw switch.

        Args:
            action: action arrow ('open' or 'close')
            contacts: Draw contacts as open circles

        Anchors:
            * a
            * b
            * c
    '''
    def __init__(self, action: Optional[ActionType] = None, contacts: bool = True, **kwargs):
        super().__init__(action=action, contacts=contacts, **kwargs)
        if contacts:
            self.segments.append(SegmentCircle((1-sw_dot_r, .7), sw_dot_r, fill='bg', zorder=3))
            self.anchors['a'] = Point((sw_dot_r, 0))
            self.anchors['b'] = Point((1-sw_dot_r, 0))
            self.anchors['c'] = Point((1-sw_dot_r, .7))
        else:
            self.anchors['a'] = Point((0, 0))
            self.anchors['b'] = Point((1, 0))
            self.anchors['c'] = Point((1, .7))
        self._labelhints['a'] = LabelHint((0, -.18), valign='top')
        self._labelhints['b'] = LabelHint((0, -.18), valign='top')
        self._labelhints['c'] = LabelHint((0, .18), valign='bottom')


class SwitchSpdt2(Element):
    ''' Single-pole double throw switch, throws above and below.

        Args:
            action: action arrow ('open' or 'close')
            contacts: Draw contacts as open circles
            arrowwidth: Width of arrowhead
            arrowlength: Length of arrowhead
            arrow_lw: line width of arrow
            arrow_color: Color of arrow

        Anchors:
            * a
            * b
            * c
    '''
    _element_defaults = {
        'arrowwidth': .15,
        'arrowlength': .25,
        'arrow_lw': None,
        'arrow_color': None,
    }
    def __init__(self, action: Optional[ActionType] = None, contacts: bool = True, **kwargs):
        super().__init__(action=action, **kwargs)

        if contacts:
            self.segments.append(Segment([(0, 0), gap, (sw_dot_r*2, .1),
                                        (.7, .25), gap, (1, .4)]))
            self.segments.append(SegmentCircle((sw_dot_r, 0), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, -.4), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, .4), sw_dot_r, fill='bg', zorder=3))
            self.anchors['a'] = Point((sw_dot_r, 0))
            self.anchors['b'] = Point((1-sw_dot_r, .4))
            self.anchors['c'] = Point((1-sw_dot_r, -.4))
        else:
            self.segments.append(Segment([(0, 0), (.85, .25), gap, (1, .4)]))
            self.anchors['a'] = Point((0, 0))
            self.anchors['b'] = Point((1, .4))
            self.anchors['c'] = Point((1, -.4))

        if action == 'open':
            self.segments.append(SegmentArc((.35, 0), width=.5, height=.75,
                                            theta1=-10, theta2=70, arrow='ccw',
                                            lw=self.params['arrow_lw'], color=self.params['arrow_color'],
                                            arrowwidth=self.params['arrowwidth'], arrowlength=self.params['arrowlength']
                                            ))
        elif action == 'close':
            self.segments.append(SegmentArc((.3, 0), width=.5, height=.75,
                                            theta1=-10, theta2=70, arrow='cw',
                                            lw=self.params['arrow_lw'], color=self.params['arrow_color'],
                                            arrowwidth=self.params['arrowwidth'], arrowlength=self.params['arrowlength']
                                            ))
        self.params['drop'] = (1, .4)
        self._labelhints['a'] = LabelHint((0, -.18), valign='top', halign='center')
        self._labelhints['b'] = LabelHint((0, .18), valign='bottom', halign='center')
        self._labelhints['c'] = LabelHint((0, -.18), valign='top', halign='center')


class Button(Element2Term):
    ''' Push button switch

        Args:
            nc: Normally closed
            contacts: Draw contacts as open circles
    '''
    def __init__(self, nc: bool = False, contacts: bool = True, **kwargs):
        super().__init__(**kwargs)

        if contacts:
            lead_path_in = [(0, 0), gap]
            lead_path_out = [gap, (1, 0)]
        else:
            lead_path_in = [(0, 0), (sw_dot_r, 0), gap]
            lead_path_out = [gap, (1-sw_dot_r, 0), (1, 0)]

        if nc:
            bary = -sw_dot_r-0.05
            button_top = sw_dot_r+0.15
        else:
            bary = .3
            button_top = .5

        actuator_path = [(sw_dot_r, bary), (1-sw_dot_r, bary),
                         gap,
                         (.5, bary), (.5, button_top)
                         ]

        self.segments.append(Segment(lead_path_in + actuator_path + lead_path_out))

        if contacts:
            self.segments.append(SegmentCircle((sw_dot_r, 0), sw_dot_r))
            self.segments.append(SegmentCircle((1-sw_dot_r, 0), sw_dot_r))


class SwitchDpst(Element):
    ''' Double-pole single-throw switch

        Args:
            link: Show dotted line linking switch levers
            contacts: Draw contacts as open circles

        Anchors:
            * p1
            * p2
            * t1
            * t2
    '''
    def __init__(self, link: bool = True, contacts: bool = True, **kwargs):
        super().__init__(**kwargs)
        yofst = -1
        if contacts:
            p1_path = [(0, 0), gap, (sw_dot_r*2, .1), (.8, .45), gap, (1, 0)]
            p2_path = [(sw_dot_r*2, yofst+.1), (.8, yofst+0.45)]
            self.anchors['p1'] = (sw_dot_r, 0)
            self.anchors['t1'] = (1-sw_dot_r, 0)
            self.anchors['p2'] = (sw_dot_r, yofst)
            self.anchors['t2'] = (1-sw_dot_r, yofst)
        else:
            p1_path = [(0, 0), (.8, .45), gap, (1, 0)]
            p2_path = [(0, yofst), (.8, yofst+0.45)]
            self.anchors['p1'] = (0, 0)
            self.anchors['t1'] = (1, 0)
            self.anchors['p2'] = (0, yofst)
            self.anchors['t2'] = (1, yofst)
        self._labelhints['p1'] = LabelHint((-.1, .15), valign='bottom', halign='right')
        self._labelhints['p2'] = LabelHint((-.1, -.15), valign='top', halign='right')
        self._labelhints['t1'] = LabelHint((.1, .15), valign='bottom', halign='left')
        self._labelhints['t2'] = LabelHint((.1, -.15), valign='top', halign='left')

        self.segments.append(Segment(p1_path))
        self.segments.append(Segment(p2_path))

        if contacts:
            self.segments.append(SegmentCircle((sw_dot_r, 0), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, 0), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((sw_dot_r, yofst), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, yofst), sw_dot_r, fill='bg', zorder=3))
        if link:
            self.segments.append(Segment([(0.5, yofst+.25),
                                          (0.5, 0.2)], ls=':'))


class SwitchDpdt(Element):
    ''' Double-pole double-throw switch

        Args:
            link: Show dotted line linking switch levers
            contacts: Draw contacts as open circles

        Anchors:
            * p1
            * p2
            * t1
            * t2
            * t3
            * t4
    '''
    def __init__(self, link: bool = True, contacts: bool = True, **kwargs):
        super().__init__(**kwargs)
        yofst = -1.4
        if contacts:
            p1_path = [(0, 0), gap, (sw_dot_r*2, .1), (.7, .25), gap, (1, .4)]
            p2_path = [(sw_dot_r*2, yofst+.1), (.7, yofst+0.25)]
            self.anchors['p1'] = (sw_dot_r, 0)
            self.anchors['t1'] = (1-sw_dot_r, .4)
            self.anchors['t2'] = (1-sw_dot_r, -.4)
            self.anchors['p2'] = (sw_dot_r, yofst)
            self.anchors['t3'] = (1-sw_dot_r, yofst+.4)
            self.anchors['t4'] = (1-sw_dot_r, yofst-.4)
        else:
            p1_path = [(0, 0), (.7, .25), gap, (1, .4)]
            p2_path = [(0, yofst), (.7, yofst+0.25)]
            self.anchors['p1'] = (0, 0)
            self.anchors['t1'] = (1, .4)
            self.anchors['t2'] = (1, -.4)
            self.anchors['p2'] = (0, yofst)
            self.anchors['t3'] = (1, yofst+.4)
            self.anchors['t4'] = (1, yofst-.4)
        self._labelhints['p1'] = LabelHint((-.1, .15), valign='bottom', halign='right')
        self._labelhints['p2'] = LabelHint((-.1, -.15), valign='top', halign='right')
        self._labelhints['t1'] = LabelHint((.1, .15), valign='bottom', halign='left')
        self._labelhints['t4'] = LabelHint((.1, -.15), valign='top', halign='left')
        self._labelhints['t2'] = LabelHint((.1, .15), valign='bottom', halign='left')
        self._labelhints['t3'] = LabelHint((.1, -.15), valign='top', halign='left')

        self.segments.append(Segment(p1_path))
        self.segments.append(Segment(p2_path))

        if contacts:
            self.segments.append(SegmentCircle((sw_dot_r, 0), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, -.4), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, .4), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((sw_dot_r, yofst), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, yofst-.4), sw_dot_r, fill='bg', zorder=3))
            self.segments.append(SegmentCircle((1-sw_dot_r, yofst+.4), sw_dot_r, fill='bg', zorder=3))
        if link:
            self.segments.append(Segment([(0.5, yofst+.25),
                                          (0.5, 0.2)], ls=':'))


class SwitchReed(Element2Term):
    ''' Reed Switch '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment(
            [(0, 0), (.85, .15), gap, (.8, 0)]))

        r = .3
        th = linspace(-math.pi/2, math.pi/2)
        x1 = [-r * math.cos(t) for t in th]  # Left semicircle
        y1 = [r * math.sin(t) for t in th]
        x2 = [1-k for k in x1]  # Right semicircle

        x = x1 + x2 + [x1[0]]   # Combined
        y = y1 + y1[::-1] + [y1[0]]
        self.segments.append(Segment(list(zip(x, y))))


class SwitchRotary(Element):
    ''' Rotary Switch

        Args:
            n: number of contacts
            dtheta: angle in degrees between each contact
            theta0: angle in degrees of first contact
            radius: radius of switch
            arrowlen: length of switch arrow
            arrowcontact: index of contact to point to

        Values for dtheta and theta will be calculated based on `n`
        if not provided.

        Anchors:
            * P
            * T[x] for each contact (starting at 1)
    '''
    def __init__(self, *,
                 n: int = 4, dtheta: Optional[float] = None, theta0: Optional[float] = None,
                 radius: float = 1, arrowlen: float = 0.75,
                 arrowcontact: int = 0,
                 **kwargs):
        super().__init__(**kwargs)
        self.elmparams['fill'] = 'bg'
        self.elmparams['zorder'] = 4
        self.segments.append(SegmentCircle((0, 0), sw_dot_r))
        self.anchors['P'] = (0, 0)

        if dtheta is None:
            dtheta = min(35, 360/(n+1))

        dtheta = math.radians(dtheta)
        if theta0 is None:
            theta0 = -dtheta * (n-1)/2

        for i in range(n):
            t = theta0 + dtheta * i
            x = radius * math.cos(t)
            y = radius * math.sin(t)
            self.segments.append(SegmentCircle((x, y), sw_dot_r))
            self.anchors[f'T{i+1}'] = (x, y)
            self._labelhints[f'T{i+1}'] = LabelHint((0, .1), valign='bottom', halign='center', fontsize=9)

            if i == arrowcontact:
                arrowx = arrowlen * math.cos(t)
                arrowy = arrowlen * math.sin(t)
                self.segments.append(Segment([(0, 0), (arrowx, arrowy)], arrow='->', zorder=2))
        self._labelhints['P'] = LabelHint((-.1, .1), valign='bottom', halign='right')


class SwitchDIP(Element):
    ''' DIP switch

        Args:
            n: Number of switches
            pattern: Boolean sequence indicating whether each switch is flipped up or down
            switchcolor: Fill color for flipped switches [default: #333333]
            swidth: Width of one switch [default: 0.4]
            spacing: Spacing between switches [default: 0.2]
    '''
    _element_defaults = {
        'switchcolor': '#333333',
        'swidth': 0.4,
        'spacing': 0.2
    }
    def __init__(self, *,
                 n: int = 3,
                 pattern: Optional[Sequence[bool]] = None,
                 switchcolor: Optional[str] = None,
                 swidth: Optional[float] = None,
                 spacing: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        _swidth: float = self.params['swidth']
        _spacing: float = self.params['spacing']
        width = _swidth * n + _spacing*(n+1)
        height = _swidth*2 + _spacing * 2

        self.segments.append(SegmentPoly(((0, 0), (width, 0), (width, height), (0, height))))
        for i in range(n):
            x = _spacing * (i+1) + _swidth * i
            up = pattern and pattern[i]
            down = pattern and not pattern[i]
            self.segments.append(SegmentPoly(((x, _spacing+_swidth), (x+_swidth, _spacing+_swidth),
                                              (x+_swidth, _spacing+_swidth*2), (x, _spacing+_swidth*2)),
                                             fill=self.params['switchcolor'] if up else None))  # Upper
            self.segments.append(SegmentPoly(((x, _spacing), (x+_swidth, _spacing),
                                              (x+_swidth, _spacing+_swidth), (x, _spacing+_swidth)),
                                             fill=self.params['switchcolor'] if down else None))  # Lower
            self.anchors[f'a{i+1}'] = (x + _swidth/2, 0)
            self.anchors[f'b{i+1}'] = (x + _swidth/2, height)
