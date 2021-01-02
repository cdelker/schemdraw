''' Schemdraw drawing segments.

    Each element is made up of one or more segments
    that define drawing primitives.
'''

from typing import Sequence, List, Literal, Dict, Any, Union
import math

from .types import BBox, XY, Linestyle, Capstyle, Joinstyle, Align
from . import util
from .util import Point
from .backends import svgtext


def roundcorners(verts: Sequence[XY], radius: float=.5) -> Sequence[XY]:
    ''' Round the corners of polygon defined by verts.
        Works for convex polygons assuming radius fits inside.

        Args:
            verts: List of (x,y) pairs defining corners of polygon
            radius: Radius of curvature

        Adapted from:
        https://stackoverflow.com/questions/24771828/algorithm-for-creating-rounded-corners-in-a-polygon
    '''
    poly: List[Point] = []
    for v in range(len(verts))[::-1]:
        p1 = verts[v]
        p2 = verts[v-1]
        p3 = verts[v-2]

        dx1 = p2[0]-p1[0]
        dy1 = p2[1]-p1[1]
        dx2 = p2[0]-p3[0]
        dy2 = p2[1]-p3[1]

        angle = (math.atan2(dy1, dx1) - math.atan2(dy2, dx2))/2
        tan = abs(math.tan(angle))
        segment = radius/tan

        def getlength(x, y):
            return math.sqrt(x*x + y*y)

        def getproportionpoint(point, segment, length, dx, dy):
            factor = segment/length
            return point[0]-dx * factor, point[1]-dy * factor

        length1 = getlength(dx1, dy1)
        length2 = getlength(dx2, dy2)
        length = min(length1, length2)

        if segment > length:
            segment = length
            radius = length * tan

        p1cross = getproportionpoint(p2, segment, length1, dx1, dy1)
        p2cross = getproportionpoint(p2, segment, length2, dx2, dy2)

        dx = p2[0]*2 - p1cross[0] - p2cross[0]
        dy = p2[1]*2 - p1cross[1] - p2cross[1]
        L = getlength(dx, dy)
        d = getlength(segment, radius)
        circlepoint = getproportionpoint(p2, d, L, dx, dy)
        startangle = math.atan2(p1cross[1] - circlepoint[1], p1cross[0]-circlepoint[0])
        endangle = math.atan2(p2cross[1] - circlepoint[1], p2cross[0]-circlepoint[0])

        while endangle < startangle:
            endangle += 2*math.pi

        ph = util.linspace(startangle, endangle, 100)
        arc = [Point((circlepoint[0] + math.cos(i)*radius, circlepoint[1] + math.sin(i)*radius)) for i in ph]

        poly.extend(arc)
    poly.append(poly[0])  # Close the loop
    return poly


