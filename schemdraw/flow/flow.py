''' Flowcharting element definitions '''

import math

from ..util import linspace
from ..segments import Segment, SegmentCircle, SegmentText
from ..elements import Element


class Box(Element):
    ''' Flowchart box

        Args:
            w: Width of box
            h: Height of box

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, w: float=3, h: float=2, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, w/2), (h, w/2),
                                      (h, -w/2), (0, -w/2), (0, 0)]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (h, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)


class Subroutine(Element):
    ''' Flowchart subroutine. Box with extra vertical lines
        near sides.

        Args:
            w: Width of box
            h: Height of box
            s: spacing of side lines

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, w: float=3.5, h: float=2, s: float=0.3, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, w/2), (h, w/2),
                                      (h, -w/2), (0, -w/2), (0, 0)]))
        self.segments.append(Segment([(0, w/2-s), (h, w/2-s)]))
        self.segments.append(Segment([(0, -w/2+s), (h, -w/2+s)]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (h, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)


class Data(Element):
    ''' Flowchart data box (parallelogram)

        Args:
            w: Width of box
            h: Height of box
            s: slant of sides

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, w: float=3, h: float=2, s: float=0.5, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, w/2+s/2), (h, w/2-s/2),
                                      (h, -w/2-s/2), (0, -w/2+s/2), (0, 0)]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (h, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)


class Start(Element):
    ''' Flowchart start/stop box (ellipse)


        Args:
            w: Width of ellipse
            h: Height of ellipse

        Anchors:
            * N
            * S
            * E
            * W    '''
    def __init__(self, w: float=3, h: float=2, **kwargs):
        super().__init__(**kwargs)
        # There's no ellipse Segment type, so draw one with a path Segment
        t = linspace(0, math.pi*2, num=50)
        y = [(w/2) * math.cos(t0) for t0 in t]
        x = [(h/2) * math.sin(t0) + h/2 for t0 in t]
        x[-1] = x[0]
        y[-1] = y[0]  # Ensure the path is actually closed
        self.segments.append(Segment(list(zip(x, y))))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (h, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)


class Decision(Element):
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
            * N
            * S
            * E
            * W
    '''
    def __init__(self, w: float=4, h: float=2,
                 N: str=None, E: str=None, S: str=None, W: str=None,
                 font: str=None, fontsize: float=14,
                 **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (h/2, w/2), (h, 0),
                                      (h/2, -w/2), (0, 0)]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (h, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)

        lblofst = .13
        if N:
            self.segments.append(SegmentText(
                (0, lblofst), N, align=('left', 'bottom'),
                font=font, fontsize=fontsize))
        if S:
            self.segments.append(SegmentText(
                (h, lblofst), S, align=('left', 'top'),
                font=font, fontsize=fontsize))
        if E:
            self.segments.append(SegmentText(
                (h/2, w/2+lblofst), E, align=('left', 'bottom'),
                font=font, fontsize=fontsize))
        if W:
            self.segments.append(SegmentText(
                (h/2, -w/2-lblofst), W, align=('right', 'bottom'),
                font=font, fontsize=fontsize))


class Connect(Element):
    ''' Flowchart connector (circle)

        Args:
            r: Radius of box

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        r = kwargs.get('r', 0.75)
        self.segments.append(SegmentCircle((r, 0), r))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (2*r, 0)
        self.anchors['W'] = (r, -r)
        self.anchors['E'] = (r, r)
        self.anchors['S'] = (2*r, 0)
        self.anchors['N'] = (0, 0)
