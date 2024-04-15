''' Logic gate definitions '''
from __future__ import annotations
from typing import Optional, Sequence
from functools import partial
import math

from ..segments import Segment, SegmentCircle
from ..elements import Element, Element2Term
from ..util import linspace


gap = (math.nan, math.nan)
gateh = 1.
gatel = .65
notbubble = .12


class And(Element):
    ''' AND gate

        Args:
            inputs: Number of inputs to gate.
            nand: Draw invert bubble on output
            inputnots: Input numbers (starting at 1) of inputs that have invert bubble
            leadin: Length of input leads [default: 0.35]
            leadout: Length of output lead [default: 0.35]

        Anchors:
            out
            in[X] - for each input
    '''
    _element_defaults = {
        'leadin': 0.35,
        'leadout': 0.35
    }
    def __init__(self, inputs: int = 2, nand: bool = False, inputnots: Optional[Sequence[int]] = None,
                 *,
                 leadin: Optional[float] = None, leadout: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        _leadin = self.params['leadin']
        _leadout = self.params['leadout']
        rad = gateh/2
        theta = linspace(math.radians(-90), math.radians(90), num=50)
        xs = [rad*math.cos(t) + gatel+_leadin for t in theta]
        ys = [rad*math.sin(t) for t in theta]

        path = list(zip(xs, ys))
        path += [(gatel+_leadin, rad), (_leadin, rad),
                 (_leadin, 0), (_leadin, -rad),
                 (gatel+_leadin, -rad)]
        self.segments.append(Segment(path))
        self.anchors['out'] = (gatel+gateh/2+_leadin+_leadout, 0)
        self.anchors['end'] = self.anchors['out']

        if nand:
            self.segments.append(SegmentCircle(
                (_leadin+gatel+gateh/2+notbubble, 0), notbubble))

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
            self.anchors['in%d' % (inputs-i)] = (0, y)

            if inputnots and (inputs-i) in inputnots:
                self.segments.append(SegmentCircle((_leadin-notbubble, y), notbubble))
                self.segments.append(Segment([(0, y), (_leadin-notbubble*2, y)]))
            else:
                self.segments.append(Segment([(0, y), (_leadin, y)]))

        # Extended back for large number of inputs
        if inputs > 3:
            self.segments.append(Segment([(_leadin, backlen/2+dy/2),
                                          (_leadin, -backlen/2-dy/2)]))

        # Output lead
        if nand:
            self.segments.append(Segment(
                [(gatel+gateh/2+_leadin+notbubble*2, 0), (gatel+gateh/2+_leadin+_leadout, 0)]))
        else:
            self.segments.append(Segment(
                [(gatel+gateh/2+_leadin, 0), (gatel+gateh/2+_leadin+_leadout, 0)]))
        self.params['drop'] = self.segments[-1].path[-1]  # type: ignore


Nand = partial(And, nand=True)


class Or(Element):
    ''' OR or XOR gate element.

        Args:
            inputs: Number of inputs to gate.
            nor: Draw invert bubble on output
            xor: Draw as exclusive-or gate
            inputnots: Input numbers (starting at 1) of inputs that have invert bubble
            leadin: Length of input leads [default: 0.35]
            leadout: Length of output lead [default: 0.35]

        Anchors:
            out
            in[X] - for each input
    '''
    _element_defaults = {
        'leadin': 0.35,
        'leadout': 0.35
    }
    def __init__(self, inputs: int = 2, nor: bool = False,
                 xor: bool = False, inputnots: Optional[Sequence[int]] = None,
                 *,
                 leadin: float = 0.35, leadout: float = 0.35, **kwargs):
        super().__init__(**kwargs)
        _leadin = self.params['leadin']
        _leadout = self.params['leadout']
        # Define OR path
        orflat = .5
        xorgap = .15
        xs = linspace(0, gatel+.05)
        ys = [x0**2 for x0 in xs]
        ys = [y0 - max(ys) for y0 in ys]
        ys = [min(ys)] + ys   # Combine the flat + parabolic parts
        xs = [0.] + [x0+orflat for x0 in xs]

        # Back/input side
        y2 = linspace(min(ys), -min(ys))
        x2 = [-y0**2 for y0 in y2]
        back = min(x2)
        x2 = [x0 - back for x0 in x2]

        # Offset for inputs
        xs = [x0 + _leadin for x0 in xs]
        x2 = [x0 + _leadin for x0 in x2]

        tip = max(xs)
        orheight = abs(min(ys))

        negy = [-y0 for y0 in ys]
        path = list(zip(xs, ys)) + list(zip(xs[::-1], negy[::-1]))
        path += list(zip(x2[::-1], y2[::-1]))

        self.segments.append(Segment(path))
        self.anchors['out'] = (tip+_leadout, 0)
        self.anchors['end'] = self.anchors['out']

        if xor:
            xxor = [x0-xorgap for x0 in x2]
            self.segments.append(Segment(list(zip(xxor, y2))))
            _leadin -= xorgap

        if nor:
            self.segments.append(SegmentCircle((tip+notbubble, 0), notbubble))

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

            xback = _leadin - y**2 - back
            if inputs > 3 and ((y > orheight) or (y < -orheight)):
                xback = _leadin

            self.anchors['in%d' % (inputs-i)] = (0, y)

            if inputnots and (inputs-i) in inputnots:
                self.segments.append(SegmentCircle(
                    (xback-notbubble, y), notbubble))
                self.segments.append(Segment([(0, y), (xback-notbubble*2, y)]))
            else:
                self.segments.append(Segment([(0, y), (xback, y)]))

        # Extended back for large number of inputs
        if inputs > 3:
            self.segments.append(Segment(
                [(_leadin, backlen/2+dy/2), (_leadin, orheight)]))
            self.segments.append(Segment(
                [(_leadin, -backlen/2-dy/2), (_leadin, -orheight)]))

        # Output lead
        if nor:
            self.segments.append(Segment([(tip+notbubble*2, 0), (tip+_leadout, 0)]))
        else:
            self.segments.append(Segment([(tip, 0), (tip+_leadout, 0)]))
        self.elmparams['drop'] = self.segments[-1].path[-1]  # type: ignore
        self.tip = tip


Nor = partial(Or, nor=True)
Xor = partial(Or, xor=True)
Xnor = partial(Or, nor=True, xor=True)


class Buf(Element2Term):
    ''' Buffer

        Anchors:
            in
            out
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), gap, (gatel, 0)]))
        self.segments.append(Segment([(0, gateh/2), (gatel, 0), (0, -gateh/2), (0, gateh/2)]))
        self.anchors['out'] = (gatel, 0)
        self.anchors['in1'] = (0, 0)


class Not(Element2Term):
    ''' Not gate/inverter

        Anchors:
            in
            out
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), gap, (gatel+notbubble*2, 0)]))
        self.segments.append(Segment([(0, gateh/2), (gatel, 0), (0, -gateh/2), (0, gateh/2)]))
        self.segments.append(SegmentCircle((gatel+notbubble, 0), notbubble))
        self.anchors['out'] = (gatel+notbubble*2, 0)
        self.anchors['in1'] = (0, 0)


