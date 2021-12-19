''' Lines, Arrows, and Labels '''

from __future__ import annotations
from typing import Sequence
import math

from ..segments import Segment, SegmentCircle, SegmentArc, SegmentPoly, SegmentBezier
from .elements import Element, Element2Term
from .twoterm import gap
from ..types import XY, Point, Arcdirection, BilateralDirection
from .. import util


class Line(Element2Term):
    ''' Straight Line '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0)]))


class Arrow(Line):
    ''' Arrow

        Args:
            double: Show arrowhead on both ends
            headwidth: Width of arrow head
            headlength: Length of arrow head
    '''
    def __init__(self, *d,
                 double: bool=False,
                 headwidth: float=0.2, headlength: float=0.25,
                 **kwargs):
        super().__init__(*d, **kwargs)
        self.double = double
        self.headlength = headlength
        self.headwidth = headwidth

        # Explicitly define center so reverses work
        self.anchors['center'] = (0, 0)

    def _place(self, xy, theta, **dwgparams):
        ''' Add arrowhead to segment after it was extended '''
        result = super()._place(xy, theta, **dwgparams)
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
        self.segments.append(Segment([(0, 0), gap, (1, 0)]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate element placement, adding lead extensions '''
        result = super()._place(dwgxy, dwgtheta, **dwgparams)
        self.segments = self.segments[1:]  # Remove line segment, but keep any text
        return result


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
    def __init__(self, *d, headwidth: float=.15, headlength: float=.2, **kwargs):
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

    def to(self, xy: XY) -> 'Element':
        ''' Specify ending position '''
        self._userparams['to'] = xy
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        self.params['lblloc'] = 'center'
        self.params['theta'] = 0
        xy: XY = Point(self._cparams.get('at', dwgxy))
        to: XY = Point(self._cparams.get('to', Point((xy.x+3, xy.y))))
        dx = to.x - xy.x
        dy = to.y - xy.y
        pa = Point((dx/2-dy*self.k, dy/2+dx*self.k))
        mid = Point((dx/2-dy*self.k/2, dy/2+dx*self.k/2))
        self.segments.append(SegmentBezier((Point((0, 0)), pa, Point((dx, dy))),
                                          arrow=self.arrow),)

        self.anchors['ctrl'] = pa
        self.anchors['mid'] = mid
        self.params['lblloc'] = 'mid'
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((dx, dy))
        self.params['drop'] = Point((dx, dy))
        valign = 'bottom'
        halign = 'left'
        hofst = 0.1
        vofst = 0.1
        if math.isclose(mid.y, pa.y, abs_tol=.01):
            valign = 'center'
            vofst = 0
        elif mid.y > pa.y:
            valign = 'top'
            vofst = -0.1
        if math.isclose(mid.x, pa.x, abs_tol=.01):
            halign = 'center'
            hofst = 0
        elif mid.x > pa.x:
            halign = 'right'
            hofst = -0.1
        self.params['lblofst'] = (hofst, vofst)
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
            arrow: arrowhead specifier, such as '->', '<-', or '<->'
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

    def to(self, xy: XY) -> 'Element':
        ''' Specify ending position '''
        self._userparams['to'] = xy
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        self.params['theta'] = 0
        xy: XY = Point(self._cparams.get('at', dwgxy))
        to: XY = Point(self._cparams.get('to', dwgxy))
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

        # This sets reasonable label positions for ArcZ and ArcS modes.
        # Other Arc3 maybe not.
        self.anchors['center'] = Point((dx/2, dy/2))
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((dx, dy))
        self.anchors['ctrl1'] = pa1
        self.anchors['ctrl2'] = pa2
        self.params['lblloc'] = 'center'
        self.params['drop'] = Point((dx, dy))
        halign = 'left'
        valign = 'bottom'
        if dy > 0:
            valign = 'top'
            self.params['lblofst'] = -0.1
        if dx <=0:
            halign = 'right'
        self.params['lblalign'] = (halign, valign)
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class ArcZ(Arc3):
    ''' Z-Curve Arc

        Use `at` and `to` methods to define endpoints.

        ArcZ approaches the endpoints horizontally, leading to
        a 'Z' shaped curve

        Args:
            k: Control point factor. Higher k means tighter curve.
            arrow: arrowhead specifier, such as '->', '<-', or '<->'
            arrowlength: Length of arrowhead
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
            arrow: arrowhead specifier, such as '->', '<-', or '<->'
            arrowlength: Length of arrowhead
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
            arrow: arrowhead specifier, such as '->', '<-', or '<->'
            arrowlength: Length of arrowhead
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

    def to(self, xy: XY) -> 'Element':
        ''' Specify ending position '''
        self._userparams['to'] = xy
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate placement of Element '''
        self._dwgparams = dwgparams
        if not self._cparams:
            self._buildparams()

        self.params['theta'] = 0
        xy: XY = Point(self._cparams.get('at', dwgxy))
        to: XY = Point(self._cparams.get('to', dwgxy))

        dx = to.x - xy.x
        dy = to.y - xy.y

        xa = dx/2
        ya = dy/2
        q = math.sqrt(dx**2 + dy**2)
        try:
            center = Point(((xa + math.sqrt(self.radius**2 - (q/2)**2) * (-dy/q)),
                            (ya + math.sqrt(self.radius**2 - (q/2)**2) * (dx/q))))
        except ValueError:
            raise ValueError(f'No solution to ArcLoop with radius {self.radius}')

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
            ofst: Offset distance from element
            length: Length of the arrow
            top: Draw arrow on top or bottom of element
            reverse: Reverse the arrow direction
    '''
    def __init__(self, ofst: float=0.4, length: float=2,
                 top: bool=True, reverse: bool=False, **kwargs):
        super().__init__(**kwargs)
        self.params['lblofst'] = .1
        self.params['drop'] = None  # None means don't move xy
        self.anchor('center')
        self.anchors['center'] = (0, 0)

        if not top:
            ofst = -ofst
            self.params['lblloc'] = 'bot'
        a, b = (-length/2, ofst), (length/2, ofst)

        if reverse:
            a, b = b, a

        self.segments.append(Segment((a, b), arrow='->', arrowwidth=.2, arrowlength=.3))

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
            super().at(xy.center)
            self.theta(xy.transform.theta)
            if 'color' in xy._userparams:
                self.color(xy._userparams.get('color'))
        else:
            super().at(xy)
        return self


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
        self.params['lblofst'] = .25
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
