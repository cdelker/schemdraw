''' Transistor elements '''

import numpy as np

from .elements import Element, gap
from .twoterm import reswidth
from ..transform import Transform
from ..segments import *
from ..adddocs import adddocs


fetw = reswidth*4
feth = reswidth*5
fetl = feth/2
fetgap = reswidth*1.5
fetr = reswidth*.7  # Radius of "not" bubble


@adddocs(Element)
class NFet(Element):
    ''' N-type Field Effect Transistor
        Anchors: `source`, `drain`, `gate`.

        Parameters
        ----------
        bulk : bool
            Draw bulk contact
    '''
    def setup(self, **kwargs):
        bulk = kwargs.pop('bulk', False)
        self.segments.append(Segment([[0, 0], [0, -fetl], [fetw, -fetl], [fetw, -fetl-fetw], [0, -fetl-fetw], [0, -2*fetl-fetw]], **kwargs))
        self.segments.append(Segment([[fetw+fetgap, -fetl], [fetw+fetgap, -fetl-fetw]], **kwargs))
        self.segments.append(Segment([[fetw+fetgap, -fetl-fetw/2], [fetw+fetgap+fetl+fetr, -fetl-fetw/2]], **kwargs))
        self.anchors['source'] = [0, -2*fetl-fetw]
        self.anchors['drain'] = [0, 0]
        self.anchors['gate'] = [fetw+fetgap+fetl+fetr, -fetl-fetw/2]
        self.params['drop'] = [0, -2*fetl-fetw]
        self.params['lblloc'] = 'lft'
        if bulk:
            self.segments.append(SegmentArrow([0, -fetl-fetw/2], [fetw, -fetl-fetw/2], headwidth=.2, **kwargs))
            self.anchors['bulk'] = [0, -fetl-fetw/2]


@adddocs(Element)
class PFet(Element):
    ''' P-type Field Effect Transistor
        Anchors: `source`, `drain`, `gate`.    
    
        Parameters
        ----------
        bulk : bool
            Draw bulk contact
    '''
    def setup(self, **kwargs):
        bulk = kwargs.pop('bulk', False)
        self.segments.append(Segment([[0, 0], [0, -fetl], [fetw, -fetl], [fetw, -fetl-fetw], [0, -fetl-fetw], [0, -2*fetl-fetw]], **kwargs))
        self.segments.append(Segment([[fetw+fetgap, -fetl], [fetw+fetgap, -fetl-fetw]], **kwargs))
        self.segments.append(Segment([[fetw+fetgap+fetr*2, -fetl-fetw/2], [fetw+fetgap+fetl+fetr, -fetl-fetw/2]], **kwargs))
        self.segments.append(SegmentCircle([fetw+fetgap+fetr, -fetl-fetw/2], fetr, **kwargs))
        
        self.anchors['source'] = [0, 0]
        self.anchors['drain'] = [0, -2*fetl-fetw]
        self.anchors['gate'] = [fetw+fetgap+fetl+fetr, -fetl-fetw/2]
        self.params['drop'] = [0, -2*fetl-fetw]
        self.params['lblloc'] = 'lft'
        if bulk:
            self.segments.append(SegmentArrow([0, -fetl-fetw/2], [fetw, -fetl-fetw/2], headwidth=.2, **kwargs))
            self.anchors['bulk'] = [0, -fetl-fetw/2]


# Junction FETs
fete = fetw*.2  # JFET extension
jfetw = reswidth*3

@adddocs(Element)
class JFet(Element):
    ''' Junction Field Effect Transistor
        Anchors: `source`, `drain`, `gate`.
    '''
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [0, -fetl], [jfetw, -fetl], [jfetw, -fetl+fete], [jfetw, -fetl-jfetw-fete],
                                       [jfetw, -fetl-jfetw], [0, -fetl-jfetw], [0, -2*fetl-jfetw]], **kwargs))
        self.segments.append(Segment([[jfetw, -fetl-jfetw], [jfetw+fetl, -fetl-jfetw]], **kwargs))
        self.params['drop'] = [jfetw+fetl, -fetl-jfetw]
        self.anchors['source'] = [0, -2*fetl-jfetw]
        self.anchors['drain'] = [0, 0]
        self.anchors['gate'] = [jfetw+fetl, -fetl-jfetw]
        self.params['lblloc'] = 'lft'