class Segment:
    ''' A segment path

        Args:
            path: List of [x,y] coordinates making the path
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment '-', '--', ':', etc.
            capstyle: Capstyle for the segment: 'butt', 'round', 'square', ('projecting')
            joinstyle: Joinstyle for the segment: 'round', 'miter', or 'bevel'
            fill: Color to fill if path is closed
            zorder: Z-order for segment
    '''
    def __init__(self, path: Sequence[XY],
                 color: str=None,
                 lw: float=None,
                 ls: Linestyle=None,
                 capstyle: Capstyle=None,
                 joinstyle: Joinstyle=None,
                 fill: str=None,
                 zorder: int=None):
        self.path: Sequence[XY] = path  # Untranformed path
        self.zorder = zorder
        self.color = color
        self.fill = fill
        self.lw = lw
        self.ls = ls
        self.capstyle = capstyle
        self.joinstyle = joinstyle

    def end(self) -> XY:
        ''' Get endpoint of this segment, untransformed '''
        return self.path[-1]

    def xform(self, transform, **style) -> 'Segment':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: Dict[str, Any] = {'zorder': self.zorder,
                                  'color': self.color,
                                  'fill': self.fill,
                                  'lw': self.lw,
                                  'ls': self.ls,
                                  'capstyle': self.capstyle,
                                  'joinstyle': self.joinstyle}
        style = {k: v for k, v in style.items() if k in params.keys()}
        params.update(style)
        return Segment(transform.transform_array(self.path), **params)

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits: (xmin, ymin, xmax, ymax)
        '''
        x = [p[0] for p in self.path]
        y = [p[1] for p in self.path]
        return BBox(min(x), min(y), max(x), max(y))

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the center of the path) '''
        self.path = [util.mirrorx(p, centerx) for p in self.path[::-1]]

    def doflip(self) -> None:
        ''' Vertically flip the element '''
        self.path = [util.flip(p) for p in self.path]

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        path = transform.transform_array(self.path)

        zorder = self.zorder if self.zorder is not None else style.get('zorder', 2)
        color = self.color if self.color else style.get('color', 'black')
        fill = self.fill if self.fill is not None else style.get('fill', None)
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)
        capstyle = self.capstyle if self.capstyle else style.get('capstyle', 'round')
        joinstyle = self.joinstyle if self.joinstyle else style.get('joinstyle', 'round')

        if fill:  # Check if path is closed
            tlist = list(map(tuple, path))  # Need path as tuples for set()
            dofill = len(tlist) != len(set(tlist))  # Path has duplicates, can fill it
            if not dofill:
                fill = None
            elif fill is True:
                fill = color
            elif fill is False:
                fill = None

        x = [p[0] for p in path]
        y = [p[1] for p in path]
        fig.plot(x, y, color=color, fill=fill,
                 ls=ls, lw=lw, capstyle=capstyle, joinstyle=joinstyle,
                 zorder=zorder)


