''' Lines, Arrows, and Labels '''

from __future__ import annotations
from typing import Sequence, Union
import warnings
import math

from ..segments import Segment, SegmentCircle, SegmentArc, SegmentPoly, SegmentBezier
from .elements import Element, Element2Term
from .twoterm import gap
from ..types import XY, Point, Arcdirection, BilateralDirection
from .. import util


class Line(Element2Term):
    r''' Straight Line

        Args:
            arrow: arrowhead specifier, such as '->', '<-', '<->', '-o', or '\|->'
    '''
    def __init__(self, *d, arrow: str=None, **kwargs):
        super().__init__(*d, **kwargs)
        arrowwidth = kwargs.get('arrowwidth', .15)
        arrowlength = kwargs.get('arrowlength', .25)
        self.segments.append(Segment([(0, 0)], arrow=arrow,
                                     arrowwidth=arrowwidth, arrowlength=arrowlength))


class Arrow(Line):
    ''' Arrow

        Args:
            double: Show arrowhead on both ends
            headwidth: Width of arrow head
            headlength: Length of arrow head
    '''
    def __init__(self, *d,
                 double: bool=False,
                 headwidth: float=0.15, headlength: float=0.25,
                 **kwargs):
        super().__init__(*d, arrowlength=headlength, arrowwidth=headwidth, **kwargs)
        self.double = double
        self.headlength = headlength
        self.headwidth = headwidth

        # Explicitly define center so reverses work
        self.anchors['center'] = (0, 0)

    def _place(self, dwgxy, dwgtheta, **dwgparams):
        ''' Add arrowhead to segment after it was extended '''
        result = super()._place(dwgxy, dwgtheta, **dwgparams)
        line = self.segments[0]  # The base line gets arrowheads
        reverse = self._cparams.get('reverse')
        arrow = '->' if not reverse else '<-'
        arrow = '<->' if self.double else arrow
        line.arrow = arrow
        return result


class LineDot(Line):
    ''' Line with a dot at the end

        Args:
            double: Show dot on both ends
            radius: Radius of the dot
            fill: Color to fill the dot, or `True` to fill with element color
    '''
    def __init__(self, *d, double: bool=False, radius: float=0.075,
                 fill: bool=True, **kwargs):
        super().__init__(*d, **kwargs)
        warnings.warn("LineDot is deprecated. Use Line().dot() or Line(arrow='-o')", DeprecationWarning)
        zorder = kwargs.get('zorder', 4)
        self.params['fill'] = fill
        self.segments.append(SegmentCircle(
            (0, 0), radius, ref='end', zorder=zorder))
        if double:
            self.segments.append(SegmentCircle((0, 0), radius,
                                               ref='start', zorder=zorder))
        # Explicitly define center so reverses work
        self.anchors['center'] = (0, 0)


