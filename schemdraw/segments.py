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
    
    def draw(self, ax, transform, **style):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
                Axis to draw on
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
            fill = color if fill is True else fill
            tlist = list(map(tuple, path))  # Need path as tuples for set()
            if len(tlist) != len(set(tlist)):  # Path has duplicates
                ax.fill(path[:, 0], path[:, 1], color=fill, zorder=zorder)
                
        ax.plot(path[:, 0], path[:, 1], zorder=zorder, color=color,
                ls=ls, lw=lw, solid_capstyle=capstyle, solid_joinstyle=joinstyle)


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
                  'zorder': self.zorder
                 }
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

    def draw(self, ax, transform, **style):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
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
        
        ax.text(xy[0], xy[1], self.text, transform=ax.transData,
                color=color, fontsize=fontsize, family=font, rotation=rotation,
                horizontalalignment=align[0], verticalalignment=align[1],
                zorder=zorder, rotation_mode=rotmode)
        

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
        self.closed = kwargs.get('closed', None)
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

    def draw(self, ax, transform, **style):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
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
        
        if fill is True:
            fillcolor = color
            dofill = True
        elif fill is False or fill is None:
            dofill = False
            fillcolor = None
        else:
            fillcolor = fill
            dofill = True

        verts = transform.transform(self.verts)
        poly = plt.Polygon(xy=verts, closed=closed, ec=color,
                           fc=fillcolor, fill=dofill, lw=lw, ls=ls,
                           capstyle=capstyle, joinstyle=joinstyle,
                           zorder=zorder)
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
        self.endref = kwargs.get('ref', None)  # Reference for adding things AFTER lead extensions
        
    def end(self):
        ''' Get endpoint of this segment, untransformed '''
        return self.center

    def doreverse(self, centerx):
        ''' Reverse the path (flip horizontal about the centerx point) '''
        self.center = mirror_point(self.center, centerx)
        self.endref = {None: None, 'start': 'end', 'end': 'start'}.get(self.endref)
        
    def doflip(self):
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

    def draw(self, ax, transform, **style):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
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

        if fill is True:
            fillcolor = color
            dofill = True
        elif fill is False or fill is None:
            dofill = False
            fillcolor = None
        else:
            fillcolor = fill
            dofill = True
        
        circ = plt.Circle(xy=center, radius=radius,
                          ec=color, fc=fillcolor, fill=dofill,
                          lw=lw, ls=ls,
                          zorder=zorder)
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
    
    def draw(self, ax, transform, **style):
        ''' Draw the segment
        
            Parameters
            ----------
            ax : Matplotlib axis
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
        
        ax.arrow(tail[0], tail[1],
                 head[0]-tail[0], head[1]-tail[1],
                 head_width=headwidth, head_length=headlength,
                 length_includes_head=True, color=color, lw=lw,
                 zorder=zorder)


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
        return SegmentArc(transform.transform(self.center), self.width, self.height, 
                          angle=angle, theta1=self.theta1, theta2=self.theta2,
                          **params)

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

    def draw(self, ax, transform, **style):
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

        zorder = self.zorder if self.zorder is not None else style.get('zorder', 1)
        color = self.color if self.color else style.get('color', 'black')
        ls = self.ls if self.ls else style.get('ls', '-')
        lw = self.lw if self.lw else style.get('lw', 2)
        
        arc = Arc(center, width=self.width, height=self.height,
                  theta1=self.theta1, theta2=self.theta2, angle=angle,
                  color=color, lw=lw, ls=ls, zorder=zorder)
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
                     head_length=.25, color=color, zorder=zorder)
        