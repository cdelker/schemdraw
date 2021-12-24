''' Connectors and bus lines '''

from __future__ import annotations
from typing import Sequence
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
            dy: Distance between parallel lines
            xstart: Fractional distance (0-1) to start vertical
                portion of first ortholine
    '''
    def __init__(self, *d, n: int=1, dy: float=0.6,
                 xstart: float=None, arrow: str=None, **kwargs):
        super().__init__(*d, **kwargs)
        self._userparams['n'] = n
        self._userparams['dy'] = dy
        self._userparams['xstart'] = xstart
        self._userparams['arrow'] = arrow
        self._userparams.setdefault('to', (1, 1))

    def to(self, xy: XY) -> 'Element':
        ''' Specify ending position of OrthoLines '''
        self._userparams['to'] = xy
        return self

    def delta(self, dx: float=0, dy: float=0):
        ''' Specify ending position relative to start position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        self.params['theta'] = 0
        xy: XY = self._cparams.get('at', dwgxy)
        to: XY = self._cparams.get('to', dwgxy)
        delta = self._cparams.get('delta', None)
        n = self._cparams.get('n', 1)
        ndy = self._cparams.get('dy', .6)
        xstart = self._cparams.get('xstart', None)
        arrow = self._cparams.get('arrow', None)
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
            dy: Distance between parallel lines
    '''
    def __init__(self, *d, n: int=1, dy: float=0.6, arrow: str=None, **kwargs):
        super().__init__(*d, **kwargs)
        self._userparams['n'] = n
        self._userparams['dy'] = dy
        self._userparams['arrow'] = arrow
        self._userparams.setdefault('to', (3, -2))

    def to(self, xy: XY) -> 'Element':
        ''' Specify ending position of OrthoLines '''
        self._userparams['to'] = xy
        return self

    def delta(self, dx: float=0, dy: float=0):
        ''' Specify ending position relative to start position '''
        self._userparams['delta'] = Point((dx, dy))
        return self
    
    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        self.params['theta'] = 0
        xy = self._cparams.get('at', dwgxy)
        to = self._cparams.get('to', None)
        delta = self._cparams.get('delta', None)
        n = self._cparams.get('n', 1)
        ndy = self._cparams.get('dy', .6)
        arrow = self._cparams.get('arrow', None)
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
        self.params['lblloc'] = 'mid'
        self.params['drop'] = (x, dy)
        self.params['droptheta'] = 90 if dy > 0 else -90
    
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class Header(Element):
    ''' Header connector element

        Args:
            rows: Number of rows
            cols: Number of columns. Pin numbering requires 1 or 2 columns
            style: Connector style, 'round', 'square', or 'screw'
            numbering: Pin numbering order. 'lr' for left-to-right numbering,
                'ud' for up-down numbering, or 'ccw' for counter-clockwise
                (integrated-circuit style) numbering. Pin 1 is always at the
                top-left corner, unless `flip` method is also called.
            shownumber: Draw pin numbers outside the header
            pinsleft: List of pin labels for left side
            pinsright: List of pin labels for right side
            pinalignleft: Vertical alignment for pins on left side
                ('center', 'top', 'bottom')
            pinalignright: Vertical alignment for pins on right side
                ('center', 'top', 'bottom')
            pinfontsizeleft: Font size for pin labels on left
            pinfontsizeright: Font size for pin labels on right
            pinspacing: Distance between pins
            edge: Distance between header edge and first pin row/column
            pinfill: Color to fill pin circles

        Anchors:
            pin[X] for each pin
    '''
    def __init__(self, *d,
                 rows: int=4, cols: int=1,
                 style: HeaderStyle='round',
                 numbering: HeaderNumbering='lr',
                 shownumber: bool=False,
                 pinsleft: Sequence[str] = None,
                 pinsright: Sequence[str] = None,
                 pinalignleft: Valign='bottom',
                 pinalignright: Valign='bottom',
                 pinfontsizeright: float=9,
                 pinfontsizeleft: float=9,
                 pinspacing: float=0.6,
                 edge: float=0.3,
                 pinfill: str='bg',
                 **kwargs):
        super().__init__(*d, **kwargs)
        if pinsleft is None:
            pinsleft = []
        if pinsright is None:
            pinsright = []
        if cols > 2:
            warnings.warn('Header numbering not supported with cols > 2')

        self.params['d'] = 'right'
        w = (cols-1) * pinspacing + edge*2
        h = (rows-1) * pinspacing + edge*2
        pinrad = .1

        self.segments.append(SegmentPoly([(0, 0), (0, h), (w, h), (w, 0)]))
        for row in range(rows):
            for col in range(cols):
                xy = (col*pinspacing+edge, h-row*pinspacing-edge)

                if style == 'square':
                    x, y = xy
                    self.segments.append(SegmentPoly([(x-pinrad, y-pinrad), (x+pinrad, y-pinrad),
                                                      (x+pinrad, y+pinrad), (x-pinrad, y+pinrad)],
                                                     fill='bg', zorder=4))
                elif style == 'screw':
                    x, y = xy
                    self.segments.append(SegmentCircle(xy, pinrad*1.75, fill=pinfill, zorder=4))
                    self.segments.append(Segment([(x+pinrad, y+pinrad), (x-pinrad, y-pinrad)], zorder=5))

                else:  # style == 'round'
                    self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))

                if numbering == 'lr' or numbering is True:
                    pnumber = str(row*cols + col + 1)
                elif numbering == 'ud':
                    pnumber = str(row + col*rows + 1)
                else:  # number == 'ccw'
                    pnumber = str(rows*col+(rows-row)) if col % 2 else str(row+1)
                self.anchors['pin{}'.format(pnumber)] = xy

                if shownumber:
                    numxy = (w+.05 if col % 2 else -.05, xy[1])
                    align = ('left' if col % 2 else 'right', 'bottom')
                    self.segments.append(SegmentText(numxy, pnumber, fontsize=pinfontsizeleft, align=align))  # type: ignore

                if pinsleft and (cols == 1 or not col % 2):
                    lblxy = (-.05, xy[1])
                    self.segments.append(SegmentText(lblxy, pinsleft[row], fontsize=pinfontsizeleft,
                                                     align=('right', pinalignleft)))

                if pinsright and (cols == 1 or col % 2):
                    lblxy = (w+.05, xy[1])
                    self.segments.append(SegmentText(lblxy, pinsright[row], fontsize=pinfontsizeright,
                                                     align=('left', pinalignright)))


class Jumper(Element):
    ''' Jumper for use on a Header element

        Set position using `at()` method with a Header
        pin location, e.g. `Jumper().at(H.in1)`

        Args:
            pinspacing: Spacing between pins
    '''
    def __init__(self, *d, pinspacing: float=0.6, **kwargs):
        super().__init__(*d, **kwargs)
        self.params['theta'] = 0
        pinrad = .1
        x = pinrad*2.5
        self.segments.append(SegmentPoly([(-x, -x), (pinspacing+x, -x),
                                         (pinspacing+x, x), (-x, x)]))


class BusConnect(Element):
    ''' Data bus connection.

        Adds the short diagonal lines that break out a bus (wide line)
        to connect to an Ic or Header element.

        Args:
            n: Number of parallel lines
            dy: Distance between parallel lines
            up: Slant up or down
            lwbus: Line width of bus line
            l: length of connection lines

        Anchors:
            * start
            * end
            * p[X] where X is int for each data line
    '''
    def __init__(self, *d, n: int=1, dy: float=0.6, up: bool=True, lwbus: float=4, l: float=3, **kwargs):
        super().__init__(*d, **kwargs)
        self.params['theta'] = 0
        dx = l
        slantx = .5
        slanty = slantx if up else -slantx

        for i in range(n):
            y = -i*dy
            self.segments.append(Segment([(0, y), (dx-slantx, y), (dx, y+slanty)]))
            self.anchors['pin{}'.format(i+1)] = (0, y)
        self.segments.append(Segment([(dx, slantx), (dx, slanty-n*dy)], lw=lwbus))
        self.params['drop'] = (dx, slantx)
        self.anchors['start'] = (dx, slantx)
        self.anchors['end'] = (dx, slantx-n*dy)


class BusLine(Line):
    ''' Data bus line. Just a wide line.

        Use BusConnect to break out connections to the BusLine.

        Args:
            lw: Line width
    '''
    def __init__(self, *d, lw: float=4, **kwargs):
        super().__init__(*d, **kwargs)
        self.params['lw'] = lw


class DB9(Element):
    ''' DB9 Connector

        Args:
            pinspacing: Distance between pins
            edge: Distance between edge and pins
            number: Draw pin numbers
            pinfill: Color to fill pin circles

        Anchors:
            * pin1 thru pin9
    '''
    def __init__(self, *d, pinspacing: float=0.6, edge: float=0.3, number: bool=False,
                 pinfill: str='bg',
                 **kwargs):
        super().__init__(*d, **kwargs)
        self.params['theta'] = 0
        w = pinspacing + edge*2
        h1 = 4 * pinspacing + edge*2
        h2 = h1 + .5
        pinrad = .1

        self.segments.append(SegmentPoly([(0, 0), (0, h1), (w, h2), (w, -.5)], cornerradius=.25))

        for i in range(4):
            xy = (edge, h1-(i+.5)*pinspacing-edge)
            self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))
            self.anchors['pin{}'.format(9-i)] = xy
            if number:
                self.segments.append(SegmentText([xy[0], xy[1]+pinrad],
                                                 str(9-i), fontsize=9,
                                                 align=('center', 'bottom')))
        for i in range(5):
            xy = (edge+pinspacing, h2-(i+.75)*pinspacing-edge)
            self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))
            self.anchors['pin{}'.format(5-i)] = xy
            if number:
                self.segments.append(SegmentText([xy[0], xy[1]+pinrad],
                                                 str(5-i), fontsize=9,
                                                 align=('center', 'bottom')))


class DB25(Element):
    ''' DB25 Connector

        Args:
            pinspacing: Distance between pins
            edge: Distance between edge and pins
            number: Draw pin numbers
            pinfill: Color to fill pin circles

        Anchors:
            * pin1 thru pin25
    '''
    def __init__(self, *d, pinspacing: float=0.6, edge: float=0.3, number: bool=False,
                 pinfill: str='bg',
                 **kwargs):
        super().__init__(*d, **kwargs)
        self.params['theta'] = 0
        w = pinspacing + edge*2
        h1 = 12 * pinspacing + edge*2
        h2 = h1 + .5
        pinrad = .1

        self.segments.append(SegmentPoly([(0, 0), (0, h1), (w, h2), (w, -.5)], cornerradius=.25))

        for i in range(12):
            xy = (edge, h1-(i+.5)*pinspacing-edge)
            self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))
            self.anchors['pin{}'.format(25-i)] = xy
            if number:
                self.segments.append(SegmentText([xy[0], xy[1]+pinrad],
                                                 str(25-i), fontsize=9,
                                                 align=('center', 'bottom')))
        for i in range(13):
            xy = (edge+pinspacing, h2-(i+.75)*pinspacing-edge)
            self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))
            self.anchors['pin{}'.format(13-i)] = xy
            if number:
                self.segments.append(SegmentText([xy[0], xy[1]+pinrad],
                                                 str(13-i), fontsize=9,
                                                 align=('center', 'bottom')))


class CoaxConnect(Element):
    ''' Coaxial connector

        Args:
            radius: Radius of outer shell
            radiusinner: Radius of inner conductor
            fillinner: Color to fill inner conductor

        Anchors:
            * center
            * N
            * S
            * E
            * W
    '''
    def __init__(self, *d, radius: float=0.4, radiusinner: float=0.12, fillinner: str='bg', **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(SegmentCircle((0, 0), radius))
        self.segments.append(SegmentCircle((0, 0), radiusinner, fill=fillinner, zorder=4))
        self.anchors['center'] = (0, 0)
        self.anchors['N'] = (0, radius)
        self.anchors['S'] = (0, -radius)
        self.anchors['E'] = (radius, 0)
        self.anchors['W'] = (-radius, 0)


class Plug(Element):
    ''' Plug (male connector) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        pluggap = 0.18
        self.segments.append(Segment([(0, 0), (1, 0), gap, (1-resheight, resheight), (1, 0),
                                      (1-resheight, -resheight)]))
        self.params['drop'] = (1+pluggap, 0)


class Jack(Element):
    ''' Jack (female connector) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (-resheight, resheight), gap,
                                      (-resheight, -resheight), (0, 0), (1, 0)]))
        self.params['drop'] = (1, 0)
