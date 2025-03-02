''' Lines, Arrows, and Labels '''

from __future__ import annotations
from typing import Optional, Sequence, Union
import math

from ..segments import Segment, SegmentCircle, SegmentArc, SegmentPoly, SegmentBezier
from .elements import Element, Element2Term
from .twoterm import gap
from ..types import XY, Point, Arcdirection, BilateralDirection, Linestyle
from .. import util
from .. import drawing_stack


class Line(Element2Term):
    r''' Straight Line

        Args:
            arrow: arrowhead specifier, such as '->', '<-', '<->', '-o', or '\|->'

        Keyword Args:
            arrowwidth: Width of arrowhead [default: .15]
            arrowlength: Length of arrowhead [default:  0.25]
    '''
    _element_defaults = {
        'arrowwidth': 0.15,
        'arrowlength': 0.25}
    def __init__(self, *, arrow: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        arrowwidth: float = self.params['arrowwidth']
        arrowlength: float = self.params['arrowlength']
        self.segments.append(Segment([(0, 0)], arrow=arrow,
                                     arrowwidth=arrowwidth, arrowlength=arrowlength))


bus_stroke = 0.25
class DataBusLine(Element2Term):
    ''' Straight Line with bus indication stripe '''
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment(
            [(0, 0), gap, (-bus_stroke/2, bus_stroke), (bus_stroke/2, -bus_stroke),
             gap, (0, 0)]))


class Arrow(Line):
    r''' Arrow

        Args:
            double: Show arrowhead on both ends

        Keyword Args:
            arrow: arrowhead specifier, such as '->', '<-', '<->', '-o', or '\|->'
            arrowwidth: Width of arrow head [default: 0.15]
            arrowlength: Length of arrow head [default: 0.25]
    '''
    def __init__(self, *,
                 double: bool = False,
                 arrowwidth: Optional[float] = None,
                 arrowlength: Optional[float] = None,
                 **kwargs):
        if double:
            kwargs.setdefault('arrow', '<->')
        else:
            kwargs.setdefault('arrow', '->')
        super().__init__(**kwargs)

        # Explicitly define center so reverses work
        self.anchors['center'] = (0, 0)


class Gap(Element2Term):
    ''' Gap for labeling port voltages, for example. Draws nothing,
        but provides place to attach a label such as ('+', 'V', '-').

        Keyword Args:
            lblloc: Label location within the gap [center]
            lblalign: Label alignment [(center, center)]
            lblofst: Offset to label [0]
    '''
    _element_defaults = {
        'lblloc': 'center',
        'lblalign': ('center', 'center'),
        'lblofst': 0
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.segments.append(Segment([(0, 0), gap, (1, 0)], visible=False))


class Dot(Element):
    ''' Connection Dot

        Keyword Args:
            radius: Radius of dot [default: 0.075]
            open: Draw as an open circle [default: False]
    '''
    _element_defaults = {
        'radius': 0.075,
        'open': False}
    def __init__(self, *,
                 radius: Optional[float] = None,
                 open: Optional[bool] = None,
                 **kwargs):
        super().__init__(**kwargs)
        fill = 'bg' if self.params['open'] else True
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)
        self.elmparams['drop'] = (0, 0)
        self.elmparams['theta'] = 0
        self.elmparams['zorder'] = 4
        self.elmparams['fill'] = fill
        self.segments.append(SegmentCircle((0, 0), self.params['radius']))


