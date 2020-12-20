''' Logic gate definitions '''

from functools import partial
import math

from ..segments import Segment, SegmentCircle
from ..elements import Element, Element2Term
from ..adddocs import adddocs
from ..util import linspace

gap = [math.nan, math.nan]
leadlen = .35
gateh = 1.
gatel = .65
notbubble = .12


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

        rad = gateh/2
        theta = linspace(math.radians(-90), math.radians(90), num=50)
        x = [rad*math.cos(t) + gatel+leadlen for t in theta]
        y = [rad*math.sin(t) for t in theta]

        path = list(zip(x, y))
        path += [[gatel+leadlen, rad], [leadlen, rad],
                 [leadlen, 0], [leadlen, -rad],
                 [gatel+leadlen, -rad]]
        self.segments.append(Segment(path))
        self.anchors['out'] = [gatel+gateh/2+leadlen*2, 0]
        self.anchors['end'] = self.anchors['out']

        if nand:
            self.segments.append(SegmentCircle(
                [leadlen+gatel+gateh/2+notbubble, 0], notbubble))

        # Set distance between inputs. A little larger for 2 input gates.
        if inputs == 2:
            dy = gateh*.5
        elif inputs == 3:
            dy = gateh*.33
        else:  # inputs > 3:
            dy = gateh*.4
            backlen = dy * (inputs-1)

        # Add the inputs and define anchor names
        for i in range(inputs):
            y = (i+1 - (inputs/2+.5)) * dy
            self.anchors['in%d' % (inputs-i)] = [0, y]

            if (inputs-i) in inputnots:
                self.segments.append(SegmentCircle([leadlen-notbubble, y], notbubble))
                self.segments.append(Segment([[0, y], [leadlen-notbubble*2, y]]))
            else:
                self.segments.append(Segment([[0, y], [leadlen, y]]))

        # Extended back for large number of inputs
        if inputs > 3:
            self.segments.append(Segment([[leadlen, backlen/2+dy/2],
                                          [leadlen, -backlen/2-dy/2]]))

        # Output lead
        if nand:
            self.segments.append(Segment(
                [[0, 0], gap, [gatel+gateh/2+leadlen+notbubble*2, 0],
                 [gatel+gateh/2+leadlen*2, 0]]))
        else:
            self.segments.append(Segment(
                [[0, 0], gap, [gatel+gateh/2+leadlen, 0],
                 [gatel+gateh/2+leadlen*2, 0]]))
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

        # Define OR path
        orflat = .5
        xorgap = .15
        x = linspace(0, gatel+.05)
        y = [x0**2 for x0 in x]
        y = [y0 - max(y) for y0 in y]
        y = [min(y)] + y   # Combine the flat + parabolic parts
        x = [0] + [x0+orflat for x0 in x]

        # Back/input side
        y2 = linspace(min(y), -min(y))
        x2 = [-y0**2 for y0 in y2]
        back = min(x2)
        x2 = [x0 - back for x0 in x2]

        # Offset for inputs
        x = [x0 + leadlen for x0 in x]
        x2 = [x0 + leadlen for x0 in x2]

        if xor:
            x = [x0 + xorgap for x0 in x]

        tip = max(x)
        orheight = abs(min(y))

        negy = [-y0 for y0 in y]
        path = list(zip(x, y)) + list(zip(x[::-1], negy[::-1]))

        if xor:
            x2xor = [x0+xorgap for x0 in x2[::-1]]
            y2xor = y2[::-1]
            path += list(zip(x2xor, y2xor))
        else:
            path += list(zip(x2[::-1], y2[::-1]))
        self.segments.append(Segment(path, **kwargs))
        self.anchors['out'] = [tip+leadlen, 0]
        self.anchors['end'] = self.anchors['out']

        if xor:
            self.segments.append(Segment(list(zip(x2, y2)), **kwargs))

        if nor:
            self.segments.append(SegmentCircle([tip+notbubble, 0], notbubble, **kwargs))

        # Set distance between inputs. A little larger for 2 input gates.
        if inputs == 2:
            dy = gateh*.5
        elif inputs == 3:
            dy = gateh*.33
        else:  # inputs > 3:
            dy = gateh*.4
            backlen = dy * (inputs-1)

        # Add the inputs and define anchor names
        for i in range(inputs):
            y = (i+1 - (inputs/2+.5)) * dy

            xback = leadlen - y**2 - back
            if inputs > 3 and ((y > orheight) or (y < -orheight)):
                xback = leadlen

            self.anchors['in%d' % (inputs-i)] = [0, y]

            if (inputs-i) in inputnots:
                self.segments.append(SegmentCircle([xback-notbubble, y], notbubble))
                self.segments.append(Segment([[0, y], [xback-notbubble*2, y]]))
            else:
                self.segments.append(Segment([[0, y], [xback, y]]))

        # Extended back for large number of inputs
        if inputs > 3:
            self.segments.append(Segment([[leadlen, backlen/2+dy/2], [leadlen, orheight]]))
            self.segments.append(Segment([[leadlen, -backlen/2-dy/2], [leadlen, -orheight]]))

        # Output lead
        if nor:
            self.segments.append(Segment([[0, 0], gap, [tip+notbubble*2, 0],
                                          [tip+leadlen, 0]]))
        else:
            self.segments.append(Segment([[0, 0], gap, [tip, 0], [tip+leadlen, 0]]))
        self.params['drop'] = self.segments[-1].path[-1]


