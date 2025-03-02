''' Schemdraw drawing segments.

    Each element is made up of one or more segments
    that define drawing primitives.
'''

from __future__ import annotations
from typing import Optional, Sequence, Any, Union, BinaryIO
import math

from .types import BBox, XY, Linestyle, Capstyle, Joinstyle, Arcdirection, EndRef, RotationMode, Halign, Valign
from . import util
from .util import Point
from .backends import svg


def roundcorners(verts: Sequence[XY], radius: float = .5) -> Sequence[XY]:
    ''' Round the corners of polygon defined by verts.
        Works for convex polygons assuming radius fits inside.

        Args:
            verts: List of (x,y) pairs defining corners of polygon
            radius: Radius of curvature

        Adapted from:
        https://stackoverflow.com/questions/24771828/algorithm-for-creating-rounded-corners-in-a-polygon
    '''
    poly: list[Point] = []
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
            path: List of (x,y) coordinates making the path
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment '-', '--', ':', etc.
            capstyle: Capstyle for the segment: 'butt', 'round', 'square', ('projecting')
            joinstyle: Joinstyle for the segment: 'round', 'miter', or 'bevel'
            fill: Color to fill if path is closed
            arrow: Arrowhead specifier, such as '->', '<-', '<->', '-o', etc.
            arrowwidth: Width of arrowhead
            arrowlength: Length of arrowhead
            clip: Bounding box to clip to
            zorder: Z-order for segment
            visible: Show the segment when drawn
    '''
    def __init__(self, path: Sequence[XY],
                 color: Optional[str | tuple[float, float, float]] = None,
                 lw: Optional[float] = None,
                 ls: Optional[Linestyle] = None,
                 capstyle: Optional[Capstyle] = None,
                 joinstyle: Optional[Joinstyle] = None,
                 fill: Optional[str] = None,
                 arrow: Optional[str] = None,
                 arrowwidth: float = 0.15,
                 arrowlength: float = 0.25,
                 clip: Optional[BBox] = None,
                 zorder: Optional[int] = None,
                 visible: bool = True):
        self.path: Sequence[XY] = [Point(p) for p in path]   # Untranformed path
        self.zorder = zorder
        self.color = color
        self.fill = fill
        self.lw = lw
        self.ls = ls
        self.arrow = arrow
        self.arrowwidth = arrowwidth
        self.arrowlength = arrowlength
        self.clip = clip
        self.capstyle = capstyle
        self.joinstyle = joinstyle
        self.visible = visible

    def xform(self, transform, **style) -> 'Segment':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: dict[str, Any] = {
            'zorder': self.zorder if self.zorder is not None else style.get('zorder', None),
            'color': self.color if self.color else style.get('color', None),
            'fill': self.fill if self.fill is not None else style.get('fill', None),
            'lw': self.lw if self.lw else style.get('lw', None),
            'ls': self.ls if self.ls else style.get('ls', None),
            'arrow': self.arrow,
            'arrowwidth': self.arrowwidth,
            'arrowlength': self.arrowlength,
            'capstyle': self.capstyle if self.capstyle else style.get('capstyle', None),
            'joinstyle': self.joinstyle if self.joinstyle else style.get('joinstyle', None),
            'visible': self.visible}
        style = {k: v for k, v in style.items() if params.get(k) is None and k in params.keys()}
        params.update(style)
        return Segment(transform.transform_array(self.path), **params)

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits: (xmin, ymin, xmax, ymax)
        '''
        hw = self.arrowwidth if self.arrow else 0
        x = [p[0] for p in self.path]
        y = [p[1] for p in self.path]
        return BBox(min(x), min(y)-hw, max(x), max(y)+hw)

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the center of the path) '''
        self.path = [util.mirrorx(p, centerx) for p in self.path[::-1]]
        if self.arrow:
            self.arrow = self.arrow[::-1].translate(self.arrow.maketrans('<>', '><'))

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
        if not self.visible:
            return
        path = transform.transform_array(self.path)
        linepath = list(path)
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

        # Shrink line a bit so it doesn't extrude through arrowhead
        if self.arrow and '<' in self.arrow:
            delta = path[1] - path[0]
            th = math.atan2(delta.y, delta.x)
            linepath[0] = Point((linepath[0].x + self.arrowlength * math.cos(th),
                                 linepath[0].y + self.arrowlength * math.sin(th)))
        if self.arrow and '>' in self.arrow:
            delta = path[-1] - path[-2]
            th = math.atan2(delta.y, delta.x)
            linepath[-1] = Point((linepath[-1].x - self.arrowlength * math.cos(th),
                                  linepath[-1].y - self.arrowlength * math.sin(th)))

        x = [p[0] for p in linepath]
        y = [p[1] for p in linepath]
        fig.plot(x, y, color=color, fill=fill,
                 ls=ls, lw=lw, capstyle=capstyle, joinstyle=joinstyle,
                 clip=self.clip, zorder=zorder)

        if self.arrow:
            if '<' in self.arrow:
                theta = math.degrees(math.atan2(path[0].y-path[1].y, path[0].x-path[1].x))
                fig.arrow(path[0], theta, color=color, zorder=zorder, clip=self.clip,
                          arrowlength=self.arrowlength, arrowwidth=self.arrowwidth, lw=1)
            elif self.arrow.startswith('o'):
                fig.circle(path[0], self.arrowwidth/2, color=color, fill=color, lw=lw,
                           clip=self.clip, zorder=zorder)
            elif self.arrow.startswith('|'):
                theta = math.atan2(path[0].y-path[1].y, path[0].x-path[1].x) + math.pi/2
                tailx = (path[0].x + self.arrowwidth/2 * math.cos(theta),
                         path[0].x - self.arrowwidth/2 * math.cos(theta))
                taily = (path[0].y + self.arrowwidth/2 * math.sin(theta),
                         path[0].y - self.arrowwidth/2 * math.sin(theta))
                fig.plot(tailx, taily, color=color, fill=fill, capstyle=capstyle,
                         joinstyle=joinstyle, clip=self.clip, zorder=zorder)

            if '>' in self.arrow:
                theta = math.degrees(math.atan2(path[-1].y-path[-2].y, path[-1].x-path[-2].x))
                fig.arrow(path[-1], theta, color=color, zorder=zorder, clip=self.clip,
                          arrowlength=self.arrowlength, arrowwidth=self.arrowwidth, lw=1)
            elif self.arrow.endswith('o'):
                fig.circle(path[-1], self.arrowwidth/2, color=color, fill=color, lw=lw,
                           clip=self.clip, zorder=zorder)
            elif self.arrow.endswith('|'):
                theta = math.atan2(path[-1].y-path[-2].y, path[-1].x-path[-2].x) + math.pi/2
                tailx = (path[-1].x + self.arrowwidth/2 * math.cos(theta),
                         path[-1].x - self.arrowwidth/2 * math.cos(theta))
                taily = (path[-1].y + self.arrowwidth/2 * math.sin(theta),
                         path[-1].y - self.arrowwidth/2 * math.sin(theta))
                fig.plot(tailx, taily, color=color, fill=fill, capstyle=capstyle,
                         joinstyle=joinstyle, clip=self.clip, zorder=zorder)


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
            rotation_global: Lock rotation to world rather than component. Defaults to True
            color: Color for this segment
            fontsize: Font size
            font: Font name/family
            mathfont: Math font name/family
            clip: Bounding box to clip to
            zorder: Z-order for segment
            visible: Show the segment when drawn
    '''
    def __init__(self, pos: XY, label: str,
                 align: Optional[tuple[Halign, Valign]] = None,
                 rotation: Optional[float] = None,
                 rotation_mode: Optional[RotationMode] = None,
                 rotation_global: bool = True,
                 color: Optional[str | tuple[float, float, float]] = None,
                 fontsize: float = 14,
                 font: Optional[str] = None,
                 mathfont: Optional[str] = None,
                 clip: Optional[BBox] = None,
                 zorder: Optional[int] = None,
                 visible: bool = True):
        self.xy = pos
        self.text = label
        self.align = align
        self.font = font
        self.mathfont = mathfont
        self.fontsize = fontsize
        self.color = color
        self.rotation = rotation
        self.rotation_mode = rotation_mode
        self.rotation_global = rotation_global
        self.clip = clip
        self.zorder = zorder
        self.visible = visible

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.xy = util.mirrorx(self.xy, centerx)
        if not self.rotation_global and self.align is not None:
            align_lookup: dict[str, Halign] = {'center': 'center', 'left': 'right', 'right': 'left'}
            leftalign = align_lookup.get(self.align[0], 'left')
            self.align = (leftalign, self.align[1])

    def doflip(self) -> None:
        ''' Vertically flip the element '''
        self.xy = util.flip(self.xy)
        if not self.rotation_global and self.align is not None:
            align_lookup: dict[str, Valign] = {'center': 'center', 'top': 'bottom', 'bottom': 'top'}
            self.align = (self.align[0], align_lookup.get(self.align[1], 'bottom'))

    def xform(self, transform, **style) -> 'SegmentText':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: dict[str, Any] = {
            'align': self.align if self.align else style.get('align', None),
            'font': self.font if self.font else style.get('font', None),
            'mathfont': self.mathfont if self.mathfont else style.get('mathfont', None),
            'fontsize': self.fontsize if self.fontsize else style.get('fontsize', style.get('size', None)),
            'color': self.color if self.color else style.get('color', None),
            'rotation': self.rotation if self.rotation else style.get('rotation', None),
            'rotation_mode': self.rotation_mode if self.rotation_mode else style.get('rotation_mode', None),
            'rotation_global': self.rotation_global,
            'clip': self.clip,
            'zorder': self.zorder if self.zorder is not None else style.get('zorder', None),
            'visible': self.visible}

        style = {k: v for k, v in style.items() if params.get(k) is None and k in params.keys()}
        params.update(style)
        if not params['rotation_global']:
            if params['rotation'] is None:
                params['rotation'] = transform.theta
            else:
                params['rotation'] = params['rotation'] + transform.theta % 360

        return SegmentText(transform.transform(self.xy),
                           self.text, **params)

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits (xmin, ymin, xmax, ymax)
        '''
        SCALE = 2/72
        w, h, dy = svg.text_size(self.text, font=self.font,
                                 mathfont=self.mathfont, size=self.fontsize)
        # h, w are in points, convert back to inches (/72)
        # then convert back to drawing units (*2)
        # This makes text the same point size regardless of inches_per_unit
        w *= SCALE
        h *= SCALE
        dy *= SCALE
        x = self.xy[0]
        y = self.xy[1]
        nlines = len(self.text.splitlines())

        if self.align is not None:
            if self.align[0] == 'center':
                x -= w/2
            elif self.align[0] == 'right':
                x -= w

            if self.align[1] == 'center':
                y -= h/2
            elif self.align[1] == 'top':
                y -= h
            elif self.align[1] == 'bottom':
                pass
            else:  # base/baseline
                # y += dy  # If baseline is base of TOP row
                y += (dy + self.fontsize*SCALE*(nlines-1))  # If baseline is base of BOTTOM row

        return BBox(x, y, x+w, y+h)

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        if not self.visible:
            return
        xy = transform.transform(self.xy)
        color = self.color if self.color else style.get('color', 'black')
        fontsize = self.fontsize if self.fontsize else style.get('fontsize', style.get('size', 14))
        font = self.font if self.font else style.get('font', 'sans-serif')
        mathfont = self.mathfont if self.mathfont else style.get('mathfont', None)
        align = self.align if self.align else style.get('align', ('center', 'center'))
        rotation = self.rotation if self.rotation else style.get('rotation', 0)
        rotmode = self.rotation_mode if self.rotation_mode else style.get('rotation_mode', 'anchor')
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 3)

        if not self.rotation_global:
            if rotation is None:
                rotation = transform.theta
            else:
                rotation = rotation + transform.theta % 360

        fig.text(self.text, xy[0], xy[1],
                 color=color, fontsize=fontsize, fontfamily=font, mathfont=mathfont,
                 rotation=rotation, rotation_mode=rotmode,
                 halign=align[0], valign=align[1], clip=self.clip, zorder=zorder)

        # Debug Text Bounding Box
        # (doesn't work when label is not rotated with element)
        #bbox = self.get_bbox()
        #xy = transform.transform((bbox.xmin, bbox.ymin))
        #xy2 = transform.transform((bbox.xmax, bbox.ymax))
        #fig.poly((xy, (xy.x, xy2.y), xy2, (xy2.x, xy.y)),
        #         color='orange', lw=2)


class SegmentPoly:
    ''' A polygon segment

        Args:
            xy: List of (x,y) coordinates making the polygon
            closed: Draw a closed polygon (default True)
            cornerradius: Round the corners to this radius (0 for no rounding)
            color: Color for this segment
            fill: Color to fill if path is closed
            lw: Line width for the segment
            ls: Line style for the segment
            hatch: Show hatch lines
            capstyle: Capstyle for the segment: 'butt', 'round', 'square', ('projecting')
            joinstyle: Joinstyle for the segment: 'round', 'miter', or 'bevel'
            clip: Bounding box to clip to
            zorder: Z-order for segment
            visible: Show the segment when drawn
    '''
    def __init__(self, verts: Sequence[XY],
                 closed: bool = True,
                 cornerradius: float = 0,
                 color: Optional[str | tuple[float, float, float]] = None,
                 fill: Optional[str] = None,
                 lw: Optional[float] = None,
                 ls: Optional[Linestyle] = None,
                 hatch: bool = False,
                 joinstyle: Optional[Joinstyle] = None,
                 capstyle: Optional[Capstyle] = None,
                 clip: Optional[BBox] = None,
                 zorder: Optional[int] = None,
                 visible: bool = True):
        self.verts = verts
        self.closed = closed
        self.cornerradius = cornerradius
        self.color = color
        self.fill = fill
        self.hatch = hatch
        self.joinstyle = joinstyle
        self.capstyle = capstyle
        self.zorder = zorder
        self.lw = lw
        self.ls = ls
        self.clip = clip
        self.visible = visible

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
        params: dict[str, Any] = {
            'color': self.color if self.color else style.get('color', None),
            'fill': self.fill if self.fill is not None else style.get('fill', None),
            'joinstyle': self.joinstyle if self.joinstyle else style.get('joinstyle', None),
            'capstyle': self.capstyle if self.capstyle else style.get('capstyle', None),
            'lw': self.lw if self.lw else style.get('lw', None),
            'ls': self.ls if self.ls else style.get('ls', None),
            'cornerradius': self.cornerradius,
            'clip': self.clip,
            'zorder': self.zorder if self.zorder is not None else style.get('zorder', None),
            'visible': self.visible}
        style = {k: v for k, v in style.items() if params.get(k) is None and k in params.keys()}
        params.update(style)
        return SegmentPoly(transform.transform_array(self.verts), **params)

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
        if not self.visible:
            return
        fill = self.fill if self.fill is not None else style.get('fill', None)
        color = self.color if self.color else style.get('color', 'black')
        if fill is not None:
            if fill is True:
                fill = color
            if fill is False:
                fill = None
            elif fill == 'bg':
                fill = style.get('bgcolor', 'white')
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
                 hatch=self.hatch, capstyle=capstyle, joinstyle=joinstyle, clip=self.clip, zorder=zorder)


class SegmentCircle:
    ''' A circle drawing segment

        Args:
            center: (x, y) center of the circle
            radius: Radius of the circle
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment
            fill: Color to fill if path is closed. True -> fill with element color.
            clip: Bounding box to clip to
            zorder: Z-order for segment
            ref: Flip reference ['start', 'end', None].
            visible: Show the segment when drawn
    '''
    def __init__(self, center: XY,
                 radius: float,
                 color: Optional[str | tuple[float, float, float]] = None,
                 lw: Optional[float] = None,
                 ls: Optional[Linestyle] = None,
                 fill: bool | str | None = None,
                 clip: Optional[BBox] = None,
                 zorder: Optional[int] = None,
                 ref: Optional[EndRef] = None,
                 visible: bool = True):
        self.center = center
        self.radius = radius
        self.zorder = zorder
        self.color = color
        self.fill = fill
        self.lw = lw
        self.ls = ls
        self.clip = clip
        self.visible = visible

        # Reference for adding things AFTER lead extensions
        self.endref = ref

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.center = util.mirrorx(self.center, centerx)
        self.endref = {'start': 'end', 'end': 'start'}.get(self.endref)  # type: ignore

    def doflip(self) -> None:
        ''' Flip the segment up/down '''
        self.center = util.flip(self.center)

    def xform(self, transform, **style) -> 'SegmentCircle' | 'SegmentArc':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: dict[str, Any] = {
            'zorder': self.zorder if self.zorder is not None else style.get('zorder', None),
            'color': self.color if self.color else style.get('color', None),
            'fill': self.fill if self.fill is not None else style.get('fill', None),
            'lw': self.lw if self.lw else style.get('lw', None),
            'ls': self.ls if self.ls else style.get('ls', None),
            'clip': self.clip,
            'ref': self.endref,
            'visible': self.visible}
        style = {k: v for k, v in style.items() if params.get(k) is None and k in params.keys()}
        params.update(style)
        if transform.zoom[0] == transform.zoom[1]:
            # It stays a circle
            return SegmentCircle(transform.transform(self.center),
                                 self.radius*transform.zoom[0], **params)
        
        # Asymmetric zoom makes circle into ellipse
        params.pop('ref', None)  # Not implemented in SegmentArc
        return SegmentArc(self.center,
                          width=self.radius*2*transform.zoom[0],
                          height=self.radius*2*transform.zoom[1],
                          angle=transform.theta,
                          theta1=0, theta2=360, **params)

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
        if not self.visible:
            return
        center = transform.transform(self.center)
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        fill = self.fill if self.fill is not None else style.get('fill', None)
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)

        if fill is not None:
            if fill is True:
                fill = color
            if fill is False:
                fill = None
            elif fill == 'bg':
                fill = style.get('bgcolor', 'white')

        fill = color if fill is True else None if fill is False else fill

        if transform.zoom[0] == transform.zoom[1]:
            radius = transform.zoom[0] * self.radius
            fig.circle(center, radius, color=color, fill=fill,
                       lw=lw, ls=ls, clip=self.clip, zorder=zorder)
        else:
            width = self.radius * 2 * transform.zoom[0]
            height = self.radius * 2 * transform.zoom[1]
            fig.arc(center, width=width, height=height,
                    theta1=0, theta2=360, angle=transform.theta,
                    color=color, lw=lw, ls=ls, fill=fill,
                    clip=self.clip, zorder=zorder)


class SegmentBezier:
    ''' Quadratic or Cubic Bezier curve segment

        Args:
            p: control points (3 or 4)
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment '-', '--', ':', etc.
            capstyle: Capstyle for the segment: 'butt', 'round', 'square', ('projecting')
            joinstyle: Joinstyle for the segment: 'round', 'miter', or 'bevel'
            fill: Color to fill if path is closed
            arrow: Arrowhead specifier, such as '->', '<-', or '<->'
            arrowwidth: Width of arrowhead
            arrowlength: Length of arrowhead
            clip: Bounding box to clip to
            zorder: Z-order for segment
            visible: Show the segment when drawn
    '''
    def __init__(self, p: Sequence[XY],
                 color: Optional[str | tuple[float, float, float]] = None,
                 lw: Optional[float] = None,
                 ls: Optional[Linestyle] = None,
                 capstyle: Optional[Capstyle] = None,
                 arrow: Optional[str] = None,
                 arrowlength: float = .25,
                 arrowwidth: float = .15,
                 clip: Optional[BBox] = None,
                 zorder: Optional[int] = None,
                 visible: bool = True):
        self.p = [Point(pi) for pi in p]
        self.arrow = arrow
        self.color = color
        self.lw = lw
        self.ls = ls
        self.capstyle = capstyle
        self.arrowlength = arrowlength
        self.arrowwidth = arrowwidth
        self.clip = clip
        self.zorder = zorder
        self.visible = visible

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.p = [Point(util.mirrorx(p, centerx)) for p in self.p]
        if self.arrow:
            self.arrow = self.arrow[::-1].translate(self.arrow.maketrans('<>', '><'))

    def doflip(self) -> None:
        ''' Vertically flip the element '''
        self.p = [Point(util.flip(p)) for p in self.p]

    def xform(self, transform, **style) -> 'SegmentBezier':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: dict[str, Any] = {
            'color': self.color if self.color else style.get('color', None),
            'lw': self.lw if self.lw else style.get('lw', None),
            'ls': self.ls if self.ls else style.get('ls', None),
            'capstyle': self.capstyle if self.capstyle else style.get('capstyle', None),
            'arrow': self.arrow,
            'arrowlength': self.arrowlength,
            'arrowwidth': self.arrowwidth,
            'clip': self.clip,
            'zorder': self.zorder if self.zorder is not None else style.get('zorder', None),
            'visible': self.visible}
        style = {k: v for k, v in style.items() if params.get(k) is None and k in params.keys()}
        params.update(style)
        return SegmentBezier(transform.transform_array(self.p), **params)

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits (xmin, ymin, xmax, ymax)
        '''
        # Brute-force approximate from Bezier curve parametric equation
        t = util.linspace(0, 1, 50)
        px = [p.x for p in self.p]
        py = [p.y for p in self.p]
        if len(self.p) == 3:
            x = [(1-tt)**2 * px[0] + 2*(1-tt)*tt*px[1] + tt**2*px[2]
                 for tt in t]
            y = [(1-tt)**2 * py[0] + 2*(1-tt)*tt*py[1] + tt**2*py[2]
                 for tt in t]
        else:
            assert len(self.p) == 4
            x = [(1-tt)**3 * px[0] + 3*(1-tt)**2*tt*px[1] + 3*(1-tt)*tt**2*px[2] + tt**3*px[3]
                 for tt in t]
            y = [(1-tt)**3 * py[0] + 3*(1-tt)**2*tt*py[1] + 3*(1-tt)*tt**2*py[2] + tt**3*py[3]
                 for tt in t]
        return BBox(min(x), min(y), max(x), max(y))

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        if not self.visible:
            return
        p = transform.transform_array(self.p)
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)
        capstyle = self.capstyle if self.capstyle else style.get('capstyle', 'round')
        fig.bezier(p, color=color, lw=lw, ls=ls, capstyle=capstyle, clip=self.clip,
                   zorder=zorder, arrow=self.arrow,
                   arrowlength=self.arrowlength, arrowwidth=self.arrowwidth)


