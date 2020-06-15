''' Logic gate definitions '''

from functools import partial
import numpy as np

from ..segments import Segment, SegmentCircle
from ..elements import Element, Element2Term


_gap = [np.nan, np.nan]
_leadlen = .35
_gateh = 1.
_gatel = .65
_notbubble = .12


class And(Element):
    ''' AND gate element

        Parameters
        ----------
        inputs : int
            Number of inputs to gate.
        nand : bool
            Draw invert bubble on output
        inputnots : list
            Input numbers (starting at 1) of inputs that have invert bubble

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        inputs = kwargs.get('inputs', 2)
        nand = kwargs.get('nand', False)
        inputnots = kwargs.get('inputnots', [])

        rad = _gateh/2
        theta = np.linspace(np.radians(-90), np.radians(90), num=50)
        arcpoints = np.vstack((rad*np.cos(theta) + _gatel+_leadlen,
                               rad*np.sin(theta)))

        path = np.transpose(arcpoints).tolist()
        path += [[_gatel+_leadlen, rad], [_leadlen, rad],
                 [_leadlen, 0], [_leadlen, -rad],
                 [_gatel+_leadlen, -rad]]
        self.segments.append(Segment(path))
        self.anchors['out'] = [_gatel+_gateh/2+_leadlen*2, 0]

        if nand:
            self.segments.append(SegmentCircle(
                [_leadlen+_gatel+_gateh/2+_notbubble, 0], _notbubble))

        # Set distance between inputs. A little larger for 2 input gates.
        if inputs == 2:
            dy = _gateh*.5
        elif inputs == 3:
            dy = _gateh*.33
        else:  # inputs > 3:
            dy = _gateh*.4
            backlen = dy * (inputs-1)

        # Add the inputs and define anchor names
        for i in range(inputs):
            y = (i+1 - (inputs/2+.5)) * dy
            self.anchors['in%d' % (inputs-i)] = [0, y]

            if (inputs-i) in inputnots:
                self.segments.append(SegmentCircle([_leadlen-_notbubble, y], _notbubble))
                self.segments.append(Segment([[0, y], [_leadlen-_notbubble*2, y]]))
            else:
                self.segments.append(Segment([[0, y], [_leadlen, y]]))

        # Extended back for large number of inputs
        if inputs > 3:
            self.segments.append(Segment([[_leadlen, backlen/2+dy/2],
                                          [_leadlen, -backlen/2-dy/2]]))

        # Output lead
        if nand:
            self.segments.append(Segment(
                [[0, 0], _gap, [_gatel+_gateh/2+_leadlen+_notbubble*2, 0],
                 [_gatel+_gateh/2+_leadlen*2, 0]]))
        else:
            self.segments.append(Segment(
                [[0, 0], _gap, [_gatel+_gateh/2+_leadlen, 0],
                 [_gatel+_gateh/2+_leadlen*2, 0]]))
        self.params['drop'] = self.segments[-1].path[-1]


Nand = partial(And, nand=True)


class Or(Element):
    ''' OR/XOR gate element.

        Parameters
        ----------
        inputs : int
            Number of inputs to gate.
        nor : bool
            Draw invert bubble on output
        xor : bool
            Draw as exclusive-or gate
        inputnots : list
            Input numbers (starting at 1) of inputs that have invert bubble
        name : string
            Define a name for gate. Only used in documentation.

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        inputs = kwargs.get('inputs', 2)
        nor = kwargs.get('nor', False)
        xor = kwargs.get('xor', False)
        inputnots = kwargs.get('inputnots', [])

        # Define OR path as a numpy array
        orflat = .5
        xorgap = .15
        x = np.linspace(0, _gatel+.05)
        y = x**2
        y = y - max(y)
        y = np.concatenate(([min(y)], y))   # Combine the flat + parabolic parts
        x = np.concatenate(([0], x+orflat))

        # Back/input side
        y2 = np.linspace(min(y), -min(y))
        x2 = -y2**2
        back = min(x2)
        x2 = x2 - back

        # Offset for inputs
        x = x + _leadlen
        x2 = x2 + _leadlen

        if xor:
            x = x + xorgap

        tip = max(x)
        orheight = abs(min(y))

        path = np.transpose(np.vstack((x, y))).tolist() + np.transpose(np.vstack((x[::-1], -y[::-1]))).tolist()
        if xor:
            path += np.transpose(np.vstack((x2[::-1]+xorgap, y2[::-1]))).tolist()
        else:
            path += np.transpose(np.vstack((x2[::-1], y2[::-1]))).tolist()
        self.segments.append(Segment(path, **kwargs))
        self.anchors['out'] = [tip+_leadlen, 0]

        if xor:
            self.segments.append(Segment(np.transpose(np.vstack((x2, y2))).tolist(), **kwargs))

        if nor:
            self.segments.append(SegmentCircle([tip+_notbubble, 0], _notbubble, **kwargs))

        # Set distance between inputs. A little larger for 2 input gates.
        if inputs == 2:
            dy = _gateh*.5
        elif inputs == 3:
            dy = _gateh*.33
        else:  # inputs > 3:
            dy = _gateh*.4
            backlen = dy * (inputs-1)

        # Add the inputs and define anchor names
        for i in range(inputs):
            y = (i+1 - (inputs/2+.5)) * dy

            xback = _leadlen - y**2 - back
            if inputs > 3 and ((y > orheight) or (y < -orheight)):
                xback = _leadlen

            self.anchors['in%d' % (inputs-i)] = [0, y]

            if (inputs-i) in inputnots:
                self.segments.append(SegmentCircle([xback-_notbubble, y], _notbubble))
                self.segments.append(Segment([[0, y], [xback-_notbubble*2, y]]))
            else:
                self.segments.append(Segment([[0, y], [xback, y]]))

        # Extended back for large number of inputs
        if inputs > 3:
            self.segments.append(Segment([[_leadlen, backlen/2+dy/2], [_leadlen, orheight]]))
            self.segments.append(Segment([[_leadlen, -backlen/2-dy/2], [_leadlen, -orheight]]))

        # Output lead
        if nor:
            self.segments.append(Segment([[0, 0], _gap, [tip+_notbubble*2, 0],
                                          [tip+_leadlen, 0]]))
        else:
            self.segments.append(Segment([[0, 0], _gap, [tip, 0], [tip+_leadlen, 0]]))
        self.params['drop'] = self.segments[-1].path[-1]


