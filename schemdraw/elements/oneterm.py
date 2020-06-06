''' One terminal element definitions '''

from collections import ChainMap
import numpy as np
import matplotlib.pyplot as plt

from ..transform import Transform
from ..segments import *
from .elements import Element
from .twoterm import resheight, gap


gndgap = 0.12
gnd_lead = 0.4
class Ground(Element):
    def setup(self, **kwargs):
        self.segments = [Segment([[0, 0], [0, -gnd_lead], [-resheight, -gnd_lead], [resheight, -gnd_lead],
                                  gap, [-resheight*.7, -gndgap-gnd_lead], [resheight*.7, -gndgap-gnd_lead],
                                  gap, [-resheight*.2, -gndgap*2-gnd_lead],
                                  [resheight*.2, -gndgap*2-gnd_lead]], **kwargs)]
        self.params['theta'] = 0
        self.params['drop'] = [0, 0]


class GroundSignal(Element):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [0, -gnd_lead], [-resheight, -gnd_lead], [0, -gnd_lead*2],
                                      [resheight, -gnd_lead], [0, -gnd_lead]], **kwargs))
        self.params['drop'] = [0, 0]


class GroundChassis(Element):
    def setup(self, **kwargs):
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, -gnd_lead], [-dx, -gnd_lead-dy]], **kwargs))
        self.segments.append(Segment([[0, -gnd_lead], [-dx, -gnd_lead], [-dx*2, -gnd_lead-dy]], **kwargs))
        self.segments.append(Segment([[0, -gnd_lead], [dx, -gnd_lead], [0, -gnd_lead-dy]], **kwargs))
        self.params['drop'] = [0, 0]

        
class Antenna(Element):
    def setup(self, **kwargs):
        lead = 0.6
        h = 0.6
        w = 0.38        
        self.segments.append(Segment([[0, 0], [0, lead], [-w, lead+h], [w, lead+h], [0, lead]], **kwargs))
        self.params['drop'] = [0, 0]


class Vss(Element):
    def setup(self, **kwargs):
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, -gnd_lead]], **kwargs))
        self.segments.append(Segment([[0, -gnd_lead], [-dx, -gnd_lead]], **kwargs))
        self.segments.append(Segment([[0, -gnd_lead], [dx, -gnd_lead]], **kwargs))
        self.params['drop'] = [0, 0]


class Vdd(Element):
    def setup(self, **kwargs):
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, gnd_lead]], **kwargs))
        self.segments.append(Segment([[0, gnd_lead], [-dx, gnd_lead]], **kwargs))
        self.segments.append(Segment([[0, gnd_lead], [dx, gnd_lead]], **kwargs))
        self.params['drop'] = [0, 0]


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
        fill = kwargs.pop('fill', 'white' if kwargs.pop('open', False) else 'black')
        args = ChainMap({'fill': fill, 'zorder': 4}, kwargs)
        self.segments.append(SegmentCircle([0, 0], radius, **args))


class Arrowhead(Element):
    def setup(self, **kwargs):
        self.segments.append(SegmentArrow([-.3, 0], [0, 0], headwidth=.3, headlength=.3, **kwargs))
        self.params['lblofst'] = .25

        
class DotDotDot(Element):   # Used to call this ELLIPSIS, but that's a reserved class in Python slicing
    ''' Ellipsis element
    
        Parameters
        ----------
        radius : float
            Radius of dots
        open : bool
            Draw open dots

        Keyword Arguments
        -----------------
        See schemdraw.Element
        
        Note
        ----
        "Ellipsis" is a reserved keyword in Python used for slicing, thus
        the name DotDotDot.
    '''
    def setup(self, **kwargs):
        radius = kwargs.pop('radius', .075)
        fill = kwargs.pop('fill', 'white' if kwargs.pop('open', False) else 'black')
        args = ChainMap({'fill': fill}, kwargs)        
        self.segments.append(SegmentCircle([.5, 0], radius, **args))
        self.segments.append(SegmentCircle([1, 0], radius, **args))
        self.segments.append(SegmentCircle([1.5, 0], radius, **args))
        self.params['drop'] = [2, 0]
        

class Label(Element):
    def setup(self, **kwargs):
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