class Gap(Element2Term):
    ''' Gap for labeling port voltages, for example. Draws nothing,
        but provides place to attach a label such as ('+', 'V', '-').
    '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), gap, (1, 0)], visible=False))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0


class Dot(Element):
    ''' Connection Dot

        Args:
            radius: Radius of dot
            open: Draw as an open circle
    '''
    def __init__(self, *d, radius: float=0.075, open: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'bg' if open else True
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)
        self.params['drop'] = (0, 0)
        self.params['theta'] = 0
        self.params['zorder'] = 4
        self.params['fill'] = fill
        self.segments.append(SegmentCircle((0, 0), radius))


class Arrowhead(Element):
    ''' Arrowhead'''
    def __init__(self, *d, headwidth: float=.15, headlength: float=.25, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([
            (-headlength, 0), (0, 0)], arrowwidth=headwidth, arrowlength=headlength, arrow='->'))
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)
        self.params['lblofst'] = .25


class DotDotDot(Element):
    ''' Ellipsis element

        Args:
            radius: Radius of dots
            open: Draw dots as open circles

        "Ellipsis" is a reserved keyword in Python used for slicing,
        thus the name DotDotDot.
    '''
    def __init__(self, *d, radius: float=0.075, open: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'bg' if open else True
        self.params['fill'] = fill
        self.segments.append(SegmentCircle((.5, 0), radius))
        self.segments.append(SegmentCircle((1, 0), radius))
        self.segments.append(SegmentCircle((1.5, 0), radius))
        self.params['drop'] = (2, 0)


class Wire(Element):
    ''' Connect the .at() and .to() positions with lines depending on shape

        Args:
            shape: Determines shape of wire:
                `-`: straight line
                `|-`: right-angle line starting vertically
                `-|`: right-angle line starting horizontally
                'z': diagonal line with horizontal end segments
                'N': diagonal line with vertical end segments
                `n`: n- or u-shaped lines
                `c`: c- or ↄ-shaped lines
            k: Distance before the wire changes directions in `n` and `c` shapes.
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o'
    '''
    def __init__(self, shape: str='-', k: float=1, arrow: str=None, **kwargs):
        super().__init__(**kwargs)
        self._userparams['shape'] = shape
        self._userparams['k'] = k
        self._userparams['arrow'] = arrow
        self._userparams.setdefault('to', (3, -2))

    def to(self, xy: XY, dx: float=0, dy: float=0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float=0, dy: float=0):
        ''' Specify ending position relative to start position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def dot(self, open: bool=False) -> 'Element':
        ''' Add a dot to the end of the element '''
        self._userparams['dot'] = True if not open else 'open'
        return self

    def idot(self, open: bool=False) -> 'Element':
        ''' Add a dot to the input/start of the element '''
        self._userparams['idot'] = True if not open else 'open'
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
        arrow = self._cparams.get('arrow', None)
        shape = self._cparams.get('shape', '-')
        k = self._cparams.get('k', 1)
        if delta is not None:
            dx, dy = delta
        else:
            dx = to[0] - xy[0]
            dy = to[1] - xy[1]

        if shape == '-':     # Straight line
            self.segments.append(Segment([(0, 0), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (dx/2, dy/2)
        elif shape == '-|':  # Right angle, horizontal first
            self.segments.append(Segment([(0, 0), (dx, 0), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (dx, dy/2)
            self.params['droptheta'] = 90 if dy > 0 else -90
        elif shape == '|-':  # Right angle, vertical first
            self.segments.append(Segment([(0, 0), (0, dy), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (dx/2, dy)
            self.params['droptheta'] = 0 if dx > 0 else 180
        elif shape in ['z', 'Z']:
            if dx > 0:
                k = abs(k)
            else:
                k = -abs(k)
            self.segments.append(Segment([(0, 0), (k, 0), (dx-k, dy), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (dx/2, dy/2)
            self.params['droptheta'] = 0 if dx > 0 else 180
        elif shape == 'N':
            if dy > 0:
                k = abs(k)
            else:
                k = -abs(k)
            self.segments.append(Segment([(0, 0), (0, k), (dx, dy-k), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (dx/2, dy/2)
            self.params['droptheta'] = 90 if dy > 0 else -90
        elif shape == 'n':   # N-shape
            self.segments.append(Segment([(0, 0), (0, k), (dx, k), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (dx/2, k)
            self.params['droptheta'] = 90 if dy > k else -90
        elif shape == 'c':   # C-shape
            self.segments.append(Segment([(0, 0), (k, 0), (k, dy), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (k, dy/2)
            self.params['droptheta'] = 0 if dx > k else 180
        else:
            raise ValueError(f'Undefined shape parameter `{shape}`.')

        if self._cparams.get('dot', False):
            fill: Union[bool, str] = 'bg' if self._cparams['dot'] == 'open' else True
            self.segments.append(SegmentCircle((dx, dy), radius=0.075, fill=fill, zorder=3))
        if self._cparams.get('idot', False):
            fill = 'bg' if self._cparams['idot'] == 'open' else True
            self.segments.append(SegmentCircle((0, 0), radius=0.075, fill=fill, zorder=3))

        self.params['lblloc'] = 'mid'
        self.params['drop'] = (dx, dy)
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((dx, dy))
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class Arc2(Element):
    ''' Arc Element

        Use `at` and `to` methods to define endpoints.

        Arc2 is a quadratic Bezier curve with control point
        halfway between the endpoints, generating a
        symmetric 'C' curve.

        Args:
            k: Control point factor. Higher k means more curvature.

        Anchors:
            start
            end
            ctrl
            mid
    '''
    def __init__(self, k=0.5, arrow=None, **kwargs):
        super().__init__(**kwargs)
        self.k = k
        self.arrow = arrow

    def to(self, xy: XY, dx: float=0, dy: float=0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float=0, dy: float=0) -> 'Element':
        ''' Specify change in position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        xy: Point = Point(self._cparams.get('at', dwgxy))
        to: Point = Point(self._cparams.get('to', Point((xy.x+3, xy.y))))
        delta = self._cparams.get('delta', None)
        if delta is not None:
            dx, dy = delta
        else:
            dx = to.x - xy.x
            dy = to.y - xy.y
        pa = Point((dx/2-dy*self.k, dy/2+dx*self.k))
        mid = Point((dx/2-dy*self.k/2, dy/2+dx*self.k/2))
        self.segments.append(SegmentBezier(
            (Point((0, 0)), pa, Point((dx, dy))), arrow=self.arrow))

        self.anchors['ctrl'] = pa
        self.anchors['mid'] = mid
        self.params['theta'] = 0
        self.params['lblloc'] = 'mid'
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((dx, dy))
        self.params['drop'] = Point((dx, dy))
        valign = 'bottom'
        halign = 'left'
        vofst = 0.1
        if math.isclose(mid.y, pa.y, abs_tol=.01):
            valign = 'center'
            vofst = 0
        elif mid.y > pa.y:
            valign = 'top'
            vofst = -0.1
        if math.isclose(mid.x, pa.x, abs_tol=.01):
            halign = 'center'
        elif mid.x > pa.x:
            halign = 'right'
        self.params['lblofst'] = vofst
        self.params['lblalign'] = (halign, valign)
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class Arc3(Element):
    ''' Arc Element

        Use `at` and `to` methods to define endpoints.

        Arc3 is a cubic Bezier curve. Control points are set
        to extend the curve at the given angle for each endpoint.

        Args:
            k: Control point factor. Higher k means tighter curve.
            th1: Angle at which the arc leaves start point
            th2: Angle at which the arc leaves end point
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o'
            arrowlength: Length of arrowhead
            arrowwidth: Width of arrowhead

        Anchors:
            start
            end
            center
            ctrl1
            ctrl2
    '''
    def __init__(self, k=0.75, th1=0, th2=180, arrow=None,
                 arrowlength=.25, arrowwidth=.2, **kwargs):
        super().__init__(**kwargs)
        self._userparams.setdefault('to', Point((1, 0)))
        self.k = k
        self.th1 = math.radians(th1)
        self.th2 = math.radians(th2)
        self.arrow = arrow
        self.arrowlength = arrowlength
        self.arrowwidth = arrowwidth

    def to(self, xy: XY, dx: float=0, dy: float=0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float=0, dy: float=0) -> 'Element':
        ''' Specify change in position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        self.params['theta'] = 0
        xy: Point = Point(self._cparams.get('at', dwgxy))
        to: Point = Point(self._cparams.get('to', dwgxy))
        delta = self._cparams.get('delta', None)
        if delta is not None:
            dx, dy = delta
        else:
            dx = to.x - xy.x
            dy = to.y - xy.y
        pa1 = Point((dx*self.k*math.cos(self.th1),
                     dy*self.k*math.sin(self.th1)))
        pa2 = Point((dx+dx*self.k*math.cos(self.th2),
                     dy+dy*self.k*math.sin(self.th2)))
        self.segments.append(SegmentBezier((Point((0, 0)), pa1, pa2, Point((dx, dy))),
                                           arrow=self.arrow,
                                           arrowlength=self.arrowlength,
                                           arrowwidth=self.arrowwidth))
        self.anchors['center'] = Point((dx/2, dy/2))
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((dx, dy))
        self.anchors['ctrl1'] = pa1
        self.anchors['ctrl2'] = pa2
        self.params['drop'] = Point((dx, dy))
        self._setlabel(dx, dy)
        return super()._place(dwgxy, dwgtheta, **dwgparams)

    def _setlabel(self, dx, dy):
        ''' Set label position/alignment '''
        # This sets reasonable label position along center of arc.
        self.params['lblloc'] = 'center'
        halign = 'left'
        valign = 'bottom'
        if dy > 0:
            valign = 'top'
            self.params['lblofst'] = -0.1
        if dx <= 0:
            halign = 'right'
        self.params['lblalign'] = (halign, valign)


class Annotate(Arc3):
    ''' Draw a curved arrow pointing to `at` position, ending at `to`
        position, with label location at the tail of the arrow
        (See also `Arc3`).

        Args:
            k: Control point factor. Higher k means tighter curve.
            th1: Angle at which the arc leaves start point
            th2: Angle at which the arc leaves end point
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o'
            arrowlength: Length of arrowhead
            arrowwidth: Width of arrowhead
    '''
    def __init__(self, k=0.75, th1=75, th2=180, arrow='<-',
                 arrowlength=.25, arrowwidth=.2, **kwargs):
        super().__init__(k=k, th1=th1, th2=th2, arrow=arrow,
                         arrowlength=arrowlength, arrowwidth=arrowwidth)
        self._userparams['to'] = Point((1, 1))

    def _setlabel(self, dx, dy):
        ''' Set label position/alignment '''
        # Attempt to align the label at the tail of the arrow.
        self.params['lblloc'] = 'end'
        p1, p2 = self.anchors['ctrl2'], self.anchors['end']
        if p1 == p2:
            th2 = -90 if dy < 0 else 90
        else:
            th2 = math.degrees(math.atan2(p2.y-p1.y, p2.x-p1.x))
        while th2 < 0:
            th2 += 360

        if th2 < 45 or th2 > 315:
            self.params['lblalign'] = ('left', 'center')
            self.params['lblofst'] = (.1, 0)
        elif 45 <= th2 <= 135:
            self.params['lblalign'] = ('center', 'bottom')
            self.params['lblofst'] = (0, .1)
        elif 135 < th2 <= 225:
            self.params['lblalign'] = ('right', 'center')
            self.params['lblofst'] = (-.1, 0)
        else:
            self.params['lblalign'] = ('center', 'top')
            self.params['lblofst'] = (0, -.1)


class ArcZ(Arc3):
    ''' Z-Curve Arc

        Use `at` and `to` methods to define endpoints.

        ArcZ approaches the endpoints horizontally, leading to
        a 'Z' shaped curve

        Args:
            k: Control point factor. Higher k means tighter curve.
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o'            arrowlength: Length of arrowhead
            arrowwidth: Width of arrowhead
    '''
    def __init__(self, k=0.75, arrow=None, arrowlength=.25, arrowwidth=.2, **kwargs):
        super().__init__(k=k, arrow=arrow, th1=0, th2=180, arrowlength=arrowlength, arrowwidth=arrowwidth, **kwargs)


class ArcN(Arc3):
    ''' N-Curve Arc

        Use `at` and `to` methods to define endpoints.

        ArcN approaches the endpoints vertically, leading to
        a 'N' shaped curve

        Args:
            k: Control point factor. Higher k means tighter curve.
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o'            arrowlength: Length of arrowhead
            arrowwidth: Width of arrowhead
    '''
    def __init__(self, k=0.75, arrow=None, arrowlength=.25, arrowwidth=.2, **kwargs):
        super().__init__(k=k, arrow=arrow, th1=90, th2=-90, arrowlength=arrowlength, arrowwidth=arrowwidth, **kwargs)


class ArcLoop(Element):
    ''' Loop Arc

        Use `at` and `to` methods to define endpoints.

        ArcLoop is an arc drawn as part of a circle.

        Args:
            radius: Radius of the arc
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o'            arrowlength: Length of arrowhead
            arrowwidth: Width of arrowhead

        Anchors:
            start
            end
            mid
            BL
            BR
            TL
            TR
    '''
    def __init__(self, radius: float=0.6, arrow: str=None, arrowlength=.25, arrowwidth=.2, **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.arrow = arrow
        self.arrowlength = arrowlength
        self.arrowwidth = arrowwidth

    def to(self, xy: XY, dx: float=0, dy: float=0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float=0, dy: float=0):
        ''' Specify ending position relative to start position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        self.params['theta'] = 0
        xy: Point = Point(self._cparams.get('at', dwgxy))
        to: Point = Point(self._cparams.get('to', dwgxy))
        delta = self._cparams.get('delta', None)
        if delta is not None:
            dx, dy = delta
        else:
            dx = to.x - xy.x
            dy = to.y - xy.y

        xa = dx/2
        ya = dy/2
        q = math.sqrt(dx**2 + dy**2)
        try:
            center = Point(((xa + math.sqrt(self.radius**2 - (q/2)**2) * (-dy/q)),
                            (ya + math.sqrt(self.radius**2 - (q/2)**2) * (dx/q))))
        except ValueError as err:
            raise ValueError(f'No solution to ArcLoop with radius {self.radius}') from err

        da = math.sqrt(xa**2 + ya**2)
        thetaa = math.atan2(ya, xa)
        thda = math.acos(da/self.radius)
        theta1 = thetaa - thda
        theta2 = thetaa + thda
        t = util.linspace(math.pi+theta2, theta1)
        x = [center.x + self.radius * math.cos(ti) for ti in t]
        y = [center.y + self.radius * math.sin(ti) for ti in t]
        self.segments.append(Segment(list(zip(x, y)), arrow=self.arrow,
                                     arrowlength=self.arrowlength,
                                     arrowwidth=self.arrowwidth))
        mid = len(x)//2
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((x[-1], y[-1]))
        self.anchors['mid'] = Point((x[mid], y[mid]))
        self.anchors['BL'] = Point((min(x), min(y)))
        self.anchors['BR'] = Point((max(x), min(y)))
        self.anchors['TL'] = Point((min(x), max(y)))
        self.anchors['TR'] = Point((max(x), max(y)))
        self.params['lblloc'] = 'mid'
        self.params['drop'] = to
        valign = 'bottom'
        halign = 'left'
        if y[mid] < y[0]:
            valign = 'top'
            self.params['lblofst'] = -.1
        if x[mid] < x[0] and x[mid] < x[-1]:
            halign = 'right'
        self.params['lblalign'] = (halign, valign)
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class Label(Element):
    ''' Label element.

        For more options, use `Label().label()` method.

        Args:
            label: text to display.
    '''
    def __init__(self, *d, label: str=None, **kwargs):
        super().__init__(*d, **kwargs)
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        if label:
            self.label(label)


class Tag(Element):
    ''' Tag/flag element for labeling signal names.

        Because text size is unknown until drawn, must specify width
        manually to fit a given text label.

        Args:
            width: Width of the tag
            height: Height of the tag
    '''
    def __init__(self, *d, width: float=1.5, height: float=0.625, **kwargs):
        super().__init__(*d, **kwargs)
        height = height / 2
        self.segments.append(SegmentPoly([(0, 0),
                                          (height, height),
                                          (width, height),
                                          (width, -height),
                                          (height, -height)]))
        self.params['lblloc'] = 'center'
        self.params['fontsize'] = 12
        self.params['lblofst'] = 0
        self.anchors['start'] = (0, 0)


class CurrentLabel(Element):
    ''' Current label arrow drawn above an element

        Use `.at()` method to place the label over an
        existing element.

        Args:
            ofst: Offset distance from centerline of element
            length: Length of the arrow
            top: Draw arrow on top or bottom of element
            reverse: Reverse the arrow direction
    '''
    def __init__(self, ofst: float=0.4, length: float=2,
                 top: bool=True, reverse: bool=False, **kwargs):
        super().__init__(**kwargs)
        self.params['lblofst'] = -.1
        self.params['drop'] = None
        self.anchor('center')
        self.anchors['center'] = (0, 0)
        self._ofst = ofst
        self._length = length
        self._top = top
        self._reverse = reverse

    def at(self, xy: XY | Element) -> 'Element':  # type: ignore[override]
        ''' Specify CurrentLabel position.

            If xy is an Element, arrow will be centered
            along element and its color will also be
            inherited.

            Args:
                xy: The absolute (x, y) position or an
                Element instance to center the arrow over
        '''
        if isinstance(xy, Element):
            try:
                pos = xy.center
            except AttributeError:
                bbox = xy.get_bbox()
                pos = Point(((bbox.xmax + bbox.xmin)/2, (bbox.ymax + bbox.ymin)/2))
            super().at(pos)

            theta = xy.transform.theta
            if (theta % 360) > 90 and (theta % 360) <= 270:
                theta += 180  # Keeps 'top=True' labels above the element
            self.theta(theta)
            if 'color' in xy._userparams:
                self.color(xy._userparams.get('color'))
        else:
            super().at(xy)
        return self

    def _place(self, dwgxy, dwgtheta, **dwgparams):
        if not self._top:
            self._ofst = -self._ofst
            self.params['lblloc'] = 'bot'
        a, b = (-self._length/2, self._ofst), (self._length/2, self._ofst)

        if self._reverse:
            a, b = b, a

        self.segments.append(Segment((a, b), arrow='->', arrowwidth=.2, arrowlength=.3))
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class CurrentLabelInline(Element):
    ''' Current direction arrow, inline with element.

        Use `.at()` method to place arrow on an Element instance

        Args:
            direction: arrow direction 'in' or 'out' of element
            ofst: Offset along lead length
            start: Arrow at start or end of element
            headlength: Length of arrowhead
            headwidth: Width of arrowhead
    '''
    def __init__(self,
                 direction: BilateralDirection='in',
                 ofst: float=0.8, start: bool=True,
                 headlength: float=0.3, headwidth: float=0.3, **kwargs):
        super().__init__(**kwargs)
        self.params['lblofst'] = 0
        self.params['drop'] = None
        self.params['zorder'] = 4

        x = ofst
        dx = headlength
        if direction == 'in':
            x += headlength
            dx = -dx

        if start:
            x = -x
            dx = -dx

        self.segments.append(Segment(((x, 0), (x+dx, 0)), arrow='->',
                                     arrowwidth=headwidth, arrowlength=headlength))

    def at(self, xy: XY | Element) -> 'Element':  # type: ignore[override]
        ''' Specify CurrentLabelInline position.

            If xy is an Element, arrow will be placed
            along the element's leads and the arrow color will
            be inherited.

            Args:
                xy: The absolute (x, y) position or an
                Element instance to place the arrow on
        '''
        if isinstance(xy, Element):
            super().at(xy.center)
            self.theta(xy.transform.theta)
            if 'color' in xy._userparams:
                self.color(xy._userparams.get('color'))
        else:
            super().at(xy)
        return self


class ZLabel(Element):
    ''' Right-angle arrow, often used to indicate impedance
        looking in to a node

        Use `.at()` method to place the label over an
        existing element.

        Args:
            ofst: Vertical offset from centerline of element
            hofst: Horizontal offset from center of element
            length: Length of the arrow tail
            lengthtip: Length of the arrow tip
            headlength: Arrowhead length
            headwidth: Arrowhead width
    '''
    def __init__(self, ofst: float=0.5, hofst: float=0.4,
                 length: float=1, lengthtip: float=.5,
                 headlength: float=0.25, headwidth: float=0.15, **kwargs):
        super().__init__(**kwargs)
        self.params['drop'] = None
        self.anchor('center')
        self.anchors['center'] = (0, 0)
        self._ofst = ofst
        self._hofst = hofst
        self._length = length
        self._lengthtip = lengthtip
        self._headlength = headlength
        self._headwidth = headwidth

    def at(self, xy: XY | Element) -> 'Element':  # type: ignore[override]
        ''' Specify CurrentLabel position.

            If xy is an Element, arrow will be centered
            along element and its color will also be
            inherited.

            Args:
                xy: The absolute (x, y) position or an
                Element instance to center the arrow over
        '''
        if isinstance(xy, Element):
            try:
                pos = xy.center
            except AttributeError:
                bbox = xy.get_bbox()
                pos = Point(((bbox.xmax + bbox.xmin)/2, (bbox.ymax + bbox.ymin)/2))
            
            super().at(pos)

            theta = xy.transform.theta
            if (theta % 360) > 90 and (theta % 360) <= 270:
                theta += 180  # Keeps 'top=True' labels above the element
            self.theta(theta)
            if 'color' in xy._userparams:
                self.color(xy._userparams.get('color'))
        else:
            super().at(xy)
        return self

    def _place(self, dwgxy, dwgtheta, **dwgparams):
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        a = Point((-self._hofst, self._ofst))
        b = Point((-self._hofst-self._lengthtip, self._ofst))
        c = Point((-self._hofst-self._lengthtip, self._ofst-self._length))
        self.anchors['head'] = a
        self.anchors['tail'] = c

        self.segments.append(Segment((c, b, a), arrow='->',
                                     arrowwidth=self._headwidth,
                                     arrowlength=self._headlength))
        
        # Attempt to align the label at the tail of the arrow.
        self.params['lblloc'] = 'tail'
        th = self._cparams.get('theta', 0)
        if self._cparams.get('flip'):
            th += 180

        th -= 90  # Because arrow is at right angle
        th = (th+360)%360

        if th < 45 or th > 315:
            self.params['lblalign'] = ('left', 'center')
            self.params['lblofst'] = (0, -.1)
        elif 45 <= th <= 135:
            self.params['lblalign'] = ('center', 'bottom')
            self.params['lblofst'] = (0, .1)
        elif 135 < th <= 225:
            self.params['lblalign'] = ('right', 'center')
            self.params['lblofst'] = (0, .1)
        else:
            self.params['lblalign'] = ('center', 'top')
            self.params['lblofst'] = (0, -.1)

        self._cparams = None  # Clear it out to pick up flip, rotate, etc.
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class LoopArrow(Element):
    ''' Loop arrow, for mesh analysis notation

        Args:
            direction: loop direction 'cw' or 'ccw'
            theta1: Angle of start of loop arrow
            theta2: Angle of end of loop arrow
            width: Width of loop
            height: Height of loop
    '''
    def __init__(self, direction: Arcdirection='cw',
                 theta1: float=35, theta2: float=-35,
                 width: float=1.0, height: float=1.0, **kwargs):
        super().__init__(**kwargs)

        self.segments.append(SegmentArc(
            (0, 0), arrow=direction, theta1=theta1, theta2=theta2,
            width=width, height=height))

        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = 0
        self.anchors['center'] = (0, 0)


class LoopCurrent(LoopArrow):
    ''' Loop current label, for mesh analysis notation,
        placed within a box of 4 existing elements.

        Args:
            elm_list: List of 4 elements surrounding loop, in
                      order (top, right, bottom, left)
            direction: loop direction 'cw' or 'ccw'
            theta1: Angle of start of loop arrow
            theta2: Angle of end of loop arrow
            pad: Distance from elements to loop
    '''
    def __init__(self, elm_list: Sequence[Element]=None,
                 direction: Arcdirection='cw',
                 theta1: float=35, theta2: float=-35,
                 pad: float=0.2, **kwargs):
        assert elm_list is not None
        bbox1 = elm_list[0].get_bbox(transform=True, includetext=False)
        bbox2 = elm_list[1].get_bbox(transform=True, includetext=False)
        bbox3 = elm_list[2].get_bbox(transform=True, includetext=False)
        bbox4 = elm_list[3].get_bbox(transform=True, includetext=False)
        top = bbox1.ymin - pad
        bot = bbox3.ymax + pad
        left = bbox4.xmax + pad
        rght = bbox2.xmin - pad
        center = ((left+rght)/2, (top+bot)/2)
        width = rght - left
        height = top - bot
        super().__init__(direction, theta1, theta2, width, height, **kwargs)
        self._userparams['at'] = center


class Rect(Element):
    ''' Rectangle Element

        Used mainly for buliding more complex elements. Corner
        arguments are relative to Element coordinates, not Drawing
        coordinates.

        Args:
            corner1: Position of top-left corner
            corner2: Position of bottom-right corner
    '''
    def __init__(self, *d, corner1: XY=(0, 0), corner2: XY=(1, 1), **kwargs):
        super().__init__(*d, **kwargs)
        c1a = (corner1[0], corner2[1])
        c2a = (corner2[0], corner1[1])
        self.segments.append(Segment([corner1, c1a, corner2, c2a, corner1], zorder=0))
        self.params['zorder'] = 0   # Put on bottom


class Encircle(Element):
    ''' Draw ellipse around all elements in the list

        Args:
            elm_list: List of elements to enclose
            padx: Horizontal distance from elements to loop
            pady: Vertical distance from elements to loop
            includelabels: Include labesl in the ellipse
    '''
    def __init__(self, elm_list: Sequence[Element]=None,
                 padx: float=0.2, pady: float=0.2,
                 includelabels: bool=True,
                 **kwargs):
        super().__init__(**kwargs)
        assert elm_list is not None
        xmin = math.inf
        xmax = -math.inf
        ymin = math.inf
        ymax = -math.inf
        for element in elm_list:
            bbox = element.get_bbox(transform=True, includetext=includelabels)
            xmin = min(xmin, bbox.xmin)
            xmax = max(xmax, bbox.xmax)
            ymin = min(ymin, bbox.ymin)
            ymax = max(ymax, bbox.ymax)
        xmin -= padx
        xmax += padx
        ymin -= pady
        ymax += pady
        center = (xmax+xmin)/2, (ymax+ymin)/2
        w = xmax-xmin
        h = ymax-ymin
        self._userparams['at'] = center
        self.segments.append(SegmentArc((0, 0), w, h, theta1=0, theta2=360))
        sinpi4 = math.sin(math.pi/4)
        cospi4 = math.cos(math.pi/4)
        sinpi8 = math.sin(math.pi/8)
        cospi8 = math.cos(math.pi/8)
        self.anchors['N'] = (0, h/2)
        self.anchors['S'] = (0, -h/2)
        self.anchors['E'] = (w/2, 0)
        self.anchors['W'] = (-w/2, 0)
        self.anchors['SE'] = (w/2*cospi4, -h/2*sinpi4)
        self.anchors['SW'] = (-w/2*cospi4, -h/2*sinpi4)
        self.anchors['NW'] = (-w/2*cospi4, h/2*sinpi4)
        self.anchors['NE'] = (w/2*cospi4, h/2*sinpi4)
        self.anchors['ENE'] = (w/2*cospi8, h/2*sinpi8)
        self.anchors['WNW'] = (-w/2*cospi8, h/2*sinpi8)
        self.anchors['ESE'] = (w/2*cospi8, -h/2*sinpi8)
        self.anchors['WSW'] = (-w/2*cospi8, -h/2*sinpi8)
        self.anchors['NNE'] = (w/2*sinpi8, h/2*cospi8)
        self.anchors['NNW'] = (-w/2*sinpi8, h/2*cospi8)
        self.anchors['SSE'] = (w/2*sinpi8, -h/2*cospi8)
        self.anchors['SSW'] = (-w/2*sinpi8, -h/2*cospi8)
        self.params['theta'] = 0


class EncircleBox(Element):
    ''' Draw rounded box around all elements in the list

        Args:
            elm_list: List elements to enclose
            cornerraidus: radius of corner rounding
            padx: Horizontal distance from elements to loop
            pady: Vertical distance from elements to loop
            includelabels: Include labels in the box
    '''
    def __init__(self, elm_list: Sequence[Element]=None,
                 cornerradius: float=0.3,
                 padx: float=0.2, pady: float=0.2,
                 includelabels: bool=True,
                 **kwargs):
        super().__init__(**kwargs)
        assert elm_list is not None
        xmin = math.inf
        xmax = -math.inf
        ymin = math.inf
        ymax = -math.inf
        for element in elm_list:
            bbox = element.get_bbox(transform=True, includetext=includelabels)
            xmin = min(xmin, bbox.xmin)
            xmax = max(xmax, bbox.xmax)
            ymin = min(ymin, bbox.ymin)
            ymax = max(ymax, bbox.ymax)
        xmin -= padx
        xmax += padx
        ymin -= pady
        ymax += pady
        center = (xmax+xmin)/2, (ymax+ymin)/2
        w = xmax-xmin
        h = ymax-ymin
        self._userparams['at'] = center
        self.segments = [SegmentPoly(
            [(-w/2, h/2), (w/2, h/2), (w/2, -h/2), (-w/2, -h/2)],
            cornerradius=cornerradius)]
        k = cornerradius - cornerradius*math.sqrt(2)/2
        self.anchors['NE'] = (w/2-k, h/2-k)
        self.anchors['NW'] = (-w/2+k, h/2-k)
        self.anchors['SE'] = (w/2-k, -h/2+k)
        self.anchors['SW'] = (-w/2+k, -h/2+k)
        self.anchors['N'] = (0, h/2)
        self.anchors['S'] = (0, -h/2)
        self.anchors['E'] = (w/2, 0)
        self.anchors['W'] = (-w/2, 0)
        self.params['theta'] = 0
