''' Schemdraw drawing segments.
    Each element is made up of one or more segments.
'''

from collections import namedtuple
import numpy as np

from .transform import mirror_point, mirror_array, flip_point

BBox = namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])


def roundcorners(verts, radius=.5):
    ''' Round the corners of polygon defined by verts.
        Works for convex polygons assuming radius fits inside.
    
        Parameters
        ----------
        verts : list
            List of (x,y) pairs defining corners of polygon
        radius : float
            Radius of curvature
    
        Adapted from:
        https://stackoverflow.com/questions/24771828/algorithm-for-creating-rounded-corners-in-a-polygon
    '''
    poly = []
    for v in range(len(verts))[::-1]:
        p1 = verts[v]
        p2 = verts[v-1]
        p3 = verts[v-2]

        dx1 = p2[0]-p1[0]
        dy1 = p2[1]-p1[1]
        dx2 = p2[0]-p3[0]
        dy2 = p2[1]-p3[1]

        angle = (np.arctan2(dy1, dx1) - np.arctan2(dy2, dx2))/2
        tan = abs(np.tan(angle))
        segment = radius/tan

        def getlength(x, y):
            return np.sqrt(x*x + y*y)

        def getproportionpoint(point, segment, length, dx, dy):
            factor = segment/length
            return np.asarray([point[0]-dx * factor,
                               point[1]-dy * factor])

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
        startangle = np.arctan2(p1cross[1] - circlepoint[1], p1cross[0]-circlepoint[0])
        endangle = np.arctan2(p2cross[1] - circlepoint[1], p2cross[0]-circlepoint[0])        
        startangle, endangle = np.unwrap([startangle, endangle])
        
        arc = []
        for i in np.linspace(startangle, endangle, 100):
            arc.append([circlepoint[0] + np.cos(i)*radius,
                        circlepoint[1] + np.sin(i)*radius])

        poly.extend(arc)
    poly.append(poly[0])  # Close the loop
    return np.asarray(poly)


class Segment(object):
    ''' A segment (path), part of an Element.

        Parameters
        ----------
        path : array-like
            List of [x,y] coordinates making the path

        Keyword Arguments
        -----------------
        color : string
             Color for this segment
        lw : float
            Line width for the segment
        ls : string
            Line style for the segment '-', '--', ':', etc.
        capstyle : string
            Capstyle for the segment: 'round', 'miter', or 'bevel'
        joinstyle : string
            Joinstyle for the segment: 'round', 'miter', or 'bevel'
        fill : string
            Color to fill if path is closed
        zorder : int
            Z-order for segment
    '''
    def __init__(self, path, **kwargs):
        self.path = np.asarray(path)  # Untranformed path
        self.zorder = kwargs.get('zorder', None)
        self.color = kwargs.get('color', None)
        self.fill = kwargs.get('fill', None)
        self.lw = kwargs.get('lw', None)
        self.ls = kwargs.get('ls', None)
        self.capstyle = kwargs.get('capstyle', None)
        self.joinstyle = kwargs.get('joinstyle', None)

    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.path[-1]

    def xform(self, transform, **style):
        ''' Return a new Segment that has been transformed
            to its global position

            Parameters
            ----------
            transform : schemdraw.Transform
                Transformation to apply
            style : Style keyword arguments from Element to apply as default
        '''
        params = {'zorder': self.zorder,
                  'color': self.color,
                  'fill': self.fill,
                  'lw': self.lw,
                  'ls': self.ls,
                  'capstyle': self.capstyle,
                  'joinstyle': self.joinstyle}
        params.update(style)
        return Segment(transform.transform(self.path), **params)

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        x = [p[0] for p in self.path]
        y = [p[1] for p in self.path]
        return BBox(min(x), min(y), max(x), max(y))

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the center of the path) '''
        self.path = mirror_array(self.path, centerx)[::-1]

    def doflip(self):
        ''' Vertically flip the element '''
        flipped = []
        for p in self.path:
            flipped.append(flip_point(p))
        self.path = flipped

    def draw(self, fig, transform, **style):
        ''' Draw the segment

            Parameters
            ----------
            fig : schemdraw.Figure
                Figure to draw on
            transform : Transform
                Transform to apply before drawing
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

        fig.plot(path[:, 0], path[:, 1], color=color, fill=fill,
                 ls=ls, lw=lw, capstyle=capstyle, joinstyle=joinstyle,
                 zorder=zorder)


