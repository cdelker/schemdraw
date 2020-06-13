''' One terminal element definitions '''

import numpy as np

from ..transform import Transform
from ..segments import *
from .elements import Element
from .twoterm import resheight, gap
from ..adddocs import adddocs


gndgap = 0.12
gnd_lead = 0.4
class Ground(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments = [Segment([[0, 0], [0, -gnd_lead], [-resheight, -gnd_lead], [resheight, -gnd_lead],
                                  gap, [-resheight*.7, -gndgap-gnd_lead], [resheight*.7, -gndgap-gnd_lead],
                                  gap, [-resheight*.2, -gndgap*2-gnd_lead],
                                  [resheight*.2, -gndgap*2-gnd_lead]])]
        self.params['theta'] = 0
        self.params['drop'] = [0, 0]
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


class GroundSignal(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [0, -gnd_lead], [-resheight, -gnd_lead], [0, -gnd_lead*2],
                                      [resheight, -gnd_lead], [0, -gnd_lead]]))
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0        
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


class GroundChassis(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, -gnd_lead], [-dx, -gnd_lead-dy]]))
        self.segments.append(Segment([[0, -gnd_lead], [-dx, -gnd_lead], [-dx*2, -gnd_lead-dy]]))
        self.segments.append(Segment([[0, -gnd_lead], [dx, -gnd_lead], [0, -gnd_lead-dy]]))
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        

        
class Antenna(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lead = 0.6
        h = 0.6
        w = 0.38        
        self.segments.append(Segment([[0, 0], [0, lead], [-w, lead+h], [w, lead+h], [0, lead]]))
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


class Vss(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, -gnd_lead]]))
        self.segments.append(Segment([[0, -gnd_lead], [-dx, -gnd_lead]]))
        self.segments.append(Segment([[0, -gnd_lead], [dx, -gnd_lead]]))
        self.theta = 0        
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


class Vdd(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment([[0, 0], [0, gnd_lead]]))
        self.segments.append(Segment([[0, gnd_lead], [-dx, gnd_lead]]))
        self.segments.append(Segment([[0, gnd_lead], [dx, gnd_lead]]))
        self.theta = 0        
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]        


