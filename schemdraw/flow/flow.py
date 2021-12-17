''' Flowcharting element definitions '''

import math

from ..util import linspace
from ..segments import Segment, SegmentCircle, SegmentPoly, SegmentText
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
        self.anchors['center'] = (h/2, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)
        self.anchors['NW'] = (0, -w/2)
        self.anchors['NE'] = (0, w/2)
        self.anchors['SW'] = (h, -w/2)
        self.anchors['SE'] = (h, w/2)
        self.anchors['NNE'] = (0, w/3)
        self.anchors['NNW'] = (0, -w/3)
        self.anchors['SSE'] = (h, w/3)
        self.anchors['SSW'] = (h, -w/3)
        self.anchors['ENE'] = (h/3, w/2)
        self.anchors['ESE'] = (2*h/3, w/2)
        self.anchors['WNW'] = (h/3, -w/2)
        self.anchors['WSW'] = (2*h/3, -w/2)


class RoundBox(Element):
    ''' Box with rounded corners '''
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
    def __init__(self, w: float=3, h: float=2, cornerradius=0.3, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentPoly(
            [(0, w/2), (h, w/2), (h, -w/2), (0, -w/2)],
            cornerradius=cornerradius))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (h, 0)
        self.anchors['center'] = (h/2, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)
        k = cornerradius - cornerradius*math.sqrt(2)/2
        self.anchors['NE'] = (k, w/2-k)
        self.anchors['NW'] = (k, -w/2+k)
        self.anchors['SE'] = (h-k, w/2-k)
        self.anchors['SW'] = (h-k, -w/2+k)


class Start(RoundBox):
    def __init__(self, w: float=3, h: float=1.25, **kwargs):
        super().__init__(w=w, h=h, cornerradius=h/2, **kwargs)


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
            * NE
            * NW
            * SE
            * SW
            * NNE
            * NNW
            * ENE
            * WNW
            * SSE
            * SSW
            * ESE
            * WSW
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
        self.anchors['center'] = (h/2, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)
        self.anchors['NW'] = (0, -w/2)
        self.anchors['NE'] = (0, w/2)
        self.anchors['SW'] = (h, -w/2)
        self.anchors['SE'] = (h, w/2)
        self.anchors['NNE'] = (0, w/3)
        self.anchors['NNW'] = (0, -w/3)
        self.anchors['SSE'] = (h, w/3)
        self.anchors['SSW'] = (h, -w/3)
        self.anchors['ENE'] = (h/3, w/2)
        self.anchors['ESE'] = (2*h/3, w/2)
        self.anchors['WNW'] = (h/3, -w/2)
        self.anchors['WSW'] = (2*h/3, -w/2)


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
            * NE
            * NW
            * SE
            * SW
    '''
    def __init__(self, w: float=3, h: float=2, s: float=0.5, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (0, w/2+s/2), (h, w/2-s/2),
                                      (h, -w/2-s/2), (0, -w/2+s/2), (0, 0)]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (h, 0)
        self.anchors['center'] = (h/2, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)
        self.anchors['NE'] = (0, w/2+s/2)
        self.anchors['SE'] = (h, w/2-s/2)
        self.anchors['NW'] = (0, -w/2+s/2)
        self.anchors['SW'] = (h, -w/2-s/2)

        
class Ellipse(Element):
    ''' Flowchart ellipse

        Args:
            w: Width of ellipse
            h: Height of ellipse

        Anchors:
            * N
            * S
            * E
            * W
            * NE
            * NW
            * SE
            * SW
    '''
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
        self.anchors['center'] = (h/2, 0)
        self.anchors['W'] = (h/2, -w/2)
        self.anchors['E'] = (h/2, w/2)
        self.anchors['S'] = (h, 0)
        self.anchors['N'] = (0, 0)
        sinpi4 = math.sin(math.pi/4)
        cospi4 = math.cos(math.pi/4)
        self.anchors['SE'] = (h/2+h/2*sinpi4, w/2*cospi4)
        self.anchors['SW'] = (h/2+h/2*sinpi4, -w/2*cospi4)
        self.anchors['NW'] = (h/2-h/2*sinpi4, -w/2*cospi4)
        self.anchors['NE'] = (h/2-h/2*sinpi4, w/2*cospi4)
        

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
        self.anchors['center'] = (h/2, 0)
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
    ''' Flowchart connector/circle

        Args:
            r: Radius of circle

        Anchors:
            * N
            * S
            * E
            * W
            * NE
            * SE
            * SW
            * NW
            * NNE
            * ENE
            * ESE
            * SSE
            * SSW
            * WSW
            * WNW
            * NNW
    '''
    def __init__(self, r: float=0.75, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(SegmentCircle((r, 0), r))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = (2*r, 0)
        self.anchors['center'] = (r, 0)
        self.anchors['N'] = (0, 0)
        self.anchors['W'] = (r, -r)
        self.anchors['E'] = (r, r)
        self.anchors['S'] = (2*r, 0)
        rsqrt2 = r * math.sqrt(2) / 2
        self.anchors['SE'] = (r+rsqrt2, rsqrt2)
        self.anchors['SW'] = (r+rsqrt2, -rsqrt2)
        self.anchors['NE'] = (r-rsqrt2, rsqrt2)
        self.anchors['NW'] = (r-rsqrt2, -rsqrt2) 
        r225 = r * math.cos(math.radians(22.5))
        r675 = r * math.cos(math.radians(67.5))
        self.anchors['NNE'] = (r-r225, r675)
        self.anchors['ENE'] = (r-r675, r225)
        self.anchors['ESE'] = (r+r675, r225)
        self.anchors['SSE'] = (r+r225, r675)
        self.anchors['NNW'] = (r-r225, -r675)
        self.anchors['WNW'] = (r-r675, -r225)
        self.anchors['WSW'] = (r+r675, -r225)
        self.anchors['SSW'] = (r+r225, -r675)


Circle = Connect