class SegmentText(object):
    ''' A text drawing segment

        Parameters
        ----------
        pos : [x, y] array
            Coordinates for text
        label : string
            Text to draw

        Keyword Arguments
        -----------------
        align : tuple
            Tuple of (horizontal, vertical) alignment where horizontal
            is ['center', 'left', 'right'] and vertical is ['center',
            'top', 'bottom']
        rotation : float
            Rotation angle (degrees)
        rotation_mode : string
            See Matplotlib documentation. 'anchor' or 'default'.
        color : string
             Color for this segment
        fontsize : float
            Font size
        font : string
            Font name/family
        zorder : int
            Z-order for segment
    '''
    def __init__(self, pos, label, **kwargs):
        self.xy = pos
        self.text = label
        self.align = kwargs.get('align', None)
        self.font = kwargs.get('font', None)
        self.fontsize = kwargs.get('fontsize', None)
        self.color = kwargs.get('color', None)
        self.rotation = kwargs.get('rotation', None)
        self.rotation_mode = kwargs.get('rotation_mode', None)
        self.zorder = kwargs.get('zorder', None)

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.xy = mirror_point(self.xy, centerx)

    def doflip(self):
        ''' Vertically flip the element '''
        self.xy = flip_point(self.xy)

    def xform(self, transform, **style):
        ''' Return a new Segment that has been transformed with all
            styling applied
        '''
        params = {'align': self.align,
                  'font': self.font,
                  'fontsize': self.fontsize,
                  'color': self.color,
                  'rotation': self.rotation,
                  'rotation_mode': self.rotation_mode,
                  'zorder': self.zorder}
        params.update(style)
        return SegmentText(transform.transform(self.xy),
                           self.text, **params)

    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.xy

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        # Matplotlib doesn't know text dimensions until AFTER it is drawn
        return BBox(np.inf, np.inf, -np.inf, -np.inf)

    def draw(self, fig, transform, **style):
        ''' Draw the segment

            Parameters
            ----------
            fig : schemdraw.Figure
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
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


class SegmentPoly(object):
    ''' A polygon segment

        Parameters
        ----------
        xy : array-like
            List of [x,y] coordinates making the polygon

        Keyword Arguments
        -----------------
        closed : bool
            Draw a closed polygon (default True)
        cornerradius : float
            Round the corners to this radius (0 for no rounding)
        color : string
            Color for this segment
        lw : float
            Line width for the segment
        ls : string
            Line style for the segment
        fill : string
            Color to fill if path is closed
        zorder : int
            Z-order for segment
    '''
    def __init__(self, verts, **kwargs):
        self.verts = verts
        self.closed = kwargs.get('closed', None)
        self.cornerradius = kwargs.get('cornerradius', 0)
        self.color = kwargs.get('color', None)
        self.fill = kwargs.get('fill', None)
        self.joinstyle = kwargs.get('joinstyle', None)
        self.capstyle = kwargs.get('capstyle', None)
        self.zorder = kwargs.pop('zorder', None)
        self.lw = kwargs.get('lw', None)
        self.ls = kwargs.get('ls', None)

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.verts = mirror_array(self.verts, centerx)[::-1]

    def doflip(self):
        ''' Vertically flip the element '''
        flipped = []
        for p in self.verts:
            flipped.append(flip_point(p))
        self.verts = flipped

    def xform(self, transform, **style):
        ''' Return a new Segment that has been transformed '''
        params = {'color': self.color,
                  'fill': self.fill,
                  'joinstyle': self.joinstyle,
                  'capstyle': self.capstyle,
                  'lw': self.lw,
                  'ls': self.ls,
                  'cornerradius': self.cornerradius,
                  'zorder': self.zorder}
        params.update(style)
        return SegmentPoly(transform.transform(self.verts), **params)

    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.verts[-1]

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        x = [p[0] for p in self.verts]
        y = [p[1] for p in self.verts]
        return BBox(min(x), min(y), max(x), max(y))

    def draw(self, fig, transform, **style):
        ''' Draw the segment

            Parameters
            ----------
            fig : schemdraw.Figure
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        closed = self.closed if self.closed is not None else style.get('closed', True)
        fill = self.fill if self.fill is not None else style.get('fill', None)
        color = self.color if self.color else style.get('color', 'black')
        joinstyle = self.joinstyle if self.joinstyle else style.get('joinstyle', 'round')
        capstyle = self.capstyle if self.capstyle else style.get('capstyle', 'round')
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        lw = self.lw if self.lw else style.get('lw', 2)
        ls = self.ls if self.ls else style.get('ls', '-')

        fill = color if fill is True else None if fill is False else fill
        verts = transform.transform(self.verts)
        
        if self.cornerradius > 0:
            verts = roundcorners(verts, self.cornerradius)
        
        fig.poly(verts, closed=closed, color=color, fill=fill, lw=lw, ls=ls,
                 capstyle=capstyle, joinstyle=joinstyle, zorder=zorder)