class SegmentArc:
    ''' An elliptical arc drawing segment

        Args:
            center: Center of the arc ellipse
            width: Width of the arc ellipse
            height: Height of the arc ellipse
            theta1: Starting angle in degrees
            theta2: Ending angle in degrees
            arrow: Direction of arrowhead ('cw' or 'ccw')
            angle: Rotation of the ellipse defining the arc
            color: Color for this segment
            lw: Line width for the segment
            ls: Line style for the segment
            clip: Bounding box to clip to
            zorder: Z-order for segment
            visible: Show the segment when drawn
    '''
    def __init__(self, center: XY,
                 width: float, height: float,
                 theta1: float = 35, theta2: float = -35,
                 arrow: Optional[Arcdirection] = None,
                 angle: float = 0,
                 color: Optional[str | tuple[float, float, float]] = None,
                 lw: Optional[float] = None,
                 ls: Optional[Linestyle] = None,
                 fill: Optional[str] = None,
                 clip: Optional[BBox] = None,
                 zorder: Optional[int] = None,
                 visible: bool = True):
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
        self.fill = fill
        self.clip = clip
        self.zorder = zorder
        self.visible = visible

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
        params: dict[str, Any] = {
            'color': self.color if self.color else style.get('color', None),
            'lw': self.lw if self.lw else style.get('lw', None),
            'ls': self.ls if self.ls else style.get('ls', None),
            'fill': self.fill if self.fill else style.get('fill', None),
            'clip': self.clip,
            'zorder': self.zorder if self.zorder is not None else style.get('zorder', None),
            'visible': self.visible}
        style = {k: v for k, v in style.items() if params.get(k) is None and k in params.keys()}
        params.update(style)
        return SegmentArc(transform.transform(self.center),
                          self.width*transform.zoom[0],
                          self.height*transform.zoom[1],
                          angle=angle,
                          arrow=self.arrow,
                          theta1=self.theta1,
                          theta2=self.theta2, **params)

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
        if not self.visible:
            return
        center = transform.transform(self.center)
        angle = self.angle + transform.theta

        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)
        fill = self.fill if self.fill else style.get('fill', None)

        width = self.width * transform.zoom[0]
        height = self.height * transform.zoom[1]
        fig.arc(center, width=width, height=height,
                theta1=self.theta1, theta2=self.theta2, angle=angle,
                color=color, lw=lw, ls=ls, fill=fill,
                clip=self.clip, zorder=zorder, arrow=self.arrow)


