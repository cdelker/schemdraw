''' One terminal element definitions '''

from collections import ChainMap
import numpy as np

from ..transform import Transform
from ..segments import *
from .elements import Element
from .twoterm import resheight, gap
from ..adddocs import adddocs


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
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


class GroundSignal(Element):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [0, -gnd_lead], [-resheight, -gnd_lead], [0, -gnd_lead*2],
                                      [resheight, -gnd_lead], [0, -gnd_lead]], **kwargs))
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0        
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


class GroundChassis(Element):
    def setup(self, **kwargs):
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, -gnd_lead], [-dx, -gnd_lead-dy]], **kwargs))
        self.segments.append(Segment([[0, -gnd_lead], [-dx, -gnd_lead], [-dx*2, -gnd_lead-dy]], **kwargs))
        self.segments.append(Segment([[0, -gnd_lead], [dx, -gnd_lead], [0, -gnd_lead-dy]], **kwargs))
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        

        
class Antenna(Element):
    def setup(self, **kwargs):
        lead = 0.6
        h = 0.6
        w = 0.38        
        self.segments.append(Segment([[0, 0], [0, lead], [-w, lead+h], [w, lead+h], [0, lead]], **kwargs))
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


class Vss(Element):
    def setup(self, **kwargs):
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, -gnd_lead]], **kwargs))
        self.segments.append(Segment([[0, -gnd_lead], [-dx, -gnd_lead]], **kwargs))
        self.segments.append(Segment([[0, -gnd_lead], [dx, -gnd_lead]], **kwargs))
        self.theta = 0        
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


class Vdd(Element):
    def setup(self, **kwargs):
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, gnd_lead]], **kwargs))
        self.segments.append(Segment([[0, gnd_lead], [-dx, gnd_lead]], **kwargs))
        self.segments.append(Segment([[0, gnd_lead], [dx, gnd_lead]], **kwargs))
        self.theta = 0        
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