class Arrowhead(Element):
    ''' Arrowhead 
    
        Args:
            headwidth: width of arrow head [default: .15]
            headlength: length of arrow head [default: .25]
    '''
    _element_defaults = {
        'headwidth': 0.15,
        'headlength': 0.25,
        'lblofst': 0.25
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        headwidth = self.params['headwidth']
        headlength = self.params['headlength'] 
        self.segments.append(Segment([
            (-headlength, 0), (0, 0)], arrowwidth=headwidth, arrowlength=headlength, arrow='->'))
        self.anchors['start'] = (0, 0)
        self.anchors['center'] = (0, 0)
        self.anchors['end'] = (0, 0)


class DotDotDot(Element):
    ''' Ellipsis element

        Keyword Args:
            radius: Radius of dots [default 0.075]
            open: Draw dots as open circles [default: False]

        "Ellipsis" is a reserved keyword in Python used for slicing,
        thus the name DotDotDot.
    '''
    _element_defaults = {
        'radius': 0.075,
        'open': False,
    }
    def __init__(self, *,
                 radius: Optional[float] = None,
                 open: Optional[bool] = None,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        r: float = self.params['radius']
        fill = 'bg' if self.params['open'] else True
        self.elmparams['fill'] = fill
        self.segments.append(SegmentCircle((.5, 0), r))
        self.segments.append(SegmentCircle((1, 0), r))
        self.segments.append(SegmentCircle((1.5, 0), r))
        self.elmparams['drop'] = (2, 0)


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
    def __init__(self, shape: str = '-', k: float = 1, *,
                 arrow: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self._userparams['shape'] = shape
        self._userparams['k'] = k
        self._userparams.setdefault('to', (3, -2))

    def to(self, xy: XY, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position relative to start position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def dot(self, open: bool = False) -> 'Element':
        ''' Add a dot to the end of the element '''
        self._userparams['dot'] = True if not open else 'open'
        return self

    def idot(self, open: bool = False) -> 'Element':
        ''' Add a dot to the input/start of the element '''
        self._userparams['idot'] = True if not open else 'open'
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams.clear()
        self._dwgparams.update(dwgparams)
        if not self._positioned:
            self._position()

        self.params['theta'] = 0
        xy = self.params.get('at', dwgxy)
        to = self.params.get('to', dwgxy)
        delta = self.params.get('delta', None)
        arrow = self.params.get('arrow', None)
        shape = self.params.get('shape', '-')
        k = self.params.get('k', 1)
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
            self.elmparams['droptheta'] = 90 if dy > 0 else -90
        elif shape == '|-':  # Right angle, vertical first
            self.segments.append(Segment([(0, 0), (0, dy), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (dx/2, dy)
            self.elmparams['droptheta'] = 0 if dx > 0 else 180
        elif shape in ['z', 'Z']:
            if dx > 0:
                k = abs(k)
            else:
                k = -abs(k)
            self.segments.append(Segment([(0, 0), (k, 0), (dx-k, dy), (dx, dy)], arrow=arrow))
            self.anchors['mid'] = (dx/2, dy/2)
            self.elmparams['droptheta'] = 0 if dx > 0 else 180
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

        if self.params.get('dot', False):
            fill: Union[bool, str] = 'bg' if self.params['dot'] == 'open' else True
            self.segments.append(SegmentCircle((dx, dy), radius=0.075, fill=fill, zorder=3))
        if self.params.get('idot', False):
            fill = 'bg' if self.params['idot'] == 'open' else True
            self.segments.append(SegmentCircle((0, 0), radius=0.075, fill=fill, zorder=3))

        self.elmparams['lblloc'] = 'mid'
        self.elmparams['drop'] = (dx, dy)
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
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o'

        Anchors:
            start
            end
            ctrl
            mid
    '''
    def __init__(self, k: float = 0.5, arrow: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.k = k
        self.arrow = arrow

    def to(self, xy: XY, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify change in position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._positioned:
            self._position()

        xy: Point = Point(self.params.get('at', dwgxy))
        to: Point = Point(self.params.get('to', Point((xy.x+3, xy.y))))
        delta = self.params.get('delta', None)
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
        self.elmparams['theta'] = 0
        self.elmparams['lblloc'] = 'mid'
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((dx, dy))
        self.elmparams['drop'] = Point((dx, dy))
        valign = 'bottom'
        halign = 'left'
        vofst = 0.1
        hofst = 0.0
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
            vofst = 0.0
            hofst = -0.1
        elif mid.x < pa.x:
            hofst = 0.1
            vofst = 0.0

        self.elmparams['lblofst'] = (hofst, vofst)
        self.elmparams['lblalign'] = (halign, valign)
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
            arrowlength: Length of arrowhead [default: 0.25]
            arrowwidth: Width of arrowhead [default: 0.2]

        Anchors:
            start
            end
            center
            ctrl1
            ctrl2
    '''
    _element_defaults = {
        'arrowlength': 0.25,
        'arrowwidth': 0.2
    }
    def __init__(self,
                 k: float = 0.75,
                 th1: float = 0.,
                 th2: float = 180,
                 arrow: Optional[str] = None,
                 *,
                 arrowlength: Optional[float] = None,
                 arrowwidth: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._userparams.setdefault('to', Point((1, 0)))
        self.k = k
        self.th1 = math.radians(th1)
        self.th2 = math.radians(th2)
        self.arrow = arrow

    def to(self, xy: XY, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify change in position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate absolute placement of Element '''
        self._dwgparams = dwgparams
        if not self._positioned:
            self._position()

        self.params['theta'] = 0
        xy: Point = Point(self.params.get('at', dwgxy))
        to: Point = Point(self.params.get('to', dwgxy))
        delta = self.params.get('delta', None)
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
                                           arrowlength=self.params['arrowlength'],
                                           arrowwidth=self.params['arrowwidth']))
        self.anchors['center'] = Point((dx/2, dy/2))
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((dx, dy))
        self.anchors['ctrl1'] = pa1
        self.anchors['ctrl2'] = pa2
        self.elmparams['drop'] = Point((dx, dy))
        self._setlabel(dx, dy)
        return super()._place(dwgxy, dwgtheta, **dwgparams)

    def _setlabel(self, dx: float, dy: float) -> None:
        ''' Set label position/alignment '''
        # This sets reasonable label position along center of arc.
        self.elmparams['lblloc'] = 'center'
        halign = 'left'
        valign = 'bottom'
        if dy > 0:
            valign = 'top'
            self.elmparams['lblofst'] = -0.1
        if dx <= 0:
            halign = 'right'
        self.elmparams['lblalign'] = (halign, valign)


class Annotate(Arc3):
    ''' Draw a curved arrow pointing to `at` position, ending at `to`
        position, with label location at the tail of the arrow
        (See also `Arc3`).

        Args:
            k: Control point factor. Higher k means tighter curve.
            th1: Angle at which the arc leaves start point
            th2: Angle at which the arc leaves end point
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o'
            arrowlength: Length of arrowhead [default: 0.25]
            arrowwidth: Width of arrowhead [default: 0.2]
    '''
    def __init__(self,
                 k: float = 0.75,
                 th1: float = 75,
                 th2: float = 180,
                 arrow: str = '<-',
                 *,
                 arrowlength: Optional[float] = None,
                 arrowwidth: Optional[float] = None,
                 **kwargs):
        super().__init__(k=k, th1=th1, th2=th2, arrow=arrow,
                         arrowlength=arrowlength, arrowwidth=arrowwidth, **kwargs)
        self._userparams['to'] = Point((1, 1))

    def _setlabel(self, dx: float, dy: float) -> None:
        ''' Set label position/alignment '''
        # Attempt to align the label at the tail of the arrow.
        self.elmparams['lblloc'] = 'end'
        p1, p2 = Point(self.anchors['ctrl2']), Point(self.anchors['end'])
        if p1 == p2:
            th2 = -90. if dy < 0 else 90.
        else:
            th2 = math.degrees(math.atan2(p2.y-p1.y, p2.x-p1.x))
        while th2 < 0:
            th2 += 360.

        if th2 < 45 or th2 > 315:
            self.elmparams['lblalign'] = ('left', 'center')
            self.elmparams['lblofst'] = (.1, 0)
        elif 45 <= th2 <= 135:
            self.elmparams['lblalign'] = ('center', 'bottom')
            self.elmparams['lblofst'] = (0, .1)
        elif 135 < th2 <= 225:
            self.elmparams['lblalign'] = ('right', 'center')
            self.elmparams['lblofst'] = (-.1, 0)
        else:
            self.elmparams['lblalign'] = ('center', 'top')
            self.elmparams['lblofst'] = (0, -.1)


class ArcZ(Arc3):
    ''' Z-Curve Arc

        Use `at` and `to` methods to define endpoints.

        ArcZ approaches the endpoints horizontally, leading to
        a 'Z' shaped curve

        Args:
            k: Control point factor. Higher k means tighter curve.
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o' [default: None]
            arrowlength: Length of arrowhead [default: 0.25]
            arrowwidth: Width of arrowhead [default: 0.2]
    '''
    def __init__(self,
                 k: float = 0.75,
                 arrow: Optional[str] = None,
                 *,
                 arrowlength: Optional[float] = None,
                 arrowwidth: Optional[float] = None,
                 **kwargs):
        super().__init__(k=k,
                         arrow=arrow,
                         th1=0,
                         th2=180,
                         arrowlength=arrowlength,
                         arrowwidth=arrowwidth,
                         **kwargs)


class ArcN(Arc3):
    ''' N-Curve Arc

        Use `at` and `to` methods to define endpoints.

        ArcN approaches the endpoints vertically, leading to
        a 'N' shaped curve

        Args:
            k: Control point factor. Higher k means tighter curve.
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o' [default: None]
            arrowlength: Length of arrowhead [default: 0.25]
            arrowwidth: Width of arrowhead [default: 0.2]
    '''
    def __init__(self,
                 k: float = 0.75,
                 arrow: Optional[str] = None,
                 *,
                 arrowlength: Optional[float] = None,
                 arrowwidth: Optional[float] = None,
                 **kwargs):
        super().__init__(k=k,
                         arrow=arrow,
                         th1=90,
                         th2=-90,
                         arrowlength=arrowlength,
                         arrowwidth=arrowwidth,
                         **kwargs)


class ArcLoop(Element):
    ''' Loop Arc

        Use `at` and `to` methods to define endpoints.

        ArcLoop is an arc drawn as part of a circle.

        Args:
            radius: Radius of the arc
            arrow: arrowhead specifier, such as '->', '<-', '<->', or '-o' [default: None]
            arrowlength: Length of arrowhead [default: 0.25]
            arrowwidth: Width of arrowhead [default: 0.2]

        Anchors:
            start
            end
            mid
            BL
            BR
            TL
            TR
    '''
    _element_defaults = {
        'arrowlength': 0.25,
        'arrowwidth': 0.2
    }
    def __init__(self,
                 radius: float = 0.6,
                 arrow: Optional[str] = None,
                 *,
                 arrowlength: Optional[float] = None,
                 arrowwidth: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.radius = radius
        self.arrow = arrow

    def to(self, xy: XY, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def delta(self, dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify ending position relative to start position '''
        self._userparams['delta'] = Point((dx, dy))
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate placement of Element '''
        self._dwgparams = dwgparams
        if not self._positioned:
            self._position()

        self.params['theta'] = 0
        xy: Point = Point(self.params.get('at', dwgxy))
        to: Point = Point(self.params.get('to', dwgxy))
        delta = self.params.get('delta', None)
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
                                     arrowlength=self.params['arrowlength'],
                                     arrowwidth=self.params['arrowwidth']))
        mid = len(x)//2
        self.anchors['start'] = Point((0, 0))
        self.anchors['end'] = Point((x[-1], y[-1]))
        self.anchors['mid'] = Point((x[mid], y[mid]))
        self.anchors['BL'] = Point((min(x), min(y)))
        self.anchors['BR'] = Point((max(x), min(y)))
        self.anchors['TL'] = Point((min(x), max(y)))
        self.anchors['TR'] = Point((max(x), max(y)))
        self.elmparams['lblloc'] = 'mid'
        self.elmparams['drop'] = to
        self.elmparams['lblofst'] = (0, .2)
        if y[mid] < y[0]:
            self.elmparams['lblofst'] = (0, -.25)
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class Label(Element):
    ''' Label element.

        For more options, use `Label().label()` method.

        Args:
            label: text to display.
    '''
    def __init__(self, label: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['lblloc'] = 'center'
        self.elmparams['lblofst'] = 0
        if label:
            self.label(label)


class Tag(Element):
    ''' Tag/flag element for labeling signal names.

        Because text size is unknown until drawn, must specify width
        manually to fit a given text label.

        Args:
            width: Width of the tag [default: 1.5]
            height: Height of the tag [default: 0.625]
    '''
    _element_defaults = {
        'width': 1.5,
        'height': 0.625,
        'lblloc': 'center',
        'fontsize': 12,
        'lblofst': 0
    }
    def __init__(self, *,
                 width: Optional[float] = None,
                 height: Optional[float] = 0.625,
                 **kwargs) -> None:
        super().__init__(**kwargs)
        w: float = self.params['width']
        h: float = self.params['height']
        h = h / 2
        self.segments.append(SegmentPoly([(0, 0),
                                          (h, h),
                                          (w, h),
                                          (w, -h),
                                          (h, -h)]))
        self.anchors['start'] = (0, 0)


class CurrentLabel(Element):
    ''' Current label arrow drawn above an element

        Use `.at()` method to place the label over an
        existing element.

        Args:
            reverse: Reverse the arrow direction
            ofst: Offset distance from centerline of element [default: 0.4]
            length: Length of the arrow [default: 2]
            top: Draw arrow on top or bottom of element [default: True]
            headlength: Length of arrowhead [default: 0.3]
            headwidth: Width of arrowhead [default: 0.2]
    '''
    _element_defaults = {
        'ofst': 0.15,
        'length': 2,
        'top': True,
        'reverse': False,
        'headlength': 0.3,
        'headwidth': 0.2,
        'anchor': 'center',
        'drop': None,
        'lblofost': -0.1
    }
    def __init__(self,
                 *,
                 length: Optional[float] = None,
                 top: Optional[bool] = None,
                 reverse: Optional[bool] = None,
                 ofst: Optional[float] = None,
                 headlength: Optional[float] = None,
                 headwidth: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.anchors['center'] = (0, 0)
        self._side = 'top'

    def at(self, xy: XY | tuple['Element', str], dx: float = 0, dy: float = 0) -> 'Element':
        ''' Specify CurrentLabel position.

            If xy is an Element, arrow will be centered
            along element and its color will also be
            inherited.

            Args:
                xy: The absolute (x, y) position or an
                Element instance to center the arrow over
        '''
        if isinstance(xy, Element):
            side = xy.params.get('ilabel', 'top')
            if not self.params.get('top', True):
                side = {'top': 'bottom',
                        'bottom': 'top',
                        'left': 'right',
                        'right': 'left'}.get(side, 'top')                

            if xy.params.get('reverse', False):
                side = {'left': 'right',
                        'right': 'left'}.get(side, side)
                if side not in ['left', 'right']:
                    self.reverse()

            if xy.params.get('flip', False) and side in ['left', 'right']:
                self.reverse()

            if side == 'left':
                self.reverse()

            theta = xy.transform.theta
            bbox = xy.get_bbox(includetext=False)
            if side == 'top':
                pos = Point(((bbox.xmax + bbox.xmin)/2, bbox.ymax))
                self.elmparams['lblloc'] = 'top'
            elif side == 'bottom':
                pos = Point(((bbox.xmax + bbox.xmin)/2, bbox.ymin))
                self.elmparams['lblloc'] = 'bot'
            elif side == 'right':
                pos = Point(((bbox.xmax, (bbox.ymax + bbox.ymin)/2)))
                self.elmparams['lblloc'] = 'bot'
                theta -= 90
            elif side == 'left':
                pos = Point(((bbox.xmin, (bbox.ymax + bbox.ymin)/2)))
                self.elmparams['lblloc'] = 'top'
                theta += 90
            
            pos = xy.transform.transform(pos)
            self._side = side
            super().at(pos)

            self.theta(theta)
            if 'color' in xy._userparams:
                self.color(xy._userparams.get('color'))
        else:
            super().at(xy)
        return self

    def _place(self, dwgxy, dwgtheta, **dwgparams):
        ofst = self.params['ofst']
        length = self.params['length']
        if self._side in ['bottom']:
            ofst = -ofst

        theta = self.params.get('theta', 0) % 360
        loc = self.params.get('lblloc', 'top')

        if self._side in ['right'] and (theta <= 90 or theta > 270):
            loc = self.elmparams.get('lblloc', 'top')
            self.elmparams['lblloc'] = {'bot': 'top',
                                        'top': 'bot'}.get(loc)

        elif self._side in ['top', 'left', 'bottom'] and (90 < theta <= 270):
            loc = self.elmparams.get('lblloc', 'top')
            self.elmparams['lblloc'] = {'bot': 'top',
                                        'top': 'bot'}.get(loc)

        a, b = (-length/2, ofst), (length/2, ofst)
        headwidth = self.params['headwidth']
        headlength = self.params['headlength']
        self.segments.append(Segment((a, b), arrow='->', arrowwidth=headwidth, arrowlength=headlength))
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class CurrentLabelInline(Element):
    ''' Current direction arrow, inline with element.

        Use `.at()` method to place arrow on an Element instance

        Args:
            direction: arrow direction 'in' or 'out' of element
            ofst: Offset along lead length
            start: Arrow at start or end of element
            headlength: Length of arrowhead [default: 0.3]
            headwidth: Width of arrowhead [default: 0.3]
    '''
    _element_defaults = {
        'headlength': 0.3,
        'headwidth': 0.3
    }
    def __init__(self,
                 direction: BilateralDirection = 'in',
                 ofst: float = 0.8,
                 start: bool = True,
                 *,
                 headlength: Optional[float] = None,
                 headwidth: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.elmparams['lblofst'] = 0
        self.elmparams['drop'] = None
        self.elmparams['zorder'] = 4

        x = ofst
        dx = self.params['headlength']
        if direction == 'in':
            x += self.params['headlength']
            dx = -dx

        if start:
            x = -x
            dx = -dx

        self.segments.append(Segment(((x, 0), (x+dx, 0)),
                                     arrow='->',
                                     arrowwidth=self.params['headwidth'],
                                     arrowlength=self.params['headlength']))

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
                self.color(xy._userparams.get('color'))  # type: ignore
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
            length: Length of the arrow tail [default: 1]
            lengthtip: Length of the arrow tip [default: 0.5]
            headlength: Arrowhead length [default: 0.25]
            headwidth: Arrowhead width [default: 0.15]
    '''
    _element_defaults = {
        'ofst': 0.5,
        'hofst': 0.4,
        'length': 1,
        'lengthtip': 0.5,
        'headlength': 0.25,
        'headwidth': 0.15,
        'drop': None,
    }
    def __init__(self, *,
                 ofst: Optional[float] = None,
                 hofst: Optional[float] = None,
                 length: Optional[float] = None,
                 lengthtip: Optional[float] = None,
                 headlength: Optional[float] = None,
                 headwidth: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self.anchor('center')
        self.anchors['center'] = (0, 0)

    def at(self, xy: XY | Element) -> 'Element':  # type: ignore[override]
        ''' Specify Element position.

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
                self.color(xy._userparams.get('color'))  # type: ignore
        else:
            super().at(xy)
        return self

    def _place(self, dwgxy, dwgtheta, **dwgparams):
        self._dwgparams = dwgparams
        if not self._positioned:
            self._position()

        a = Point((-self.params['hofst'], self.params['ofst']))
        b = Point((-self.params['hofst']-self.params['lengthtip'], 
                   self.params['ofst']))
        c = Point((-self.params['hofst']-self.params['lengthtip'],
                   self.params['ofst']-self.params['length']))
        self.anchors['head'] = a
        self.anchors['tail'] = c

        self.segments.append(Segment((c, b, a), arrow='->',
                                     arrowwidth=self.params['headwidth'],
                                     arrowlength=self.params['headlength']))

        # Attempt to align the label at the tail of the arrow.
        self.elmparams['lblloc'] = 'tail'
        th = self.params.get('theta', 0)
        if self.params.get('flip'):
            th += 180

        th -= 90  # Because arrow is at right angle
        th = (th+360) % 360

        if th < 45 or th > 315:
            self.elmparams['lblalign'] = ('left', 'center')
            self.elmparams['lblofst'] = (0, -.1)
        elif 45 <= th <= 135:
            self.elmparams['lblalign'] = ('center', 'bottom')
            self.elmparams['lblofst'] = (0, .1)
        elif 135 < th <= 225:
            self.elmparams['lblalign'] = ('right', 'center')
            self.elmparams['lblofst'] = (0, .1)
        else:
            self.elmparams['lblalign'] = ('center', 'top')
            self.elmparams['lblofst'] = (0, -.1)

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
    _element_defaults = {
        'lblloc': 'center',
        'lblofst': 0,
        'theta': 0,
    }
    def __init__(self, direction: Arcdirection = 'cw',
                 theta1: float = 35, theta2: float = -35,
                 width: float = 1.0, height: float = 1.0, **kwargs):
        super().__init__(**kwargs)

        self.segments.append(SegmentArc(
            (0, 0), arrow=direction, theta1=theta1, theta2=theta2,
            width=width, height=height))

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
    def __init__(self, elm_list: Optional[Sequence[Element]] = None,
                 direction: Arcdirection = 'cw',
                 theta1: float = 35, theta2: float = -35,
                 pad: float = 0.2, **kwargs):
        assert elm_list is not None
        drawing_stack.push_element(None)  # Flush the stack to make sure all elm_list are placed
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
            fill: Color to fill if not None [default: inherit]
            lw: Line width [default: inherit]
            ls: Line style '-', '--', ':', etc. [default: inherit]
    '''
    _element_defaults = {
        'zorder': 0,  # Put on bottom
    }
    def __init__(self,
                 corner1: XY = (0, 0),
                 corner2: XY = (1, 1),
                 *,
                 fill: Optional[str] = None,
                 lw: Optional[float] = None,
                 ls: Optional[Linestyle] = None,
                 **kwargs):
        super().__init__(**kwargs)
        c1a = (corner1[0], corner2[1])
        c2a = (corner2[0], corner1[1])
        self.segments.append(Segment([corner1, c1a, corner2, c2a, corner1], zorder=0))


class Encircle(Element):
    ''' Draw ellipse around all elements in the list

        Args:
            elm_list: List of elements to enclose
            padx: Horizontal distance from elements to loop [default: .2]
            pady: Vertical distance from elements to loop [default: .2]
            includelabels: Include labels in the ellipse
    '''
    _element_defaults = {
        'padx': 0.2,
        'pady': 0.2,
        'theta': 0
    }
    def __init__(self,
                 elm_list: Optional[Sequence[Element]] = None,
                 *,
                 padx: Optional[float] = None,
                 pady: Optional[float] = None,
                 includelabels: bool = True,
                 **kwargs):
        drawing_stack.push_element(None)  # Flush the stack to make sure all elm_list are placed
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
        xmin -= self.params['padx']
        xmax += self.params['padx']
        ymin -= self.params['pady']
        ymax += self.params['pady']
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


class EncircleBox(Element):
    ''' Draw rounded box around all elements in the list

        Args:
            elm_list: List elements to enclose
            cornerraidus: radius of corner rounding [default: 0.3]
            padx: Horizontal distance from elements to loop [default: 0.2]
            pady: Vertical distance from elements to loop [default: 0.2]
            includelabels: Include labels in the box
    '''
    _element_defaults = {
        'cornerradius': 0.3,
        'padx': 0.2,
        'pady': 0.2,
        'theta': 0
    }
    def __init__(self,
                 elm_list: Optional[Sequence[Element]] = None,
                 *,
                 cornerradius: float = 0.3,
                 padx: Optional[float] = None,
                 pady: Optional[float] = None,
                 includelabels: bool = True,
                 **kwargs):
        drawing_stack.push_element(None)  # Flush the stack to make sure all elm_list are placed
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
        xmin -= self.params['padx']
        xmax += self.params['padx']
        ymin -= self.params['pady']
        ymax += self.params['pady']
        center = (xmax+xmin)/2, (ymax+ymin)/2
        w = xmax-xmin
        h = ymax-ymin
        self._userparams['at'] = center
        self.segments = [SegmentPoly(
            [(-w/2, h/2), (w/2, h/2), (w/2, -h/2), (-w/2, -h/2)],
            cornerradius=self.params['cornerradius'])]
        k = self.params['cornerradius'] - self.params['cornerradius']*math.sqrt(2)/2
        self.anchors['NE'] = (w/2-k, h/2-k)
        self.anchors['NW'] = (-w/2+k, h/2-k)
        self.anchors['SE'] = (w/2-k, -h/2+k)
        self.anchors['SW'] = (-w/2+k, -h/2+k)
        self.anchors['N'] = (0, h/2)
        self.anchors['S'] = (0, -h/2)
        self.anchors['E'] = (w/2, 0)
        self.anchors['W'] = (-w/2, 0)