class SegmentText:
    ''' A text drawing segment

        Args:
            pos: (x, y) coordinates for text
            label: Text to draw
            align: Tuple of (horizontal, vertical) alignment where horizontal
                is ('center', 'left', 'right') and vertical is ('center',
                'top', 'bottom')
            rotation: Rotation angle in degrees
            rotation_mode: See Matplotlib documentation. 'anchor' or 'default'.
            color: Color for this segment
            fontsize: Font size
            font: Font name/family
            zorder: Z-order for segment
    '''
    def __init__(self, pos: Sequence[float], label: str,
                 align: Align=None,
                 rotation: float=None,
                 rotation_mode: Literal['anchor', 'default']=None,
                 color: str=None,
                 fontsize: float=14,
                 font: str=None,
                 zorder: int=None):
        self.xy = pos
        self.text = label
        self.align = align
        self.font = font
        self.fontsize = fontsize
        self.color = color
        self.rotation = rotation
        self.rotation_mode = rotation_mode
        self.zorder = zorder

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.xy = util.mirrorx(self.xy, centerx)

    def doflip(self) -> None:
        ''' Vertically flip the element '''
        self.xy = util.flip(self.xy)

    def xform(self, transform, **style) -> 'SegmentText':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: Dict[str, Any] = {'align': self.align,
                                  'font': self.font,
                                  'fontsize': self.fontsize,
                                  'color': self.color,
                                  'rotation': self.rotation,
                                  'rotation_mode': self.rotation_mode,
                                  'zorder': self.zorder}

        style = {k: v for k, v in style.items() if k in params.keys()}
        params.update(style)
        return SegmentText(transform.transform(self.xy),
                           self.text, **params)

    def end(self) -> Sequence[float]:
        ''' Get endpoint of this segment, untransformed '''
        return self.xy

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits (xmin, ymin, xmax, ymax)
        '''
        w, h, _ = svgtext.text_approx_size(self.text, 'Arial', self.fontsize)
        # h, w are in points, convert back to inches (/72)
        # then convert back to drawing units (*2)
        # This makes text the same point size regardless of inches_per_unit
        w = w/72*2
        h = h/72*2
        x = self.xy[0]
        y = self.xy[1]
        if self.align is not None:
            if self.align[0] == 'center':
                x -= w/2
            elif self.align[0] == 'right':
                x -= w
            if self.align[1] == 'center':
                y -= h/2
            elif self.align[1] == 'top':
                y -= h

        return BBox(x-.1, y-.1, x+w+.2, y+h+.2)

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        xy = transform.transform(self.xy)
        color = self.color if self.color else style.get('color', 'black')
        fontsize = self.fontsize if self.fontsize else style.get('fontsize', style.get('size', 14))
        font = self.font if self.font else style.get('font', 'sans-serif')
        align = self.align if self.align else style.get('align', ('center', 'center'))
        rotation = self.rotation if self.rotation else style.get('rotation', 0)
        rotmode = self.rotation_mode if self.rotation_mode else style.get('rotation_mode', 'anchor')
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 3)

        fig.text(self.text, xy[0], xy[1],
                 color=color, fontsize=fontsize, fontfamily=font,
                 rotation=rotation, rotation_mode=rotmode,
                 halign=align[0], valign=align[1], zorder=zorder)


class SegmentPoly:
    ''' A polygon segment

        Args:
            xy: List of [x,y] coordinates making the polygon
            closed: Draw a closed polygon (default True)
            cornerradius: Round the corners to this radius (0 for no rounding)
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment
            fill: Color to fill if path is closed
            zorder: Z-order for segment
    '''
    def __init__(self, verts: Sequence[Sequence[float]],
                 closed: bool=True,
                 cornerradius: float=0,
                 color: str=None,
                 fill: str=None,
                 lw: float=None,
                 ls: Linestyle=None,
                 joinstyle: Joinstyle=None,
                 capstyle: Capstyle=None,
                 zorder: int=None):
        self.verts = verts
        self.closed = closed
        self.cornerradius = cornerradius
        self.color = color
        self.fill = fill
        self.joinstyle = joinstyle
        self.capstyle = capstyle
        self.zorder = zorder
        self.lw = lw
        self.ls = ls

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.verts = [util.mirrorx(v, centerx) for v in self.verts[::-1]]

    def doflip(self) -> None:
        ''' Vertically flip the element '''
        self.verts = [util.flip(p) for p in self.verts]

    def xform(self, transform, **style) -> 'SegmentPoly':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: Dict[str, Any] = {'color': self.color,
                                  'fill': self.fill,
                                  'joinstyle': self.joinstyle,
                                  'capstyle': self.capstyle,
                                  'lw': self.lw,
                                  'ls': self.ls,
                                  'cornerradius': self.cornerradius,
                                  'zorder': self.zorder}
        style = {k: v for k, v in style.items() if k in params.keys()}
        params.update(style)
        return SegmentPoly(transform.transform_array(self.verts), **params)

    def end(self) -> Sequence[float]:
        ''' Get endpoint of this segment, untransformed '''
        return self.verts[-1]

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits (xmin, ymin, xmax, ymax)
        '''
        x = [p[0] for p in self.verts]
        y = [p[1] for p in self.verts]
        return BBox(min(x), min(y), max(x), max(y))

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        fill = self.fill if self.fill is not None else style.get('fill', None)
        color = self.color if self.color else style.get('color', 'black')
        joinstyle = self.joinstyle if self.joinstyle else style.get('joinstyle', 'round')
        capstyle = self.capstyle if self.capstyle else style.get('capstyle', 'round')
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        lw = self.lw if self.lw else style.get('lw', 2)
        ls = self.ls if self.ls else style.get('ls', '-')

        fill = color if fill is True else None if fill is False else fill
        verts = transform.transform_array(self.verts)

        if self.cornerradius > 0:
            verts = roundcorners(verts, self.cornerradius)

        fig.poly(verts, closed=self.closed, color=color, fill=fill, lw=lw, ls=ls,
                 capstyle=capstyle, joinstyle=joinstyle, zorder=zorder)


