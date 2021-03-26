''' Process Engineering Elements '''

import math
from typing import Literal, Sequence

from ..util import linspace
from ..segments import Segment, SegmentCircle, SegmentText, SegmentPoly, SegmentArc
from ..elements import Element
from ..types import XY


#
# 1. VESSELS AND TANKS
#

class Tank(Element):
    '''1.1 Tank, vessel
        
        Args:
            h: height
            w: width
        
        Anchors:
            * W
            * S
    '''
    
    def __init__(self, h: float = 12, w: float = 9, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentPoly([(0,0), (0, h), (w, h), (w, 0)]))
        
        self.anchors['W'] = (0, h*10/12)
        self.anchors['S'] = (w/2, 0)

        
class Cistern(Element):
    '''1.2 Container, Tank, Cistern
    
        Args:
            h: Height of the tank
            w: Width of the tank
            level: Level of the liquid in the tank (0..1)
       
       Anchors:
           * NW
           * N
           * NE
           * W
           * E
           * SW
           * S
           * SE
    '''
    
    def __init__(self,
                 h: float = 6,
                 w: float = 8,
                 level:float = 0.75,
                 *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(w, h), (w, 0), (0, 0), (0, h)]))
        self.segments.append(Segment([(w, h*level), (0, h*level)], lw=0.5))
        
        self.anchors['NW'] = (0.25*w, 1*h)
        self.anchors['N'] = (0.5*w, 1*h)
        self.anchors['NE'] = (0.75*w, 1*h)
        self.anchors['W'] = (0, 0.75*h)
        self.anchors['E'] = (1, 0.75*h)
        self.anchors['SW'] = (0, 0)
        self.anchors['S'] = (0.5*w, 0)
        self.anchors['SE'] = (1*w, 0) 

#
# 2. COLUMNS WITH INTERNALS
#

#
# 3. HEAT EXCHANGERS
#

class HeatExchanger(Element):
    '''3.1 Heat Exchanger (general), condenser
    
        Args:
            r: radius
    
        Anchors:
            * N
            * S
            * W
            * E
    '''
    def __init__(self, r: float = 4, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentCircle([0, 0], r))
        self.segments.append(Segment([(-r, 0), (-2/4*r, 0), (0, 2/4*r), (0, -2/4*r), (2/4*r, 0), (r, 0)]))
        
        self.anchors['N'] = (0, r)
        self.anchors['S'] = (0, -r)
        self.anchors['W'] = (-r, 0)
        self.anchors['E'] = (r, 0)
 
        
class PlateExchanger(Element):
    '''3.6 Heat Exchanger of plate type
    
        Args:
            h: Heigth
            w: Width
            n: Num. of plates (default 3)
            
        Anchors:
            * NW
            * SW
            * NE
            * SE
        '''
        
    def __init__(self, h: float = 4, w: float = 13, n: int = 3, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentPoly([(0,0), (0, h), (w, h), (w, 0)]))
        self.segments.append(Segment([(1/13*w, h), (12/13*w, 0)]))
        self.segments.append(Segment([(1/13*w, 0), (12/13*w, h)]))
# Diseño de draw.io        
#         self.segments.append(Segment([(-0.15*w, 0.1*h), (0, 0.1*h), (w, 0.9*h), (w*1.15, 0.9*h)]))
#         self.segments.append(Segment([(-0.15*w, 0.9*h), (0, 0.9*h), (w, 0.1*h), (w*1.15, 0.1*h)]))
        
        num_plates = n
        step = w/(num_plates+1)
        for i in range(num_plates):
            self.segments.append(Segment([((i+1)*step, 0), ((i+1)*step, h)]))

# Diseño de draw.io    
#         self.segments.append(Segment([(w*1.15, 0.1*h-0.075*h), (w*1.15, 0.1*h+0.075*h)]))
#         self.segments.append(Segment([(w*1.15, 0.9*h-0.075*h), (w*1.15, 0.9*h+0.075*h)]))
#         self.segments.append(Segment([(-w*0.15, 0.1*h-0.075*h), (-w*0.15, 0.1*h+0.075*h)]))
#         self.segments.append(Segment([(-w*0.15, 0.9*h-0.075*h), (-w*0.15, 0.9*h+0.075*h)]))
        
        self.anchors['NE'] = (12/13*w, h)
        self.anchors['NW'] = (1/13*w, h)
        self.anchors['SE'] = (1/13*w, 0)
        self.anchors['SW'] = (12/13*w, 0)

#
# 4. STEAM GENERATORS, FURNACES, RECOOLING DEVICE
#

class Boiler(Element):
    '''4.1 Boiler with dome
    
        Args:
            h: Heigth
            w: Width
            
        Anchors:
            * N
            * W
        '''
        
    def __init__(self, h: float = 10, w: float = 8, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentPoly([(0, 0), (w, 0), (w, h*8/10), (0, h*8/10)]))
        self.segments.append(SegmentArc(center = (w/2, h*8/10), width=4/8*w, height=4/10*h, theta1=0, theta2=180))
        
        self.anchors['N'] = (w/2, h*10/10)
        self.anchors['W'] = (0, h*6/8)

#
# 5. COOLING TOWER
#

class CoolingTower(Element):
    '''5.1 Cooling tower (general)
    
        Args:
            h: Heigth
            w: Width
            
        Anchors:
            * E
            * W
        '''
        
    def __init__(self, h: float = 10, w: float = 8, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentPoly([(0, 0), (w, 0), (w, h*2/10), (0, h*2/10)]))
        self.segments.append(SegmentPoly([(0, h*2/10), (w, h*2/10), (w*6/8, h), (w*2/10, h)]))
        
        self.anchors['E'] = (w, h*2/10)
        self.anchors['W'] = (0, h*2/8)


