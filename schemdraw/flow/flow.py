''' Flowcharting element definitions '''

import math

from ..util import linspace
from ..segments import Segment, SegmentCircle, SegmentPoly, SegmentText
from ..elements import Element


class Box(Element):
    ''' Flowchart Process Box

        Args:
            w: Width of box
            h: Height of box

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, w: float=3, h: float=2, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, h/2), (w, h/2),
                                      (w, -h/2), (0, -h/2), (0, 0)]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = 0
        self.anchors['center'] = (w/2, 0)
        self.anchors['N'] = (w/2, h/2)
        self.anchors['E'] = (w, 0)
        self.anchors['S'] = (w/2, -h/2)
        self.anchors['W'] = (0, 0)
        self.anchors['NW'] = (0, h/2)
        self.anchors['NE'] = (w, h/2)
        self.anchors['SW'] = (0, -h/2)
        self.anchors['SE'] = (w, -h/2)
        self.anchors['NNE'] = (3*w/4, h/2)
        self.anchors['NNW'] = (w/4, h/2)
        self.anchors['SSE'] = (3*w/4, -h/2)
        self.anchors['SSW'] = (w/4, -h/2)
        self.anchors['ENE'] = (w, h/3)
        self.anchors['ESE'] = (w, -h/3)
        self.anchors['WNW'] = (0, h/3)
        self.anchors['WSW'] = (0, -h/3)

    def _place(self, dwgxy, dwgtheta, **dwgparams):
        ''' Make the box flow in the current drawing direction '''
        if 'anchor' not in self._userparams and 'drop' not in self.params:
            while dwgtheta < 0:
                dwgtheta += 360

            # Pick closest anchor
            thetas = [0, 45, 90, 135, 180, 225, 270, 315]
            anchors = ['W', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW']
            idx = min(range(len(thetas)), key=lambda i: abs(thetas[i]-dwgtheta))
            anchor = anchors[idx]
            self.params['anchor'] = anchor
            dropanchor = anchor.translate(anchor.maketrans('NESW', 'SWNE'))
            if dropanchor in self.anchors:
                self.params['drop'] = self.anchors[dropanchor]
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class RoundBox(Box):
    ''' Alternate Process box with rounded corners

        Args:
            w: Width of box
            h: Height of box

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, w: float=3, h: float=2, cornerradius: float=0.3, **kwargs):
        super().__init__(w, h, **kwargs)
        self.segments = [SegmentPoly(
            [(0, h/2), (w, h/2), (w, -h/2), (0, -h/2)],
            cornerradius=cornerradius)]
        k = cornerradius - cornerradius*math.sqrt(2)/2
        self.anchors['NE'] = (w-k, h/2-k)
        self.anchors['NW'] = (k, h/2-k)
        self.anchors['SE'] = (w-k, -h/2+k)
        self.anchors['SW'] = (k, -h/2+k)


class Terminal(RoundBox):
    ''' Flowchart start/end terminal

        Args:
            w: Width of box
            h: Height of box

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, w: float=3, h: float=1.25, **kwargs):
        super().__init__(w=w, h=h, cornerradius=h/2, **kwargs)
        self.params['drop'] = self.anchors['S']
        self.params['droptheta'] = -90
        self.params['anchor'] = 'N'


class Subroutine(Box):
    ''' Flowchart subroutine/predefined process. Box with extra
        vertical lines near sides.

        Args:
            w: Width of box
            h: Height of box
            s: spacing of side lines

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, w: float=3.5, h: float=2, s: float=0.3, **kwargs):
        super().__init__(w, h, **kwargs)
        self.segments.append(Segment([(w-s, h/2), (w-s, -h/2)]))
        self.segments.append(Segment([(s, h/2), (s, -h/2)]))


class Data(Box):
    ''' Flowchart data or input/output box (parallelogram)

        Args:
            w: Width of box
            h: Height of box
            s: slant of sides

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, w: float=3, h: float=2, s: float=0.5, **kwargs):
        super().__init__(w, h, **kwargs)
        self.segments = []
        self.segments.append(SegmentPoly([(0, 0), (s/2, h/2), (w+s/2, h/2),
                                          (w-s/2, -h/2), (-s/2, -h/2)]))
        self.anchors['N'] = (w/2+s/2, h/2)
        self.anchors['S'] = (w/2-s/2, -h/2)
        self.anchors['NE'] = (w+s/2, h/2)
        self.anchors['SE'] = (w-s/2, -h/2)
        self.anchors['NW'] = (s/2, h/2)
        self.anchors['SW'] = (-s/2, -h/2)
        self.anchors['ENE'] = (w+s/4, h/4)
        self.anchors['WNW'] = (s/4, h/4)
        self.anchors['ESE'] = (w-s/4, -h/4)
        self.anchors['WSW'] = (-s/4, -h/4)
        self.anchors['NNE'] = (3*w/4+s/2, h/2)
        self.anchors['SSE'] = (3*w/4-s/2, -h/2)
        self.anchors['NNW'] = (w/4+s/2, h/2)
        self.anchors['SSW'] = (w/4-s/2, -h/2)


class Ellipse(Box):
    ''' Flowchart ellipse

        Args:
            w: Width of ellipse
            h: Height of ellipse

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, w: float=3, h: float=2, **kwargs):
        super().__init__(**kwargs)
        self.segments = []
        # There's no ellipse Segment type, so draw one with a path Segment
        t = linspace(0, math.pi*2, num=50)
        y = [(h/2) * math.sin(t0) for t0 in t]
        x = [(w/2) * math.cos(t0) + w/2 for t0 in t]
        x[-1] = x[0]
        y[-1] = y[0]  # Ensure the path is actually closed
        self.segments.append(Segment(list(zip(x, y))))
        sinpi4 = math.sin(math.pi/4)
        cospi4 = math.cos(math.pi/4)
        sinpi8 = math.sin(math.pi/8)
        cospi8 = math.cos(math.pi/8)
        self.anchors['SE'] = (w/2+w/2*cospi4, -h/2*sinpi4)
        self.anchors['SW'] = (w/2-w/2*cospi4, -h/2*sinpi4)
        self.anchors['NW'] = (w/2-w/2*cospi4, h/2*sinpi4)
        self.anchors['NE'] = (w/2+w/2*cospi4, h/2*sinpi4)
        self.anchors['ENE'] = (w/2+w/2*cospi8, h/2*sinpi8)
        self.anchors['WNW'] = (w/2-w/2*cospi8, h/2*sinpi8)
        self.anchors['ESE'] = (w/2+w/2*cospi8, -h/2*sinpi8)
        self.anchors['WSW'] = (w/2-w/2*cospi8, -h/2*sinpi8)
        self.anchors['NNE'] = (w/2+w/2*sinpi8, h/2*cospi8)
        self.anchors['NNW'] = (w/2-w/2*sinpi8, h/2*cospi8)
        self.anchors['SSE'] = (w/2+w/2*sinpi8, -h/2*cospi8)
        self.anchors['SSW'] = (w/2-w/2*sinpi8, -h/2*cospi8)


