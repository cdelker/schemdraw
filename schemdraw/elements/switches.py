''' Switches and buttons '''

from collections import ChainMap

from .elements import Element, Element2Term, gap
from ..transform import Transform
from ..segments import *
from ..adddocs import adddocs


sw_dot_r = .12


@adddocs(Element2Term)
class Switch(Element2Term):
    ''' Switch
    
        Parameters
        ----------
        action : string or None
            'open' or 'close', action arrow to draw
    '''
    def setup(self, **kwargs):
        action = kwargs.get('action', None)        
        self.segments.append(Segment([[0, 0], gap, [sw_dot_r*2, .1], [.8, .45], gap, [1, 0]], **kwargs))
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, 0], sw_dot_r, **kwargs))        
        if action == 'open':
            self.segments.append(SegmentArc([.4, .1], width=.5, height=.75, theta1=-10, theta2=70, arrow='ccw'))
        if action == 'close':
            self.segments.append(SegmentArc([.4, .25], width=.5, height=.75, theta1=-10, theta2=70, arrow='cw'))


@adddocs(Switch)
class SwitchSpdt(Switch):
    ''' Single-pole double throw switch.
        Anchors: `a`, `b`, `c`.
    '''
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentCircle([1-sw_dot_r, .7], sw_dot_r, **kwargs))
        self.anchors['a'] = [0, 0]
        self.anchors['b'] = [1, 0]
        self.anchors['c'] = [1, .7]


@adddocs(Element)
class SwitchSpdt2(Element):
    ''' Single-pole double throw switch, throws above and below.
        Anchors: `a`, `b`, `c`.
    
        Parameters
        ----------
        action : string or None
            'open' or 'close', action arrow to draw
    '''
    def setup(self, **kwargs):
        action = kwargs.get('action', None)        
        self.segments.append(Segment([[0, 0], gap, [sw_dot_r*2, .1], [.7, .25], gap, [1, .4]], **kwargs))
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, -.4], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, .4], sw_dot_r, **kwargs))
        self.anchors['a'] = [0, 0]
        self.anchors['b'] = [1, .4]
        self.anchors['c'] = [1, -.4]
        if action == 'open':
            self.segments.append(SegmentArc([.35, 0], width=.5, height=.75, theta1=-10, theta2=70, arrow='ccw'))
        elif action == 'close':
            self.segments.append(SegmentArc([.3, 0], width=.5, height=.75, theta1=-10, theta2=70, arrow='cw'))            
        self.params['drop'] = [1, .4]


@adddocs(Element2Term)
class Button(Element2Term):
    ''' Push button

        Parameters
        ----------
        nc : bool
            Normally closed?
    '''
    def setup(self, **kwargs):
        if kwargs.get('nc', False):
            self.segments.append(Segment([[0, 0], gap, [sw_dot_r, -sw_dot_r-.05],
                                          [1-sw_dot_r, -sw_dot_r-.05], gap, [.5, -sw_dot_r-.05],
                                          [.5, sw_dot_r+.15], gap, [1, 0]], **kwargs))            
        else:
            self.segments.append(Segment([[0, 0], gap, [sw_dot_r, .3], [1-sw_dot_r, .3],
                                         gap, [.5, .3], [.5, .5], gap, [1, 0]], **kwargs))
            
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, 0], sw_dot_r, **kwargs))        

        
class SwitchDpst(Element):
    def setup(self, **kwargs):
        yofst = -1
        self.segments.append(Segment([[0, 0], gap, [sw_dot_r*2, .1], [.8, .45], gap, [1, 0]], **kwargs))
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, 0], sw_dot_r, **kwargs))        
        self.segments.append(Segment([[0, yofst], gap, [sw_dot_r*2, yofst+.1], [.8, yofst+.45], gap, [1, yofst]], **kwargs))
        self.segments.append(SegmentCircle([sw_dot_r, yofst], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, yofst], sw_dot_r, **kwargs))
        kwargs = ChainMap({'ls': ':'}, kwargs)
        self.segments.append(Segment([[0.5, yofst+.25], [0.5, 0.2]], **kwargs))
        self.anchors['p1'] = [0, 0]
        self.anchors['t1'] = [1, 0]
        self.anchors['p2'] = [0, yofst]
        self.anchors['t2'] = [1, yofst]
        

class SwitchDpdt(Element):
    def setup(self, **kwargs):
        yofst = -1.4
        self.segments.append(Segment([[0, 0], gap, [sw_dot_r*2, .1], [.7, .25], gap, [1, .4]], **kwargs))
        self.segments.append(SegmentCircle([sw_dot_r, 0], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, -.4], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, .4], sw_dot_r, **kwargs))
        self.segments.append(Segment([[0, yofst], gap, [sw_dot_r*2, yofst+.1], [.7, yofst+.25], gap, [1, yofst+.4]], **kwargs))
        self.segments.append(SegmentCircle([sw_dot_r, yofst], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, yofst-.4], sw_dot_r, **kwargs))
        self.segments.append(SegmentCircle([1-sw_dot_r, yofst+.4], sw_dot_r, **kwargs))
        kwargs = ChainMap({'ls': ':'}, kwargs)
        self.segments.append(Segment([[0.5, yofst+.25], [0.5, 0.2]], **kwargs))
        self.anchors['p1'] = [0, 0]
        self.anchors['t1'] = [1, .4]
        self.anchors['t2'] = [1, -.4]
        self.anchors['p2'] = [0, yofst]
        self.anchors['t3'] = [1, yofst+.4]
        self.anchors['t4'] = [1, yofst-.4]  