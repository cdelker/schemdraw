'''
SchemDraw - Electrical Schematic Drawing

https://cdelker.bitbucket.io/SchemDraw/
'''

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.patches import Arc
import copy
from collections import namedtuple

from . import elements

# Set up matplotlib parameters
mpl.rcParams['figure.subplot.left']   = 0.05
mpl.rcParams['figure.subplot.bottom'] = 0.05
mpl.rcParams['figure.subplot.right']  = 0.95
mpl.rcParams['figure.subplot.top']    = 0.90
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['mathtext.fontset'] = 'stixsans'
mpl.rcParams['mathtext.default'] = 'regular'

# Define transformation matricies
mirror_matrix = np.array([[-1, 0], [0, 1]])
flip_matrix = np.array([[1, 0], [0, -1]])
BBox = namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])


def _angle(a, b):
    ''' Compute angle from coordinate a to b '''
    theta = np.degrees(np.arctan2(b[1] - a[1], (b[0] - a[0])))
    return theta


def _distance(a, b):
    ''' Compute distance from A to B '''
    r = np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return r


def _flatten_elements(elm_def):
    ''' Combine element with its base elements. '''
    while 'base' in elm_def:
        base_elm = elm_def['base']
        elm_def.pop('base')

        elm_def['paths'] = elm_def.get('paths', []) + base_elm.get('paths',  [])
        elm_def['labels'] = elm_def.get('labels', []) + base_elm.get('labels', [])
        elm_def['shapes'] = elm_def.get('shapes', []) + base_elm.get('shapes', [])

        # New anchors with same name should overwrite old
        d = base_elm.get('anchors', {}).copy()
        d.update(elm_def.get('anchors', {}))
        elm_def['anchors'] = d

        for i in base_elm:
            # Everything that's not a list. New key/values overwrite old.
            # If base has a base, will be added and loop will pick it up.
            if i not in ['paths', 'labels', 'shapes', 'anchors'] and i not in elm_def:
                elm_def[i] = base_elm[i]
    return elm_def


def group_elements(drawing, anchors=None):
    ''' Combine all elements in a drawing into a single element that can be added to
        another drawing. Returns an element definition.

        Parameters
        ----------
        drawing: Drawing
            The Drawing object. All elements in this drawing will be combined.
        anchors: dict (optional)
            New anchor dictionary to use for the new element.
    '''
    elmdef = {'paths': [],
              'pathparams': [],
              'shapes': [],
              'labels': [],
              'extend': False}
    for elm in drawing.elements:
        for segment in elm.segments:
            newdef = segment.getdef()
            elmdef['paths'].extend(newdef.get('paths', []))
            elmdef['pathparams'].extend(newdef.get('pathparams', []))
            elmdef['shapes'].extend(newdef.get('shapes', []))
            elmdef['labels'].extend(newdef.get('labels', []))

    if anchors is not None:
        elmdef['anchors'] = anchors

    elmdef['drop'] = drawing.here
    return elmdef