class SegmentCircle:
    ''' A circle drawing segment

        Args:
            center: (x, y) center of the circle
            radius: Radius of the circle
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment
            fill: Color to fill if path is closed. True -> fill with element color.
            zorder: Z-order for segment
            ref: Flip reference ['start', 'end', None].
    '''
    def __init__(self, center: Sequence[float], radius: float,
                 color: str=None,
                 lw: float=None,
                 ls: Linestyle=None,
                 fill: Union[bool, str]=None,
                 zorder: int=None,
                 ref: Literal['start', 'end']=None):
        self.center = center
        self.radius = radius
        self.zorder = zorder
        self.color = color
        self.fill = fill
        self.lw = lw
        self.ls = ls

        # Reference for adding things AFTER lead extensions
        self.endref = ref

    def end(self) -> Sequence[float]:
        ''' Get endpoint of this segment, untransformed '''
        return self.center

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.center = util.mirrorx(self.center, centerx)
        self.endref = {'start': 'end', 'end': 'start'}.get(self.endref)  # type: ignore

    def doflip(self) -> None:
        ''' Flip the segment up/down '''
        self.center = util.flip(self.center)

    def xform(self, transform, **style) -> 'SegmentCircle':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: Dict[str, Any] = {'zorder': self.zorder,
                                  'color': self.color,
                                  'fill': self.fill,
                                  'lw': self.lw,
                                  'ls': self.ls,
                                  'ref': self.endref}
        style = {k: v for k, v in style.items() if k in params.keys()}
        params.update(style)
        return SegmentCircle(transform.transform(self.center, self.endref),
                             self.radius, **params)

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits (xmin, ymin, xmax, ymax)
        '''
        xmin = self.center[0] - self.radius
        xmax = self.center[0] + self.radius
        ymin = self.center[1] - self.radius
        ymax = self.center[1] + self.radius
        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        center = transform.transform(self.center, self.endref)
        radius = transform.zoom * self.radius
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        fill = self.fill if self.fill is not None else style.get('fill', None)
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)

        fill = color if fill is True else None if fill is False else fill
        fig.circle(center, radius, color=color, fill=fill,
                   lw=lw, ls=ls, zorder=zorder)


class SegmentArrow:
    ''' An arrow drawing segment

        Args:
            tail: Start coordinate of arrow
            head: End coordinate of arrow
            headwidth: Width of arrowhead
            headlength: Length of arrowhead
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment
            zorder: Z-order for segment
    '''
    def __init__(self, tail: Sequence[float], head: Sequence[float],
                 headwidth: float=None, headlength: float=None,
                 color: str=None, lw: float=None,
                 ref: Literal['start', 'end']=None,
                 zorder: int=None):
        self.tail = tail
        self.head = head
        self.zorder = zorder
        self.headwidth = headwidth
        self.headlength = headlength
        self.color = color
        self.lw = lw
        self.endref = ref

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.tail = util.mirrorx(self.tail, centerx)
        self.head = util.mirrorx(self.head, centerx)
        self.endref = {'start': 'end', 'end': 'start'}.get(self.endref)  # type: ignore

    def doflip(self) -> None:
        self.tail = util.flip(self.tail)
        self.head = util.flip(self.head)

    def xform(self, transform, **style) -> 'SegmentArrow':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        # See https://github.com/python/mypy/issues/5382
        # for this weird type annotation
        params: Dict[str, Any] = {'zorder': self.zorder,
                                  'color': self.color,
                                  'lw': self.lw,
                                  'headwidth': self.headwidth,
                                  'headlength': self.headlength,
                                  'ref': self.endref}
        style = {k: v for k, v in style.items() if k in params.keys()}
        params.update(style)
        return SegmentArrow(transform.transform(self.tail, ref=self.endref),
                            transform.transform(self.head, ref=self.endref),
                            **params)

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits (xmin, ymin, xmax, ymax)
        '''
        hw = self.headwidth if self.headwidth else .1
        xmin = min(self.tail[0], self.head[0])
        ymin = min(self.tail[1], self.head[1])
        xmax = max(self.tail[0], self.head[0])
        ymax = max(self.tail[1], self.head[1])
        return BBox(xmin, ymin-hw, xmax, ymax+hw)

    def end(self) -> Sequence[float]:
        ''' Get endpoint of this segment, untransformed '''
        return self.head

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        tail = transform.transform(self.tail, ref=self.endref)
        head = transform.transform(self.head, ref=self.endref)
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        lw = self.lw if self.lw else style.get('lw', 2)
        headwidth = self.headwidth if self.headwidth else style.get('headwidth', .2)
        headlength = self.headlength if self.headlength else style.get('headlength', .2)

        fig.arrow(tail[0], tail[1], head[0]-tail[0], head[1]-tail[1],
                  headwidth=headwidth, headlength=headlength,
                  color=color, lw=lw, zorder=zorder)


