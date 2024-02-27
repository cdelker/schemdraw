''' Schemdraw base Element class '''

from __future__ import annotations
from typing import Sequence, MutableMapping, Any, Union, Optional
from collections import ChainMap
from dataclasses import dataclass
import warnings
import math

from .. import default_canvas
from ..segments import Segment, SegmentText, SegmentCircle, BBox, SegmentType
from ..transform import Transform
from .. import util
from ..util import Point
from ..types import XY, Linestyle, Halign, Valign, LabelLoc
from .. import drawing_stack

from ..backends.svg import Figure as svgFigure
try:
    from ..backends.mpl import Figure as mplFigure
except ImportError:
    mplFigure = None  # type: ignore


gap = (math.nan, math.nan)  # Put a gap in a path


@dataclass
class Label:
    ''' Element Label Parameters. '''
    label: str | Sequence[str]
    loc: LabelLoc | None = None   # top, bot, lft, rgt, OR anchor
    ofst: XY | float | None = None
    halign: Halign | None = None
    valign: Valign | None = None
    rotate: bool | float = False  # True=same angle as element; False = 0
    fontsize: float | None = None
    font: str | None = None
    mathfont: str | None = None
    color: str | None = None


class Element:
    ''' Standard circuit element.

        Keyword Arguments are equivalent to calling
        setter methods.

        Args:
            d: Drawing direction ('up', 'down', 'left', 'right')

        Attributes:
            anchors: Dictionary of anchor positions in element
                coordinates
            absanchors: Dictionary of anchor positions in absolute
                drawing coordinates
            segments: List of drawing primitives making up the element
            transform: Transformation from element to drawing coordinates
            absdrop: Drop position in drawing coordinates, set after the
                element is added to a drawing
            defaults: Default parameters for the element

        Anchor names are dynmically added as attributes after placing the
        element in a Drawing.
    '''
    _element_defaults: dict[str, Any] = {}     # Default parameters for subclassed elements
    defaults: ChainMap[str, Any] = ChainMap()  # Subclasses will chainmap this with parents  
    def __init__(self, **kwargs) -> None:
        self._userparams.update(kwargs)         # Specified by user
        self._localshift: XY = Point((0, 0))
        self._userlabels: list[Label] = []

        self.anchors: MutableMapping[str, Union[Point, tuple[float, float]]] = {}  # Untransformed anchors
        self.absanchors: MutableMapping[str, Any] = {}  # Transformed, absolute anchors
        self.segments: list[SegmentType] = []
        self.transform = Transform(0, (0, 0))
        self._positioned = False  # Has the element been placed in a drawing via self._position()?

        if 'xy' in self._userparams:  # Allow legacy 'xy' parameter
            self._userparams.setdefault('at', self._userparams.pop('xy'))

        drawing_stack.push_element(self)

    def __new__(cls, *args, **kwargs):
        ''' Create a new Element instance, building chainmap of params '''
        new = super().__new__(cls)
        new._dwgparams = {}  # Defaults from drawing
        new.elmparams = {}  # Parameters specified by element. Similar to _element_defaults, but may be dynamic
        new._userparams = {name: value for name, value in kwargs.items() if value is not None}
        new.params = ChainMap(new._userparams, new.elmparams, new.defaults, new._dwgparams)
        return new

    def __init_subclass__(self):
        ''' Initialize an Element subclass, building chainmap of default parameters
            from parent classes.
        '''
        if len(self.__mro__) > 1 and hasattr(self.__mro__[1], 'defaults'):
            if self.__mro__[1]._element_defaults is not self._element_defaults:
                self.defaults = self.__mro__[1].defaults.new_child(self._element_defaults)
            else:
                self.defaults = self.__mro__[1].defaults.new_child()
        else:
            self.defaults = ChainMap()

    def __getattr__(self, name: str) -> Any:
        ''' Allow getting anchor position as attribute '''
        anchornames = ['start', 'end', 'center', 'istart', 'iend',
                       'N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW',
                       'NNE', 'NNW', 'ENE', 'WNW', 'SSE', 'SSW', 'ESE', 'WSW']
        if (name in anchornames + list(vars(self).get('anchors', {}).keys()) and
            not name in vars(self).get('absanchors', {})):
                # Not placed yet
                drawing_stack.push_element(self)

        if name in vars(self).get('absanchors', {}):
            return vars(self).get('absanchors')[name]  # type: ignore
        raise AttributeError(f'{name} not defined in Element')

    def up(self) -> 'Element':
        ''' Set the direction to up '''
        if 'd' in self._userparams:
            warnings.warn(f"Duplicated direction parameter in element. `{self._userparams['d']}` changed to `up`.")
        self._userparams['d'] = 'up'
        return self

    def down(self) -> 'Element':
        ''' Set the direction to down '''
        if 'd' in self._userparams:
            warnings.warn("Duplicated direction parameter in element."
                          f" `{self._userparams['d']}` changed to `down`.")
        self._userparams['d'] = 'down'
        return self

    def left(self) -> 'Element':
        ''' Set the direction to left '''
        if 'd' in self._userparams:
            warnings.warn("Duplicated direction parameter in element."
                          f" `{self._userparams['d']}` changed to `left`.")
        self._userparams['d'] = 'left'
        return self

    def right(self) -> 'Element':
        ''' Set the direction to right '''
        if 'd' in self._userparams:
            warnings.warn("Duplicated direction parameter in element."
                          f" `{self._userparams['d']}` changed to `right`.")
        self._userparams['d'] = 'right'
        return self

    def theta(self, theta: float) -> 'Element':
        ''' Set the drawing direction angle in degrees '''
        if 'd' in self._userparams:
            warnings.warn("Duplicate direciton parameter in element:"
                          f" `{self._userparams['d']}` replaced with `theta={theta}`")
        self._userparams['theta'] = theta
        return self

    def drop(self, drop: Union[str, Point]) -> 'Element':
        ''' Set the drop position - where to leave the current drawing position after
            placing this element
        '''
        self._userparams['drop'] = drop
        return self

    def at(self, xy: XY | tuple['Element', str], dx: float = 0, dy: float = 0) -> 'Element':
        ''' Set the element xy position

            Args:
                xy: (x,y) position or tuple of (Element, anchorname)
        '''
        if 'at' in self._userparams:
            warnings.warn("Duplicate `at` parameter in element: "
                          f"`{self._userparams['at']}` changed to `{xy}`.")
        if isinstance(xy[1], str):
            self._userparams['at'] = xy
            if dx != 0 or dy != 0:
                raise ValueError('dx and dy must be zero for anchorname XY')
        else:
            xy = Point(xy)
            self._userparams['at'] = Point((xy.x + dx, xy.y + dy))
        return self

    def scale(self, scale: float = 1) -> 'Element':
        ''' Apply scale/zoom factor to element '''
        self._userparams['zoom'] = Point((scale, scale))
        return self

    def scalex(self, scale: float = 1) -> 'Element':
        ''' Apply horizontal scale/zoom to element '''
        oldscale = self._userparams.get('zoom', Point((1, 1)))
        self._userparams['zoom'] = Point((scale, oldscale.y))
        return self

    def scaley(self, scale: float = 1) -> 'Element':
        ''' Apply vertical scale/zoom to element '''
        oldscale = self._userparams.get('zoom', Point((1, 1)))
        self._userparams['zoom'] = Point((oldscale.x, scale))
        return self

    def flip(self) -> 'Element':
        ''' Apply flip up/down '''
        self._userparams['flip'] = True
        return self

    def reverse(self) -> 'Element':
        ''' Apply reverse left/right '''
        if 'reverse' in self._userparams:
            self._userparams['reverse'] = not self._userparams['reverse']
        else:
            self._userparams['reverse'] = True
        return self

    def anchor(self, anchor: str) -> 'Element':
        ''' Specify anchor for placement. The anchor will be
            aligned with the position specified by `at()` method.
        '''
        if 'anchor' in self._userparams:
            warnings.warn("Duplicate anchor parameter in element: "
                          f"`{self._userparams['anchor']}` changed to `{anchor}`.")

        self._userparams['anchor'] = anchor
        return self

    def color(self, color: str) -> 'Element':
        ''' Sets the element color

            Args:
                color: color name or hex value (ie '#FFFFFF')
        '''
        self._userparams['color'] = color
        return self

    def linestyle(self, ls: Linestyle) -> 'Element':
        ''' Sets the element line style

            Args:
                ls: Line style ('-', ':', '--', '-.').
        '''
        self._userparams['ls'] = ls
        return self

    def linewidth(self, lw: float) -> 'Element':
        ''' Sets the element line width

            Args:
                lw: Line width
        '''
        self._userparams['lw'] = lw
        return self

    def fill(self, color: bool | str = True) -> 'Element':
        ''' Sets the element fill color.

            Args:
                color: Color string name or hex value, or
                `True` to fill with the element line color.
        '''
        self._userparams['fill'] = color
        return self

    def style(self, color: Optional[str] = None, fill: Optional[str] = None,
              ls: Optional[Linestyle] = None, lw: Optional[float] = None) -> 'Element':
        ''' Apply all style parameters

            Args:
                color: Color string or hex value
                fill: Color string or hex
                ls: Line style ('-', ':', '--', '-.')
                lw: Line width
        '''
        if color is not None:
            self.color(color)
        if fill is not None:
            self.fill(fill)
        if ls is not None:
            self.linestyle(ls)
        if lw is not None:
            self.linewidth(lw)
        return self

    def zorder(self, zorder: int) -> 'Element':
        ''' Sets the element zorder. Higher zorders will be drawn above
            lower zorder elements.
        '''
        self._userparams['zorder'] = zorder
        return self

    def hold(self) -> 'Element':
        ''' Do not move the Drawing `here` position after placing this element '''
        self._userparams['move_cur'] = False
        return self

    def label(self,
              label: str | Sequence[str],
              loc: Optional[LabelLoc] = None,
              ofst: XY | float | None = None,
              halign: Optional[Halign] = None,
              valign: Optional[Valign] = None,
              rotate: bool | float = False,
              fontsize: Optional[float] = None,
              font: Optional[str] = None,
              mathfont: Optional[str] = None,
              color: Optional[str] = None):
        ''' Add a label to the Element.

            Args:
                label: The text string or list of strings. If list, each string will
                    be evenly spaced along the element (e.g. ['-', 'V', '+'])
                loc: Label position within the Element. Either ('top', 'bottom', 'left',
                    'right'), or the name of an anchor within the Element.
                ofst: Offset from default label position
                halign: Horizontal text alignment ('center', 'left', 'right')
                valign: Vertical text alignment ('center', 'top', 'bottom')
                rotate: True to rotate label with element, or specify rotation
                    angle in degrees
                fontsize: Size of label font
                font: Name/font-family of label text
                mathfont: Name/font-family of math text
                color: Color of label
        '''
        if not rotate:
            rotate = 0
        elif isinstance(rotate, bool):
            rotate = True
        self._userlabels.append(Label(label, loc, ofst, halign, valign, rotate, fontsize, font, mathfont, color))
        return self

    def _position(self) -> None:
        ''' Convert relative positions to absolute coordinates in self.params,
            and apply flip/reverse
        '''
        # Accomodate xy positions based on OTHER elements before they are fully set up.
        if 'at' in self._userparams and isinstance(self._userparams['at'][1], str):
            element, pos = self._userparams['at']
            if pos in element.absanchors:
                xy = element.absanchors[pos]
            else:
                raise KeyError(f'Unknown anchor name {pos}')
            self._userparams['at'] = xy

        self._flipreverse()
        self._positioned = True

    def _flipreverse(self) -> None:
        ''' Flip and/or reverse element's segments if necessary '''
        if self._userparams.get('flip', False):
            for s in self.segments:
                s.doflip()
            for name, pt in self.anchors.items():
                self.anchors[name] = Point(pt).flip()

        if self._userparams.get('reverse', False):
            if 'center' in self.anchors:
                centerx = self.anchors['center'][0]
            else:
                xmin, _, xmax, _ = self.get_bbox(includetext=False)
                centerx = (xmin + xmax)/2
            [s.doreverse(centerx) for s in self.segments]  # type: ignore
            for name, pt in self.anchors.items():
                self.anchors[name] = Point(pt).mirrorx(centerx)

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate element position within the drawing
        
            Args:
                dwgxy: Current XY position within drawing
                dwgtheta: Current theta in the drawing
                dwgparams: Default parameters of the drawing
            
            Returns:
                xy: New XY position after placing the element
                theta: New theta after placing the element
        '''
        self._dwgparams.clear()  # Don't remove the original object so self.params ChainMap gets the new values.
        self._dwgparams.update(dwgparams)
        if not self._positioned:
            self._position()

        anchor = self.params.get('anchor', None)
        zoom = self.params.get('zoom', self.params.get('scale', 1))
        xy = self.params.get('at', dwgxy)

        # Get bounds of element, used for positioning user labels
        self.bbox = self.get_bbox(includetext=False)

        theta: float
        if 'endpts' in self.params:
            theta = dwgtheta
        elif self.params.get('d') is not None:
            d = self.params.get('d')
            if str(d).lstrip('-').isnumeric():
                theta = float(str(d))
            else:
                theta = {'u': 90, 'r': 0, 'l': 180, 'd': 270}[d[0].lower()]  # type: ignore
        else:
            theta = self.params.get('theta', dwgtheta)

        if anchor is not None:
            self._localshift = -Point(self.anchors[anchor])
        self.transform = Transform(theta, xy, self._localshift, zoom)

        # Add user-defined labels
        lblloc = self.params.get('lblloc', 'top')
        lblsize = self.params.get('lblsize', self.params.get('fontsize', 14))
        lblrotate = self.params.get('lblrotate', False)
        lblcolor = self.params.get('color', 'black')
        kwlabels = {
            'top': self.params.get('toplabel', None),
            'bot': self.params.get('botlabel', None),
            'lft': self.params.get('lftlabel', None),
            'rgt': self.params.get('rgtlabel', None),
            'center': self.params.get('clabel', None)
            }
        if 'label' in self.params:
            kwlabels[lblloc] = self.params.get('label')

        # Add labels defined in **kwargs to the _userlabels list
        for loc, label in kwlabels.items():
            if label is not None:
                rotate = (theta if lblrotate else 0)
                self.label(label, loc, fontsize=lblsize, rotate=rotate, color=lblcolor)

        for label in self._userlabels:
            self._place_label(label, theta)

        # Add element-specific anchors
        for name, pos in self.anchors.items():
            self.absanchors[name] = self.transform.transform(pos)
        self.absanchors['xy'] = self.transform.transform((0, 0))

        drop = self.params.get('drop', None)
        if drop is not None and drop in self.anchors:
            # User specified as anchor position
            self.absdrop = self.transform.transform(self.anchors[drop]), theta
        elif drop is not None and self.params.get('move_cur', True):
            if self.params.get('droptheta', None) is not None:
                # Element-specified drop angle
                self.absdrop = self.transform.transform(drop), self.params.get('droptheta', 0.)
            elif self.params.get('theta', None) == 0:
                # Element-specified theta of 0, don't change theta
                self.absdrop = self.transform.transform(drop), dwgtheta
            else:
                self.absdrop = self.transform.transform(drop), theta
        else:  # drop is None:
            self.absdrop = Point(dwgxy), dwgtheta
        return self.absdrop

    def get_bbox(self, transform=False, includetext=True):
        ''' Get element bounding box

            Args:
                transform: Apply the element transform to the bbox
                    to get bounds in Drawing coordinates
                includetext: Consider text when calculating bounding
                    box. Text width and height can vary by font,
                    so this produces an estimate of bounds.

            Returns:
                Corners of the bounding box, (xmin, ymin, xmax, ymax)
        '''
        xmin = ymin = math.inf
        xmax = ymax = -math.inf
        for segment in self.segments:
            if not includetext and isinstance(segment, SegmentText):
                continue
            if transform:
                segment = segment.xform(self.transform)
            segxmin, segymin, segxmax, segymax = segment.get_bbox()
            xmin = min(xmin, segxmin)
            xmax = max(xmax, segxmax)
            ymin = min(ymin, segymin)
            ymax = max(ymax, segymax)

        return BBox(xmin, ymin, xmax, ymax)

    def _position_label(self, label: Label, theta: float = 0) -> Label:
        ''' Calculate position of label
        
            Args:
                label: The label to position
                theta: Element drawing direction
        '''
        if label.rotate is None:
            label.rotate = 0
        elif label.rotate is True:
            label.rotate = theta
        label.rotate = (label.rotate + 360) % 360
        if 90 < label.rotate < 270:
            label.rotate -= 180  # Keep the label from going upside down

        # Set label default location if not specified
        if label.loc is None:
            label.loc = self.params.get('lblloc', 'top')

        # Allow some aliases for positional locations
        label.loc = {'bot': 'bottom',
                     'B': 'bottom',
                     'lft': 'left',
                     'L': 'left',
                     'rgt': 'right',
                     'R': 'right',
                     'T': 'top'}.get(label.loc, label.loc)

        # Ensure a 'top' label is always on top, regardless of rotation
        if (theta % 360) > 90 and (theta % 360) <= 270:
            if label.loc == 'top':
                label.loc = 'bottom'
            elif label.loc == 'bottom':
                label.loc = 'top'
            elif label.loc == 'left':
                label.loc = 'right'
            elif label.loc == 'right':
                label.loc = 'left'
        return label

    def _align_label(self, label: Label, theta: float = 0) -> tuple[Halign, Valign, Point]:
        ''' Calculate label alignment and offset based on angle and location
            relative to the element

            Args:
                label: The label to position
                theta: Element drawing direction

            Returns:
                Align: suggested horizontal and vertical alignment
                Offset: suggested horizontal and vertical offset from label position
        '''
        newofst = label.ofst
        assert newofst is not None
        if isinstance(label.ofst, (float, int)):
            newofst = Point((label.ofst, label.ofst))
        else:
            newofst = Point(newofst)  # type: ignore

        if label.loc == 'center':
            newhalign: Halign = 'center'
            newvalign: Valign = 'center'

        elif label.loc and label.loc in self.anchors: 
            # Anchor is on an edge
            x1, y1, x2, y2 = self.get_bbox(includetext=False)
            newhalign = newvalign = 'center'
            if math.isclose(self.anchors[label.loc][0], x1, abs_tol=.15):
                # Label on left edge
                newhalign = 'right'
            elif math.isclose(self.anchors[label.loc][0], x2, abs_tol=.15):
                # Label on right edge
                newhalign = 'left'
            else:
                # Not on left or right edge
                newhalign = 'center'

            if math.isclose(self.anchors[label.loc][1], y1, abs_tol=.15):
                # Label on bottom edge
                newvalign = 'top'
            elif math.isclose(self.anchors[label.loc][1], y2, abs_tol=.15):
                # Label on top edge
                newvalign = 'bottom'
            else:
                # Not on top or bottom edge
                newvalign = 'center'

            # Fix offset if provided as single value
            if isinstance(label.ofst, (float, int)):
                pofst = label.ofst
                newofst = {
                    ('center', 'bottom'): (0, pofst),
                    ('right', 'bottom'): (-pofst, pofst),
                    ('right', 'center'): (-pofst, 0),
                    ('right', 'top'): (-pofst, -pofst),
                    ('center', 'top'): (0, -pofst),
                    ('left', 'top'): (pofst, -pofst),
                    ('left', 'center'): (pofst, 0),
                    ('left', 'bottom'): (pofst, pofst)
                }.get((newhalign, newvalign), (0, pofst))
                newofst = Point(newofst)

        else:
            # Align based on position relative to the element
            # Below alignment dictionary works for label on top.
            # Rotate angle for other sides.
            th = theta - label.rotate
            th = {'left': th+90,
                  'bottom': th+180,
                  'right': th+270}.get(label.loc, th)  # type: ignore
            th = (th+360) % 360  # Normalize angle so it's positive, clockwise

            # Alignment for label in different positions
            rotalign: list[tuple[Halign, Valign]] = [
                ('center', 'bottom'),  # label on top
                ('right', 'bottom'),
                ('right', 'center'),   # label on left
                ('right', 'top'),
                ('center', 'top'),     # label on bottom
                ('left', 'top'),
                ('left', 'center'),    # label on right
                ('left', 'bottom')]
            newhalign, newvalign = rotalign[int(round((th/360)*8) % 8)]

            # Ensure label.ofst is a Point (x,y) pair
            if isinstance(label.ofst, (float, int)):
                if label.loc == 'bottom':
                    newofst = (0, -label.ofst)
                elif label.loc == 'left':
                    newofst = (-label.ofst, 0)
                elif label.loc == 'right':
                    newofst = (label.ofst, 0)
                else:
                    newofst = (0, label.ofst)
                newofst = Point(newofst)
        return newhalign, newvalign, newofst

    def _place_label(self, label: Label, theta: float = 0) -> None:
        ''' Adds the label SegmentText to the element, after element placement

            Args:
                label: The Label to add
                theta: Current drawing angle
        '''
        # Make a copy of the label to modify with auto-placement values
        label = Label(label.label, label.loc, label.ofst, label.halign,
                      label.valign, label.rotate, label.fontsize,
                      label.font, label.mathfont, label.color)

        if label.halign is None:
            label.halign = self.params.get('lblalign', (None, None))[0]
        if label.valign is None:
            label.valign = self.params.get('lblalign', (None, None))[1]

        if label.ofst is None:
            label.ofst = self.params.get('lblofst', .1)
        
        label = self._position_label(label, theta)
        halign, valign, ofst = self._align_label(label, theta)
        label.halign = label.halign if label.halign is not None else halign
        label.valign = label.valign if label.valign is not None else valign
        label.ofst = ofst

        # Parameters to send to SegmentText
        segment_params = {
            'color': label.color if label.color else self.params.get('color'),
            'font': label.font if label.font else self.params.get('font'),
            'mathfont': label.mathfont if label.mathfont else self.params.get('mathfont'),
            'fontsize': label.fontsize if label.fontsize else self.params.get('fontsize', 14),
            'align': (label.halign, label.valign),
            'rotation': label.rotate}

        xmax = self.bbox.xmax
        xmin = self.bbox.xmin
        ymax = self.bbox.ymax
        ymin = self.bbox.ymin
        if not math.isfinite(xmax+xmin+ymax+ymin):
            xmax = xmin = ymax = ymin = .1

        if isinstance(label.label, (list, tuple)):
            if label.loc == 'top':
                xdiv = (xmax-xmin)/(len(label.label)+1)
                for i, lbltxt in enumerate(label.label):
                    xy = Point((xmin+xdiv*(i+1), ymax))
                    self.segments.append(SegmentText(xy+label.ofst, lbltxt, **segment_params))
            elif label.loc == 'bottom':
                xdiv = (xmax-xmin)/(len(label.label)+1)
                for i, lbltxt in enumerate(label.label):
                    xy = Point((xmin+xdiv*(i+1), ymin))
                    self.segments.append(SegmentText(xy+label.ofst, lbltxt, **segment_params))
            elif label.loc == 'left':
                ydiv = (ymax-ymin)/(len(label.label)+1)
                for i, lbltxt in enumerate(label.label):
                    xy = Point((xmin, ymin+ydiv*(i+1)))
                    self.segments.append(SegmentText(xy+label.ofst, lbltxt, **segment_params))
            elif label.loc == 'right':
                ydiv = (ymax-ymin)/(len(label.label)+1)
                for i, lbltxt in enumerate(label.label):
                    xy = Point((xmax, ymin+ydiv*(i+1)))
                    self.segments.append(SegmentText(xy+label.ofst, lbltxt, **segment_params))
            elif label.loc == 'center':
                xdiv = (xmax-xmin)/(len(label.label)+1)
                for i, lbltxt in enumerate(label.label):
                    xy = Point((xmin+xdiv*(i+1), 0))
                    self.segments.append(SegmentText(xy+label.ofst, lbltxt, **segment_params))

        elif isinstance(label.label, str):  # keep the elif instead of else for type hinting
            if label.loc and label.loc in self.anchors:
                xy = Point(self.anchors[label.loc])
            elif label.loc == 'top':
                xy = Point(((xmax+xmin)/2, ymax))
            elif label.loc == 'bottom':
                xy = Point(((xmax+xmin)/2, ymin))
            elif label.loc == 'left':
                xy = Point((xmin, (ymax+ymin)/2))
            elif label.loc == 'right':
                xy = Point((xmax, (ymax+ymin)/2))
            elif label.loc == 'center':
                xy = Point(((xmax+xmin)/2, (ymax+ymin)/2))
            else:
                raise ValueError(f'Undefined location {label.loc}')
            self.segments.append(SegmentText(xy+label.ofst, label.label, **segment_params))

    def _draw_on_figure(self):
        ''' Draw the element on a new figure. Useful for _repr_ functions. '''
        if default_canvas.default_canvas == 'matplotlib':
            fig = mplFigure()
        else:
            fig = svgFigure(bbox=self.get_bbox(transform=True))
        if not self._positioned:
            self._place((0, 0), 0)
        fig.set_bbox(self.get_bbox(transform=True))
        self._draw(fig)
        return fig

    def _repr_svg_(self):
        ''' SVG representation for Jupyter '''
        fig = self._draw_on_figure()
        return fig.getimage(ext='svg').decode()

    def _repr_png_(self):
        ''' PNG representation for Jupyter '''
        if default_canvas.default_canvas == 'svg':
            return None
        fig = self._draw_on_figure()
        return fig.getimage(ext='png')

    def _draw(self, fig) -> None:
        ''' Draw the element on a Figure '''
        if len(self.segments) == 0:
            self._place((0, 0), 0)
        for segment in self.segments:
            segment.draw(fig, self.transform, **self.params)

        if self.params.get('elmbbox', False):
            # Draw element bounding box
            bbox = self.get_bbox()
            Segment(((bbox.xmin, bbox.ymin), (bbox.xmax, bbox.ymin),
                     (bbox.xmax, bbox.ymax), (bbox.xmin, bbox.ymax), (bbox.xmin, bbox.ymin)),
                     color='blue', lw=.5).draw(fig, self.transform)


class ElementDrawing(Element):
    ''' Create an element from a Drawing

        Args:
            drawing: The Drawing instance to convert to an element
    '''
    def __init__(self, drawing, **kwargs):
        super().__init__(**kwargs)
        self.drawing = drawing
        self.segments = self.drawing.get_segments()
        self.anchors = self.drawing.anchors
        self.elmparams['drop'] = self.drawing._here
        self.elmparams['d'] = 'right'  # Reset drawing direction
        

class Element2Term(Element):
    ''' Two terminal element. The element leads can be automatically
        extended to the start and ending positions.

        Anchors:
            * start
            * center
            * end
    '''
    _element_defaults = {
        'leadcolor': None,  # Inherit
        'dotradius': 0.075
    }
    def to(self, xy: XY, dx: float = 0, dy: float = 0) -> 'Element2Term':
        ''' Sets ending position of element

            Args:
                xy: Ending position of element
                dx: X-offset from xy position
                dy: Y-offset from xy position
        '''
        xy = Point(xy)
        self._userparams['to'] = Point((xy.x + dx, xy.y + dy))
        return self

    def tox(self, x: float | XY | Element) -> 'Element2Term':
        ''' Sets ending x-position of element (for horizontal elements) '''
        self._userparams['tox'] = x
        return self

    def toy(self, y: float | XY | Element) -> 'Element2Term':
        ''' Sets ending y-position of element (for vertical elements) '''
        self._userparams['toy'] = y
        return self

    def up(self, length: Optional[float] = None) -> 'Element':
        ''' Set the direction to up '''
        if 'd' in self._userparams:
            warnings.warn(f"Duplicated direction parameter in element. `{self._userparams['d']}` changed to `up`.")
        self._userparams['d'] = 'up'
        if length:
            self._userparams['l'] = length
        return self

    def down(self, length: Optional[float] = None) -> 'Element':
        ''' Set the direction to down '''
        if 'd' in self._userparams:
            warnings.warn(f"Duplicated direction parameter in element. `{self._userparams['d']}` changed to `down`.")
        self._userparams['d'] = 'down'
        if length:
            self._userparams['l'] = length
        return self

    def left(self, length: Optional[float] = None) -> 'Element':
        ''' Set the direction to left '''
        if 'd' in self._userparams:
            warnings.warn(f"Duplicated direction parameter in element. `{self._userparams['d']}` changed to `left`.")
        self._userparams['d'] = 'left'
        if length:
            self._userparams['l'] = length
        return self

    def right(self, length: Optional[float] = None) -> 'Element':
        ''' Set the direction to right '''
        if 'd' in self._userparams:
            warnings.warn(f"Duplicated direction parameter in element. `{self._userparams['d']}` changed to `right`.")
        self._userparams['d'] = 'right'
        if length:
            self._userparams['l'] = length
        return self

    def length(self, length: float) -> 'Element2Term':
        ''' Sets total length of element '''
        self._userparams['l'] = length
        return self

    def endpoints(self, start: XY, end: XY) -> 'Element2Term':
        ''' Sets absolute endpoints of element '''
        self._userparams['endpts'] = (start, end)
        return self

    def dot(self, open: bool = False) -> 'Element2Term':
        ''' Add a dot to the end of the element '''
        self._userparams['dot'] = True if not open else 'open'
        return self

    def idot(self, open: bool = False) -> 'Element2Term':
        ''' Add a dot to the input/start of the element '''
        self._userparams['idot'] = True if not open else 'open'
        return self

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        ''' Calculate element placement, adding lead extensions '''
        self._dwgparams.clear()
        self._dwgparams.update(dwgparams)
        if not self._positioned:
            self._position()

        totlen = self.params.get('l', self.params.get('unit', 3))
        endpts = self.params.get('endpts', None)
        to = self.params.get('to', None)
        tox = self.params.get('tox', None)
        toy = self.params.get('toy', None)
        anchor = self.params.get('anchor', None)
        zoom = self.params.get('zoom', self.params.get('scale', 1))
        xy = Point(self.params.get('at', dwgxy))

        # set up transformation
        theta = self.params.get('theta', dwgtheta)
        if endpts is not None:
            theta = util.angle(endpts[0], endpts[1])
        elif to is not None:
            theta = util.angle(xy, to)
        elif self.params.get('d') is not None:
            d = self.params.get('d')
            if str(d).lstrip('-').isnumeric():
                theta = d
            else:
                theta = {'u': 90, 'r': 0, 'l': 180, 'd': 270}[d[0].lower()]  # type: ignore

        # Get offset to element position within drawing (global shift)
        if endpts is not None:
            xy = Point(endpts[0])

        if endpts is not None:
            totlen = util.dist(endpts[0], endpts[1])
        elif to is not None:
            # Move until X or Y position is 'end'. Depends on direction
            totlen = util.dist(xy, to)
        elif tox is not None:
            # Allow either full coordinate (only keeping x), or just an x value
            if isinstance(tox, (int, float)):
                x = float(tox)
            else:
                x = tox[0]
            endpt = Point((x, xy[1]))
            totlen = util.dist(xy, endpt)
            theta = 180 if xy.x > x else 0
            self.elmparams['theta'] = theta
        elif toy is not None:
            # Allow either full coordinate (only keeping y), or just a y value
            if isinstance(toy, (int, float)):
                y = toy
            else:
                y = toy[1]
            endpt = Point((xy[0], y))
            totlen = util.dist(xy, endpt)
            theta = -90 if xy.y > y else 90
            self.elmparams['theta'] = theta

        self.anchors['istart'] = self.segments[0].path[0]  # type: ignore
        self.anchors['iend'] = self.segments[0].path[-1]  # type: ignore
        if self.params.get('extend', True):
            assert isinstance(self.segments[0], Segment)
            in_path = self.segments[0].path
            dz = util.delta(in_path[-1], in_path[0])   # Defined delta of path
            in_len = math.hypot(*dz)    # Defined length of path
            try:
                # Zoom is a Point
                lead_len = (totlen - in_len*zoom[0])/2 / zoom[0]
            except TypeError:
                lead_len = (totlen - in_len*zoom)/2 / zoom

            if lead_len > 0:  # Don't make element shorter
                start = Point(in_path[0]) - Point((lead_len, 0))
                end = Point(in_path[-1]) + Point((lead_len, 0))
                self._localshift = -start
                self.segments[0].path = [start] + self.segments[0].path + [end]  # type: ignore
                if in_len > 0 and (leadcolor := self.params.get('leadcolor')):
                    self.segments[0].color = leadcolor

            else:
                start = Point(in_path[0])
                end = Point(in_path[-1])
                self._localshift = Point((0, 0))

            # Adjust position of endpoints (arrowheads, dots, etc.)
            for i, segment in enumerate(self.segments):
                if getattr(segment, 'endref', None) == 'end':
                    xform = Transform(0, end)
                    self.segments[i] = segment.xform(xform)
                elif getattr(segment, 'endref', None) == 'start':
                    xform = Transform(0, start)
                    self.segments[i] = segment.xform(xform)
        else:
            start = Point(self.segments[0].path[0])  # type: ignore
            end = Point(self.segments[0].path[-1])  # type: ignore

        if self.params.get('dot', False):
            fill: Union[bool, str] = 'bg' if self.params['dot'] == 'open' else True
            radius = self.params.get('dotradius', 0.075)
            self.segments.append(SegmentCircle(end, radius=radius, fill=fill, zorder=3))
        if self.params.get('idot', False):
            fill = 'bg' if self.params['idot'] == 'open' else True
            radius = self.params.get('dotradius', 0.075)
            self.segments.append(SegmentCircle(start, radius=radius, fill=fill, zorder=3))

        self._place_anchors(start, end)
        if anchor is not None:
            self._localshift = self._localshift-Point(self.anchors[anchor])
        transform = Transform(theta, xy, self._localshift, zoom=zoom)

        self.absanchors = {}
        if len(self.segments) == 0:
            self.absanchors['start'] = transform.transform((0, 0))
            self.absanchors['end'] = transform.transform((0, 0))
            self.absanchors['center'] = transform.transform((0, 0))
        else:
            self.absanchors['start'] = transform.transform(start)
            self.absanchors['end'] = transform.transform(end)
            self.absanchors['center'] = transform.transform((start+end)/2)

        self.params['drop'] = end
        return super()._place(xy, theta, **dwgparams)

    def _place_anchors(self, start, end):
        ''' Allow positioning anchors before the element is placed '''
        self.anchors['start'] = Point(start)
        self.anchors['end'] = Point(end)
        self.anchors['center'] = (start+end)/2