class Decision(Box):
    ''' Flowchart decision (diamond)

        Args:
            w: Width of box
            h: Height of box
            N: text for North decision branch
            S: text for South decision branch
            E: text for East decision branch
            W: text for West decision branch
            font: Font family/name
            fontsize: Point size of label font

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, w: float=4, h: float=2,
                 N: str=None, E: str=None, S: str=None, W: str=None,
                 font: str=None, fontsize: float=14,
                 **kwargs):
        super().__init__(w, h, **kwargs)
        self.segments = []
        self.segments.append(SegmentPoly([(0, 0), (w/2, h/2), (w, 0), (w/2, -h/2)]))
        self.anchors['NE'] = (3*w/4, h/4)
        self.anchors['NW'] = (w/4, h/4)
        self.anchors['SE'] = (3*w/4, -h/4)
        self.anchors['SW'] = (w/4, -h/4)
        self.anchors['NNE'] = (5*w/8, 3*h/8)
        self.anchors['NNW'] = (3*w/8, 3*h/8)
        self.anchors['SSE'] = (5*w/8, -3*h/8)
        self.anchors['SSW'] = (3*w/8, -3*h/8)
        self.anchors['ENE'] = (7*w/8, h/8)
        self.anchors['ESE'] = (7*w/8, -h/8)
        self.anchors['WNW'] = (w/8, h/8)
        self.anchors['WSW'] = (w/8, -h/8)

        lblofst = .13
        if N:
            self.segments.append(SegmentText(
                (w/2+lblofst, h/2+lblofst), N, align=('left', 'bottom'),
                font=font, fontsize=fontsize))
        if S:
            self.segments.append(SegmentText(
                (w/2+lblofst, -h/2-lblofst), S, align=('left', 'top'),
                font=font, fontsize=fontsize))
        if E:
            self.segments.append(SegmentText(
                (w+lblofst, lblofst), E, align=('left', 'bottom'),
                font=font, fontsize=fontsize))
        if W:
            self.segments.append(SegmentText(
                (-lblofst, lblofst), W, align=('right', 'bottom'),
                font=font, fontsize=fontsize))


class Connect(Box):
    ''' Flowchart connector/circle

        Args:
            r: Radius of circle

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, r: float=0.75, **kwargs):
        super().__init__(w=r*2, h=r*2, **kwargs)
        self.segments = []
        self.segments.append(SegmentCircle((r, 0), r))
        rsqrt2 = r * math.sqrt(2) / 2
        self.anchors['SE'] = (r+rsqrt2, -rsqrt2)
        self.anchors['SW'] = (r-rsqrt2, -rsqrt2)
        self.anchors['NE'] = (r+rsqrt2, rsqrt2)
        self.anchors['NW'] = (r-rsqrt2, rsqrt2)
        r225 = r * math.cos(math.radians(22.5))
        r675 = r * math.cos(math.radians(67.5))
        self.anchors['NNE'] = (r+r675, r225)
        self.anchors['ENE'] = (r+r225, r675)
        self.anchors['ESE'] = (r+r225, -r675)
        self.anchors['SSE'] = (r+r675, -r225)
        self.anchors['NNW'] = (r-r675, r225)
        self.anchors['WNW'] = (r-r225, r675)
        self.anchors['WSW'] = (r-r225, -r675)
        self.anchors['SSW'] = (r-r675, -r225)


class StateEnd(Connect):
    ''' End/Accept State (double circle)

        Args:
            r: radius
            dr: distance between circles

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, r: float=0.75, dr=.15, **kwargs):
        super().__init__(r, **kwargs)
        self.segments.append(SegmentCircle((r, 0), r-dr))


Process = Box
RoundProcess = RoundBox
Start = Terminal
Circle = Connect
State = Connect
