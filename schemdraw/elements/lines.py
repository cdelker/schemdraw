''' Lines, Arrows, and Labels '''

from collections import ChainMap

from ..transform import Transform
from ..segments import *
from .elements import Element
from .twoterm import Element2Term, gap
from ..adddocs import adddocs



class Line(Element2Term):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0,0]], **kwargs))
        
        
@adddocs(Element2Term)
class Arrow(Line):
    ''' Arrow element
    
        Parameters
        ----------
        double : bool
            Show arrowhead on both ends

    '''
    def setup(self, **kwargs):
        super().setup(**kwargs)
#        kwargs = ChainMap(kwargs, {'headwidth':.3, 'headlength': .3})
        self.segments.append(SegmentArrow([-.3, 0], [0, 0], ref='end', **kwargs))
        if kwargs.get('double', False):
            self.segments.append(SegmentArrow([.3, 0], [0, 0], ref='start', **kwargs))


@adddocs(Element2Term)
class LineDot(Line):
    ''' Line with a dot at the end
    
        Parameters
        ----------
        double : bool
            Show dot on both ends
    '''    
    def setup(self, **kwargs):
        super().setup(**kwargs)
        radius = kwargs.get('radius', 0.075)
        fill = kwargs.pop('fill', 'white' if kwargs.get('open', False) else 'black')
        args = ChainMap({'fill': fill, 'zorder': 4}, kwargs)
        self.segments.append(SegmentCircle([0, 0], radius, ref='end', **args))
        if kwargs.get('double', False):
            self.segments.append(SegmentCircle([0, 0], radius, ref='start', **args))


class Gap(Element2Term):
    def setup(self, **kwargs):
        kwargs['color'] = self.userparams.get('color', 'white')
        self.segments.append(Segment([[0, 0], gap, [1, 0]], **kwargs))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['zorder'] = 0


class Dot(Element):
    ''' Connection Dot
    
        Parameters
        ----------
        radius : float
            Radius of dot
            
        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def setup(self, **kwargs):
        radius = kwargs.pop('radius', 0.075)
        if 'fill' not in kwargs or kwargs['fill'] is None:
            fill = 'white' if kwargs.get('open', False) else True
            kwargs = ChainMap({'fill': fill}, kwargs)
        kwargs = ChainMap({'zorder': 9}, kwargs)
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.segments.append(SegmentCircle([0, 0], radius, **kwargs))


class Arrowhead(Element):
    def setup(self, **kwargs):
        self.segments.append(SegmentArrow([-.3, 0], [0, 0], headwidth=.3, headlength=.3, **kwargs))
        self.theta = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]                
        self.params['lblofst'] = .25


@adddocs(Element)
class DotDotDot(Element):
    ''' Ellipsis element
    
        Parameters
        ----------
        radius : float
            Radius of dots
        open : bool
            Draw open dots

        Note
        ----
        "Ellipsis" is a reserved keyword in Python used for slicing, thus
        the name DotDotDot.
    '''
    def setup(self, **kwargs):
        radius = kwargs.pop('radius', .075)
        if 'fill' not in kwargs or kwargs['fill'] is None:
            fill = 'white' if kwargs.get('open', False) else True
            kwargs = ChainMap({'fill': fill}, kwargs)
        self.segments.append(SegmentCircle([.5, 0], radius, **kwargs))
        self.segments.append(SegmentCircle([1, 0], radius, **kwargs))
        self.segments.append(SegmentCircle([1.5, 0], radius, **kwargs))
        self.params['drop'] = [2, 0]
        

class Label(Element):
    def setup(self, **kwargs):
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0

        
@adddocs(Element)
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
    '''        
    def setup(self, **kwargs):
        ofst = kwargs.pop('ofst', 0.4)
        length = kwargs.pop('length', 2)
        top = kwargs.pop('top', True)
        reverse = kwargs.pop('rev', False)
        self.params['lblofst'] = .1    
        self.params['drop'] = None  # None means don't move xy from previous element
        self.anchor = 'center'
        self.anchors['center'] = [0, 0]        

        if not top:
            ofst = -ofst
            self.params['lblloc'] = 'bot'
        a, b = [-length/2, ofst], [length/2, ofst]
        
        if reverse:
            a, b = b, a

        self.segments.append(SegmentArrow(a, b, headwidth=.2, headlength=.3, **kwargs))


@adddocs(Element)
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


@adddocs(Element)
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
    '''
    def setup(self, **kwargs):
        direction = kwargs.get('direction', 'cw')
        kwargs.setdefault('theta1', 35)
        kwargs.setdefault('theta2', -35)
        kwargs.setdefault('width', .75)
        kwargs.setdefault('height', .75)
        self.segments.append(SegmentArc([0, 0], arrow=direction, **kwargs))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = 0
        self.anchors['center'] = [0, 0]


class Rect(Element):
    def setup(self, **kwargs):
        c1 = kwargs.get('corner1', [0, 0])
        c2 = kwargs.get('corner2', [1, 1])
        c1a = [c1[0], c2[1]]
        c2a = [c2[0], c1[1]]
        self.segments.append(Segment([c1, c1a, c2, c2a, c1], **kwargs))
        self.params['zorder'] = 0   # Put on bottom
        