class SegmentArc:
    ''' An arc drawing segment

        Args:
            center: Center of the arc ellipse
            width: Width of the arc ellipse
            height: Height of the arc ellipse
            theta1: Starting angle in degrees
            theta2: Ending angle in degrees
            angle: Rotation of the ellipse defining the arc
            arrow: Direction of arrowhead ('cw' or 'ccw')
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment
            fill: Color to fill if path is closed
            zorder: Z-order for segment
    '''
    def __init__(self, center: Sequence[float],
                 width: float, height: float,
                 theta1: float=35, theta2: float=-35,
                 arrow: Literal['cw', 'ccw']=None,
                 angle: float=0,
                 color: str=None,
                 lw: float=None,
                 ls: Linestyle=None,
                 zorder: int=None):
        self.center = center
        self.width = width
        self.height = height
        self.theta1 = theta1
        self.theta2 = theta2
        self.arrow = arrow
        self.angle = angle
        self.color = color
        self.lw = lw
        self.ls = ls
        self.zorder = zorder

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.center = util.mirrorx(self.center, centerx)
        self.theta1, self.theta2 = 180-self.theta2, 180-self.theta1
        self.arrow = {'cw': 'ccw', 'ccw': 'cw'}.get(self.arrow, None)  # type: ignore

    def doflip(self) -> None:
        ''' Vertically flip the element '''
        self.center = util.flip(self.center)
        self.theta1, self.theta2 = -self.theta2, -self.theta1
        self.arrow = {'cw': 'ccw', 'ccw': 'cw'}.get(self.arrow, None)  # type: ignore

    def xform(self, transform, **style) -> 'SegmentArc':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        angle = self.angle + transform.theta
        params: Dict[str, Any] = {'color': self.color,
                                  'lw': self.lw,
                                  'ls': self.ls,
                                  'zorder': self.zorder}
        style = {k: v for k, v in style.items() if k in params.keys()}
        params.update(style)
        return SegmentArc(transform.transform(self.center),
                          self.width*transform.zoom, self.height*transform.zoom, angle=angle,
                          theta1=self.theta1, theta2=self.theta2, **params)

    def end(self) -> Sequence[float]:
        ''' Get endpoint of this segment, untransformed '''
        return self.center

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits (xmin, ymin, xmax, ymax)
        '''
        # Who wants to do trigonometry when we can just brute-force the bounding box?
        theta1, theta2 = math.radians(self.theta1), math.radians(self.theta2)
        # the phi parameter in parametric form is not the same as the angle along ellipse
        # (see https://www.petercollingridge.co.uk/tutorials/computational-geometry/finding-angle-around-ellipse/)
        t1 = math.atan2(self.width*math.sin(theta1), self.height*math.cos(theta1))
        t2 = math.atan2(self.width*math.sin(theta2), self.height*math.cos(theta2))
        while t2 < t1:
            t2 += 2*math.pi
        t = util.linspace(t1, t2, num=500)
        sint = list(map(math.sin, t))
        cost = list(map(math.cos, t))
        phi = math.radians(self.angle)
        cosphi = math.cos(phi)
        sinphi = math.sin(phi)
        rx = self.width/2
        ry = self.height/2
        xx = [self.center[0] + rx * ct*cosphi - ry * st*sinphi for st, ct in zip(sint, cost)]
        yy = [self.center[1] + rx * ct*sinphi + ry * st*cosphi for st, ct in zip(sint, cost)]
        return BBox(min(xx), min(yy), max(xx), max(yy))

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        center = transform.transform(self.center)
        angle = self.angle + transform.theta

        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)

        width = self.width * transform.zoom
        height = self.height * transform.zoom
        fig.arc(center, width=width, height=height,
                theta1=self.theta1, theta2=self.theta2, angle=angle,
                color=color, lw=lw, ls=ls, zorder=zorder, arrow=self.arrow)
