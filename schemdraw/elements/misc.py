''' Other elements '''

from collections import ChainMap
import numpy as np

from .elements import Element, Element2Term, gap
from .twoterm import resheight
from ..transform import Transform
from ..segments import *
from ..adddocs import adddocs


@adddocs(Element)
class Speaker(Element):
    ''' Speaker element with two inputs. Anchors: `in1`, `in2`. '''
    def setup(self, **kwargs):
        sph = .5
        self.segments.append(Segment([[0, 0], [resheight, 0]], **kwargs))
        self.segments.append(Segment([[0, -sph], [resheight, -sph]], **kwargs))
        self.segments.append(SegmentPoly([[resheight, sph/2], [resheight, -sph*1.5], [resheight*2, -sph*1.5], [resheight*2, sph/2]], **kwargs))
        self.segments.append(SegmentPoly([[resheight*2, sph/2], [resheight*3.5, sph*1.25], [resheight*3.5, -sph*2.25], [resheight*2, -sph*1.5]], closed=False, **kwargs))
        self.anchors['in1'] = [0, 0]
        self.anchors['in2'] = [0, -sph]
        self.params['drop'] = [0, -sph]


@adddocs(Element)
class Mic(Element):
    ''' Microphone element with two inputs. Anchors: `in1`, `in2`. '''
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


 