class Drawing(object):
    ''' Set up a new circuit drawing.

        Parameters
        ----------
        unit: float
            Default length of a 2-terminal element, including leads.
            The zigzag portion of resistor element is length 1 unit.
        inches_per_unit: float
            Inches per unit to scale drawing into real dimensions
        txtofst: float
            Default distance from element to text label
        fontsize: int
            Default font size for labels
        font: string
            matplotlib font-family

        Attributes
        ----------
        here: [x, y] float array
            Current x, y drawing position
        theta: float
            Current drawing angle (degrees)
        elements: list
            List of Element objects added to the Drawing

        Keyword Arguments
        -----------------
        color: string
            Matplotlib color name to apply to all circuit elements
        lw: float
            Default line width
        ls: string
            Default Matplotlib line style
    '''
    def __init__(self, unit=3.0, inches_per_unit=0.5, txtofst=0.1, fontsize=16, font='sans-serif', **kwargs):
        self.unit = unit
        self.inches_per_unit = inches_per_unit
        self.txtofst = txtofst
        self.fontsize = fontsize
        self.font = font
        self.params = kwargs

        # Drawing state variables
        self.here = np.array([0, 0])
        self.theta = 0
        self._state = []
        self.elements = []

    def add(self, elm_def, **kwargs):
        ''' Create an Element object and add it to the schematic.

            Parameters
            ----------
            elm_def: dict
                Element definition dictionary (see Element class)

            Keyword Arguments
            -----------------
            move_cur : bool
                Move the Drawing.here position after drawing this element.
                (Default True)

            See Element class for full list of Keyword Arguments.

            Returns
            -------
            elm : Element instance
                The new element
        '''
        e = Element(elm_def, self, **kwargs)
        self.elements.append(e)
        if kwargs.get('move_cur', True) and elm_def.get('move_cur', True):
            self.here = e.here
            self.theta = e.theta
        return e

    def push(self):
        ''' Push/save the drawing state. Drawing.here and Drawing.theta are saved. '''
        self._state.append((self.here, self.theta))

    def pop(self):
        ''' Pop/load the drawing state. Location and angle are returned to
            previously pushed state.
        '''
        if len(self._state) > 0:
            self.here, self.theta = self._state.pop()

    def draw(self, ax=None, showframe=False, showplot=True):
        ''' Draw the diagram.

            Parameters
            ----------
            ax : Matplotlib Axis
                Axis to draw on. If omitted, new axis will be created.
            showframe : bool
                Show the plot frame/axis. Useful for debugging.
            showplot : bool
                Show the plot in matplotlib window in non-interactive mode.
        '''
        mpl.rcParams['font.size'] = self.fontsize
        mpl.rcParams['font.family'] = self.font

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.get_figure()

        for element in self.elements:
            element.draw(ax)

        ax.autoscale_view(True)  # This autoscales all the shapes too
        # NOTE: arrows don't seem to be included in autoscale!
        xlim = np.array(ax.get_xlim())
        ylim = np.array(ax.get_ylim())
        xlim[0] = xlim[0]-.1   # Add a .1 unit border to pick up lost pixels
        ylim[0] = ylim[0]-.1
        xlim[1] = xlim[1]+.1
        ylim[1] = ylim[1]+.1
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        w = xlim[1]-xlim[0]
        h = ylim[1]-ylim[0]

        if not showframe:
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            ax.set_frame_on(False)

        self.ax = ax
        self.fig = ax.get_figure()
        ax.get_figure().set_size_inches(self.inches_per_unit*w, self.inches_per_unit*h)
        if not plt.isinteractive() and showplot:
            plt.show()

        # Resize again in case plt.show() messes with sizes
        ax.get_figure().set_size_inches(self.inches_per_unit*w, self.inches_per_unit*h)

    def save(self, fname, transparent=True, dpi=72):
        ''' Save figure to a file

            Parameters
            ----------
            fname : string
                Filename to save. File type automatically determined
                from extension (png, svg, jpg)
            transparent : bool
                Save as transparent background, if available
            dpi : float
                Dots-per-inch for raster formats
        '''
        self.fig.savefig(fname, bbox_extra_artists=self.ax.get_default_bbox_extra_artists(), bbox_inches='tight', transparent=transparent, dpi=dpi)

    def labelI(self, elm, label='', arrowofst=0.4, arrowlen=2, reverse=False, top=True):
        ''' Add an arrow element along side another element

            Parameters
            ----------
            elm : Element instance
                Element to add arrow to
            label : string or list
                String or list of strings to evenly space along arrow
            arrowofst : float
                Distance from element to arrow
            arrowlen : float
                Length of arrow as multiple of Drawing.unit
            reverse : bool
                Reverse the arrow direction
            top : bool
                Draw arrow on top (True) or bottom (False) of element
        '''
        if not top:
            arrowofst = -arrowofst

        x = elm.center[0] - np.sin(np.deg2rad(elm.theta))*arrowofst
        y = elm.center[1] + np.cos(np.deg2rad(elm.theta))*arrowofst

        if reverse:
            arrowlen = -arrowlen

        arrow = copy.deepcopy(elements.ARROW_I)
        arrow['shapes'][0]['start'] = [1-arrowlen/2, 0]
        arrow['shapes'][0]['end'] = [1+arrowlen/2, 0]

        if top:
            self.add(arrow, theta=elm.theta, label=label, anchor='center', xy=[x, y])
        else:
            self.add(arrow, theta=elm.theta, botlabel=label, anchor='center', xy=[x, y])

    def labelI_inline(self, elm, label='', botlabel='', d='in', start=True, ofst=0):
        ''' Add an arrowhead for labeling current inline with leads.
            Works on 2-terminal elements.

            Parameters
            ----------
            elm : Element instance
                Element to add arrow to
            label : string
                Text to draw above the arrowhead
            botlabel : string
                Text to draw below the arrowhead
            d : ['in', 'out']
                Arrowhead direction, into or out of the element
            start : bool
                Place arrowhead near start (True) or end (False) of element
            ofst : float
                Additional offset along elemnet leads
        '''
        arrowofst = 1.1 + ofst
        if d == 'in':
            arrowofst -= 0.3  # Account for length of arrowhead
        if start:
            x = elm.center[0] - np.cos(np.deg2rad(elm.theta))*arrowofst
            y = elm.center[1] - np.sin(np.deg2rad(elm.theta))*arrowofst
        else:
            x = elm.center[0] + np.cos(np.deg2rad(elm.theta))*arrowofst
            y = elm.center[1] + np.sin(np.deg2rad(elm.theta))*arrowofst

        if start:
            if d == 'in':
                reverse = False
            else:
                reverse = True
        else:
            if d == 'in':
                reverse = True
            else:
                reverse = False
        self.add(elements.ARROWHEAD, theta=elm.theta, reverse=reverse, 
                 xy=[x, y], label=label, botlabel=botlabel)

    def loopI(self, elm_list, label='', d='cw', theta1=35, theta2=-35, pad=.2):
        ''' Draw an arc to indicate a loop current bordered by elements in list

            Parameters
            ----------
            elm_list : list of Element instances
                Boundary elements in order of top, right, bot, left
            label : string
                Text label to draw in center of loop
            d : ['cw', 'ccw']
                Arc/arrow direction
            theta1 : float
                Start angle of arrow arc (degrees)
            theta2 : float
                End angle of arrow arc (degrees)
            pad : float
                Distance between elements and arc
        '''
        bbox1 = elm_list[0].get_bbox(transform=True)
        bbox2 = elm_list[1].get_bbox(transform=True)
        bbox3 = elm_list[2].get_bbox(transform=True)
        bbox4 = elm_list[3].get_bbox(transform=True)
        top = bbox1.ymin
        bot = bbox3.ymax
        left = bbox4.xmax
        rght = bbox2.xmin
        top = top - pad
        bot = bot + pad
        rght = rght - pad
        left = left + pad
        center = [(left+rght)/2, (top+bot)/2]
        loop = {'shapes': [{'shape': 'arc',
                            'center': [0, 0],
                            'theta1': theta1,
                            'theta2': theta2,
                            'width': rght-left,
                            'height': top-bot,
                            'arrow': d}],
                'move_cur': False,
                'lblloc': 'center',
                'lblofst': 0}

        L = self.add(loop, xy=center, d='right')
        L.add_label(label, loc='center', ofst=0, align=('center', 'center'))
        return L


