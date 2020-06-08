''' Sources, meters, and lamp elements '''

import numpy as np

from .elements import Element, Element2Term, gap
from .twoterm import resheight
from ..transform import Transform
from ..segments import *


class Source(Element2Term):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [0, 0], gap, [1, 0], [1, 0]], **kwargs))
        self.segments.append(SegmentCircle([0.5, 0], 0.5, **kwargs))
        self.params['theta'] = 90


class SourceV(Source):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        plus_len = .2
        self.segments.append(Segment([[.25, -plus_len/2], [.25, plus_len/2]], **kwargs)),   # '-' sign
        self.segments.append(Segment([[.75-plus_len/2, 0], [.75+plus_len/2, 0]], **kwargs)) # '+' sign
        self.segments.append(Segment([[.75, -plus_len/2], [.75, plus_len/2]], **kwargs))    # '+' sign
        

class SourceI(Source):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentArrow([.25, 0], [.75, 0], **kwargs))

        
class SourceSin(Source):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        sin_y = np.linspace(.25, .75, num=25) - 0.5
        sin_x = .2 * np.sin((sin_y-.25)*np.pi*2/.5) + 0.5
        sin_path = np.transpose(np.vstack((sin_x, sin_y)))
        self.segments.append(Segment(sin_path, **kwargs))


class SourceControlled(Element2Term):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [.5, .5], [1, 0], [.5, -.5], [0, 0], gap, [1, 0]], **kwargs))
        self.params['theta'] = 90


class SourceControlledV(SourceControlled):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        plus_len = .2
        self.segments.append(Segment([[.25, -plus_len/2], [.25, plus_len/2]], **kwargs))  # '-' sign
        self.segments.append(Segment([[.75-plus_len/2, 0], [.75+plus_len/2, 0]], **kwargs))  # '+' sign
        self.segments.append(Segment([[.75, -plus_len/2], [.75, plus_len/2]], **kwargs))  # '+' sign

        
class SourceControlledI(SourceControlled):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentArrow([.25, 0], [.75, 0], **kwargs))


batw = resheight*.75
bat1 = resheight*1.5
bat2 = resheight*.75        
class BatteryCell(Element2Term):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], gap, [batw, 0]], **kwargs))
        self.segments.append(Segment([[0, bat1], [0, -bat1]], **kwargs))
        self.segments.append(Segment([[batw, bat2], [batw, -bat2]], **kwargs))

    

class Battery(Element2Term):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], gap, [batw*3, 0]], **kwargs))
        self.segments.append(Segment([[0, bat1], [0, -bat1]], **kwargs))
        self.segments.append(Segment([[batw, bat2], [batw, -bat2]], **kwargs))
        self.segments.append(Segment([[batw*2, bat1], [batw*2, -bat1]], **kwargs))
        self.segments.append(Segment([[batw*3, bat2], [batw*3, -bat2]], **kwargs))
        

class MeterV(Source):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        kwargs = dict(kwargs)
        kwargs.pop('label', None)
        self.segments.append(SegmentText([.5, 0], 'V', **kwargs))


class MeterI(Source):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        kwargs = dict(kwargs)
        kwargs.pop('label', None)
        self.segments.append(SegmentText([.5, 0], 'I', **kwargs))


class MeterA(Source):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        kwargs = dict(kwargs)
        kwargs.pop('label', None)        
        self.segments.append(SegmentText([.5, 0], 'A', **kwargs))


class MeterOhm(Source):        
    def setup(self, **kwargs):
        super().setup(**kwargs)
        kwargs = dict(kwargs)
        kwargs.pop('label', None)
        self.segments.append(SegmentText([.5, 0], '$\Omega$', **kwargs))


class Lamp(Source):
    def setup(self, **kwargs):
        super().setup(**kwargs)        
        a = .25
        b = .7
        t = np.linspace(1.4, 3.6*np.pi, 100)
        x = a*t - b*np.sin(t)
        y = a - b * np.cos(t)
        x = (x - x[0])  # Scale to about the right size
        x = x / x[-1]
        y = (y - y[0]) * .25
        lamp_path = np.transpose(np.vstack((x, y)))
        self.segments.append(Segment(lamp_path, **kwargs))


