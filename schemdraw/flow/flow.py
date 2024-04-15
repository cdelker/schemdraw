''' Flowcharting element definitions '''
from __future__ import annotations
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
    ''' Flowchart Process Box. Default box has minimum size (3, 2)
        but will expand to fit the label text. Size may be manually
        fixed using w and h arguments.

        Args:
            w: Width of box
            h: Height of box

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    _element_defaults = {
        'w': 3,
        'h': 2,
        'minsize': (3, 2),
        'pad': 0.25,
        'lblloc': 'center',
        'lblofst': 0,
        'theta': 0
    }
    def _set_anchors(self):
        w, h = self.params['w'], self.params['h']
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

    def _set_size(self) -> tuple[float, float]:
        minw, minh = self.params['minsize']
        mainlabels = [label for label in self._userlabels if label.loc is None]
        if mainlabels:
            minw, minh = labelsize(mainlabels[0], self.params['pad'])
            minw = max(minw, self.params['minsize'][0])
            minh = max(minh, self.params['minsize'][1])

        self._userparams.setdefault('w', minw)
        self._userparams.setdefault('h', minh)
        return self._userparams['w'], self._userparams['h']

    def _set_segments(self):
        w, h = self.params['w'], self.params['h']
        self.segments.append(Segment([(0, 0), (0, h/2), (w, h/2),
                                      (w, -h/2), (0, -h/2), (0, 0)]))
    
    def _place(self, dwgxy, dwgtheta, **dwgparams):
        ''' Make the box flow in the current drawing direction '''
        self._set_size()
        self._set_segments()
        self._set_anchors()

        if 'anchor' not in self.params:
            while dwgtheta < 0:
                dwgtheta += 360

            # Pick closest anchor
            thetas = [0, 45, 90, 135, 180, 225, 270, 315]
            anchors = ['W', 'SW', 'S', 'SE', 'E', 'NE', 'N', 'NW']
            idx = min(range(len(thetas)), key=lambda i: abs(thetas[i]-dwgtheta))
            anchor = anchors[idx]
            self.elmparams['anchor'] = anchor
            dropanchor = anchor.translate(anchor.maketrans('NESW', 'SWNE'))
            if dropanchor in self.anchors:
                self.elmparams['drop'] = self.anchors[dropanchor]
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class RoundBox(Box):
    ''' Alternate Process box with rounded corners

        Args:
            w: Width of box
            h: Height of box
            cornerradius: Radius of round corners [default: 0.3]

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    _element_defaults = {
        'cornerradius': 0.3
    }
    def __init__(self, *, cornerradius: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)

    def _set_segments(self):
        w, h = self.params['w'], self.params['h']
        self.segments = [SegmentPoly(
            [(0, h/2), (w, h/2), (w, -h/2), (0, -h/2)],
            cornerradius=self.params['cornerradius'])]
        
    def _set_anchors(self):
        super()._set_anchors()
        w, h = self.params['w'], self.params['h']
        cornerradius = self.params['cornerradius']
        k = cornerradius - cornerradius*math.sqrt(2)/2
        self.anchors['NE'] = (w-k, h/2-k)
        self.anchors['NW'] = (k, h/2-k)
        self.anchors['SE'] = (w-k, -h/2+k)
        self.anchors['SW'] = (k, -h/2+k)
        self.anchors['NNE'] = (3*w/4 if cornerradius < w/4 else w-cornerradius, h/2)
        self.anchors['NNW'] = (w/4 if cornerradius < w/4 else cornerradius, h/2)
        self.anchors['SSE'] = (3*w/4 if cornerradius < w/4 else w-cornerradius, -h/2)
        self.anchors['SSW'] = (w/4 if cornerradius < w/4 else cornerradius, -h/2)
        self.anchors['ENE'] = (w, h/4 if cornerradius < h/4 else h/2-cornerradius)
        self.anchors['ESE'] = (w, -h/4 if cornerradius < h/4 else -h/2+cornerradius)
        self.anchors['WNW'] = (0, h/4 if cornerradius < h/4 else h/2-cornerradius)
        self.anchors['WSW'] = (0, -h/4 if cornerradius < h/4 else -h/2+cornerradius)


