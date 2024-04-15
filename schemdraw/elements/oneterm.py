''' One terminal element definitions '''
from __future__ import annotations
from typing import Optional

from ..segments import Segment
from .elements import Element
from .twoterm import resheight, gap

gndgap = 0.12
_gnd_lead = 0.4


class Ground(Element):
    ''' Ground connection
    
        Keyword Args:
            lead: Show lead wire [default: True]
    '''
    _element_defaults = {
        'lead': True,
        'theta': 0,
        'drop': (0, 0)
    }
    def __init__(self, *,
                 lead: Optional[bool] = None,
                 **kwargs):
        super().__init__(**kwargs)
        gnd_lead = _gnd_lead if self.params['lead'] else 0
        self.segments.append(Segment(
            [(0, 0), (0, -gnd_lead), (-resheight, -gnd_lead),
             (resheight, -gnd_lead), gap, (-resheight*.7, -gndgap-gnd_lead),
             (resheight*.7, -gndgap-gnd_lead), gap,
             (-resheight*.2, -gndgap*2-gnd_lead),
             (resheight*.2, -gndgap*2-gnd_lead)]))
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)


class GroundSignal(Element):
    ''' Signal ground
    
        Keyword Args:
            lead: Show lead wire
    '''
    _element_defaults = {
        'lead': True,
        'theta': 0,
        'drop': (0, 0)
    }
    def __init__(self, *,
                 lead: bool = True,
                 **kwargs):
        super().__init__(**kwargs)
        gnd_lead = _gnd_lead if self.params['lead'] else 0
        self.segments.append(Segment(
            [(0, 0), (0, -gnd_lead), (-resheight, -gnd_lead), (0, -gnd_lead-resheight),
             (resheight, -gnd_lead), (0, -gnd_lead)]))
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)


class GroundChassis(Element):
    ''' Chassis ground
 
        Keyword Args:
            lead: Show lead wire
    '''
    _element_defaults = {
        'lead': True,
        'drop': (0, 0),
        'theta': 0
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        gnd_lead = _gnd_lead if self.params['lead'] else 0
        dx = resheight*.75
        dy = resheight
        self.segments.append(Segment(
            [(0, 0), (0, -gnd_lead), (-dx, -gnd_lead-dy)]))
        self.segments.append(Segment(
            [(0, -gnd_lead), (-dx, -gnd_lead), (-dx*2, -gnd_lead-dy)]))
        self.segments.append(Segment(
            [(0, -gnd_lead), (dx, -gnd_lead), (0, -gnd_lead-dy)]))
        self.elmparams['drop'] = (0, 0)
        self.elmparams['theta'] = 0
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)


class Antenna(Element):
    ''' Antenna '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        lead = 0.6
        h = 0.6
        w = 0.38
        self.segments.append(Segment(
            [(0, 0), (0, lead), (-w, lead+h), (w, lead+h), (0, lead)]))
        self.elmparams['drop'] = (0, 0)
        self.elmparams['theta'] = 0
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)


class AntennaLoop(Element):
    ''' Loop antenna (diamond style) '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        lead = 0.2
        h = 0.5
        self.segments.append(Segment(
            [(0, 0), (0, lead), (-h, h+lead), (lead/2, h*2+1.5*lead),
             (h+lead, h+lead), (lead, lead), (lead, 0)]))
        self.elmparams['drop'] = (0, 0)
        self.elmparams['theta'] = 0
        self.anchors['start'] = (0, 0)
        self.anchors['end'] = (lead, 0)


class AntennaLoop2(Element):
    ''' Loop antenna (square style) '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        lead = .25
        h = 1
        x1 = -h/2-lead/2
        x2 = x1 + lead
        x3 = h/2+lead/2
        x4 = x3 + lead
        y1 = lead
        y2 = lead*2
        y3 = h+y2
        y4 = y3+lead
        self.segments.append(Segment(
            [(0, 0), (0, y1), (x1, y1), (x1, y3), (x3, y3), (x3, y2),
             (x2, y2), (x2, y4), (x4, y4), (x4, y1), (lead, y1), (lead, 0)]))
        self.elmparams['drop'] = (lead, 0)
        self.elmparams['theta'] = 0
        self.anchors['start'] = (0, 0)
        self.anchors['end'] = (lead, 0)


class Vss(Element):
    ''' Vss connection
        
        Keyword Args:
            lead: Show lead wire
    '''
    _element_defaults = {
        'lead': True,
        'drop': (0, 0),
        'theta': 0,
        'lblloc': 'bottom'
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dx = resheight*.75
        gnd_lead = _gnd_lead if self.params['lead'] else 0
        self.segments.append(Segment([(0, 0), (0, -gnd_lead)]))
        self.segments.append(Segment([(0, -gnd_lead), (-dx, -gnd_lead)]))
        self.segments.append(Segment([(0, -gnd_lead), (dx, -gnd_lead)]))
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)


class Vdd(Element):
    ''' Vdd connection
        
        Keyword Args:
            lead: Show lead wire
    '''
    _element_defaults = {
        'lead': True,
        'drop': (0, 0),
        'theta': 0
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dx = resheight*.75
        gnd_lead = _gnd_lead if self.params['lead'] else 0
        self.segments.append(Segment([(0, 0), (0, gnd_lead)]))
        self.segments.append(Segment([(0, gnd_lead), (-dx, gnd_lead)]))
        self.segments.append(Segment([(0, gnd_lead), (dx, gnd_lead)]))
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)


class NoConnect(Element):
    ''' No Connection '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        dx = resheight*.75
        dy = resheight*.75
        self.segments.append(Segment([(-dx, -dy), (dx, dy)]))
        self.segments.append(Segment([(-dx, dy), (dx, -dy)]))
        self.elmparams['drop'] = (0, 0)
        self.elmparams['theta'] = 0
        self.elmparams['lblloc'] = 'bottom'
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)