class SegmentCircle(object):
    ''' A circle drawing segment

        Parameters
        ----------
        center : [x, y] array
            Center of the circle
        radius : float
            Radius of the circle

        Keyword Arguments
        -----------------
        color : string
             Color for this segment
        lw : float
            Line width for the segment
        ls : string
            Line style for the segment
        fill : string
            Color to fill if path is closed
        zorder : int
            Z-order for segment
        ref: string
            Flip reference ['start', 'end', None].
    '''
    def __init__(self, center, radius, **kwargs):
        self.center = np.asarray(center)
        self.radius = radius
        self.zorder = kwargs.pop('zorder', None)
        self.color = kwargs.get('color', None)
        self.fill = kwargs.get('fill', None)
        self.lw = kwargs.get('lw', None)
        self.ls = kwargs.get('ls', None)

        # Reference for adding things AFTER lead extensions
        self.endref = kwargs.get('ref', None)

    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.center

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.center = mirror_point(self.center, centerx)
        self.endref = {None: None, 'start': 'end', 'end': 'start'}.get(self.endref)

    def doflip(self):
        ''' Flip the segment up/down '''
        self.center = flip_point(self.center)

    def xform(self, transform, **style):
        ''' Return a new Segment that has been transformed '''
        params = {'zorder': self.zorder,
                  'color': self.color,
                  'fill': self.fill,
                  'lw': self.lw,
                  'ls': self.ls,
                  'ref': self.endref}
        params.update(style)
        return SegmentCircle(transform.transform(self.center, self.endref),
                             self.radius, **params)

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        xmin = self.center[0] - self.radius
        xmax = self.center[0] + self.radius
        ymin = self.center[1] - self.radius
        ymax = self.center[1] + self.radius
        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, fig, transform, **style):
        ''' Draw the segment

            Parameters
            ----------
            fig : schemdraw.Figure
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
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


class SegmentArrow(object):
    ''' An arrow drawing segment

        Parameters
        ----------
        start : [x, y] array
            Start coordinate of arrow
        end : [x, y] array
            End (head) coordinate of arrow

        Keyword Arguments
        -----------------
        headwidth : float
            Width of arrowhead
        headlength : float
            Lenght of arrowhead
        color : string
             Color for this segment
        lw : float
            Line width for the segment
        ls : string
            Line style for the segment
        zorder : int
            Z-order for segment
    '''
    def __init__(self, tail, head, **kwargs):
        self.tail = tail
        self.head = head
        self.zorder = kwargs.pop('zorder', None)
        self.headwidth = kwargs.get('headwidth', None)
        self.headlength = kwargs.get('headlength', None)
        self.color = kwargs.get('color', None)
        self.lw = kwargs.get('lw', None)
        self.ls = kwargs.get('ls', None)
        self.endref = kwargs.get('ref', None)

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.tail = mirror_point(self.tail, centerx)
        self.head = mirror_point(self.head, centerx)
        self.endref = {None: None, 'start': 'end', 'end': 'start'}.get(self.endref)

    def doflip(self):
        self.tail = flip_point(self.tail)
        self.head = flip_point(self.head)

    def xform(self, transform, **style):
        ''' Return a new Segment that has been transformed '''
        params = {'zorder': self.zorder,
                  'color': self.color,
                  'ls': self.ls,
                  'lw': self.lw,
                  'headwidth': self.headwidth,
                  'headlength': self.headlength,
                  'ref': self.endref}
        params.update(style)
        return SegmentArrow(transform.transform(self.tail, ref=self.endref),
                            transform.transform(self.head, ref=self.endref),
                            **params)

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        hw = self.headwidth if self.headwidth else .1
        xmin = min(self.tail[0], self.head[0])
        ymin = min(self.tail[1], self.head[1]-hw)
        xmax = max(self.tail[0], self.head[0])
        ymax = max(self.tail[1], self.head[1]+hw)
        return BBox(xmin, ymin, xmax, ymax)

    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.head

    def draw(self, fig, transform, **style):
        ''' Draw the segment

            Parameters
            ----------
            fig : schemdraw.Figure
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        tail = transform.transform(self.tail, ref=self.endref)
        head = transform.transform(self.head, ref=self.endref)
        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)
        headwidth = self.headwidth if self.headwidth else style.get('headwidth', .2)
        headlength = self.headlength if self.headlength else style.get('headlength', .2)

        fig.arrow(tail[0], tail[1], head[0]-tail[0], head[1]-tail[1],
                  headwidth=headwidth, headlength=headlength,
                  color=color, lw=lw, zorder=zorder)