Nor = partial(Or, nor=True)
Xor = partial(Or, xor=True)
Xnor = partial(Or, nor=True, xor=True)


class Buf(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [_leadlen, 0], _gap, [_gatel+_leadlen, 0]]))
        self.segments.append(Segment([[_gatel+_leadlen, 0], [_gatel+_leadlen*2, 0]]))
        self.segments.append(Segment([[_leadlen, 0], [_leadlen, -_gateh/2],
                                      [_gatel+_leadlen, 0], [_leadlen, _gateh/2], [_leadlen, 0]]))
        self.anchors['out'] = [_gatel+_gateh/2+_leadlen*2, 0]
        self.anchors['in'] = [0, 0]


class Not(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [_leadlen, 0], _gap,
                                      [_gatel+_leadlen+_notbubble*2, 0]]))
        self.segments.append(Segment([[_gatel+_leadlen+_notbubble*2, 0],
                                      [_gatel+_leadlen*2, 0]]))
        self.segments.append(Segment([[_leadlen, 0], [_leadlen, -_gateh/2],
                                      [_gatel+_leadlen, 0], [_leadlen, _gateh/2],
                                      [_leadlen, 0]]))
        self.segments.append(SegmentCircle([_gatel+_leadlen+_notbubble, 0], _notbubble))
        self.anchors['out'] = [_gatel+_gateh/2+_leadlen*2, 0]
        self.anchors['in'] = [0, 0]


class NotNot(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [_leadlen-_notbubble*2, 0], _gap,
                                      [_gatel+_leadlen+_notbubble*2, 0]]))
        self.segments.append(Segment([[_gatel+_leadlen+_notbubble*2, 0],
                                      [_gatel+_leadlen*2, 0]]))
        self.segments.append(Segment([[_leadlen, 0], [_leadlen, -_gateh/2],
                                      [_gatel+_leadlen, 0], [_leadlen, _gateh/2],
                                      [_leadlen, 0]]))
        self.segments.append(SegmentCircle([_gatel+_leadlen+_notbubble, 0], _notbubble))
        self.segments.append(SegmentCircle([_leadlen-_notbubble, 0], _notbubble))
        self.anchors['out'] = [_gatel+_gateh/2+_leadlen*2, 0]
        self.anchors['in'] = [0, 0]