class Terminal(RoundBox):
    ''' Flowchart start/end terminal

        Args:
            w: Width of box
            h: Height of box

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    _element_defaults = {
        'w': 3,
        'h': 1.25,
        'minsize': (3, 1.25),
        'droptheta': -90,
        'anchor': 'N'
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _set_size(self) -> tuple[float, float]:
        w, h = super()._set_size()
        self.elmparams['cornerradius'] = h/2
        return w, h

    def _set_anchors(self):
        super()._set_anchors()
        self.elmparams['drop'] = self.anchors['S']


class Subroutine(Box):
    ''' Flowchart subroutine/predefined process. Box with extra
        vertical lines near sides.

        Args:
            w: Width of box
            h: Height of box
            s: spacing of side lines [default: 0.3]

        Anchors:
            * 16 compass points (N, S, E, W, NE, NNE, etc.)
    '''
    _element_defaults = {
        's': 0.3
    }
    def __init__(self, *, s: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)

    def _set_size(self) -> tuple[float, float]:
        w, h = super()._set_size()
        w += self.params['s']*2
        self._userparams['w'] = w
        return w, h

    def _set_segments(self):
        super()._set_segments()
        w, h = self.params['w'], self.params['h']
        s = self.params['s']
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
    _element_defaults = {
        'slant': 0.5
    }
    def __init__(self, *, slant: Optional[float] = 0.5, **kwargs):
        super().__init__(**kwargs)

    def _set_segments(self):
        w, h = self.params['w'], self.params['h']
        s = self.params['slant']
        self.segments.append(SegmentPoly([(0, 0), (s/2, h/2), (w+s/2, h/2),
                                          (w-s/2, -h/2), (-s/2, -h/2)]))

    def _set_anchors(self):
        w, h = self.params['w'], self.params['h']
        s = self.params['slant']
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
        w, h = self.params['w'], self.params['h']
        # There's no ellipse Segment type, so draw one with a path Segment
        t = linspace(0, math.pi*2, num=50)
        y = [(h/2) * math.sin(t0) for t0 in t]
        x = [(w/2) * math.cos(t0) + w/2 for t0 in t]
        x[-1] = x[0]
        y[-1] = y[0]  # Ensure the path is actually closed
        self.segments.append(Segment(list(zip(x, y))))

    def _set_anchors(self):
        super()._set_anchors()
        w, h = self.params['w'], self.params['h']
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

    def _set_size(self) -> tuple[float, float]:
        minw, minh = self.params['minsize']
        pad = self.params['pad']
        mainlabels = [label for label in self._userlabels if label.loc is None]
        if mainlabels:
            minw, minh = labelsize(mainlabels[0], pad)
            tantheta = math.tan(math.radians(25)) # = h/2 / extraw
            fullw = minw + (minh/2/tantheta)
            fullh = minh + (tantheta*minw)
            minw = max(fullw, self.params['minsize'][0])
            minh = max(fullh, self.params['minsize'][1])

        self._userparams.setdefault('w', minw)
        self._userparams.setdefault('h', minh)
        return self._userparams['w'], self._userparams['h']
        
    def _set_segments(self):
        w, h = self.params['w'], self.params['h']
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
        w, h = self.params['w'], self.params['h']
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
    _element_defaults = {
        'h': 1.5,
        'w': 1.5,
        'r': 0.75,
        'minsize': (1.5, 1.5)
    }
    def _set_size(self) -> tuple[float, float]:
        pad = self.params['pad']
        mainlabels = [label for label in self._userlabels if label.loc is None]        
        if mainlabels:
            w, h = labelsize(mainlabels[0], pad)
            w = max(self.params['minsize'][0], w)
            h = max(self.params['minsize'][1], h)
        else:
            w, h = self.params['minsize']

        if 'r' in self._userparams:
            w = h = self._userparams.get('r')*2
        self._userparams.setdefault('w', w)
        self._userparams.setdefault('h', h)
        return self._userparams['w'], self._userparams['h']

    def _set_segments(self):
        r2 = self.params['w']
        r = r2/2
        self.segments = []
        self.segments.append(SegmentCircle((r, 0), r))

    def _set_anchors(self):
        super()._set_anchors()
        r2 = self.params['w']
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
    def _set_size(self) -> tuple[float, float]:
        w, h = super()._set_size()
        dr = self._userparams.get('dr', .15)
        self.elmparams['w'] = w+dr*2
        self.elmparams['h'] = h+dr*2
        return self.params['w'], self.params['h']
        
    def _set_segments(self):
        super()._set_segments()
        r2 = self.params['w']
        r = r2/2
        dr = self._userparams.get('dr', .15)
        self.segments.append(SegmentCircle((r, 0), r-dr))


Process = Box
RoundProcess = RoundBox
Start = Terminal
Circle = Connect
State = Connect