class Transform(object):
    ''' Class defining transformation matrix

        Parameters
        ----------
        rotate: array-like
            Rotation matrix
        shift: array-like
            Shift matrix [x, y]
        zoom: float
            Zoom factor
    '''
    def __init__(self, rotate, shift, zoom=1):
        self.rotate = np.asarray(rotate)
        self.shift = np.asarray(shift)
        self.zoom = zoom

    def transform(self, pt):
        ''' Apply the transform to the point

            Parameters
            ----------
            pt: [x, y] array
                Original coordinates

            Returns
            -------
            pt: [x, y] array
                Transformed coordinates
        '''
        return np.dot(pt*self.zoom, self.rotate) + self.shift

    def transform_array(self, pts):
        ''' Apply the transform to multiple points

            Parameters
            ----------
            pts: array
                List of points to transform
        '''
        arr = np.empty((len(pts), 2))
        for i, pt in enumerate(pts):
            arr[i] = self.transform(pt)
        return arr


class Segment(object):
    ''' A segment (path), part of an Element.

        Parameters
        ----------
        path : array-like
            List of [x,y] coordinates making the path
        transform : Transform instance
            Transformation for the path to drawing coordinates

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
        fill : string
            Matplotlib color to fill (if path is closed)
        zorder : int
            Z-order for segment
    '''
    def __init__(self, path, transform, **kwargs):
        self._path = np.asarray(path)  # Untranformed path
        self.path = self._path.copy()
        self.path = transform.transform_array(self._path)

        self.zorder = kwargs.pop('zorder', 2)
        self.color = kwargs.get('color', 'black')
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')
        self.capstyle = kwargs.get('capstyle', 'round')
        self.fill = kwargs.get('fill', None)

    def getdef(self):
        ''' Get element defintion dictionary for this segment '''
        return {'paths': [self.path],
                'pathparams': [{
                'ls': self.ls,
                'lw': self.lw,
                'color': self.color,
                'zorder': self.zorder,
                'capstyle': self.capstyle,
                'fill': self.fill}]
               }

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        xmin = ymin = np.inf
        xmax = ymax = -np.inf
        for p in self._path:
            xmin = min(xmin, p[0])
            ymin = min(ymin, p[1])
            xmax = max(xmax, p[0])
            ymax = max(ymax, p[1])
        return BBox(xmin, ymin, xmax, ymax)
  
    def draw(self, ax):
        ''' Draw the segment '''
        if self.fill is not None:
            tlist = list(map(tuple, self.path))  # Need path as tuples for set()
            if len(tlist) != len(set(tlist)):  # duplicate points, assume closed shape
                ax.fill(self.path[:, 0], self.path[:, 1], color=self.fill, zorder=self.zorder)

        ax.plot(self.path[:, 0], self.path[:, 1], color=self.color, lw=self.lw,
                solid_capstyle=self.capstyle, ls=self.ls, zorder=self.zorder)