class SegmentArc(object):
    ''' An arc drawing segment

        Parameters
        ----------
        center : [x, y] array
            Center of the circle
        width : float
            Width of the arc ellipse
        height : float
            Height of the arc ellipse
        reverse : bool
            Element has been reversed

        Keyword Arguments
        -----------------
        theta1 : float
            Starting angle (degrees)
        theta2 : float
            Ending angle (degrees)
        angle : float
            Rotation of the ellipse defining the arc
        arrow : [None, 'cw', 'ccw']
            Direction of arrowhead
        color : string
             Color for this segment
        lw : float
            Line width for the segment
        ls : string
            Line style for the segment
        fill : string
            Color to fill if path is closed
        zorder : int
            Z-order for segment
    '''
    def __init__(self, center, width, height, **kwargs):
        self.center = center
        self.width = width
        self.height = height
        self.theta1 = kwargs.get('theta1', 35)
        self.theta2 = kwargs.get('theta2', -35)
        self.arrow = kwargs.get('arrow', None)  # cw or ccw
        self.angle = kwargs.get('angle', 0)
        self.color = kwargs.get('color', None)
        self.lw = kwargs.get('lw', None)
        self.ls = kwargs.get('ls', None)
        self.zorder = kwargs.get('zorder', None)

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.center = mirror_point(self.center, centerx)
        self.theta1, self.theta2 = 180-self.theta2, 180-self.theta1
        self.arrow = {'cw': 'ccw', 'ccw': 'cw'}.get(self.arrow, None)

    def doflip(self):
        ''' Vertically flip the element '''
        self.center = flip_point(self.center)
        self.theta1, self.theta2 = -self.theta2, -self.theta1
        self.arrow = {'cw': 'ccw', 'ccw': 'cw'}.get(self.arrow, None)

    def xform(self, transform, **style):
        ''' Return a new Segment that has been transformed '''
        angle = self.angle + transform.theta
        params = {'color': self.color,
                  'lw': self.lw,
                  'ls': self.ls,
                  'zorder': self.zorder}
        params.update(style)
        return SegmentArc(transform.transform(self.center),
                          self.width, self.height, angle=angle,
                          theta1=self.theta1, theta2=self.theta2, **params)

    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.center

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        # Who wants to do trigonometry when we can just brute-force the bounding box?
        theta1, theta2 = self.theta1, self.theta2
        while theta2 < theta1:
            theta2 += 360
        t = np.deg2rad(np.linspace(theta1, theta2, num=500))
        phi = np.deg2rad(self.angle)
        rx = self.width/2
        ry = self.height/2
        xx = self.center[0] + rx * np.cos(t)*np.cos(phi) - ry * np.sin(t)*np.sin(phi)
        yy = self.center[1] + rx * np.cos(t)*np.sin(phi) + ry * np.sin(t)*np.cos(phi)
        return BBox(xx.min(), yy.min(), xx.max(), yy.max())

    def draw(self, fig, transform, **style):
        ''' Draw the segment

            Parameters
            ----------
            fig : schemdraw.Figure
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        center = transform.transform(self.center)
        angle = self.angle + transform.theta

        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)

        fig.arc(center, width=self.width, height=self.height,
                theta1=self.theta1, theta2=self.theta2, angle=angle,
                color=color, lw=lw, ls=ls, zorder=zorder, arrow=self.arrow)