class Tristate(Element2Term):
    ''' Tristate inverter
        Args:
            outputnot: Draw invert bubble on output
            controlnot: Active-low control

        Anchors:
            in
            out
            c
    '''
    def __init__(self, outputnot: bool = True, controlnot: bool = False, **kwargs):
        kwargs['outputnot'] = outputnot
        kwargs['control'] = controlnot
        super().__init__(**kwargs)
        if outputnot:
          self.segments.append(Segment([(0, 0), gap, (gatel+notbubble*2, 0)]))
          self.segments.append(SegmentCircle((gatel+notbubble, 0), notbubble))
        else:
          self.segments.append(Segment([(0, 0), gap, (gatel, 0)]))
        self.segments.append(Segment([(0, gateh/2), (gatel, 0), (0, -gateh/2), (0, gateh/2)]))
        if controlnot:
          self.segments.append(SegmentCircle((gatel/2, .42), notbubble))
          self.segments.append(Segment([(gatel/2, .42+notbubble), (gatel/2, .7)]))
        else:  
          self.segments.append(Segment([(gatel/2, .28), (gatel/2, .7)]))
        self.anchors['out'] = (gatel+notbubble*2, 0)
        self.anchors['in1'] = (0, 0)
        self.anchors['c'] = (gatel/2, .7)


class NotNot(Element2Term):
    ''' Double inverter

        Anchors:
            in
            out
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(-notbubble*2, 0), gap, (gatel+notbubble*2, 0)]))
        self.segments.append(Segment([(0, gateh/2), (gatel, 0), (0, -gateh/2), (0, gateh/2)]))
        self.segments.append(SegmentCircle((gatel+notbubble, 0), notbubble))
        self.segments.append(SegmentCircle((gatel+notbubble, 0), notbubble))
        self.segments.append(SegmentCircle((-notbubble, 0), notbubble))
        self.anchors['out'] = (gatel+notbubble*2, 0)
        self.anchors['in1'] = (0, 0)


class Tgate(Element2Term):
    ''' Transmission gate.

        Anchors:
            in
            out
            c
            cbar
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment(
            [(0, 0), gap, (gatel, 0)]))
        self.segments.append(Segment(
            [(0, 0), (0, -gateh/2), (gatel, 0),
             (0, gateh/2), (0, 0)]))
        self.segments.append(Segment(
            [(gatel, 0), (gatel, -gateh/2), (0, 0),
             (gatel, gateh/2), (gatel, 0)]))
        self.segments.append(SegmentCircle((gatel/2, .28+.08), .08))
        self.segments.append(Segment(
            [(gatel/2, .28+.16), (gatel/2, .7)]))
        self.segments.append(Segment(
            [(gatel/2, -.28), (gatel/2, -.7)]))
        self.anchors['out'] = (gatel, 0)
        self.anchors['in1'] = (0, 0)
        self.anchors['c'] = (gatel/2, -.7)
        self.anchors['cbar'] = (gatel/2, .7)


class Schmitt(Buf):
    ''' Schmitt Trigger

        Anchors:
            in
            out
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.07, -.15), (.25, -.15), (.25, .15), gap,
                                      (.33, .15), (.15, .15), (.15, -.15)], lw=1))


class SchmittNot(Not):
    ''' Inverted Schmitt Trigger

        Anchors:
            in
            out
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(.07, -.15), (.25, -.15), (.25, .15), gap,
                                      (.33, .15), (.15, .15), (.15, -.15)], lw=1))


class SchmittAnd(And):
    ''' Schmitt Trigger AND

        Anchors:
            in1
            in2
            out
    '''
    def __init__(self, *, leadin: float = 0.35, leadout: float = 0.35, **kwargs):
        super().__init__(leadin=leadin, leadout=leadout, **kwargs)
        xofst = self.params['leadin']+gatel/2
        self.segments.append(Segment([(xofst+.07, -.15), (xofst+.25, -.15),
                                      (xofst+.25, .15), gap,
                                      (xofst+.33, .15), (xofst+.15, .15),
                                      (xofst+.15, -.15)], lw=1))


SchmittNand = partial(SchmittAnd, nand=True)
