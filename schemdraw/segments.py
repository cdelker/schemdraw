''' Schemdraw drawing segments. Each element is made up of one or more segments. '''

from collections import namedtuple
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

from .transform import mirror_point, mirror_array, flip_point

BBox = namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])


class Segment(object):
    ''' A segment (path), part of an Element.

        Parameters
        ----------
        path : array-like
            List of [x,y] coordinates making the path

        Keyword Arguments
        -----------------
        color : string
             Matplotlib color for this segment
        lw : float
            Line width for the segment
        ls : string
            Matplotlib line style for the segment
        capstyle : string
            Matplotlib capstyle for the segment
        joinstyle : string
            Matplotlib joinstyle for the segment
        fill : string
            Matplotlib color to fill (if path is closed)
        zorder : int
            Z-order for segment
    '''
    def __init__(self, path, **kwargs):
        self.path = np.asarray(path)  # Untranformed path
        self.zorder = kwargs.pop('zorder', 2)
        self.color = kwargs.get('color', 'black')
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')
        self.capstyle = kwargs.get('capstyle', 'round')
        self.joinstyle = kwargs.get('joinstyle', 'round')
        self.fill = kwargs.get('fill', None)
        self.kwargs = kwargs

    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.path[-1]
        
    def xform(self, transform):
        ''' Return a new Segment that has been transformed
            to its global position
        '''
        return Segment(transform.transform(self.path), **self.kwargs)

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        xmin = ymin = np.inf
        xmax = ymax = -np.inf
        for p in self.path:
            xmin = min(xmin, p[0])
            ymin = min(ymin, p[1])
            xmax = max(xmax, p[0])
            ymax = max(ymax, p[1])
        return BBox(xmin, ymin, xmax, ymax)

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the center of the path) '''
        self.path = mirror_array(self.path, centerx)[::-1]
    
    def doflip(self):
        ''' Vertically flip the element '''
        flipped = []
        for p in self.path:
            flipped.append(flip_point(p))
        self.path = flipped
    
    def draw(self, ax, transform):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        path = transform.transform_array(self.path)

        if self.fill is not None:
            fill = self.color if self.fill is True else self.fill
            tlist = list(map(tuple, path))  # Need path as tuples for set()
            if len(tlist) != len(set(tlist)):  # Duplicate points - assume closed shape
                ax.fill(path[:, 0], path[:, 1], color=fill, zorder=self.zorder)

        ax.plot(path[:, 0], path[:, 1], color=self.color, lw=self.lw,
                solid_capstyle=self.capstyle, solid_joinstyle=self.joinstyle,
                ls=self.ls, zorder=self.zorder)


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
             Matplotlib color for this segment
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
        self.align = kwargs.get('align', ('center', 'center'))
        self.font = kwargs.get('font', 'sans-serif')
        self.fontsize = kwargs.get('fontsize', kwargs.get('size', 14))
        self.color = kwargs.get('color', 'black')
        self.rotation = kwargs.get('rotation', 0)
        self.rotation_mode = kwargs.get('rotation_mode', 'anchor')  # 'anchor' or 'default'
        self.zorder = kwargs.get('zorder', 3)
        self.kwargs = kwargs

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''        
        self.xy = mirror_point(self.xy, centerx)
    
    def doflip(self):
        ''' Vertically flip the element '''
        self.xy = flip_point(self.xy)

    def xform(self, transform):
        ''' Return a new Segment that has been transformed '''
        return SegmentText(transform.transform(self.xy), self.text, **self.kwargs)

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

    def draw(self, ax, transform):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        xy = transform.transform(self.xy)
        ax.text(xy[0], xy[1], self.text, transform=ax.transData,
                color=self.color, fontsize=self.fontsize, family=self.font, rotation=self.rotation,
                horizontalalignment=self.align[0], verticalalignment=self.align[1],
                zorder=self.zorder, rotation_mode=self.rotation_mode)
        

class SegmentPoly(object):
    ''' A polygon segment

        Parameters
        ----------
        xy : array-like
            List of [x,y] coordinates making the polygon
        transform : Transform instance
            Transformation for the path to drawing coordinates

        Keyword Arguments
        -----------------
        closed : bool
            Draw a closed polygon (default True)
        color : string
            Matplotlib color for this segment
        lw : float
            Line width for the segment
        ls : string
            Matplotlib line style for the segment
        fill : string
            Matplotlib color to fill (if path is closed)
        zorder : int
            Z-order for segment
    '''
    def __init__(self, verts, **kwargs):
        self.verts = verts
        self.closed = kwargs.get('closed', True)
        self.color = kwargs.get('color', 'black')
        self.fill = kwargs.get('fill', None)
        self.joinstyle = kwargs.get('joinstyle', 'round')
        self.capstyle = kwargs.get('capstyle', 'round')
        self.zorder = kwargs.pop('zorder', 1)
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')
        self.kwargs = kwargs

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''        
        self.verts = mirror_array(self.verts, centerx)[::-1]
    
    def doflip(self):
        ''' Vertically flip the element '''        
        flipped = []
        for p in self.verts:
            flipped.append(flip_point(p))
        self.verts = flipped
        
    def xform(self, transform):
        ''' Return a new Segment that has been transformed '''
        return SegmentPoly(transform.transform(self.verts), **self.kwargs)

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
        xmin = ymin = np.inf
        xmax = ymax = -np.inf
        for v in self.verts:
            xmin = min(xmin, v[0])
            ymin = min(ymin, v[1])
            xmax = max(xmax, v[0])
            ymax = max(ymax, v[1])
        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, ax, transform):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        if self.fill is True:
            fillcolor = self.color
            dofill = True
        elif self.fill is not None:
            fillcolor = self.fill
            dofill = True
        else:
            dofill = False
            fillcolor = None

        verts = transform.transform(self.verts)
        poly = plt.Polygon(xy=verts, closed=self.closed, ec=self.color,
                           fc=fillcolor, fill=dofill, lw=self.lw, ls=self.ls,
                           capstyle=self.capstyle, joinstyle=self.joinstyle,
                           zorder=self.zorder)
        ax.add_patch(poly)

        
        
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
             Matplotlib color for this segment
        lw : float
            Line width for the segment
        ls : string
            Matplotlib line style for the segment
        fill : string
            Matplotlib color to fill (if path is closed)
        zorder : int
            Z-order for segment
    '''
    def __init__(self, center, radius, **kwargs):
        self.center = np.asarray(center)
        self.radius = radius
        self.zorder = kwargs.pop('zorder', 1)
        self.color = kwargs.get('color', 'black')
        self.fill = kwargs.get('fill', None)
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')
        self.ref = kwargs.get('ref', None)
        self.kwargs = kwargs

    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.center

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.center = mirror_point(self.center, centerx)

    def doflip(self):
        self.cener = flip_point(self.center)
    
    def xform(self, transform):
        ''' Return a new Segment that has been transformed '''
        return SegmentCircle(transform.transform(self.center), self.radius, **self.kwargs)

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        center = self.center
        xmin = center[0] - self.radius
        xmax = center[0] + self.radius
        ymin = center[1] - self.radius
        ymax = center[1] + self.radius
        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, ax, transform):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        center = transform.transform(self.center, self.ref)
        radius = transform.zoom * self.radius

        if self.fill is True:
            fillcolor = self.color
            dofill = True
        elif self.fill is not None:
            fillcolor = self.fill
            dofill = True
        else:
            dofill = False
            fillcolor = None
        
        circ = plt.Circle(xy=center, radius=radius,
                          ec=self.color, fc=fillcolor, fill=dofill,
                          lw=self.lw, ls=self.ls,
                          zorder=self.zorder)
        ax.add_patch(circ)

        
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
             Matplotlib color for this segment
        lw : float
            Line width for the segment
        ls : string
            Matplotlib line style for the segment
        zorder : int
            Z-order for segment
    '''
    def __init__(self, tail, head, **kwargs):
        self.tail = tail
        self.head = head
        self.zorder = kwargs.pop('zorder', 1)
        self.headwidth = kwargs.get('headwidth', .1)
        self.headlength = kwargs.get('headlength', .2)
        self.color = kwargs.get('color', 'black')
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')
        self.ref = kwargs.get('ref', None)
        self.kwargs = kwargs

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.tail = mirror_point(self.tail, centerx)
        self.head = mirror_point(self.head, centerx)
    
    def doflip(self):
        self.tail = flip_point(self.tail)###[self.tail[0], -self.tail[1]]
        self.head = flip_point(self.head)####[self.head[0], -self.head[1]]        

    def xform(self, transform):
        ''' Return a new Segment that has been transformed '''
        return SegmentArrow(transform.transform(self.tail), transform.transform(self.head), **self.kwargs)

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        xmin = min(self.tail[0], self.head[0])
        ymin = min(self.tail[1], self.head[1])
        xmax = max(self.tail[0], self.head[0])
        ymax = max(self.tail[1], self.head[1])
        return BBox(xmin, ymin, xmax, ymax)

    def end(self):
        ''' Get endpoint of this segment, untransformed '''        
        return self.head
    
    def draw(self, ax, transform):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        tail = transform.transform(self.tail, ref=self.ref)
        head = transform.transform(self.head, ref=self.ref)
        ax.arrow(tail[0], tail[1],
                 head[0]-tail[0], head[1]-tail[1],
                 head_width=self.headwidth, head_length=self.headlength,
                 length_includes_head=True, color=self.color, lw=self.lw,
                 zorder=self.zorder)


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
        transform : Transform instance
            Transformation for the path to drawing coordinates

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
             Matplotlib color for this segment
        lw : float
            Line width for the segment
        ls : string
            Matplotlib line style for the segment
        fill : string
            Matplotlib color to fill (if path is closed)
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
        self.color = kwargs.get('color', 'black')
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')
        self.zorder = kwargs.get('zorder', 1)
        self.angle = kwargs.get('angle', 0)
        self.kwargs = kwargs

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

    def xform(self, transform):
        ''' Return a new Segment that has been transformed '''
        kwargs = self.kwargs.copy()
        kwargs['angle'] = self.angle + transform.theta
        return SegmentArc(transform.transform(self.center), self.width, self.height, **kwargs)

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
        t = np.deg2rad(np.linspace(self.theta1, self.theta2, num=500))
        phi = np.deg2rad(self.angle)        
        rx = self.width/2
        ry = self.height/2
        xx = self.center[0] + rx * np.cos(t)*np.cos(phi) - ry * np.sin(t)*np.sin(phi)
        yy = self.center[1] + rx * np.cos(t)*np.sin(phi) + ry * np.sin(t)*np.cos(phi)
        return BBox(xx.min(), yy.min(), xx.max(), yy.max())
#        xmin = self.center[0] - self.width
#        ymin = self.center[1] - self.height
#        xmax = self.center[0] + self.width
#        ymax = self.center[1] + self.height
#        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, ax, transform):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
                Axis to draw on
            transform : Transform
                Transform to apply before drawing
        '''
        center = transform.transform(self.center)
        angle = self.angle + transform.theta
        arc = Arc(center, width=self.width, height=self.height,
                  theta1=self.theta1, theta2=self.theta2, angle=angle,
                  color=self.color, lw=self.lw, ls=self.ls, zorder=self.zorder)
        ax.add_patch(arc)

        if self.arrow is not None:
            # Apply stretch to theta to match MPL's arc
            # (See change https://github.com/matplotlib/matplotlib/pull/8047/files)
            x, y = np.cos(np.deg2rad(self.theta2)), np.sin(np.deg2rad(self.theta2))
            th2 = np.rad2deg(np.arctan2((self.width/self.height)*y, x))
            x, y = np.cos(np.deg2rad(self.theta1)), np.sin(np.deg2rad(self.theta1))
            th1 = np.rad2deg(np.arctan2((self.width/self.height)*y, x))
            if self.arrow == 'ccw':
                dx = np.cos(np.deg2rad(th2+90)) / 100
                dy = np.sin(np.deg2rad(self.theta2+90)) / 100
                s = [center[0] + self.width/2*np.cos(np.deg2rad(th2)),
                     center[1] + self.height/2*np.sin(np.deg2rad(th2))]
            else:
                dx = -np.cos(np.deg2rad(th1+90)) / 100
                dy = - np.sin(np.deg2rad(th1+90)) / 100

                s = [center[0] + self.width/2*np.cos(np.deg2rad(th1)),
                     center[1] + self.height/2*np.sin(np.deg2rad(th1))]

            # Rotate the arrow head
            co = np.cos(np.radians(angle))
            so = np.sin(np.radians(angle))
            m = np.array([[co, so], [-so, co]])
            s = np.dot(s-center, m)+center
            darrow = np.dot([dx, dy], m)

            ax.arrow(s[0], s[1], darrow[0], darrow[1], head_width=.15,
                     head_length=.25, color=self.color, zorder=self.zorder)
        