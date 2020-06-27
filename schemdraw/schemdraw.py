''' Schemdraw Drawing class '''

from collections import namedtuple
import warnings
import numpy as np

from .elements import Element
from .elements.lines import LoopCurrent, CurrentLabel, CurrentLabelInline
from .backends.mpl import Figure

BBox = namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])


class Drawing(object):
    ''' Create a schematic drawing

        Parameters
        ----------
        *elements : Element
            List of Element instances to add to the drawing
        unit : float
            Full length of a 2-terminal element. Inner zig-zag portion
            of a resistor is 1.0 units.
        inches_per_unit : float
            Inches per drawing unit for setting drawing scale
        lblofst : float
            Offset between element and its label
        fontsize : float
            Default font size for text labels
        font : string
            Default font family for text labels
        color : string or tuple
            Default color name or RGB (0-1) tuple
        lw : float
            Default line width for elements
        ls : string
            Default line style '-', ':', '--', etc.
        fill : string or tuple
            Deault fill color for closed elements
    '''
    def __init__(self, *elements, unit=3.0, inches_per_unit=0.5, lblofst=0.1,
                 fontsize=16, font='sans-serif', color='black',
                 lw=2, ls='-', fill=None):
        self.elements = []
        self.inches_per_unit = inches_per_unit
        self.unit = unit
        self.dwgparams = {'unit': unit,
                          'font': font,
                          'fontsize': fontsize,
                          'lblofst': lblofst,
                          'color': color,
                          'lw': lw,
                          'ls': ls,
                          'fill': fill}

        self.here = [0, 0]
        self.theta = 0
        self._state = []  # Push/Pop stack

        for element in elements:
            self.add(element)

    def get_bbox(self):
        ''' Get drawing bounding box '''
        xmin = np.inf
        xmax = -np.inf
        ymin = np.inf
        ymax = -np.inf
        for element in self.elements:
            bbox = element.get_bbox(transform=True)
            xmin = min(bbox.xmin, xmin)
            xmax = max(bbox.xmax, xmax)
            ymin = min(bbox.ymin, ymin)
            ymax = max(bbox.ymax, ymax)
        return BBox(xmin, ymin, xmax, ymax)

    def get_segments(self):
        ''' Get flattened list of all segments in the drawing '''
        segments = []
        for element in self.elements:
            segments.extend([s.xform(element.transform, **element.cparams)
                             for s in element.segments])
        return segments

    def _repr_svg_(self):
        ''' SVG representation for Jupyter '''
        return self.draw().getimage('svg')

    def _repr_png_(self):
        ''' PNG representation for Jupyter '''
        return self.draw().getimage('png')

    def add(self, element, **kwargs):
        ''' Add an element to the drawing.

            Parameters
            ----------
            element : schemdraw.elements.Element
                The element class to add.
            **kwargs : passed to element instantiation if element is a class
        '''
        if not isinstance(element, Element):
            # Instantiate it (for support of legacy add method)
            element = element(**kwargs)
        elif len(kwargs) > 0:
            warnings.warn('kwargs to add method are ignored because element is already instantiated')

        self.here, self.theta = element.place(self.here, self.theta, **self.dwgparams)
        self.elements.append(element)
        return element

    def add_elements(self, *elements):
        ''' Add multiple elements to the drawing '''
        for element in elements:
            self.add(element)

    def push(self):
        ''' Push/save the drawing state.
            Drawing.here and Drawing.theta are saved.
        '''
        self._state.append((self.here, self.theta))

    def pop(self):
        ''' Pop/load the drawing state. Location and angle are returned to
            previously pushed state.
        '''
        if len(self._state) > 0:
            self.here, self.theta = self._state.pop()

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
        top = bbox1.ymin - pad
        bot = bbox3.ymax + pad
        left = bbox4.xmax + pad
        rght = bbox2.xmin - pad
        center = [(left+rght)/2, (top+bot)/2]
        element = LoopCurrent(xy=center, label=label, width=rght-left,
                              height=top-bot, direction=d, theta1=theta1,
                              theta2=theta2)
        self.add(element)
        return element

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
        element = CurrentLabel(xy=elm.center, theta=elm.transform.theta, label=label,
                               ofst=arrowofst, length=arrowlen, rev=reverse, top=top)
        self.add(element)
        return element

    def labelI_inline(self, elm, label='', botlabel='', d='in', start=True, ofst=.8):
        ''' Add an arrowhead for labeling current inline with leads.
            Works on Element2Term elements.

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
                Offset from center of element
        '''
        element = CurrentLabelInline(xy=elm.center, label=label, botlabel=botlabel,
                                     direction=d, ofst=ofst, start=start,
                                     theta=elm.transform.theta)
        self.add(element)
        return element

    def draw(self, showframe=False):
        ''' Draw the schematic

            Parameters
            ----------
            showframe : bool
                Show axis frame. Useful for debugging a drawing.
        '''
        fig = Figure(bbox=self.get_bbox(),
                     inches_per_unit=self.inches_per_unit,
                     showframe=showframe)
        for element in self.elements:
            element.draw(fig)
        fig.show()  # Show figure in window if not inline/Jupyter mode
        return fig  # Otherwise return Figure and let _repr_ display it

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
        fig = self.draw()
        fig.save(fname, transparent=transparent, dpi=dpi)
