''' Schemdraw base Element class '''

from collections import ChainMap
import numpy as np

from ..backends.mpl import Figure
from ..adddocs import adddocs
from ..segments import SegmentText, BBox
from ..transform import Transform, mirror_point, flip_point

gap = [np.nan, np.nan]  # Put a gap in a path


def angle(a, b):
    ''' Compute angle from coordinate a to b '''
    theta = np.degrees(np.arctan2(b[1] - a[1], (b[0] - a[0])))
    return theta


def distance(a, b):
    ''' Compute distance from A to B '''
    r = np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return r


class Element(object):
    ''' Parent class for a single circuit element.

        Keyword Arguments
        -------------------------
        d : string
            Drawing direction ['down', 'up', 'left', 'right'] or
            abbreviated ['d', 'u', 'l', 'r']
        at : float list [x, y]
            Starting coordinate of element, defaults to current
            drawing position. OR xy can be tuple of (Element, anchorname)
            to be resolved after the Element has been placed (see Walrus
            mode in documentation)
        xy : float list [x, y]
            Alias for at keyword
        theta : float
            Angle (degrees) of element. Overrides the `d` parameter.
        flip : bool
            Flip the element up/down
        reverse : bool
            Reverse the element (for example a DIODE)
        zoom : float
            Zoom/magnification factor for element. Default = 1.
        anchor : string
            Name of the "pin" in the element to place at `xy` in the
            Drawing. Typically used for elements with more than two
            terminals. For example, an OPAMP element has `in1`, `in2`,
            and `out` anchors.
        label, toplabel, botlabel, lftlabel, rgtlabel : string or list
            Add a string to label the element on the given side.
            Can be a string or list of strings that will be evenly-
            spaced along the element (['-', 'V1', '+']). Use $
            for latex formatting, for example `$R_1 = 100 \\Omega$`.
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
        lblloc : ['top', 'bot', 'lft', 'rgt', 'center']
            Location for drawing the label specified by `label`
            parameter.
        zorder : int
            Z-order parameter for placing element in front or behind
            others.
        color : string
            Color for the element
        ls : string
            Line style for the element '-', '--', ':', etc.
        lw : float
            Line width for the element
        fill : string
            Fill color for elements with closed paths or shapes
        move_cur : bool
            Move the Drawing cursor to the endpoint of the element
    '''
    def __init__(self, d=None, **kwargs):
        self.userparams = kwargs
        if d is not None:  # Allow direction to be specified as first param without name
            self.userparams['d'] = d

        self.dwgparams = {}  # Set by drawing in place() method
        self.params = {}     # Set by element defintion in setup() method
        self.cparams = None  # Combined (ChainMap) of above params
        self.localshift = 0
        self.anchors = {}     # Untransformed anchors
        self.absanchors = {}  # Transformed, absolute anchors
        self.segments = []
        self.transform = Transform(0, [0, 0])

        if 'xy' in self.userparams:  # Allow legacy 'xy' parameter
            self.userparams.setdefault('at', self.userparams.pop('xy'))

    def buildparams(self):
        ''' Combine parameters from user, setup, and drawing '''
        # Accomodate xy positions based on OTHER elements before they are fully set up.
        if 'at' in self.userparams and isinstance(self.userparams['at'][1], str):
            element, pos = self.userparams['at']
            if pos in element.absanchors:
                xy = element.absanchors[pos]
            else:
                raise KeyError('Unknown anchor name {}'.format(pos))
            self.userparams['at'] = xy

        # All subsequent actions get params from cparams
        self.cparams = ChainMap(self.userparams, self.params, self.dwgparams)
        self.flipreverse()

    def flipreverse(self):
        ''' Flip and/or reverse segments if necessary '''
        if self.userparams.get('flip', False):
            [s.doflip() for s in self.segments]
            for name, pt in self.anchors.items():
                self.anchors[name] = flip_point(pt)

        if self.userparams.get('reverse', False):
            if 'center' in self.anchors:
                centerx = self.anchors['center'][0]
            else:
                xmin, _, xmax, _ = self.get_bbox()
                centerx = (xmin + xmax)/2
            [s.doreverse(centerx) for s in self.segments]
            for name, pt in self.anchors.items():
                self.anchors[name] = mirror_point(pt, centerx)

    def place(self, dwgxy, dwgtheta, **dwgparams):
        ''' Determine position within the drawing '''
        self.dwgparams = dwgparams
        if self.cparams is None:
            self.buildparams()

        anchor = self.cparams.get('anchor', None)
        zoom = self.cparams.get('zoom', 1)
        xy = np.asarray(self.cparams.get('at', dwgxy))

        # Get bounds of element, used for positioning user labels
        self.bbox = self.get_bbox()

        if 'endpts' in self.cparams:
            theta = dwgtheta
        elif self.cparams.get('d') is not None:
            theta = {'u': 90, 'r': 0, 'l': 180, 'd': 270}[self.cparams.get('d')[0].lower()]
        else:
            theta = self.cparams.get('theta', dwgtheta)

        if anchor is not None:
            self.localshift = -np.asarray(self.anchors[anchor])
        self.transform = Transform(theta, xy, self.localshift, zoom)

        # Add user-defined labels
        # user-defined labels - allow element def to define label location
        lblofst = self.cparams.get('lblofst', .1)
        lblloc = self.cparams.get('lblloc', 'top')
        lblsize = self.cparams.get('lblsize', self.cparams.get('fontsize', 14))
        lblrotate = self.cparams.get('lblrotate', False)
        lblcolor = self.cparams.get('color', 'black')
        userlabels = {
            'top': self.cparams.get('toplabel', None),
            'bot': self.cparams.get('botlabel', None),
            'lft': self.cparams.get('lftlabel', None),
            'rgt': self.cparams.get('rgtlabel', None),
            'center': self.cparams.get('clabel', None)
            }
        if 'label' in self.cparams:
            userlabels[lblloc] = self.cparams.get('label')

        for loc, label in userlabels.items():
            if label is not None:
                rotation = (theta if lblrotate else 0)
                self.add_label(label, loc, ofst=lblofst, size=lblsize,
                               rotation=rotation, color=lblcolor)

        # Add element-specific anchors
        for name, pos in self.anchors.items():
            self.absanchors[name] = self.transform.transform(np.array(pos))
        self.absanchors['xy'] = self.transform.transform([0, 0])

        # Set all anchors as attributes
        for name, pos in self.absanchors.items():
            if getattr(self, name, None) is not None:
                # Don't clobber element parameter names!
                name = 'anchor_' + name
            setattr(self, name, pos)

        drop = self.cparams.get('drop', None)
        if drop is None or not self.cparams.get('move_cur', True):
            return dwgxy, dwgtheta
        elif self.params.get('theta', None) == 0:
            # Element def specified theta = 0, don't change
            return self.transform.transform(drop), dwgtheta
        else:
            return self.transform.transform(drop), theta

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
            if transform:
                segment = segment.xform(self.transform)
            segxmin, segymin, segxmax, segymax = segment.get_bbox()
            xmin = min(xmin, segxmin)
            xmax = max(xmax, segxmax)
            ymin = min(ymin, segymin)
            ymax = max(ymax, segymax)

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
            ofst : float or list
                Offset between text and element. Defaults to Element.lblofst.
                Can be list of [x, y] offets.
            align : tuple
                Tuple of (horizontal, vertical) alignment where horizontal
                is ['center', 'left', 'right'] and vertical is ['center',
                'top', 'bottom']
            rotation : float
                Rotation angle (degrees)

            Keyword Arguments
            -----------------
            fontsize : float
                Font size
            font:
            color: string
                Label text color
        '''
        if isinstance(ofst, (list, tuple)) and loc in ['top', 'lft', 'bot', 'rgt']:
            raise TypeError('Offset must not be list for loc={}'.format(loc))

        if ofst is None:
            ofst = self.cparams.get('lblofst', .1)

        rotation = (rotation + 360) % 360
        if rotation > 90 and rotation < 270:
            rotation -= 180  # Keep the label from going upside down

        # This ensures a 'top' label is always on top, regardless of rotation
        theta = self.transform.theta
        if (theta % 360) > 90 and (theta % 360) <= 270:
            if loc == 'top':
                loc = 'bot'
            elif loc == 'bot':
                loc = 'top'
            elif loc == 'lft':
                loc = 'rgt'
            elif loc == 'rgt':
                loc = 'lft'

        if align is None:   # Determine best alignment for label based on angle
            th = theta - rotation
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
            elif loc in self.anchors:
                x1, y1, x2, y2 = self.get_bbox()
                if self.anchors[loc][1] == 0:
                    alignV = 'center'
                elif self.anchors[loc][1] > (y2+y1)/2:
                    alignV = 'bottom'
                else:
                    alignV = 'top'
                    ofst = -ofst
                if self.anchors[loc][0] > (x2+x1)/2:
                    alignH = 'left'
                else:
                    alignH = 'right'

                align = (alignH, alignV)
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
        xmax = self.bbox.xmax
        xmin = self.bbox.xmin
        ymax = self.bbox.ymax
        ymin = self.bbox.ymin
        if not np.isfinite(xmax+xmin+ymax+ymin):
            xmax = xmin = ymax = ymin = .1

        lblparams = dict(ChainMap(kwargs, self.cparams))
        lblparams.pop('label', None)  # Can't pop from nested chainmap, convert to flat dict first
        lblparams.update({'align': align, 'rotation': rotation})

        if isinstance(label, (list, tuple)):
            # Divide list along length
            if loc == 'top':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    xy = [xmin+xdiv*(i+1), ymax+ofst]
                    self.segments.append(SegmentText(np.asarray(xy), lbltxt, **lblparams))
            elif loc == 'bot':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    xy = [xmin+xdiv*(i+1), ymin-ofst]
                    self.segments.append(SegmentText(np.asarray(xy), lbltxt, **lblparams))
            elif loc == 'lft':
                for i, lbltxt in enumerate(label):
                    ydiv = (ymax-ymin)/(len(label)+1)
                    xy = [xmin-ofst, ymin+ydiv*(i+1)]
                    self.segments.append(SegmentText(np.asarray(xy), lbltxt, **lblparams))
            elif loc == 'rgt':
                for i, lbltxt in enumerate(label):
                    ydiv = (ymax-ymin)/(len(label)+1)
                    xy = [xmax+ofst, ymin+ydiv*(i+1)]
                    self.segments.append(SegmentText(np.asarray(xy), lbltxt, **lblparams))
            elif loc == 'center':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    xy = [xmin+xdiv*(i+1), ofst]
                    self.segments.append(SegmentText(np.asarray(xy), lbltxt, **lblparams))

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
            elif loc in self.anchors:
                xy = np.asarray(self.anchors[loc])
                if isinstance(ofst, (list, tuple)):
                    xy = xy + ofst
                else:
                    xy = np.asarray([xy[0], xy[1]+ofst])
            else:
                raise ValueError('Undefined location {}'.format(loc))
            self.segments.append(SegmentText(np.asarray(xy), label, **lblparams))

    def _draw_on_figure(self):
        ''' Draw the element on a new figure. Useful for _repr_ functions. '''
        fig = Figure()
        if self.cparams is None:
            self.place([0, 0], 0)
        fig.set_bbox(self.get_bbox(transform=True))
        self.draw(fig)
        return fig

    def _repr_svg_(self):
        ''' SVG representation for Jupyter '''
        fig = self._draw_on_figure()
        return fig.getimage(ext='svg')

    def _repr_png_(self):
        ''' PNG representation for Jupyter '''
        fig = self._draw_on_figure()
        return fig.getimage(ext='png')

    def draw(self, fig):
        ''' Draw the element '''
        if len(self.segments) == 0:
            self.place([0, 0], 0)
        for segment in self.segments:
            segment.draw(fig, self.transform, **self.cparams)


@adddocs(Element)
class ElementDrawing(Element):
    ''' Create an element from a Drawing

        Parameters
        ----------
        drawing: Drawing instance
            The drawing to convert to an element
    '''
    def __init__(self, drawing, **kwargs):
        super().__init__(**kwargs)
        self.drawing = drawing
        self.segments = self.drawing.get_segments()
        self.params['drop'] = self.drawing.here


@adddocs(Element)
class Element2Term(Element):
    ''' Two terminal element, with automatic lead extensions to result in the
        desired length. Anchors: start, center, end.

        Keyword Arguments
        -----------------
        to : [x, y] float array
            The end coordinate of the element
        tox : float
            x-value of end coordinate. y-value will be same as start
        toy : float
            y-value of end coordinate. x-value will be same as start
        l : float
            Total length of element
        endpts: tuple of 2 [x, y] float arrays
            The start and end points of the element. Overrides other
            2-terminal placement parameters.
    '''
    def place(self, dwgxy, dwgtheta, **dwgparams):
        ''' Place the element, adding lead extensions '''
        self.dwgparams = dwgparams
        if self.cparams is None:
            self.buildparams()

        totlen = self.cparams.get('l', self.cparams.get('unit', 3))
        endpts = self.cparams.get('endpts', None)
        to = self.cparams.get('to', None)
        tox = self.cparams.get('tox', None)
        toy = self.cparams.get('toy', None)
        anchor = self.cparams.get('anchor', None)
        zoom = self.cparams.get('zoom', 1)
        xy = np.asarray(self.cparams.get('at', dwgxy))

        # set up transformation
        theta = self.cparams.get('theta', dwgtheta)
        if endpts is not None:
            theta = angle(endpts[0], endpts[1])
        elif self.cparams.get('d') is not None:
            theta = {'u': 90, 'r': 0, 'l': 180, 'd': 270}[self.cparams.get('d')[0].lower()]
        elif to is not None:
            theta = angle(xy, np.asarray(to))

        # Get offset to element position within drawing (global shift)
        if endpts is not None:
            xy = endpts[0]

        if endpts is not None:
            totlen = distance(endpts[0], endpts[1])
        elif to is not None:
            # Move until X or Y position is 'end'. Depends on direction
            totlen = distance(xy, np.asarray(to))
        elif tox is not None:
            # Allow either full coordinate (only keeping x), or just an x value
            if isinstance(tox, float) or isinstance(tox, int):
                x = float(tox)
            else:
                x = tox[0]
            endpt = [x, xy[1]]
            totlen = distance(xy, endpt)
        elif toy is not None:
            # Allow either full coordinate (only keeping y), or just a y value
            if isinstance(toy, float) or isinstance(toy, int):
                y = toy
            else:
                y = toy[1]
            endpt = [xy[0], y]
            totlen = distance(xy, endpt)

        self.localshift = 0
        if self.cparams.get('extend', True):
            in_path = np.array(self.segments[0].path)
            dz = in_path[-1]-in_path[0]   # Defined delta of path
            in_len = np.sqrt(dz[0]*dz[0]+dz[1]*dz[1])   # Defined length of path
            lead_len = (totlen - in_len)/2

            if lead_len > 0:  # Don't make element shorter
                start = in_path[0] - np.array([lead_len, 0])
                end = in_path[-1] + np.array([lead_len, 0])
                self.localshift = -start
                self.segments[0].path = np.concatenate(([start], self.segments[0].path, [end]))
            else:
                start = in_path[0]
                end = in_path[-1]
                self.localshift = 0

        self.anchors['start'] = start
        self.anchors['end'] = end
        self.anchors['center'] = (start+end)/2

        if anchor is not None:
            self.localshift = -np.asarray(self.anchors[anchor])
        transform = Transform(theta, xy, self.localshift, zoom)

        self.absanchors = {}
        if len(self.segments) == 0:
            self.absanchors['start'] = transform.transform(np.array([0, 0]))
            self.absanchors['end'] = transform.transform(np.array([0, 0]))
            self.absanchors['center'] = transform.transform(np.array([0, 0]))
        else:
            self.absanchors['start'] = transform.transform(start)
            self.absanchors['end'] = transform.transform(end)
            self.absanchors['center'] = transform.transform((start+end)/2)

        self.params['drop'] = end
        return super().place(xy, theta, **dwgparams)
