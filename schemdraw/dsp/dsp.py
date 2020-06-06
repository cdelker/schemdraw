''' Signal processing elements '''

import numpy as np

from ..segments import *
from ..elements import Element

from ..flow import Box


class Square(Element):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [0, .5], [1, .5], [1, -.5], [0, -0.5], [0, 0]], **kwargs))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.anchors['N'] = [0.5, 0.5]
        self.anchors['S'] = [0.5, -0.5]
        self.anchors['E'] = [1, 0]
        self.anchors['W'] = [0, 0]
        self.params['drop'] = [1, 0]
    

class Circle(Element):
    def setup(self, **kwargs):    
        rad = .5
        k = rad*np.sqrt(2)/2  # Diagonal distance
        self.segments.append(SegmentCircle([rad, 0], rad, **kwargs))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['drop'] = [2*rad, 0]
        self.anchors['N'] = [rad, rad]
        self.anchors['S'] = [rad, -rad]
        self.anchors['E'] = [2*rad, 0]
        self.anchors['W'] = [0, 0]
        self.anchors['NW'] = [rad-k, k]
        self.anchors['NE'] = [rad+k, k]
        self.anchors['SW'] = [rad-k, k]
        self.anchors['SE'] = [rad+k, k]
        self.anchors['center'] = [rad, 0]

        
class Sum(Circle):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(Segment([[.5, .2], [.5, -.2]], **kwargs))
        self.segments.append(Segment([[.3, 0], [.7, 0]], **kwargs))


class SumSigma(Circle):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentText(label='$\Sigma$', pos=[0.45, 0], align=('center', 'center'), **kwargs))

        
class Mixer(Circle):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        rad = .5
        k = rad*np.sqrt(2)/2  # Diagonal distance        
        self.segments.append(Segment([[rad+k, k], [rad-k, -k]], **kwargs))
        self.segments.append(Segment([[rad+k, -k], [rad-k, k]], **kwargs))
        self.params['lblloc'] = 'top'
        self.params['lblofst'] = 0.2


class Speaker(Element):
    # Speaker with only one terminal
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [0, 0.25], [0.25, 0.25], [0.25, -.25], [0, -.25], [0, 0]], **kwargs))
        self.segments.append(Segment([[0.25, 0.25], [0.5, 0.5], [0.5, -0.5], [0.25, -0.25], [.25, .25]], **kwargs))


class Amp(Element):
    def setup(self, **kwargs):
        amph = 1.
        ampl = .75
        self.segments.append(Segment([[0, 0], [0, -amph/2], [ampl, 0], [0, amph/2], [0, 0]], **kwargs))
        self.params['drop'] = [ampl, 0]
        self.anchors['in'] = [0, 0]
        self.anchors['out'] = [ampl, 0]


def _makesine():
    sinx = np.linspace(-np.pi, np.pi, num=20)
    siny = -np.sin(sinx)
    sinx = sinx / np.pi *.3 + .5
    siny = siny / 10
    path = list(zip(sinx, siny)) 
    return path

        
class OscillatorBox(Square):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        path = _makesine()
        self.segments.append(Segment(path, **kwargs))

        
class Oscillator(Circle):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        path = _makesine()
        self.segments.append(Segment(path, **kwargs))

        
class Filter(Square):
    ''' Filter element
    
        Parameters
        ----------
        response : string
            Filter response: 'lp', 'bp', 'hp', or 'notch' for
            low-pass, band-pass, high-pass, and notch/band-stop filters
            
        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def setup(self, **kwargs):
        super().setup(**kwargs)
        response = kwargs.get('response', None)
        
        path = _makesine()
        path1 = [[p[0], p[1]+.25] for p in path]
        path2 = [[p[0], p[1]-.25] for p in path]        
        self.segments.append(Segment(path, **kwargs))
        self.segments.append(Segment(path1, **kwargs))
        self.segments.append(Segment(path2, **kwargs))

        if response:
            if response.lower() in ['bp', 'lp']:
                self.segments.append(Segment([[.45, .17], [.55, .33]], **kwargs))    # Slash through high f
            if response.lower() in ['bp', 'hp']:
                self.segments.append(Segment([[.45, -.33], [.55, -.17]], **kwargs))  # Slash through low f
            if response.lower() in ['lp', 'hp', 'notch']:
                self.segments.append(Segment([[.45, -.08], [.55, .08]], **kwargs))  # Slash through mid f
        

class Adc(Element):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [.22, .5], [1.4, .5], [1.4, -.5], [.22, -.5], [0, 0]], **kwargs))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['drop'] = [1.4, 0]
        self.anchors['in'] = [0, 0]
        self.anchors['out'] = [1.4, 0]
        self.anchors['E'] = [1.4, 0]
        self.anchors['W'] = [0, 0]


class Dac(Element):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], [0, .5], [1.18, .5], [1.4, 0], [1.18, -.5], [0, -.5], [0, 0]], **kwargs))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['drop'] = [1.4, 0]
        self.anchors['in'] = [0, 0]
        self.anchors['out'] = [1.4, 0]
        self.anchors['E'] = [1.4, 0]
        self.anchors['W'] = [0, 0]


class Demod(Square):
    # Demodulator, box with diode in it
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(Segment([[.15, 0], [.3, 0]], **kwargs))
        self.segments.append(Segment([[.3, .25], [.7, 0], [.3, -.25], [.3, .25]], **kwargs))
        self.segments.append(Segment([[.7, .25], [.7, -.25]], **kwargs))
        self.segments.append(Segment([[.7, 0], [.85, 0]], **kwargs))
