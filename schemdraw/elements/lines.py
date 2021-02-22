''' Lines, Arrows, and Labels '''

from __future__ import annotations
from typing import Literal, Sequence
import math

from ..segments import Segment, SegmentArrow, SegmentCircle, SegmentArc, SegmentPoly
from .elements import Element, Element2Term
from .twoterm import gap
from ..types import XY, Point


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
        self.segments.append(SegmentArrow((-headlength, 0), (0, 0),
                                          ref='end',
                                          headwidth=headwidth,
                                          headlength=headlength))
        if self.double:
            self.segments.append(SegmentArrow((headlength, 0), (0, 0),
                                              ref='start',
                                              headwidth=headwidth,
                                              headlength=headlength))
        # Explicitly define center so reverses work
        self.anchors['center'] = (0, 0)
        
    def _place(self, xy, theta, **dwgparams):
        ''' Shorten the underlying line so it doesn't stick out
            from arrowhead
        '''
        result = super()._place(xy, theta, **dwgparams)
        line = self.segments[0]  # The base line which needs to be shortened
        xy1 = line.path[0]
        xy2 = line.path[-1]
        dx = xy2[0] - xy1[0]
        dy = xy2[1] - xy1[1]
        theta = math.atan2(dy, dx)
        newhead = xy2
        newtail = xy1
        reverse = self._cparams.get('reverse')

        if reverse or self.double:
            newtail = (xy1[0] + self.headlength * math.cos(theta),
                       xy1[1] + self.headlength * math.sin(theta))
        
        if (not reverse) or self.double:
            newhead = (xy2[0] - self.headlength * math.cos(theta),
                       xy2[1] - self.headlength * math.sin(theta))
            
        line.path[0] = newtail
        line.path[-1] = newhead
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
        self.segments.append(SegmentArrow(
            (-.3, 0), (0, 0), headwidth=headwidth, headlength=headlength))
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

        self.segments.append(SegmentArrow(
            a, b, headwidth=.2, headlength=.3))

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
                 direction: Literal['in', 'out']='in',
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

        self.segments.append(SegmentArrow(
            (x, 0), (x+dx, 0), headwidth=headwidth, headlength=headlength))

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


class LoopCurrent(Element):
    ''' Loop current label, for mesh analysis notation

        Args:
            elm_list: List of 4 elements surrounding loop, in
                      order (top, right, bottom, left)
            direction: loop direction 'cw' or 'ccw'
            theta1: Angle of start of loop arrow
            theta2: Angle of end of loop arrow
            width: Width of loop
            height: Height of loop
    '''
    def __init__(self, elm_list: Sequence[Element]=None,
                 direction: Literal['cw', 'ccw']='cw',
                 theta1: float=35, theta2: float=-35,
                 pad: float=0.2, **kwargs):
        super().__init__(**kwargs)
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

        self.segments.append(SegmentArc(
            (0, 0), arrow=direction, theta1=theta1, theta2=theta2,
            width=width, height=height))

        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = 0
        self.anchors['center'] = (0, 0)
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