#
# 6. FILTERS, LIQUID FILTERS, GAS FILTERS
#

class Filter(Element):
    '''6.1 Liquid filter (general)
    
        Args:
            h: Heigth
            w: Width
            
        Anchors:
            * N
            * S
        '''
        
    def __init__(self, h: float = 10, w: float = 6, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentPoly([(0, 0), (w, 0), (w, h), (0, h)]))
        self.segments.append(Segment([(0, h*5/10), (w*1/6, h*5/10)]))
        self.segments.append(Segment([(w*2/6, h*5/10), (w*4/6, h*5/10)]))
        self.segments.append(Segment([(w*5/6, h*5/10), (w, h*5/10)]))
        
        self.anchors['N'] = (w/2, h)
        self.anchors['S'] = (w/2, 0)


#
# 7. SCREENING DEVICES, SIEVES, AND RAKES
#

class Sieve(Element):
    '''7.1 Screening device, sieve, strainer, general
        
        Args:
            h: Heigth
            w: Width
            
        Anchors:
            * N
            * S
            * E
        '''
        
    def __init__(self, h: float = 10, w: float = 6, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentPoly([(0, h), (w, h), (w, h*3/10), (w/2, 0), (0, h*3/10)]))
        self.segments.append(Segment([(0, h), (w, h*3/10)], ls = '--'))
        
        self.anchors['N'] = (w/2, h)
        self.anchors['S'] = (w/2, 0)
        self.anchors['E'] = (w, h*4/1)

#
# 8. SEPARATORS
#

#
# 9. CENTRIFUGES
#
        
class DiscCentrifuge(Element):
    '''9.4 Centrifuge, separator disc-type
        
        Args:
            h: height
            w: width
        
        Anchors:
            * N
            * NE
            * SE
    '''

    def __init__(self, h: float = 8, w: float = 8, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentPoly([(0,0), (0, h), (w, h), (w, 0)]))
        self.segments.append(Segment([(w/2, h*7/8), (w/2, -h*1/8)]))
        self.segments.append(Segment([(w*1/8, h*1/8), (w*7/8, h*1/8)]))
        self.segments.append(Segment([(w*1/8, h*3.5/8), (w/2, h*5/8), (w*7/8, h*3.5/8)]))
        self.segments.append(Segment([(w*1/8, h*5.5/8), (w/2, h*7/8), (w*7/8, h*5.5/8)]))
        
        self.anchors['N'] = (w/2, h)
        self.anchors['NE'] = (w, h*6/8)
        self.anchors['SE'] = (w, 0)

#
# 10. DRIER
#

#
# 11. CRUSHING/GRINDING MACHINES
#

#
# 12. MIXERS/KNEADERS
#

#
# 13. SHAPING MACHINES -- PROCESSING IN VERTICAL DIRECTION
#

#
# 14. SHAPING MACHINES -- PROCESING IN HORIZONTAL DIRECTION
#

#
# 15. LIQUID PUMPS
#

class Pump(Element):
    '''15.1 Pump, liquid type (general)
    
        Args:
            r: radius
    
        Anchors:
            * W
            * E
    '''
    def __init__(self, r: float = 3, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentCircle([0, 0], r))
        self.segments.append(Segment([(0, r), (r, 0)]))
        self.segments.append(Segment([(0, -r), (r, 0)]))
        
        self.anchors['W'] = (-r, 0)
        self.anchors['E'] = (r, 0)

#
# 16. COMPRESSORS, VACUUM PUMPS
#

#
# 17. BLOWERS, FANS
#

#
# 18. LIFTING, CONVEYING AND TRANSPORT EQUIPMENT
#

#
# 19. PROPORTIONERS, FEEDERS AND DISTRIBUTION FACILITIES
#

#
# 20. ENGINES
#

# 
# 21. VALVES
#

class Valve(Element):
    '''21.1 Valve (general)
        
        Anchors:
            * W
            * E
            * center
    '''
    
    def __init__(self, h: float = 2, w: float = 4, *d, **kwargs):
        super().__init__(*d, **kwargs)
        
        self.segments.append(SegmentPoly([(0,0), (w, h), (w, 0), (0, h)]))
        
        self.anchors['W'] = (0, 1/4*h)
        self.anchors['E'] = (w, 1/4*h)

#
# 22. CHECK VALVES
#

#
# 23. VALVES AND FITTINGS WITH SAFETY FUNCTION
#

#
# 24. FITTINGS
#

#
# 25. GRAPHYCAL SYMBOLS FOR PIPING
#

#
# 26. APPARATUS ELEMENTS
#

#
# 27. INTERNALS
        
#
# 28. AGITATORS, STIRRERS
#

class Stirrer(Element):
    '''28.1 Agitator (general), Stirrer (general)
        
        Args:
            l: Length of the axis
        
        Anchors:
            * N
    '''
    
    def __init__(self, h: float = 6, w: float = 4, l: float = 1, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(2/4*w, h*1/6), (2/4*w, h*l)]))
        self.segments.append(Segment([(0, 0), (0, 2/6*h), (w, 0), (w, 2/6*h)]))

#
# 29. INTERNAL CHARACTERISTICS AND BUILT-IN-COMPONENTS
#