@adddocs(Element)
class JFetN(JFet):
    ''' N-type Junction Field Effect Transistor
        Anchors: `source`, `drain`, `gate`.

        Parameters
        ----------
        circle : bool
            Draw circle around the transistor
    '''
    def setup(self, **kwargs):
        super().setup(**kwargs)
        circle = kwargs.get('circle', False)
        self.segments.append(SegmentArrow([jfetw+.1, -fetl-jfetw], [jfetw+.3, -fetl-jfetw], headwidth=.3, headlength=.2, **kwargs))
        if circle:
            self.segments.append(SegmentCircle([jfetw/2, -fetw], fetw*1.1, **kwargs))


@adddocs(Element)
class JFetP(JFet):
    ''' P-type Junction Field Effect Transistor
        Anchors: `source`, `drain`, `gate`.

        Parameters
        ----------
        circle : bool
            Draw circle around the transistor
    '''
    def setup(self, **kwargs):
        super().setup(**kwargs)        
        circle = kwargs.get('circle', False)
        self.segments.append(SegmentArrow([jfetw+.25, -fetl-jfetw], [jfetw, -fetl-jfetw], headwidth=.3, headlength=.2, **kwargs))
        if circle:
            self.segments.append(SegmentCircle([jfetw/2, -fetw], fetw*1.1, **kwargs))


# BJT transistors
bjt_r = reswidth*3.3   # Radius of BJT circle
bjt_v = bjt_r*2/3  # x coord of vertical line
bjt_v_len = bjt_r*4/3  # height of vertical line
bjt_a = bjt_v_len/4    # Intercept of emitter/collector lines
bjt_emx = bjt_v + bjt_r*.7  # x-coord of emitter exiting circle
bjt_emy = bjt_v_len*.7    # y-coord of emitter exiting circle

@adddocs(Element)
class Bjt(Element):
    ''' Bipolar Junction Transistor
        Anchors: `collector`, `emitter`, `base`.

        Parameters
        ----------
        circle : bool
            Draw circle around the transistor
    '''
    def setup(self, **kwargs):
        circle = kwargs.get('circle', False)
        self.segments.append(Segment([[0, 0], [bjt_v, 0]], **kwargs))
        self.segments.append(Segment([[bjt_v, bjt_v_len/2], [bjt_v, -bjt_v_len/2]], **kwargs))
        self.segments.append(Segment([[bjt_v, bjt_a], [bjt_emx, bjt_emy], [bjt_emx, bjt_emy+bjt_a]], **kwargs))
        self.segments.append(Segment([[bjt_v, -bjt_a], [bjt_emx, -bjt_emy], [bjt_emx, -bjt_emy-bjt_a]], **kwargs))
        if circle:
            self.segments.append(SegmentCircle([bjt_r, 0], bjt_r, **kwargs))
        self.params['drop'] = [bjt_emx, bjt_emy+bjt_a]
        self.params['lblloc'] = 'rgt'
        self.anchors['base'] = [0, 0]
        self.anchors['collector'] = [bjt_emx, bjt_emy+bjt_a]
        self.anchors['emitter'] = [bjt_emx, -bjt_emy-bjt_a]


class BjtNpn(Bjt):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentArrow([bjt_v, -bjt_a], [bjt_emx, -bjt_emy], headwidth=.2, **kwargs))


class BjtPnp(Bjt):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentArrow([bjt_emx, bjt_emy], [bjt_v, bjt_a], headwidth=.2, **kwargs))
        self.anchors['base'] = [0, 0]
        self.anchors['collector'] = [bjt_emx, -bjt_emy-bjt_a]
        self.anchors['emitter'] = [bjt_emx, bjt_emy+bjt_a]


@adddocs(Element)
class BjtPnp2c(BjtPnp):
    ''' PNP Bipolar Junction Transistor with 2 collectors
        Anchors: `collector`, `C2`, `emitter`, `base`.
    '''    
    def setup(self, **kwargs):
        super().setup(**kwargs)
        bjt_2c_dy = -.25        
        self.segments.append(Segment([[bjt_v, -bjt_a-bjt_2c_dy], [bjt_emx, -bjt_emy-bjt_2c_dy]], **kwargs))
        self.anchors['C2'] = [bjt_emx, -bjt_emy-bjt_2c_dy]