class SegmentPath:
    ''' Segment defined like svg <path> element made of
        M, L, C, Q, Z, etc....
    '''
    def __init__(self,
                 path: Sequence[XY | str], 
                 color: Optional[str | tuple[float, float, float]] = None,
                 lw: Optional[float] = None,
                 ls: Optional[Linestyle] = None,
                 capstyle: Optional[Capstyle] = None,
                 joinstyle: Optional[Joinstyle] = None,
                 fill: Optional[str] = None,
                 clip: Optional[BBox] = None,
                 zorder: Optional[int] = None,
                 visible: bool = True):
        self.path: Sequence[XY | str] = path  # Control points and strings 'M', 'L', 'C', etc.
        #drawing on SVG backend simply builds d into a <path>
        #drawing on MPL backend uses matplotlib.patches.PathPatch

        self.zorder = zorder
        self.color = color
        self.fill = fill
        self.lw = lw
        self.ls = ls
        self.clip = clip
        self.capstyle = capstyle
        self.joinstyle = joinstyle
        self.visible = visible

    def xform(self, transform, **style) -> 'SegmentPath':
        params: dict[str, Any] = {
            'zorder': self.zorder if self.zorder is not None else style.get('zorder', None),
            'color': self.color if self.color else style.get('color', None),
            'fill': self.fill if self.fill is not None else style.get('fill', None),
            'lw': self.lw if self.lw else style.get('lw', None),
            'ls': self.ls if self.ls else style.get('ls', None),
            'capstyle': self.capstyle if self.capstyle else style.get('capstyle', None),
            'joinstyle': self.joinstyle if self.joinstyle else style.get('joinstyle', None),
            'visible': self.visible}
        style = {k: v for k, v in style.items() if params.get(k) is None and k in params.keys()}
        params.update(style)

        xpath = []
        for p in self.path:
            try:  # Point
                xpath.append(transform.transform(Point(p)))  # type: ignore
            except TypeError:
                xpath.append(p)  # String

        return SegmentPath(xpath, **params)

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits: (xmin, ymin, xmax, ymax)
        '''
        x = [p[0] for p in self.path if not isinstance(p, str)]
        y = [p[1] for p in self.path if not isinstance(p, str)]
        return BBox(min(x), min(y), max(x), max(y))

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the path (flip horizontal about the center of the path) '''
        #self.path = [util.mirrorx(p, centerx) for p in self.path[::-1]]
        
    def doflip(self) -> None:
        ''' Vertically flip the element '''
        #self.path = [util.flip(p) for p in self.path]

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the segment

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        if not self.visible:
            return

        xpath = []
        for p in self.path:
            try:  # Point
                xpath.append(transform.transform(Point(p)))  # type: ignore
            except TypeError:
                xpath.append(p)  # String

        zorder = self.zorder if self.zorder is not None else style.get('zorder', 2)
        color = self.color if self.color else style.get('color', 'black')
        fill = self.fill if self.fill is not None else style.get('fill', None)
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)
        capstyle = self.capstyle if self.capstyle else style.get('capstyle', 'round')
        joinstyle = self.joinstyle if self.joinstyle else style.get('joinstyle', 'round')

        fig.path(xpath, color=color, fill=fill,
                 ls=ls, lw=lw, capstyle=capstyle, joinstyle=joinstyle,
                 clip=self.clip, zorder=zorder)


