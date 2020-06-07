''' Schemdraw base Element class '''

from io import StringIO, BytesIO
from collections import ChainMap
import numpy as np
from matplotlib.pyplot import Figure

from ..segments import *
from ..transform import Transform, mirror_point, flip_point

gap = [np.nan, np.nan]  # Put a gap in a path (matplotlib skips NaNs)    


class Element(object):
    ''' Element Keyword Arguments
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
        lblloc : ['top', 'bot', 'lft', 'rgt', 'center']
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

    def setup(self, **kwargs):
        ''' Set up element definition. Subclass this to define different elements. '''
        self.segments = []
        self.params = {}

    def buildparams(self):
        ''' Combine parameters from user, setup, and drawing '''
        self.setup(**ChainMap(self.userparams, self.dwgparams))

        if 'xy' in self.userparams:
            self.userparams.setdefault('at', self.userparams.pop('xy'))

        # Accomodate xy positions based on other elements before they are fully set up.
        if 'at' in self.userparams and isinstance(self.userparams['at'][1], str):
            element, pos = self.userparams['at']
            if pos in element.absanchors:
                xy = element.absanchors[pos]
            else:
                raise KeyError('Unknown anchor name {}'.format(pos))
            self.userparams['at'] = xy

        self.cparams = ChainMap(self.userparams, self.params, self.dwgparams)  # All subsequent actions get params from this one
        self.flipreverse()
        
    def flipreverse(self):
        ''' Flip and/or reverse segments if necessary '''
        if self.cparams.get('flip', False):
            [s.doflip() for s in self.segments]
            for name, pt in self.anchors.items():
                self.anchors[name] = flip_point(pt)
            
        if self.cparams.get('reverse', False):
            if 'center' in self.anchors:
                centerx = self.anchors['center'][0]
            else:
                xmin, xmax, _, _ = self.get_bbox()
                centerx = (xmin + xmax)/2
            [s.doreverse(centerx) for s in self.segments]
            for name, pt in self.anchors.items():
                self.anchors[name] = mirror_point(pt, centerx)
    
    def place(self, dwgxy, dwgtheta, **dwgparams):
        ''' Determine position within the drawing '''
        self.dwgparams = dwgparams
        if self.cparams is None:
            self.buildparams()
        
        localshift = np.array([0, 0])
        
        params = {}
        anchor = self.cparams.get('anchor', None)
        zoom = self.cparams.get('zoom', 1)
        xy = np.asarray(self.cparams.get('at', dwgxy))
        
        # Get bounds of element, used for positioning user labels
        self.xmin, self.ymin, self.xmax, self.ymax = self.get_bbox()
        
        if self.cparams.get('d') is not None:
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
                self.add_label(label, loc, ofst=lblofst, size=lblsize, rotation=rotation, color=lblcolor)
        
        # Add element-specific anchors
        for name, pos in self.anchors.items():
            self.absanchors[name] = self.transform.transform(np.array(pos))        
        self.absanchors['xy'] = self.transform.transform([0, 0])
        
        # Set all anchors as attributes
        for name, pos in self.absanchors.items():
            if getattr(self, name, None) is not None:  # Try not to clobber element parameter names!
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
            fontsize : float
                Font size
            font:
            color: string
                Matplotlib color
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

        lblparams = dict(ChainMap(kwargs, self.cparams))
        lblparams.pop('label', None)  # Can't pop from nested chainmap, convert to flat dict first
        size = lblparams.get('fontsize', lblparams.get('size', 14))
        font = lblparams.get('font', 'sans-serif')
        lblparams.update({'align': align, 'rotation': rotation})

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
        fig.subplots_adjust(
            left=0.05,
            bottom=0.05,
            right=0.95,
            top=0.90)
        ax = fig.add_subplot()
        ax.autoscale_view(True)  # This autoscales all the shapes too        
        self.draw(ax)
        
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
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        ax.set_frame_on(False)
        inches_per_unit = 0.5
        ax.get_figure().set_size_inches(inches_per_unit*w, inches_per_unit*h)
        return fig

    def _repr_svg_(self):
        output = StringIO()
        fig = self._draw_on_figure()
        fig.savefig(output, format='svg', bbox_inches='tight')
        return output.getvalue()

    def _repr_png_(self):
        output = BytesIO()
        fig = self._draw_on_figure()
        fig.savefig(output, format='png', bbox_inches='tight')
        return output.getvalue()

    def draw(self, ax):
        ''' Draw the element '''
        if len(self.segments) == 0:
            self.place([0, 0], 0)

        for segment in self.segments:
            segment.draw(ax, self.transform)


class ElementDrawing(Element):
    ''' Create an element from a Drawing
    
        Parameters
        ----------
        drawing: Drawing instance
            The drawing to convert to an element
        
        Keyword arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, drawing, **kwargs):
        self.drawing = drawing
        super().__init__(**kwargs)

    def setup(self, **kwargs):
        ''' Set up the element by combineing all segments in drawing '''
        for element in self.drawing.elements:
            self.segments.extend([s.xform(element.transform) for s in element.segments])
        self.params['drop'] = self.drawing.here