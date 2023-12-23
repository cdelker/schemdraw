''' Flowcharting element definitions '''
from typing import Optional
import math

from ..util import linspace
from ..segments import Segment, SegmentCircle, SegmentPoly, SegmentText
from ..elements import Element
from ..backends import svg


def labelsize(label, pad):
    ''' Get unit size of label and padding '''
    font = 'sans' if label.font is None else label.font
    size = 14 if label.fontsize is None else label.fontsize
    w72, h72, _ = svg.text_size(label.label, font=font, size=size)
    w = w72/64*2 + pad*2
    h = h72/64*2 + pad*2
    return w, h


class Box(Element):
    ''' Flowchart Process Box

        Args:
            w: Width of box
            h: Height of box

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._size = 3, 2
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = 0

    def _set_anchors(self):
        w, h = self._size
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

    def _set_size(self):
        w, h = self._size
        pad = self._userparams.get('pad', .25)
        padw = padh = pad
        mainlabels = [label for label in self._userlabels if label.loc is None]
        if mainlabels:
            w, h = labelsize(mainlabels[0], pad)
            w = max(w, self._size[0])
            h = max(h, self._size[1])

        w = self._userparams.get('w', w)
        h = self._userparams.get('h', h)
        self._size = w, h
        return self._size

    def _set_segments(self):
        w, h = self._size
        self.segments.append(Segment([(0, 0), (0, h/2), (w, h/2),
                                      (w, -h/2), (0, -h/2), (0, 0)]))
    
    def _place(self, dwgxy, dwgtheta, **dwgparams):
        ''' Make the box flow in the current drawing direction '''
        self._set_size()
        self._set_segments()
        self._set_anchors()

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
    def __init__(self, cornerradius: float = 0.3, **kwargs):
        super().__init__(**kwargs)
        self.cornerradius = cornerradius

    def _set_segments(self):
        w, h = self._size
        self.segments = [SegmentPoly(
            [(0, h/2), (w, h/2), (w, -h/2), (0, -h/2)],
            cornerradius=self.cornerradius)]
        
    def _set_anchors(self):
        super()._set_anchors()
        w, h = self._size
        k = self.cornerradius - self.cornerradius*math.sqrt(2)/2
        self.anchors['NE'] = (w-k, h/2-k)
        self.anchors['NW'] = (k, h/2-k)
        self.anchors['SE'] = (w-k, -h/2+k)
        self.anchors['SW'] = (k, -h/2+k)
        self.anchors['NNE'] = (3*w/4 if self.cornerradius < w/4 else w-self.cornerradius, h/2)
        self.anchors['NNW'] = (w/4 if self.cornerradius < w/4 else self.cornerradius, h/2)
        self.anchors['SSE'] = (3*w/4 if self.cornerradius < w/4 else w-self.cornerradius, -h/2)
        self.anchors['SSW'] = (w/4 if self.cornerradius < w/4 else self.cornerradius, -h/2)
        self.anchors['ENE'] = (w, h/4 if self.cornerradius < h/4 else h/2-self.cornerradius)
        self.anchors['ESE'] = (w, -h/4 if self.cornerradius < h/4 else -h/2+self.cornerradius)
        self.anchors['WNW'] = (0, h/4 if self.cornerradius < h/4 else h/2-self.cornerradius)
        self.anchors['WSW'] = (0, -h/4 if self.cornerradius < h/4 else -h/2+self.cornerradius)


class Terminal(RoundBox):
    ''' Flowchart start/end terminal

        Args:
            w: Width of box
            h: Height of box

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._size = 3, 1.25
        self.params['droptheta'] = -90
        self.params['anchor'] = 'N'

    def _set_size(self):
        super()._set_size()
        _, h = self._size
        self.cornerradius = h/2

    def _set_anchors(self):
        super()._set_anchors()
        self.params['drop'] = self.anchors['S']


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
    def __init__(self, s: float = 0.3, **kwargs):
        self.spacing = s
        self._size = 3.5, 2
        super().__init__(**kwargs)

    def _set_size(self):
        w, h = super()._set_size()
        w += self.spacing*2
        self._size = w, h
        
    def _set_segments(self):
        super()._set_segments()
        w, h = self._size
        s = self.spacing
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
    def __init__(self, s: float = 0.5, **kwargs):
        super().__init__(**kwargs)
        self.spacing = s

    def _set_segments(self):
        w, h = self._size
        s = self.spacing
        self.segments.append(SegmentPoly([(0, 0), (s/2, h/2), (w+s/2, h/2),
                                          (w-s/2, -h/2), (-s/2, -h/2)]))

    def _set_anchors(self):
        w, h = self._size
        s = self.spacing
        super()._set_anchors()
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
    def _set_segments(self):
        w, h = self._size
        # There's no ellipse Segment type, so draw one with a path Segment
        t = linspace(0, math.pi*2, num=50)
        y = [(h/2) * math.sin(t0) for t0 in t]
        x = [(w/2) * math.cos(t0) + w/2 for t0 in t]
        x[-1] = x[0]
        y[-1] = y[0]  # Ensure the path is actually closed
        self.segments.append(Segment(list(zip(x, y))))

    def _set_anchors(self):
        super()._set_anchors()
        w, h = self._size
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
    def __init__(self, N: Optional[str] = None, E: Optional[str] = None, S: Optional[str] = None, W: Optional[str] = None,
                 font: Optional[str] = None, fontsize: float = 14,
                 **kwargs):
        super().__init__(**kwargs)
        self._size = 4, 2.25
        self._font = font
        self._fontsize = fontsize
        self._N = N
        self._E = E
        self._W = W
        self._S = S

    def _set_size(self):
        w, h = self._size
        pad = self._userparams.get('pad', .25)
        padw = padh = pad
        mainlabels = [label for label in self._userlabels if label.loc is None]
        if mainlabels:
            w, h = labelsize(mainlabels[0], pad)
            # h is set by pad, adjust w to fit full text
            tantheta = math.tan(math.radians(25)) # = h/2 / extraw
            fullw = w + (h/2/tantheta)
            fullh = h + (tantheta*w)
            w = max(fullw, self._size[0])
            h = max(fullh, self._size[1])

        w = self._userparams.get('w', w)
        h = self._userparams.get('h', h)
        self._size = w, h
        return self._size
        
    def _set_segments(self):
        w, h = self._size
        font = self._font
        fontsize = self._fontsize
        self.segments.append(SegmentPoly([(0, 0), (w/2, h/2), (w, 0), (w/2, -h/2)]))

        lblofst = .13        
        N, E, S, W = self._N, self._E, self._S, self._W
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

    def _set_anchors(self):
        w, h = self._size
        super()._set_anchors()
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


