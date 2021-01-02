''' Switches and buttons '''
from typing import Optional, Literal

from .elements import Element, Element2Term, gap
from ..segments import Segment, SegmentCircle, SegmentArc
from ..types import Point

sw_dot_r = .12

ActionType = Optional[Literal['open', 'close']]


class Switch(Element2Term):
    ''' Toggle Switch

        Args:
            action: action arrow ('open' or 'close')
    '''
    def __init__(self, *d, action: ActionType=None, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(
            [[0, 0], gap, [sw_dot_r*2, .1], [.8, .45], gap, [1, 0]]))
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, 0], sw_dot_r))
        if action == 'open':
            self.segments.append(SegmentArc([.4, .1], width=.5, height=.75,
                                            theta1=-10, theta2=70,
                                            arrow='ccw'))
        if action == 'close':
            self.segments.append(SegmentArc([.4, .25], width=.5, height=.75,
                                            theta1=-10, theta2=70,
                                            arrow='cw'))


class SwitchSpdt(Switch):
    ''' Single-pole double throw switch.

        Args:
            action: action arrow ('open' or 'close')

        Anchors:
            a
            b
            c
    '''
    def __init__(self, *d, action: ActionType=None, **kwargs):
        super().__init__(*d, action=action, **kwargs)
        self.segments.append(SegmentCircle([1-sw_dot_r, .7], sw_dot_r))
        self.anchors['a'] = Point((0, 0))
        self.anchors['b'] = Point((1, 0))
        self.anchors['c'] = Point((1, .7))


class SwitchSpdt2(Element):
    ''' Single-pole double throw switch, throws above and below.

        Args:
            action: action arrow ('open' or 'close')

        Anchors:
            a
            b
            c
    '''
    def __init__(self, *d, action: ActionType=None, **kwargs):
        super().__init__(*d, action=action, **kwargs)
        self.segments.append(Segment([[0, 0], gap, [sw_dot_r*2, .1],
                                      [.7, .25], gap, [1, .4]]))
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, -.4], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, .4], sw_dot_r))
        self.anchors['a'] = Point((0, 0))
        self.anchors['b'] = Point((1, .4))
        self.anchors['c'] = Point((1, -.4))
        if action == 'open':
            self.segments.append(SegmentArc([.35, 0], width=.5, height=.75,
                                            theta1=-10, theta2=70,
                                            arrow='ccw'))
        elif action == 'close':
            self.segments.append(SegmentArc([.3, 0], width=.5, height=.75,
                                            theta1=-10, theta2=70,
                                            arrow='cw'))
        self.params['drop'] = [1, .4]


class Button(Element2Term):
    ''' Push button switch

        Args:
            nc: Normally closed
    '''
    def __init__(self, *d, nc: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        if nc:
            self.segments.append(Segment(
                [[0, 0], gap, [sw_dot_r, -sw_dot_r-.05],
                 [1-sw_dot_r, -sw_dot_r-.05], gap, [.5, -sw_dot_r-.05],
                 [.5, sw_dot_r+.15], gap, [1, 0]]))
        else:
            self.segments.append(Segment(
                [[0, 0], gap, [sw_dot_r, .3], [1-sw_dot_r, .3],
                 gap, [.5, .3], [.5, .5], gap, [1, 0]]))

        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, 0], sw_dot_r))


class SwitchDpst(Element):
    ''' Double-pole single-throw switch

        Args:
            link: Show dotted line linking switch levers

        Anchors:
            p1
            p2
            t1
            t2
    '''
    def __init__(self, *d, link: bool=True, **kwargs):
        super().__init__(*d, **kwargs)
        yofst = -1
        self.segments.append(Segment([[0, 0], gap, [sw_dot_r*2, .1],
                                      [.8, .45], gap, [1, 0]]))
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, 0], sw_dot_r))
        self.segments.append(Segment([[0, yofst], gap, [sw_dot_r*2, yofst+.1],
                                      [.8, yofst+.45], gap, [1, yofst]]))
        self.segments.append(SegmentCircle([sw_dot_r, yofst], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, yofst], sw_dot_r))
        if link:
            self.segments.append(Segment([[0.5, yofst+.25],
                                          [0.5, 0.2]], ls=':'))
        self.anchors['p1'] = [0, 0]
        self.anchors['t1'] = [1, 0]
        self.anchors['p2'] = [0, yofst]
        self.anchors['t2'] = [1, yofst]


class SwitchDpdt(Element):
    ''' Double-pole double-throw switch

        Args:
            link: Show dotted line linking switch levers

        Anchors:
            p1
            p2
            t1
            t2
            t3
            t4
    '''
    def __init__(self, *d, link: bool=True, **kwargs):
        super().__init__(*d, **kwargs)
        yofst = -1.4
        self.segments.append(Segment([[0, 0], gap, [sw_dot_r*2, .1],
                                      [.7, .25], gap, [1, .4]]))
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, -.4], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, .4], sw_dot_r))
        self.segments.append(Segment([[0, yofst], gap, [sw_dot_r*2, yofst+.1],
                                      [.7, yofst+.25], gap, [1, yofst+.4]]))
        self.segments.append(SegmentCircle([sw_dot_r, yofst], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, yofst-.4], sw_dot_r))
        self.segments.append(SegmentCircle([1-sw_dot_r, yofst+.4], sw_dot_r))
        if link:
            self.segments.append(Segment([[0.5, yofst+.25],
                                          [0.5, 0.2]], ls=':'))
        self.anchors['p1'] = [0, 0]
        self.anchors['t1'] = [1, .4]
        self.anchors['t2'] = [1, -.4]
        self.anchors['p2'] = [0, yofst]
        self.anchors['t3'] = [1, yofst+.4]
        self.anchors['t4'] = [1, yofst-.4]
