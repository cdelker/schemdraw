''' Other elements '''

import numpy as np

from .elements import Element
from .twoterm import Element2Term, resheight
from ..transform import Transform
from ..segments import *


class Speaker(Element):
    def setup(self, **kwargs):
        sph = .5
        self.segments.append(Segment([[0, 0], [resheight, 0]], **kwargs))
        self.segments.append(Segment([[0, -sph], [resheight, -sph]], **kwargs))
        self.segments.append(SegmentPoly([[resheight, sph/2], [resheight, -sph*1.5], [resheight*2, -sph*1.5], [resheight*2, sph/2]], **kwargs))
        self.segments.append(SegmentPoly([[resheight*2, sph/2], [resheight*3.5, sph*1.25], [resheight*3.5, -sph*2.25], [resheight*2, -sph*1.5]], closed=False))
        self.anchors['in1'] = [0, 0]
        self.anchors['in2'] = [0, -sph]
        self.params['drop'] = [0, -sph]
                             

class Mic(Element):
    def setup(self, **kwargs):
        sph = .5
        self.segments.append(Segment([[0, 0], [resheight, 0]], **kwargs))  # Upper lead
        self.segments.append(Segment([[0, -sph], [resheight, -sph]], **kwargs))  # Lower lead
        self.segments.append(Segment([[-resheight*2, resheight], [-resheight*2, -resheight*3]], **kwargs))  # Vertical flat
        self.segments.append(SegmentArc([-resheight*2, -resheight], theta1=270, theta2=90, width=resheight*4, height=resheight*4, **kwargs))
        self.anchors['in1'] = [resheight, 0]
        self.anchors['in2'] = [resheight, -sph]
        self.params['drop'] = [0, -sph]


class Motor(Element2Term):
    def setup(self, **kwargs):
        mw = .22
        self.segments.append(Segment([[-mw, 0], [-mw, 0], gap, [1+mw, 0], [1+mw, 0]], **kwargs))        
        self.segments.append(Segment([[0, -mw], [0-mw, -mw], [0-mw, mw], [0, mw]], **kwargs))
        self.segments.append(Segment([[1, -mw], [1+mw, -mw], [1+mw, mw], [1, mw]], **kwargs))
        self.segments.append(SegmentCircle([0.5, 0], 0.5, **kwargs))


class CurrentLabel(Element):
    ''' Current label arrow drawn above an element

        Parameters
        ----------
        ofst : float
            Offset distance from element
        length : float
            Length of the arrow
        top : bool
            Draw arrow on top or bottom of element
        rev : bool
            Reverse the arrow direction

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''        
    def setup(self, **kwargs):
        ofst = kwargs.pop('ofst', 0.4)
        length = kwargs.pop('length', 2)
        top = kwargs.pop('top', True)
        reverse = kwargs.pop('rev', False)
        self.lblofst = .1    
        self.drop = None  # None means don't move xy from previous element
        self.anchor = 'center'
        self.anchors['center'] = [0, 0]        

        if not top:
            ofst = -ofst

        a, b = [-length/2, ofst], [length/2, ofst]
        self.segments.append(SegmentArrow(a, b, headwidth=.2, headlength=.3, **kwargs))


class CurrentLabelInline(Element):
    ''' Loop current label

        Parameters
        ----------
        direction : string
            'in' or 'out' arrow direction
        ofst : float
            Offset along lead length
        start : bool
            Arrow at start or end of element
        headlength : float
            Length of arrowhead
        headwidth : float
            Width of arrowhead

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''    
    def setup(self, **kwargs):
        direction = kwargs.get('direction', 'in')
        ofst = kwargs.get('ofst', .8)
        start = kwargs.get('start', True)
        self.lblofst = .25
        self.drop = None
        hlen = kwargs.get('headlength', .3)
        hwid = kwargs.get('headwidth', .3)
        
        x = ofst
        dx = hlen
        if direction == 'in':
            x += hlen
            dx = -dx
        
        if start:
            x = -x
            dx = -dx

        self.segments.append(SegmentArrow([x, 0], [x+dx, 0], headwidth=hwid, headlength=hlen, **kwargs))


class LoopCurrent(Element):
    ''' Loop current label

        Parameters
        ----------
        direction : string
            'cw' or 'ccw' loop direction
        theta1 : float
            Angle of start of loop arrow
        theta2 : float
            Angle of end of loop arrow
        width : float
            Width of loop
        height : float
            Height of loop

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def setup(self, **kwargs):
        direction = kwargs.get('direction', 'cw')
        theta1 = kwargs.get('theta1', 35)
        theta2 = kwargs.get('theta2', -35)
        width = kwargs.get('width', .75)
        height = kwargs.get('height', .75)
        self.segments.append(SegmentArc([0, 0], theta1=theta1, theta2=theta2, width=width, height=height, arrow=direction))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = 0        
 