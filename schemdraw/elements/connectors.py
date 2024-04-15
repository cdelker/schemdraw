''' Connectors and bus lines '''

from __future__ import annotations
from typing import Optional, Sequence
import warnings

from ..segments import Segment, SegmentText, SegmentCircle, SegmentPoly
from ..elements import Element, Line
from .twoterm import resheight, gap
from ..types import Point, XY, Valign, HeaderStyle, HeaderNumbering


class OrthoLines(Element):
    ''' Orthogonal multiline connectors

        Use `at()` and `to()` methods to specify starting and
        ending location of OrthoLines.

        The default lines are spaced to provide connection to
        pins with default spacing on Ic element or connector
        such as a Header.

        Args:
            n: Number of parallel lines
            dy: Distance between parallel lines [default: 0.6]
            xstart: Fractional distance (0-1) to start vertical
                portion of first ortholine
    '''
    _element_defaults = {
        'dy': 0.6,
    }
    def __init__(self, *,
                 n: int = 1,
                 dy: Optional[float] = None,
                 xstart: Optional[float] = None,
                 arrow: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._userparams.setdefault('to', (1, 1))

    def to(self, xy: XY) -> 'Element':
        ''' Specify ending position of OrthoLines '''
        self._userparams['to'] = xy
        return self

    def delta(self, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position relative to start position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._positioned:
            self._position()

        self.params['theta'] = 0
        xy: XY = self.params.get('at', dwgxy)
        to: XY = self.params.get('to', dwgxy)
        delta = self.params.get('delta', None)
        n = self.params.get('n', 1)
        ndy = self.params.get('dy', .6)
        xstart = self.params.get('xstart', None)
        arrow = self.params.get('arrow', None)
        if delta is not None:
            dx, dy = delta
        else:
            dx = to[0] - xy[0]
            dy = to[1] - xy[1]

        if abs(dy) < .05:
            for i in range(n):
                y = -i*ndy
                self.segments.append(Segment([(0, y), (dx, y)]))
        else:
            # x0 is first line to go up
            if xstart is not None:
                if dy > 0:
                    x0 = dx*xstart
                else:
                    x0 = dx*xstart - ndy - ndy*(n-1)*xstart
                    # xstart=0 --> -ndy; xstart=1 --> dx-ndy*n
            elif dx > 0:
                x0 = dx/2 - (ndy*(n-1)/2)
            else:
                x0 = dx/2 + (ndy*(n-1)/2)

            for i in range(n):
                y = -i*ndy
                if dy > 0:
                    x = x0 + ndy*i if dx > 0 else x0 - ndy*i
                else:
                    x = x0 + (n-i)*ndy if dx > 0 else x0 - (n-i)*ndy
                self.segments.append(Segment([(0, y), (x, y), (x, y+dy), (dx, y+dy)], arrow=arrow))
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class RightLines(Element):
    ''' Right-angle multi-line connectors

        Use `at()` and `to()` methods to specify starting and ending
        location.

        The default lines are spaced to provide connection to
        pins with default spacing on Ic element or connector
        such as a Header.

        Args:
            n: Number of parallel lines
            dy: Distance between parallel lines [default: 0.6]
    '''
    _element_defaults = {
        'dy': 0.6,
        'to': (3, -2),
        'theta': 0,
        'n': 1
    }
    def __init__(self, *,
                 n: int = 1,
                 dy: Optional[float] = None,
                 arrow: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)

    def to(self, xy: XY) -> 'Element':
        ''' Specify ending position of OrthoLines '''
        self._userparams['to'] = xy
        return self

    def delta(self, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position relative to start position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._positioned:
            self._position()

        xy = self.params.get('at', dwgxy)
        delta = self.params.get('delta', None)
        to = self.params['to']
        n = self.params['n']
        ndy = self.params['dy']
        arrow = self.params.get('arrow', None)
        if delta is not None:
            dx, dy = delta
        else:
            dx = to[0] - xy[0]
            dy = to[1] - xy[1]
        for i in range(n):
            y = -i*ndy
            if dy > 0:
                x = dx - i*ndy if dx < 0 else dx + i*ndy
            else:
                x = dx + (n-i-1)*ndy if dx > 0 else dx - (n-i-1)*ndy
            self.segments.append(Segment([(0, y), (x, y), (x, dy)], arrow=arrow))

        self.anchors['mid'] = (dx/2, 0)
        self.elmparams['lblloc'] = 'mid'
        self.elmparams['drop'] = (x, dy)
        self.elmparams['droptheta'] = 90 if dy > 0 else -90
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class Header(Element):
    ''' Header connector element

        Args:
            rows: Number of rows
            cols: Number of columns. Pin numbering requires 1 or 2 columns
            pinsleft: List of pin labels for left side
            pinsright: List of pin labels for right side
            style: Connector style, 'round', 'square', or 'screw' [default: round]
            numbering: Pin numbering order. 'lr' for left-to-right numbering,
                'ud' for up-down numbering, or 'ccw' for counter-clockwise
                (integrated-circuit style) numbering. Pin 1 is always at the
                top-left corner, unless `flip` method is also called. [default: lr]
            shownumber: Draw pin numbers outside the header
            pinalignleft: Vertical alignment for pins on left side
                ('center', 'top', 'bottom') [default: 'bottom']
            pinalignright: Vertical alignment for pins on right side
                ('center', 'top', 'bottom') [default: 'bottom']
            pinfontsizeleft: Font size for pin labels on left [default: 9]
            pinfontsizeright: Font size for pin labels on right [default: 9]
            pinspacing: Distance between pins [default: 0.6]
            edge: Distance between header edge and first pin row/column [default: 0.3]
            pinfill: Color to fill pin circles [default: bg]

        Anchors:
            pin[X] for each pin
    '''
    _element_defaults = {
        'pinspacing': 0.6,
        'style': 'round',
        'numbering': 'lr',
        'pinfontsizeleft': 9,
        'pinfontsizeright': 9,
        'edge': 0.3,
        'pinfill': 'bg',
        'shownumber': False,
        'pinalignleft': 'bottom',
        'pinalignright': 'bottom',
        'pinrad': 0.1
    }
    def __init__(self,
                 rows: int = 4,
                 cols: int = 1,
                 pinsleft: Optional[Sequence[str]] = None,
                 pinsright: Optional[Sequence[str]] = None,
                 *,
                 style: Optional[HeaderStyle] = None,
                 numbering: Optional[HeaderNumbering] = None,
                 shownumber: Optional[bool] = None,
                 pinalignleft: Optional[Valign] = None,
                 pinalignright: Optional[Valign] = None,
                 pinfontsizeright: Optional[float] = None,
                 pinfontsizeleft: Optional[float] = None,
                 pinspacing: Optional[float] = None,
                 edge: Optional[float] = None,
                 pinfill: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)
        if pinsleft is None:
            pinsleft = []
        if pinsright is None:
            pinsright = []
        if cols > 2:
            warnings.warn('Header numbering not supported with cols > 2')

        self.elmparams['d'] = 'right'
        w = (cols-1) * self.params['pinspacing'] + self.params['edge']*2
        h = (rows-1) * self.params['pinspacing'] + self.params['edge']*2
        pinrad = self.params['pinrad']

        self.segments.append(SegmentPoly([(0, 0), (0, h), (w, h), (w, 0)]))
        for row in range(rows):
            for col in range(cols):
                xy = (col*self.params['pinspacing']+self.params['edge'],
                      h-row*self.params['pinspacing']-self.params['edge'])

                if self.params['style'] == 'square':
                    x, y = xy
                    self.segments.append(SegmentPoly([(x-pinrad, y-pinrad), (x+pinrad, y-pinrad),
                                                      (x+pinrad, y+pinrad), (x-pinrad, y+pinrad)],
                                                     fill='bg', zorder=4))
                elif self.params['style'] == 'screw':
                    x, y = xy
                    self.segments.append(SegmentCircle(xy, pinrad*1.75, fill=self.params['pinfill'], zorder=4))
                    self.segments.append(Segment([(x+pinrad, y+pinrad), (x-pinrad, y-pinrad)], zorder=5))

                else:  # self.params['style'] == 'round'
                    self.segments.append(SegmentCircle(xy, pinrad, fill=self.params['pinfill'], zorder=4))

                if self.params['numbering'] == 'lr' or self.params['numbering'] is True:
                    pnumber = str(row*cols + col + 1)
                elif self.params['numbering'] == 'ud':
                    pnumber = str(row + col*rows + 1)
                else:  # number == 'ccw'
                    pnumber = str(rows*col+(rows-row)) if col % 2 else str(row+1)
                self.anchors['pin{}'.format(pnumber)] = xy

                if self.params['shownumber']:
                    numxy = (w+.05 if col % 2 else -.05, xy[1])
                    align = ('left' if col % 2 else 'right', 'bottom')
                    self.segments.append(SegmentText(
                        numxy, pnumber, fontsize=self.params['pinfontsizeleft'], align=align))  # type: ignore

                if pinsleft and (cols == 1 or not col % 2):
                    lblxy = (-.05, xy[1])
                    self.segments.append(SegmentText(lblxy, pinsleft[row], fontsize=self.params['pinfontsizeleft'],
                                                     align=('right', self.params['pinalignleft'])))

                if pinsright and (cols == 1 or col % 2):
                    lblxy = (w+.05, xy[1])
                    self.segments.append(SegmentText(lblxy, pinsright[row], fontsize=self.params['pinfontsizeright'],
                                                     align=('left', self.params['pinalignleft'])))


class Jumper(Element):
    ''' Jumper for use on a Header element

        Set position using `at()` method with a Header
        pin location, e.g. `Jumper().at(H.in1)`

        Args:
            pinspacing: Spacing between pins [default: 0.6]
    '''
    _element_defaults = {
        'pinspacing': 0.6,
        'pinrad': 0.1,
        'theta': 0
    }
    def __init__(self, *,
                 pinspacing: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        pinrad = self.params['pinrad']
        x = pinrad*2.5
        self.segments.append(SegmentPoly([(-x, -x), (self.params['pinspacing']+x, -x),
                                         (self.params['pinspacing']+x, x), (-x, x)]))


class BusConnect(Element):
    ''' Data bus connection.

        Adds the short diagonal lines that break out a bus (wide line)
        to connect to an Ic or Header element.

        Args:
            n: Number of parallel lines
            up: Slant up or down
            dy: Distance between parallel lines [default: 0.6]
            lwbus: Line width of bus line [default: 4]
            l: length of connection lines [default: 3]

        Anchors:
            * start
            * end
            * p[X] where X is int for each data line
    '''
    _element_defaults = {
        'dy': 0.6,
        'lwbus': 4,
        'l': 3,
        'slantx': 0.5
    }
    def __init__(self,
                 n: int = 1,
                 up: bool = True,
                 *,
                 dy: Optional[float] = None,
                 lwbus: Optional[float] = None,
                 l: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.params['theta'] = 0

        deltax = self.params['l']
        deltay = self.params['dy']
        lw = self.params['lwbus']
        slantx = self.params['slantx']
        slanty = slantx if up else -slantx

        for i in range(n):
            y = -i*deltay
            self.segments.append(Segment([(0, y), (deltax-slantx, y), (deltax, y+slanty)]))
            self.anchors[f'pin{i+1}'] = (0, y)
        self.segments.append(Segment([(deltax, slantx), (deltax, slanty-n*deltay)], lw=lw))
        self.elmparams['drop'] = (deltax, slantx)
        self.anchors['start'] = (deltax, slantx)
        self.anchors['end'] = (deltax, slantx-n*deltay)


class BusLine(Line):
    ''' Data bus line. Just a wide line.

        Use BusConnect to break out connections to the BusLine.

        Args:
            lw: Line width [default: 4]
    '''
    _element_defaults = {
        'lw': 4
    }
    def __init__(self, lw: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)


class DB9(Element):
    ''' DB9 Connector

        Args:
            pinspacing: Distance between pins [default: 0.6]
            edge: Distance between edge and pins [default: 0.3]
            number: Draw pin numbers [default: False]
            pinfill: Color to fill pin circles [default: bg]

        Anchors:
            * pin1 thru pin9
    '''
    _element_defaults = {
        'pinspacing': 0.6,
        'edge': 0.3,
        'pinfill': 'bg',
        'pinrad': 0.1,
        'number': False,
        'theta': 0,
    }
    def __init__(self, *,
                 pinspacing: Optional[float] = None,
                 edge: Optional[float] = None,
                 number: Optional[bool] = None,
                 pinfill: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)
        spacing = self.params['pinspacing']
        edgepad = self.params['edge']
        fill = self.params['pinfill']
        w = spacing + edgepad*2
        h1 = 4 * spacing + edgepad*2
        h2 = h1 + .5
        pinrad = self.params['pinrad']

        self.segments.append(SegmentPoly([(0, 0), (0, h1), (w, h2), (w, -.5)], cornerradius=.25))

        for i in range(4):
            xy = (edgepad, h1-(i+.5)*spacing-edgepad)
            self.segments.append(SegmentCircle(xy, pinrad, fill=fill, zorder=4))
            self.anchors[f'pin{9-i}'] = xy
            if self.params['number']:
                self.segments.append(SegmentText((xy[0], xy[1]+pinrad),
                                                 str(9-i), fontsize=9,
                                                 align=('center', 'bottom')))
        for i in range(5):
            xy = (edgepad+spacing, h2-(i+.75)*spacing-edgepad)
            self.segments.append(SegmentCircle(xy, pinrad, fill=fill, zorder=4))
            self.anchors[f'pin{5-i}'] = xy
            if self.params['number']:
                self.segments.append(SegmentText((xy[0], xy[1]+pinrad),
                                                 str(5-i), fontsize=9,
                                                 align=('center', 'bottom')))


class DB25(Element):
    ''' DB25 Connector

        Args:
            pinspacing: Distance between pins [default: 0.6]
            edge: Distance between edge and pins [default: 0.3]
            number: Draw pin numbers
            pinfill: Color to fill pin circles [default: bg]

        Anchors:
            * pin1 thru pin25
    '''
    _element_defaults = {
        'pinspacing': 0.6,
        'edge': 0.3,
        'pinfill': 'bg',
        'number': False,
        'pinrad': 0.1,
        'theta': 0
    }
    def __init__(self, *,
                 pinspacing: Optional[float] = None,
                 edge: Optional[float] = None,
                 number: Optional[bool] = None,
                 pinfill: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)
        spacing = self.params['pinspacing']
        edgepad = self.params['edge']
        fill = self.params['pinfill']
        w = spacing + edgepad*2
        h1 = 12 * spacing + edgepad*2
        h2 = h1 + .5
        pinrad = self.params['pinrad']

        self.segments.append(SegmentPoly([(0, 0), (0, h1), (w, h2), (w, -.5)], cornerradius=.25))

        for i in range(12):
            xy = (edgepad, h1-(i+.5)*spacing-edgepad)
            self.segments.append(SegmentCircle(xy, pinrad, fill=fill, zorder=4))
            self.anchors[f'pin{25-i}'] = xy
            if number:
                self.segments.append(SegmentText((xy[0], xy[1]+pinrad),
                                                 str(25-i), fontsize=9,
                                                 align=('center', 'bottom')))
        for i in range(13):
            xy = (edgepad+spacing, h2-(i+.75)*spacing-edgepad)
            self.segments.append(SegmentCircle(xy, pinrad, fill=fill, zorder=4))
            self.anchors[f'pin{13-i}'] = xy
            if number:
                self.segments.append(SegmentText((xy[0], xy[1]+pinrad),
                                                 str(13-i), fontsize=9,
                                                 align=('center', 'bottom')))


class CoaxConnect(Element):
    ''' Coaxial connector

        Args:
            radius: Radius of outer shell [defualt: 0.4]
            radiusinner: Radius of inner conductor [default: 0.12]
            fillinner: Color to fill inner conductor [default: bg]

        Anchors:
            * center
            * N
            * S
            * E
            * W
    '''
    _element_defaults = {
        'radius': 0.4,
        'radiusinner': 0.12,
        'fillinner': 'bg'
    }
    def __init__(self, *,
                 radius: Optional[float] = None, 
                 radiusinner: Optional[float] = None,
                 fillinner: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)
        r1 = self.params['radius']
        r2 = self.params['radiusinner']
        fill = self.params['fillinner']
        self.segments.append(SegmentCircle((0, 0), r1))
        self.segments.append(SegmentCircle((0, 0), r2, fill=fill, zorder=4))
        self.anchors['center'] = (0, 0)
        self.anchors['N'] = (0, r1)
        self.anchors['S'] = (0, -r1)
        self.anchors['E'] = (r1, 0)
        self.anchors['W'] = (-r1, 0)


class Plug(Element):
    ''' Plug (male connector) '''
    _element_defaults = {
        'pluggap': 0.18
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pluggap = self.params['pluggap']
        self.segments.append(Segment([(0, 0), (1, 0), gap, (1-resheight, resheight), (1, 0),
                                      (1-resheight, -resheight)]))
        self.elmparams['drop'] = (1+pluggap, 0)


class Jack(Element):
    ''' Jack (female connector) '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), (-resheight, resheight), gap,
                                      (-resheight, -resheight), (0, 0), (1, 0)]))
        self.elmparams['drop'] = (1, 0)


class Terminal(Element):
    ''' Terminal element
    
        Args:
            r: Radius of terminal [default: 0.18]
            open: Draw as open circle
    '''
    _element_defaults = {
        'r': 0.18,
        'open': True,
        'fill': 'bg',
        'drop': (0, 0),
        'theta': 0,
        'zorder': 4,
    }
    def __init__(self, *,
                 r: Optional[float] = None,
                 open: Optional[bool] = None,
                 **kwargs):
        super().__init__(**kwargs)
        radius = self.params['r']
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)
        self.elmparams['fill'] = 'bg' if self.params['open'] else True
        self.segments.append(SegmentCircle((0, 0), radius))
        kx = 1.0
        ky = 2.0
        self.segments.append(Segment(
            [(-kx*radius, -ky*radius),
             ( kx*radius,  ky*radius)]))