Nor = partial(Or, nor=True)
Xor = partial(Or, xor=True)
Xnor = partial(Or, nor=True, xor=True)


class Buf(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [leadlen, 0], gap, [gatel+leadlen, 0]]))
        self.segments.append(Segment([[gatel+leadlen, 0], [gatel+leadlen*2, 0]]))
        self.segments.append(Segment([[leadlen, 0], [leadlen, -gateh/2],
                                      [gatel+leadlen, 0], [leadlen, gateh/2], [leadlen, 0]]))
        self.anchors['out'] = [gatel+gateh/2+leadlen*2, 0]
        self.anchors['in'] = [0, 0]


class Not(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [leadlen, 0], gap,
                                      [gatel+leadlen+notbubble*2, 0]]))
        self.segments.append(Segment([[gatel+leadlen+notbubble*2, 0],
                                      [gatel+leadlen*2, 0]]))
        self.segments.append(Segment([[leadlen, 0], [leadlen, -gateh/2],
                                      [gatel+leadlen, 0], [leadlen, gateh/2],
                                      [leadlen, 0]]))
        self.segments.append(SegmentCircle([gatel+leadlen+notbubble, 0], notbubble))
        self.anchors['out'] = [gatel+leadlen+notbubble*2, 0]
        self.anchors['in'] = [0, 0]


class NotNot(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [leadlen-notbubble*2, 0], gap,
                                      [gatel+leadlen+notbubble*2, 0]]))
        self.segments.append(Segment([[gatel+leadlen+notbubble*2, 0],
                                      [gatel+leadlen*2, 0]]))
        self.segments.append(Segment([[leadlen, 0], [leadlen, -gateh/2],
                                      [gatel+leadlen, 0], [leadlen, gateh/2],
                                      [leadlen, 0]]))
        self.segments.append(SegmentCircle([gatel+leadlen+notbubble, 0], notbubble))
        self.segments.append(SegmentCircle([leadlen-notbubble, 0], notbubble))
        self.anchors['out'] = [gatel+gateh/2+leadlen*2, 0]
        self.anchors['in'] = [0, 0]


@adddocs(Element2Term)
class Tgate(Element2Term):
    ''' Transmission gate. Anchors: `in`, `out`, `c`, `cbar`. '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [leadlen, 0], gap, [gatel+leadlen, 0]]))
        self.segments.append(Segment([[leadlen, 0], [leadlen, -gateh/2], [gatel+leadlen, 0],
                                      [leadlen, gateh/2], [leadlen, 0]]))
        self.segments.append(Segment([[leadlen+gatel, 0], [leadlen+gatel, -gateh/2], [leadlen, 0],
                                      [leadlen+gatel, gateh/2], [leadlen+gatel, 0]]))
        self.segments.append(SegmentCircle([leadlen+gatel/2, .28+.08], .08))
        self.segments.append(Segment([[leadlen+gatel/2, .28+.16], [leadlen+gatel/2, .7]]))
        self.segments.append(Segment([[leadlen+gatel/2, -.28], [leadlen+gatel/2, -.7]]))
        self.anchors['out'] = [gatel+gateh/2+leadlen*2, 0]
        self.anchors['in'] = [0, 0]
        self.anchors['c'] = [leadlen+gatel/2, -.7]
        self.anchors['cbar'] = [leadlen+gatel/2, .7]


class Schmitt(Buf):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        xofst = leadlen
        self.segments.append(Segment([[xofst+.07, -.15], [xofst+.25, -.15],
                                      [xofst+.25, .15], gap,
                                      [xofst+.33, .15], [xofst+.15, .15],
                                      [xofst+.15, -.15]], lw=1))


class SchmittNot(Not):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        xofst = leadlen
        self.segments.append(Segment([[xofst+.07, -.15], [xofst+.25, -.15],
                                      [xofst+.25, .15], gap,
                                      [xofst+.33, .15], [xofst+.15, .15],
                                      [xofst+.15, -.15]], lw=1))


class SchmittAnd(And):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        xofst = .65
        self.segments.append(Segment([[xofst+.07, -.15], [xofst+.25, -.15],
                                      [xofst+.25, .15], gap,
                                      [xofst+.33, .15], [xofst+.15, .15],
                                      [xofst+.15, -.15]], lw=1))


SchmittNand = partial(SchmittAnd, nand=True)