class SegmentCircle(object):
    ''' A circle drawing segment

        Parameters
        ----------
        center : [x, y] array
            Center of the circle
        radius : float
            Radius of the circle
        transform : Transform instance
            Transformation for the path to drawing coordinates

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
    def __init__(self, center, radius, transform, **kwargs):
        self._center = np.asarray(center)
        self._radius = radius
        self.center = center.copy()
        self.radius = radius
        self.center = transform.transform(self.center)
        self.radius = transform.zoom * self.radius

        self.zorder = kwargs.pop('zorder', 1)
        self.color = kwargs.get('color', 'black')
        self.fillcolor = kwargs.get('fill', None)
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')

    def getdef(self):
        ''' Get element defintion dictionary for this segment '''
        return {'shapes': [
                    {'shape': 'circle',
                     'center': self.center,
                     'radius': self.radius,
                     'color': self.color,
                     'fill': self.fillcolor is not None,
                     'fillcolor': self.fillcolor,
                     'ls': self.ls,
                     'lw': self.lw,
                     'zorder': self.zorder}]}

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        center = self._center
        xmin = center[0] - self.radius
        xmax = center[0] + self.radius
        ymin = center[1] - self.radius
        ymax = center[1] + self.radius
        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, ax):
        ''' Draw the segment '''
        fill = self.fillcolor is not None
        circ = plt.Circle(xy=self.center, radius=self.radius,
                          ec=self.color, fc=self.fillcolor, fill=fill,
                          lw=self.lw, ls=self.ls,
                          zorder=self.zorder)
        ax.add_patch(circ)


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
    def __init__(self, xy, transform, **kwargs):
        self._xy = xy
        self.xy = xy.copy()
        self.xy = transform.transform_array(self.xy)
        self.closed = kwargs.get('closed', True)
        self.color = kwargs.get('color', 'black')
        self.fill = kwargs.get('fill', None)
        self.zorder = kwargs.pop('zorder', 1)
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')

    def getdef(self):
        ''' Get element defintion dictionary for this segment '''
        return {'shapes': [
                    {'shape': 'poly',
                     'xy': self.xy,
                     'closed': self.closed,
                     'color': self.color,
                     'fill': self.fill is not None,
                     'fillcolor': self.fill,
                     'ls': self.ls,
                     'lw': self.lw,
                     'zorder': self.zorder}]}

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        xmin = ymin = np.inf
        xmax = ymax = -np.inf
        for v in self._xy:
            xmin = min(xmin, v[0])
            ymin = min(ymin, v[1])
            xmax = max(xmax, v[0])
            ymax = max(ymax, v[1])
        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, ax):
        ''' Draw the segment '''
        fill = self.fill is not None
        poly = plt.Polygon(xy=self.xy, closed=self.closed, ec=self.color,
                           fc=self.fill, fill=fill, lw=self.lw, ls=self.ls,
                           zorder=self.zorder)
        ax.add_patch(poly)


class SegmentArrow(object):
    ''' An arrow drawing segment

        Parameters
        ----------
        start : [x, y] array
            Start coordinate of arrow
        end : [x, y] array
            End (head) coordinate of arrow
        radius : float
            Radius of the circle
        transform : Transform instance
            Transformation for the path to drawing coordinates

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
    def __init__(self, start, end, transform, **kwargs):
        self._start = start
        self._end = end
        self.start = start
        self.end = end
        self.start = transform.transform(self.start)
        self.end = transform.transform(self.end)
        self.zorder = kwargs.pop('zorder', 1)
        self.headwidth = kwargs.get('headwidth', .1)
        self.headlength = kwargs.get('headlength', .2)
        self.color = kwargs.get('color', 'black')
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')

    def getdef(self):
        ''' Get element defintion dictionary for this segment '''
        return {'shapes': [
                    {'shape': 'arrow',
                     'start': self.start,
                     'end': self.end,
                     'headwidth': self.headwidth,
                     'headlength': self.headlength,
                     'color': self.color,
                     'ls': self.ls,
                     'lw': self.lw,
                     'zorder': self.zorder}]}

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        start = self._start
        end = self._end
        xmin = min(start[0], end[0])
        ymin = min(start[1], end[1])
        xmax = max(start[0], end[0])
        ymax = max(start[1], end[1])
        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, ax):
        ''' Draw the segment '''
        ax.arrow(self.start[0], self.start[1],
                 self.end[0]-self.start[0], self.end[1]-self.start[1],
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
    def __init__(self, center, width, height, transform, reverse=False, **kwargs):
        self._center = center
        self.center = transform.transform(self._center)
        self.width = width
        self.height = height
        self.theta1 = kwargs.get('theta1', 35)
        self.theta2 = kwargs.get('theta2', 35)
        self.angle = kwargs.get('angle', 0)
        self.arrow = kwargs.get('arrow', None)  # cw or ccw
        self.color = kwargs.get('color', 'black')
        self.lw = kwargs.get('lw', 2)
        self.ls = kwargs.get('ls', '-')
        self.zorder = kwargs.pop('zorder', 1)
        if reverse:
            self.theta1, self.theta2 = self.theta1+180, self.theta2+180
            self.angle += 180

    def getdef(self):
        ''' Get element defintion dictionary for this segment '''
        return {'shapes': [
                    {'shape': 'arc',
                     'center': self.center,
                     'theta1': self.theta1,
                     'theta2': self.theta2,
                     'angle': self.angle,
                     'arrow': self.arrow,
                     'color': self.color,
                     'ls': self.ls,
                     'lw': self.lw,
                     'zorder': self.zorder}]}

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        center = self._center
        xmin = center[0] - self.width
        ymin = center[1] - self.height
        xmax = center[0] + self.width
        ymax = center[1] + self.height
        return BBox(xmin, ymin, xmax, ymax)

    def draw(self, ax):
        ''' Draw the segment '''
        arc = Arc(self.center, width=self.width, height=self.height,
                  theta1=self.theta1, theta2=self.theta2, angle=self.angle,
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
                s = [self.center[0] + self.width/2*np.cos(np.deg2rad(th2)),
                     self.center[1] + self.height/2*np.sin(np.deg2rad(th2))]
            else:
                dx = -np.cos(np.deg2rad(th1+90)) / 100
                dy = - np.sin(np.deg2rad(th1+90)) / 100

                s = [self.center[0] + self.width/2*np.cos(np.deg2rad(th1)),
                     self.center[1] + self.height/2*np.sin(np.deg2rad(th1))]

            # Rotate the arrow head
            co = np.cos(np.radians(self.angle))
            so = np.sin(np.radians(self.angle))
            m = np.array([[co, so], [-so, co]])
            s = np.dot(s-self.center, m)+self.center
            darrow = np.dot([dx, dy], m)

            ax.arrow(s[0], s[1], darrow[0], darrow[1], head_width=.15,
                     head_length=.25, color=self.color, zorder=self.zorder)


class SegmentText(object):
    ''' A text drawing segment

        Parameters
        ----------
        pos : [x, y] array
            Coordinates for text
        label : string
            Text to draw
        transform : Transform instance
            Transformation for the path to drawing coordinates

        Keyword Arguments
        -----------------
        align : tuple
            Tuple of (horizontal, vertical) alignment where horizontal
            is ['center', 'left', 'right'] and vertical is ['center',
            'top', 'bottom']
        rotation : float
            Rotation angle (degrees)
        rotation_mode : string
            See Matplotlib documentation.
        color : string
             Matplotlib color for this segment
        size : float
            Font size
        zorder : int
            Z-order for segment
    '''
    def __init__(self, pos, label, transform, **kwargs):
        self._xy = pos
        self.text = label
        self.xy = transform.transform(self._xy)
        self.align = kwargs.get('align', ('center', 'center'))
        self.fontsize = kwargs.get('size', 14)
        self.color = kwargs.get('color', 'black')
        self.rotation = kwargs.get('rotation', 0)
        self.rotation_mode = kwargs.get('rotation_mode', 'anchor')  # 'anchor' or 'default'
        self.zorder = kwargs.get('zorder', 3)

    def getdef(self):
        ''' Get element defintion dictionary for this segment '''
        return {'labels': [{
                 'label': self.text,
                 'pos': self.xy,
                 'align': self.align,
                 'size': self.fontsize,
                 'color': self.color,
                 'zorder': self.zorder,
                 'rotation': self.rotation,
                }]}

    def get_bbox(self):
        ''' Get bounding box (untransformed)

            Returns
            -------
            xmin, ymin, xmax, ymax
                Bounding box limits
        '''
        return BBox(np.inf, np.inf, -np.inf, -np.inf)

    def draw(self, ax):
        ''' Draw the segment '''
        ax.text(self.xy[0], self.xy[1], self.text, transform=ax.transData,
                color=self.color, fontsize=self.fontsize, rotation=self.rotation,
                horizontalalignment=self.align[0], verticalalignment=self.align[1],
                zorder=self.zorder, rotation_mode=self.rotation_mode)##rotation_mode='anchor')


def _reversedef(elmdef, flip, reverse):
    ''' Flip up-down and/or reverse left-right element dictionary

        Parameters
        ----------
        elmdef : dict
            Element dictionary to reverse/flip
        flip, reverse : bool
            Whether to apply flip and reverse

        Returns
        elmdef : dict
            Reverse and/or flipped element definition
    '''
    # First, find center, assuming last path sets endpoints
    if 'paths' not in elmdef or not reverse:
        centerx = 0
    else:
        mainpath = elmdef['paths'][-1]
        centerx = (mainpath[0][0] + mainpath[-1][0])/2

    def _reverse(pt):
        pt = [pt[0]-centerx, pt[1]]
        return np.dot(pt, mirror_matrix) + np.array([centerx, 0])

    def _flip(pt):
        return [pt[0], -pt[1]]
    
    def translate(pt):
        if reverse:
            pt = _reverse(pt)
        if flip:
            pt = _flip(pt)
        return pt

    # Now flip/reverse all coordinates in def
    elmdef = copy.deepcopy(_flatten_elements(elmdef))

    newpaths = []
    for path in elmdef.get('paths', []):
        pts = []
        for pt in path:
            pts.append(translate(pt))
        if reverse:
            pts = pts[::-1]
        newpaths.append(pts)
    elmdef['paths'] = newpaths

    for shape in elmdef.get('shapes', []):
        for name in ['start', 'end', 'center']:
            if name in shape:
                shape[name] = translate(shape[name])

        if 'xy' in shape:
            newxy = []
            for xy in shape['xy']:
                newxy.append(translate(xy))
            shape['xy'] = newxy

        if reverse and 'theta1' in shape and 'theta2' in shape:
            shape['theta1'], shape['theta2'] = shape['theta1']+180, shape['theta2']+180

    for label in elmdef.get('labels', []):
        if 'pos' in label:
            label['pos'] = translate(label['pos'])

    for anchorname in elmdef.get('anchors', {}).keys():
        pos = elmdef['anchors'][anchorname]
        elmdef['anchors'][anchorname] = translate(pos)

    return elmdef


class Element(object):
    ''' Circuit element.

        Parameters
        ----------
        elm_def: dict
            Element definition dictionary (see Element class)
        drawing: Drawing
            The Drawing object

        Keyword Arguments
        -----------------
        xy : [x, y] float array
            Starting coordinate of element. Defaults to Drawing.here,
            the endpoint of the last drawn element.
        d : ['up', 'down', 'left', 'right']
            Direction of element.
        theta : float
            Angle (in degrees) of element. Overrides `d` parameter.
        flip : bool
            Flip the element up/down
        reverse : bool
            Reverse the element (for example a DIODE)
        anchor : string
            Name of the "pin" in the element to place at `xy` in the
            Drawing. Typically used for elements with more than two
            terminals. For example, an OPAMP element has `in1`, `in2`,
            and `out` anchors.

        Parameters that override `d` parameter:
        to : [x, y] float array
            The end coordinate of the element
        tox : float
            x-value of end coordinate. y-value will be same as start
        toy : float
            y-value of end coordinate. x-value will be same as start
        l : float
            Total length of element
        zoom : float
            Zoom/magnification factor for element. Default = 1.

        endpts: tuple of 2 [x, y] float arrays
            The start and end points of the element. Overrides `xy`
            and `to` parameters.

        label, toplabel, botlabel, lftlabel, rgtlabel : string or list
            Add a string to label the element on the given side.
            Can be a string or list of strings that will be evenly-
            spaced along the element (['-', 'V1', '+']). Use $
            for latex formatting, for example `$R_1 = 100 \Omega$`.
            See also: `add_label` method.
        lblofst : float
            Offset between label and element
        lblsize : float
            Font size of labels, overrides Drawing.fontsize
            for this element
        lblrotate : bool
            Rotate the label text to align with the element,
            for example vertical text with an element having
            `d="up"`.
        lblloc : ['top', 'bottom', 'left', 'right', 'center']
            Location for drawing the label specified by `label`
            parameter.

        zorder : int
            Z-order parameter for placing element in front or behind
            others.

        color : string
            Matplotlib color for the element
        ls : string
            Matplotlib line style for the element
        lw : float
            Line width for the element
        fill : string
            Fill color for elements with closed paths or shapes
    '''
    def __init__(self, elm_def, drawing, **kwargs):
        self.segments = []  # List of all things to draw
        self.defn = copy.deepcopy(elm_def)
        if 'base' in self.defn:
            self.defn = _flatten_elements(self.defn)

        self.flip = kwargs.pop('flip', False)       # Flip (up/down when theta=0)
        self.reverse = kwargs.pop('reverse', False) # Reverse (left/right)
        zoom = kwargs.pop('zoom', 1)           # Zoom fraction
        self.zorder = kwargs.pop('zorder', 1)  # zorder of the element as a whole, to stack multiple elements

        if self.flip or self.reverse:
            self.defn = _reversedef(self.defn, self.flip, self.reverse)

        self.drawing = drawing
        shapes = self.defn.get('shapes', [])
        paths = self.defn.get('paths', [])
        pathparams = self.defn.get('pathparams', [{}] * len(paths))
        labels = self.defn.get('labels', [])
        totlen = kwargs.pop('l', drawing.unit)
        theta = kwargs.pop('theta', None)
        endpts = kwargs.pop('endpts', None)
        direction = kwargs.pop('d', None)
        to = kwargs.pop('to', None)
        tox = kwargs.pop('tox', None)
        toy = kwargs.pop('toy', None)
        xy = kwargs.pop('xy', drawing.here)
        anchor = kwargs.pop('anchor', None)

        # user-defined labels - allow element def to define label location
        self.lblofst = kwargs.pop('lblofst', self.defn.get('lblofst', drawing.txtofst))
        lblloc = kwargs.pop('lblloc', self.defn.get('lblloc', 'top'))
        lblsize = kwargs.pop('lblsize', drawing.fontsize)
        lblrotate = kwargs.pop('lblrotate', False)
        userlabels = {
            'top': kwargs.pop('toplabel', None),
            'bot': kwargs.pop('botlabel', None),
            'lft': kwargs.pop('lftlabel', None),
            'rgt': kwargs.pop('rgtlabel', None),
            'center': kwargs.pop('clabel', None)
            }
        if 'label' in kwargs:
            userlabels[lblloc] = kwargs.pop('label')

        # Parameters, such as color, linewidth, linestyle, are inhereted from drawing
        # but are overriden by anything in element definition dictionary
        # and these can be overridden by the user via add() arguments
        # ALL parameters can be modified from the segments list
        self.userparams = kwargs

        # set up transformation
        default_theta = self.defn.get('theta', drawing.theta)
        if endpts is not None:
            self.theta = _angle(endpts[0], endpts[1])
        elif theta is not None:
            self.theta = theta
        elif direction is not None:
            self.theta = {'u': 90, 'r': 0, 'l': 180, 'd': 270}[direction[0].lower()]
        elif to is not None:
            self.theta = _angle(xy, to)
        else:
            self.theta = default_theta

        # Get offset to element position within drawing
        if endpts is not None:
            self.shift = endpts[0]
        else:
            self.shift = xy

        # Set up initial translation matrix
        c = np.cos(np.radians(self.theta))
        s = np.sin(np.radians(self.theta))
        rotate = np.array([[c, s], [-s, c]])

        # convert paths to proper arrays
        self.path_def = [np.array(p) for p in self.defn.get('paths', [])]

        # Extend the leads to make the element the desired length
        if len(self.path_def) == 0:
            start = np.array([0, 0])
            end = np.array([0, 0])
            leadofst = 0

        elif self.defn.get('extend', True):
            # Adjust the last path in definition to include lead extensions
            in_path = self.path_def[-1]   # Path to get extension
            dz = in_path[-1]-in_path[0]   # Defined delta of path
            in_len = np.sqrt(dz[0]*dz[0]+dz[1]*dz[1])   # Defined length of path

            if endpts is not None:
                totlen = _distance(endpts[0], endpts[1])
            elif to is not None:
                # Move until X or Y position is 'end'. Depends on direction
                totlen = _distance(self.shift, to)
            elif tox is not None:
                # Allow either full coordinate (only keeping x), or just an x value
                if isinstance(tox, float) or isinstance(tox, int):
                    x = float(tox)
                else:
                    x = tox[0]
                endpt = [x, self.shift[1]]
                totlen = _distance(self.shift, endpt)
            elif toy is not None:
                # Allow either full coordinate (only keeping y), or just a y value
                if isinstance(toy, float) or isinstance(toy, int):
                    y = toy
                else:
                    y = toy[1]
                endpt = [self.shift[0], y]
                totlen = _distance(self.shift, endpt)

            lead_len = (totlen - in_len)/2
            start = in_path[0] - np.array([lead_len, 0])
            end = in_path[-1] + np.array([lead_len, 0])
            leadofst = start
            p = np.vstack((start, in_path, end))
            self.path_def[-1] = p  # Put the modified path into pathdef

        else:  # Don't extend leads
            start = self.path_def[-1][0]
            end = self.path_def[-1][-1]
            leadofst = 0

        self.transform = Transform(rotate, self.shift, zoom)

        # Get offset due to anchoring.
        if anchor is not None:
            if 'anchors' in self.defn and anchor in self.defn['anchors']:
                leadofst = np.array(self.defn['anchors'][anchor])
            else:
                raise ValueError('Anchor {} not defined in element'.format(anchor))
        self.leadofst = leadofst
                
        if len(self.path_def) > 0:
            drop = self.transform.transform(self.defn.get('drop', np.asarray(self.path_def[-1][-1])-leadofst))
        else:
            drop = self.transform.transform(self.defn.get('drop', -leadofst))

        # Now add all the other paths, adding in extend offset
        for idx, p in enumerate(self.path_def):
            params = self._setup_params(pathparams[idx])
            self.segments.append(Segment(path=p-leadofst, transform=self.transform, **params))

        # Add shapes
        for shape in shapes:
            # Apply defaults or user orverride to shape parameters
            shapeargs = self._setup_params(shape)
            shapetype = shapeargs.pop('shape', None)

            # Adjust xy based on leadofst before adding segment
            if shapetype == 'circle':
                shapeargs['center'] = np.asarray(shapeargs.get('center', [0, 0])) - leadofst
                self.segments.append(SegmentCircle(transform=self.transform, **shapeargs))

            elif shapetype == 'poly':
                shapeargs['xy'] = np.asarray(shapeargs.get('xy', [0, 0])) - leadofst
                self.segments.append(SegmentPoly(transform=self.transform, **shapeargs))

            elif shapetype == 'arrow':
                shapeargs['start'] = np.asarray(shapeargs.get('start', [0, 0])) - leadofst
                shapeargs['end'] = np.asarray(shapeargs.get('end', [1, 0])) - leadofst
                self.segments.append(SegmentArrow(transform=self.transform, **shapeargs))

            elif shapetype == 'arc':
                shapeargs['center'] = np.asarray(shapeargs.get('center', [0, 0])) - leadofst
                shapeargs.setdefault('angle', self.theta)
                self.segments.append(SegmentArc(transform=self.transform, reverse=self.reverse, **shapeargs))

            else:
                raise NotImplementedError('Shape {} not defined'.format(shapetype))

        # Add labels from element definition
        for label in labels:
            labelargs = self._setup_params(label)
            labelargs['rotation'] = labelargs.get('rotation', 0) + self.theta
            labelargs['pos'] = np.asarray(labelargs.get('pos', [0, 0])) - leadofst
            self.segments.append(SegmentText(transform=self.transform, **labelargs))
            
        # Get bounds of element, used for positioning user labels
        self.xmin, self.ymin, self.xmax, self.ymax = self.get_bbox()

        # Add user-defined labels
        for loc, label in userlabels.items():
            if label is not None:
                rotation = (self.theta if lblrotate else 0)
                self.add_label(label, loc, ofst=self.lblofst, size=lblsize, rotation=rotation)

        # Define anchors
        if len(self.path_def) == 0:
            setattr(self, 'start', self.transform.transform(np.array([0, 0])))
            setattr(self, 'end', self.transform.transform((np.array([0, 0]))))
            setattr(self, 'center', self.transform.transform((np.array([0, 0]))))
        else:
            setattr(self, 'start', self.transform.transform(start-leadofst))
            setattr(self, 'end', self.transform.transform(end-leadofst))
            setattr(self, 'center', self.transform.transform((start+end-2*leadofst)/2))
        if 'anchors' in self.defn:
            for aname, apoint in self.defn['anchors'].items():
                if getattr(self, aname, None) is not None:  # Try not to clobber element parameter names!
                    aname = 'anchor_' + aname
                setattr(self, aname, self.transform.transform(np.array(apoint)-leadofst))

        # Set 'here' property for new drawing position (no flipping or reversing in this translate)
        self.here = drop

    def _setup_params(self, params):
        ''' Setup parameters for the segment, inheriting from the
            Drawing, Element, or keyword arguments.
        '''
        newparams = self.drawing.params.copy()
        newparams.update(params)
        newparams.update(self.userparams)

        if 'fill' in self.userparams:  # fill is color string in add method
            fillcolor = self.userparams.get('fill')
        elif params.get('fill', False):  # In elementdef, fill is boolean
            fillcolor = params.get('fillcolor', newparams.get('color', 'black'))
        else:
            fillcolor = None
        newparams['fill'] = fillcolor
        return newparams

    def get_bbox(self, transform=False):
        ''' Get element bounding box, including path and shapes.

            Parameters
            ----------
            transform : bool
                Apply the element transform to the bbox

            Returns
            -------
            xmin, ymin, xmax, ymax
                Corners of the bounding box
        '''
        xmin = ymin = np.inf
        xmax = ymax = -np.inf
        for segment in self.segments:
            segxmin, segymin, segxmax, segymax = segment.get_bbox()
            xmin = min(xmin, segxmin)
            xmax = max(xmax, segxmax)
            ymin = min(ymin, segymin)
            ymax = max(ymax, segymax)

        # Don't want to propogate infinities (e.g. shape not defined above)
        if xmax == -np.Inf: xmax = 0
        if ymax == -np.Inf: ymax = 0
        if xmin ==  np.Inf: xmin = 0
        if ymin ==  np.Inf: ymin = 0

        if transform:
            xmin, ymin = self.transform.transform([xmin, ymin])
            xmax, ymax = self.transform.transform([xmax, ymax])
            xmin, xmax = min(xmin, xmax), max(xmin, xmax)
            ymin, ymax = min(ymin, ymax), max(ymin, ymax)
        return BBox(xmin, ymin, xmax, ymax)

    def add_label(self, label, loc='top', ofst=None, align=None, rotation=0, **kwargs):
        ''' Add a label to the element

            Parameters
            ----------
            label : string or list
                Text to add. If list, list items will be evenly spaced
                along the element.
            loc : ['top', 'bot', 'lft', 'rgt']
                Location for text relative to element
            ofst : float
                Offset between text and element. Defaults to Element.lblofst.
            align : tuple
                Tuple of (horizontal, vertical) alignment where horizontal
                is ['center', 'left', 'right'] and vertical is ['center',
                'top', 'bottom']
            rotation : float
                Rotation angle (degrees)
                
            Keyword Arguments
            -----------------
            size : float
                Font size
            color: string
                Matplotlib color
        '''
        if isinstance(ofst, (list, tuple)) and loc in ['top', 'lft', 'bot', 'rgt']:
            raise TypeError('Offset must not be list for loc={}'.format(loc))

        if ofst is None:
            ofst = self.lblofst

        rotation = (rotation + 360) % 360
        if rotation > 90 and rotation < 270:
            rotation -= 180  # Keep the label from going upside down
            
        anchornames = self.defn.get('anchors', [])
            
        # This ensures a 'top' label is always on top, regardless of rotation
        if (self.theta % 360) > 90 and (self.theta % 360) <= 270:
            if loc == 'top':
                loc = 'bot'
            elif loc == 'bot':
                loc = 'top'
            elif loc == 'lft':
                loc = 'rgt'
            elif loc == 'rgt':
                loc = 'lft'
        
        if align is None:   # Determine best alignment for label based on angle
            th = self.theta - rotation
            # Below alignment divisions work for label on top. Rotate angle for other sides.
            if loc == 'lft':
                th = th + 90
            elif loc == 'bot':
                th = th + 180
            elif loc == 'rgt':
                th = th + 270
            th = th % 360  # Normalize angle so it's positive, clockwise

            if loc == 'center':
                align = ('center', 'center')
            elif th < 22.5:       # 0 to +22 deg
                align = ('center', 'bottom')
            elif th < 22.5+45:    # 22 to 67
                align = ('right', 'bottom')
            elif th < 22.5+45*2:  # 67 to 112
                align = ('right', 'center')
            elif th < 22.5+45*3:  # 112 to 157
                align = ('right', 'top')
            elif th < 22.5+45*4:  # 157 to 202
                align = ('center', 'top')
            elif th < 22.5+45*5:  # 202 to 247
                align = ('left', 'top')
            elif th < 22.5+45*6:  # 247 to 292
                align = ('left', 'center')
            elif th < 22.5+45*7:  # 292 to 337
                align = ('left', 'bottom')
            else:                 # 337 to 0
                align = ('center', 'bottom')
        xmax = self.xmax
        xmin = self.xmin
        ymax = self.ymax
        ymin = self.ymin

        size = kwargs.get('size', self.drawing.fontsize)

        lblparams = self.drawing.params.copy()
        lblparams.update(self.userparams)
        lblparams.update(kwargs)
        lblparams.update({'align': align, 'rotation': rotation, 
                          'transform': self.transform, 'fontsize': size})

        if isinstance(label, (list, tuple)):
            # Divide list along length
            if loc == 'top':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    xy = [xmin+xdiv*(i+1), ymax+ofst]
                    self.segments.append(SegmentText(np.asarray(xy), label[i], **lblparams))
            elif loc == 'bot':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    xy = [xmin+xdiv*(i+1), ymin-ofst]
                    self.segments.append(SegmentText(np.asarray(xy), label[i], **lblparams))
            elif loc == 'lft':
                for i, lbltxt in enumerate(label):
                    ydiv = (ymax-ymin)/(len(label)+1)
                    xy = [xmin-ofst, ymin+ydiv*(i+1)]
                    self.segments.append(SegmentText(np.asarray(xy), label[i], **lblparams))
            elif loc == 'rgt':
                for i, lbltxt in enumerate(label):
                    ydiv = (ymax-ymin)/(len(label)+1)
                    xy = [xmax+ofst, ymin+ydiv*(i+1)]
                    self.segments.append(SegmentText(np.asarray(xy), label[i], **lblparams))
            elif loc == 'center':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    xy = [xmin+xdiv*(i+1), ofst]
                    self.segments.append(SegmentText(np.asarray(xy), label[i], **lblparams))

        elif isinstance(label, str):
            # Place in center
            if loc == 'top':
                xy = [(xmax+xmin)/2, ymax+ofst]
            elif loc == 'bot':
                xy = [(xmax+xmin)/2, ymin-ofst]
            elif loc == 'lft':
                xy = [xmin-ofst, (ymax+ymin)/2]
            elif loc == 'rgt':
                xy = [xmax+ofst, (ymax+ymin)/2]
            elif loc == 'center':
                if isinstance(ofst, (list, tuple)):
                    xy = [(xmax+xmin)/2+ofst[0], (ymax+ymin)/2+ofst[1]]
                else:
                    xy = [(xmax+xmin)/2, (ymax+ymin)/2+ofst]
            elif loc in anchornames:
                xy = np.asarray(anchornames[loc])
                if isinstance(ofst, (list, tuple)):
                    xy = xy + ofst - self.leadofst
                else:
                    xy = np.asarray([xy[0], xy[1]+ofst]) - self.leadofst
            else:
                raise ValueError('Undefined location {}'.format(loc))
            self.segments.append(SegmentText(np.asarray(xy), label, **lblparams))

    def draw(self, ax):
        ''' Draw the element on the axis '''
        for segment in sorted(self.segments, key=lambda x: x.zorder):
            segment.draw(ax)