class Connect(Box):
    ''' Flowchart connector/circle

        Args:
            r: Radius of circle

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._size = 1.5, 1.5

    def _set_size(self):
        pad = self._userparams.get('pad', .25)

        mainlabels = [label for label in self._userlabels if label.loc is None]        
        if mainlabels:
            w, h = labelsize(mainlabels[0], pad)
            w = max(self._size[0], w)
            h = max(self._size[1], h)
        else:
            w, h = self._size

        if 'r' in self._userparams:
            w = h = self._userparams.get('r')*2
        self._size = w, h
        return self._size

    def _set_segments(self):
        r2, _ = self._size
        r = r2/2
        self.segments = []
        self.segments.append(SegmentCircle((r, 0), r))

    def _set_anchors(self):
        super()._set_anchors()
        r2, _ = self._size
        r = r2/2
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
    def _set_size(self):
        w, h = super()._set_size()
        dr = self._userparams.get('dr', .15)
        self._size = w+dr*2, h+dr*2
        return self._size
        
    def _set_segments(self):
        super()._set_segments()
        r2, _ = self._size
        r = r2/2
        dr = self._userparams.get('dr', .15)
        self.segments.append(SegmentCircle((r, 0), r-dr))


Process = Box
RoundProcess = RoundBox
Start = Terminal
Circle = Connect
State = Connect
