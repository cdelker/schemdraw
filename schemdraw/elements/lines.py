''' Lines, Arrows, and Labels '''

from ..segments import Segment, SegmentArrow, SegmentCircle, SegmentArc, SegmentPoly
from .elements import Element
from .twoterm import Element2Term, gap, resheight
from ..adddocs import adddocs


class Line(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0]]))


@adddocs(Element2Term)
class Arrow(Line):
    ''' Arrow element

        Parameters
        ----------
        double : bool
            Show arrowhead on both ends
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([-.3, 0], [0, 0], ref='end'))
        if kwargs.get('double', False):
            self.segments.append(SegmentArrow([0, 0], [-.3, 0], ref='start'))
        self.anchors['center'] = [0, 0]  # Explicitly define center so reverses work


@adddocs(Element2Term)
class LineDot(Line):
    ''' Line with a dot at the end

        Parameters
        ----------
        double : bool
            Show dot on both ends
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        radius = kwargs.get('radius', 0.075)
        fill = None if kwargs.get('open', False) else kwargs.get('fill', True)
        zorder = kwargs.get('zorder', 4)
        self.segments.append(SegmentCircle(
            [0, 0], radius, ref='end', fill=fill, zorder=zorder))
        if kwargs.get('double', False):
            self.segments.append(SegmentCircle(
                [0, 0], radius, ref='start'))
        self.anchors['center'] = [0, 0]  # Explicitly define center so reverses work


class Gap(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        color = self.userparams.get('color', 'white')
        self.segments.append(Segment([[0, 0], gap, [1, 0]], color=color))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['zorder'] = 0


class Dot(Element):
    ''' Connection Dot

        Parameters
        ----------
        radius : float
            Radius of dot

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        radius = kwargs.pop('radius', 0.075)
        fill = 'white' if kwargs.get('open', False) else kwargs.get('fill', True)
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]
        self.params['drop'] = [0, 0]
        self.params['theta'] = 0
        self.params['zorder'] = 4
        self.segments.append(SegmentCircle([0, 0], radius, fill=fill))


class Arrowhead(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow(
            [-.3, 0], [0, 0], headwidth=.3, headlength=.3))
        self.theta = 0
        self.anchors['start'] = [0, 0]
        self.anchors['center'] = [0, 0]
        self.anchors['end'] = [0, 0]
        self.params['lblofst'] = .25


@adddocs(Element)
class DotDotDot(Element):
    ''' Ellipsis element

        Parameters
        ----------
        radius : float
            Radius of dots
        open : bool
            Draw open dots

        Note
        ----
        "Ellipsis" is a reserved keyword in Python used for slicing, thus
        the name DotDotDot.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        radius = kwargs.pop('radius', .075)
        fill = None if kwargs.get('open', False) else kwargs.get('fill', True)
        self.segments.append(SegmentCircle([.5, 0], radius, fill=fill))
        self.segments.append(SegmentCircle([1, 0], radius, fill=fill))
        self.segments.append(SegmentCircle([1.5, 0], radius, fill=fill))
        self.params['drop'] = [2, 0]
        

class Label(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0


@adddocs(Element)
class Tag(Element):
    ''' Tag/flag element for labeling signal names.
        Because text size is unknown until drawn, must specify width manually.

        Parameters
        ----------
        width : float
            Width of the tag    
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        width = kwargs.get('width', 1.5)
        h = resheight * 1.25
        self.segments.append(SegmentPoly([[0, 0], [h, h], [width, h],
                                          [width, -h], [h, -h]]))
        self.params['lblloc'] = 'center'
        self.params['fontsize'] = 12
        self.params['lblofst'] = 0
        self.anchors['start'] = [0, 0]


@adddocs(Element)
class CurrentLabel(Element):
    ''' Current label arrow drawn above an element

        Parameters
        ----------
        ofst : float
            Offset distance from element
        length : float
            Length of the arrow
        top : bool
            Draw arrow on top or bottom of element
        rev : bool
            Reverse the arrow direction
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ofst = kwargs.get('ofst', 0.4)
        length = kwargs.get('length', 2)
        top = kwargs.get('top', True)
        reverse = kwargs.get('rev', False)
        self.params['lblofst'] = .1
        self.params['drop'] = None  # None means don't move xy from previous element
        self.anchor = 'center'
        self.anchors['center'] = [0, 0]

        if not top:
            ofst = -ofst
            self.params['lblloc'] = 'bot'
        a, b = [-length/2, ofst], [length/2, ofst]

        if reverse:
            a, b = b, a

        self.segments.append(SegmentArrow(
            a, b, headwidth=.2, headlength=.3))


@adddocs(Element)
class CurrentLabelInline(Element):
    ''' Loop current label

        Parameters
        ----------
        direction : string
            'in' or 'out' arrow direction
        ofst : float
            Offset along lead length
        start : bool
            Arrow at start or end of element
        headlength : float
            Length of arrowhead
        headwidth : float
            Width of arrowhead
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        direction = kwargs.get('direction', 'in')
        ofst = kwargs.get('ofst', .8)
        start = kwargs.get('start', True)
        self.params['lblofst'] = .25
        self.params['drop'] = None
        hlen = kwargs.get('headlength', .3)
        hwid = kwargs.get('headwidth', .3)

        x = ofst
        dx = hlen
        if direction == 'in':
            x += hlen
            dx = -dx

        if start:
            x = -x
            dx = -dx

        self.segments.append(SegmentArrow(
            [x, 0], [x+dx, 0], headwidth=hwid, headlength=hlen))


@adddocs(Element)
class LoopCurrent(Element):
    ''' Loop current label

        Parameters
        ----------
        direction : string
            'cw' or 'ccw' loop direction
        theta1 : float
            Angle of start of loop arrow
        theta2 : float
            Angle of end of loop arrow
        width : float
            Width of loop
        height : float
            Height of loop
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        direction = kwargs.get('direction', 'cw')
        theta1 = kwargs.get('theta1', 35)
        theta2 = kwargs.get('theta2', -35)
        width = kwargs.get('width', 0.75)
        height = kwargs.get('height', 0.75)
        self.segments.append(SegmentArc(
            [0, 0], arrow=direction, theta1=theta1, theta2=theta2,
            width=width, height=height))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = 0
        self.anchors['center'] = [0, 0]


class Rect(Element):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        c1 = kwargs.get('corner1', [0, 0])
        c2 = kwargs.get('corner2', [1, 1])
        c1a = [c1[0], c2[1]]
        c2a = [c2[0], c1[1]]
        fill = kwargs.get('fill', False)
        self.segments.append(Segment([c1, c1a, c2, c2a, c1], zorder=0, fill=fill))
        self.params['zorder'] = 0   # Put on bottom