class SegmentImage:
    ''' PNG or SVG Image '''
    def __init__(self,
                 image: str | BinaryIO,
                 xy: Point = Point((0, 0)),   # Lower Left
                 width: float = 3,
                 height: float = 1,
                 rotate: float = 0,
                 imgfmt: Optional[str] = None,
                 zorder: Optional[int] = None):
        self.image = image
        self.xy = Point(xy)
        self.width = width
        self.height = height
        self.rotate = rotate
        self.imgfmt = imgfmt
        self.zorder = zorder
        self.visible = True

    def get_bbox(self) -> BBox:
        ''' Get bounding box (untransformed)

            Returns:
                Bounding box limits (xmin, ymin, xmax, ymax)
        '''
        if self.rotate % 360 == 0:
            return BBox(self.xy.x, self.xy.y, self.xy.x+self.width, self.xy.y+self.height)

        p1 = self.xy.rotate(self.rotate)
        p2 = (self.xy + Point((self.width, 0))).rotate(self.rotate)
        p3 = (self.xy + Point((self.width, self.height))).rotate(self.rotate)
        p4 = (self.xy + Point((0, self.height))).rotate(self.rotate)

        return BBox(
            min(p.x for p in (p1, p2, p3, p4)),
            min(p.y for p in (p1, p2, p3, p4)),
            max(p.x for p in (p1, p2, p3, p4)),
            max(p.y for p in (p1, p2, p3, p4))
            )


    def xform(self, transform, **style) -> 'SegmentImage':
        ''' Return a new Segment that has been transformed
            to its global position

            Args:
                transform: Transformation to apply
                style: Style parameters from Element to apply as default
        '''
        params: dict[str, Any] = {
            'zorder': self.zorder if self.zorder is not None else style.get('zorder', None)}
        
        style = {k: v for k, v in style.items() if params.get(k) is None and k in params.keys()}
        params.update(style)
        return SegmentImage(self.image, transform.transform(self.xy),
                            width=self.width*transform.zoom[0],
                            height=self.height*transform.zoom[1],
                            rotate=self.rotate+transform.theta,
                            imgfmt=self.imgfmt,
                             **params)

    def doreverse(self, centerx: float) -> None:
        ''' Reverse the image '''
        raise ValueError('Reversing an ElementImage is not supported.')

    def doflip(self) -> None:
        ''' Vertically flip the element '''
        raise ValueError('Flipping an ElementImage is not supported.')

    def draw(self, fig, transform, **style) -> None:
        ''' Draw the image

            Args:
                fig: schemdraw.Figure to draw on
                transform: Transform to apply before drawing
                style: Default style parameters
        '''
        if not self.visible:
            return

        xy = transform.transform(self.xy)
        width = self.width * transform.zoom[0]
        height = self.height * transform.zoom[1]
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        fig.image(self.image, xy,
                  width=width, height=height,
                  rotate=self.rotate+transform.theta,
                  imgfmt=self.imgfmt,
                  zorder=zorder)


SegmentType = Union[Segment, SegmentText, SegmentPoly, SegmentArc, SegmentCircle, SegmentBezier, SegmentPath, SegmentImage]
