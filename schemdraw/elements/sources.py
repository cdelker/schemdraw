''' Sources, meters, and lamp elements '''

import numpy as np

from .elements import Element, Element2Term, gap
from .twoterm import resheight
from ..transform import Transform
from ..segments import *


class Source(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [0, 0], gap, [1, 0], [1, 0]]))
        self.segments.append(SegmentCircle([0.5, 0], 0.5,))
        self.params['theta'] = 90


class SourceV(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plus_len = .2
        self.segments.append(Segment([[.25, -plus_len/2], [.25, plus_len/2]])),   # '-' sign
        self.segments.append(Segment([[.75-plus_len/2, 0], [.75+plus_len/2, 0]])) # '+' sign
        self.segments.append(Segment([[.75, -plus_len/2], [.75, plus_len/2]]))    # '+' sign
        

class SourceI(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([.25, 0], [.75, 0]))

        
class SourceSin(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sin_y = np.linspace(.25, .75, num=25) - 0.5
        sin_x = .2 * np.sin((sin_y-.25)*np.pi*2/.5) + 0.5
        sin_path = np.transpose(np.vstack((sin_x, sin_y)))
        self.segments.append(Segment(sin_path))


class SourceControlled(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [.5, .5], [1, 0], [.5, -.5], [0, 0], gap, [1, 0]]))
        self.params['theta'] = 90


class SourceControlledV(SourceControlled):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        plus_len = .2
        self.segments.append(Segment([[.25, -plus_len/2], [.25, plus_len/2]]))  # '-' sign
        self.segments.append(Segment([[.75-plus_len/2, 0], [.75+plus_len/2, 0]]))  # '+' sign
        self.segments.append(Segment([[.75, -plus_len/2], [.75, plus_len/2]]))  # '+' sign

        
class SourceControlledI(SourceControlled):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([.25, 0], [.75, 0]))


batw = resheight*.75
bat1 = resheight*1.5
bat2 = resheight*.75        
class BatteryCell(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], gap, [batw, 0]]))
        self.segments.append(Segment([[0, bat1], [0, -bat1]]))
        self.segments.append(Segment([[batw, bat2], [batw, -bat2]]))

    

class Battery(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], gap, [batw*3, 0]]))
        self.segments.append(Segment([[0, bat1], [0, -bat1]]))
        self.segments.append(Segment([[batw, bat2], [batw, -bat2]]))
        self.segments.append(Segment([[batw*2, bat1], [batw*2, -bat1]]))
        self.segments.append(Segment([[batw*3, bat2], [batw*3, -bat2]]))
        

class MeterV(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentText([.5, 0], 'V'))


class MeterI(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentText([.5, 0], 'I'))


class MeterA(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentText([.5, 0], 'A'))


class MeterOhm(Source):        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentText([.5, 0], '$\Omega$'))


class Lamp(Source):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        a = .25
        b = .7
        t = np.linspace(1.4, 3.6*np.pi, 100)
        x = a*t - b*np.sin(t)
        y = a - b * np.cos(t)
        x = (x - x[0])  # Scale to about the right size
        x = x / x[-1]
        y = (y - y[0]) * .25
        lamp_path = np.transpose(np.vstack((x, y)))
        self.segments.append(Segment(lamp_path))


