''' Schemdraw Drawing class '''

from __future__ import annotations
from typing import Type, Any
from collections import ChainMap
import warnings
import math

from .types import BBox, Backends, ImageFormat, Linestyle, Arcdirection, XY, ImageType, BilateralDirection
from .elements import Element, _set_elm_backend
from .elements.lines import LoopCurrent, CurrentLabel, CurrentLabelInline
from .segments import Segment, SegmentText, SegmentArc, SegmentCircle, SegmentPoly
from .util import Point

from .backends.svg import Figure as svgFigure
try:
    from .backends.mpl import Figure as mplFigure
except ImportError:
    mplFigure = None  # type: ignore


Figure: Type[svgFigure] | Type[mplFigure]
if mplFigure is None:
    Figure = svgFigure
else:
    Figure = mplFigure
_set_elm_backend(Figure)


def use(backend: Backends='matplotlib') -> None:
    ''' Change default backend, either 'matplotlib' or 'svg' '''
    global Figure
    if backend == 'matplotlib':
        if mplFigure is None:
            raise ValueError('Could not import Matplotlib.')
        Figure = mplFigure
    else:
        Figure = svgFigure
    _set_elm_backend(Figure)


def config(unit: float=3.0, inches_per_unit: float=0.5,
           lblofst: float=0.1, fontsize: float=14,
           font: str='sans-serif', color: str='black',
           lw: float=2, ls: Linestyle='-',
           fill: str=None, bgcolor: str=None) -> None:
    ''' Set global schemdraw style configuration
 
        Args:
            unit: Full length of a 2-terminal element. Inner zig-zag portion
                of a resistor is 1.0 units.
            inches_per_unit: Inches per drawing unit for setting drawing scale
            lblofst: Default offset between element and its label
            fontsize: Default font size for text labels
            font: Default font family for text labels
            color: Default color name or RGB (0-1) tuple
            lw: Default line width for elements
            ls: Default line style
            fill: Deault fill color for closed elements
    '''
    schemdrawstyle['unit'] = unit
    schemdrawstyle['inches_per_unit'] = inches_per_unit
    schemdrawstyle['lblofst'] = lblofst
    schemdrawstyle['fontsize'] = fontsize
    schemdrawstyle['font'] = font
    schemdrawstyle['color'] = color
    schemdrawstyle['lw'] = lw
    schemdrawstyle['ls'] = ls
    schemdrawstyle['fill'] = fill 
    if bgcolor:
        schemdrawstyle['bgcolor'] = bgcolor


schemdrawstyle: dict[str, Any] = {}  # Global style
config()  # Initialize default configuration


def theme(theme='default'):
    ''' Set schemdraw theme (line color and background color).
        Themes match those in jupyter-themes package
        (https://github.com/dunovank/jupyter-themes).

        Available themes:
            * default (black on white)
            * dark (white on black)
            * solarizedd
            * solarizedl
            * onedork
            * oceans16
            * monokai
            * gruvboxl
            * gruvboxd
            * grade3
            * chesterish
    '''
    if theme == 'default':
        config(bgcolor='white')
    elif theme == 'dark':
        schemdrawstyle['color'] = 'white'
        schemdrawstyle['bgcolor'] = 'black'
    elif theme == 'solarizedd':
        schemdrawstyle['bgcolor'] = '#002b36'
        schemdrawstyle['color'] = '#657b83'
    elif theme == 'solarizedl':
        schemdrawstyle['bgcolor'] = '#eee8d5'
        schemdrawstyle['color'] = '#073642'
    elif theme == 'onedork':
        schemdrawstyle['bgcolor'] = '#373e4b'
        schemdrawstyle['color'] = '#899ab8'
    elif theme == 'oceans16':
        schemdrawstyle['bgcolor'] = '#384151'
        schemdrawstyle['color'] = '#CDD2E9'
    elif theme == 'monokai':
        schemdrawstyle['bgcolor'] = '#232323'
        schemdrawstyle['color'] = '#BBBBBB'
    elif theme == 'gruvboxl':
        schemdrawstyle['bgcolor'] = '#ebdbb2'
        schemdrawstyle['color'] = '#3c3836'
    elif theme == 'gruvboxd':
        schemdrawstyle['bgcolor'] = '#1d2021'
        schemdrawstyle['color'] = '#d5c4a1'
    elif theme == 'grade3':
        schemdrawstyle['bgcolor'] = '#ffffff'
        schemdrawstyle['color'] = '#3f3d46'
    elif theme == 'chesterish':
        schemdrawstyle['bgcolor'] = '#323A48'
        schemdrawstyle['color'] = '#92A2BD'
    else:
        raise ValueError(f'Unknown theme {theme}')


class Drawing:
    ''' A schematic drawing

        See `schemdraw.config` method for argument defaults

        Args:
            *elements: List of Element instances to add to the drawing
            unit: Full length of a 2-terminal element. Inner zig-zag portion
                of a resistor is 1.0 units.
            inches_per_unit: Inches per drawing unit for setting drawing scale
            lblofst: Default offset between element and its label
            fontsize: Default font size for text labels
            font: Default font family for text labels
            color: Default color name or RGB (0-1) tuple
            lw: Default line width for elements
            ls: Default line style
            fill: Deault fill color for closed elements

        Attributes:
            here: (xy tuple) Current drawing position. The next element will
                be added at this position unless specified otherwise.
            theta: (float) Current drawing angle, in degrees. The next
                element will be added with this angle unless specified
                otherwise.
    '''
    def __init__(self, *elements: Element, unit: float=None,
                 inches_per_unit: float=None, lblofst: float=None,
                 fontsize: float=None, font: str=None,
                 color: str=None, lw: float=None, ls: Linestyle=None,
                 fill: str=None):
        self.elements: list[Element] = []
        self.inches_per_unit = inches_per_unit if inches_per_unit is not None else schemdrawstyle.get('inches_per_unit')
        self.unit = unit if unit is not None else schemdrawstyle.get('unit')
        
        self.dwgparams: dict[str, Any] = {}
        if unit:
            self.dwgparams['unit'] = unit
        if font:
            self.dwgparams['font'] = font
        if fontsize:
            self.dwgparams['fontsize'] = fontsize
        if lblofst:
            self.dwgparams['lblofst'] = lblofst
        if color:
            self.dwgparams['color'] = color
        if ls:
            self.dwgparams['ls'] = ls
        if lw:
            self.dwgparams['lw'] = lw
        if fill:
            self.dwgparams['fill'] = fill

        self.here: XY = Point((0, 0))
        self.theta: float = 0
        self._state: list[tuple[Point, float]] = []  # Push/Pop stack
        self._interactive = False
        self.fig = None

        for element in elements:
            self.add(element)

    def interactive(self, interactive: bool=True):
        ''' Enable interactive mode (matplotlib backend only). Matplotlib
            must also be set to interactive with `plt.ion()`.
        '''
        self._interactive = interactive

    def get_bbox(self) -> BBox:
        ''' Get drawing bounding box '''
        xmin = math.inf
        xmax = -math.inf
        ymin = math.inf
        ymax = -math.inf
        for element in self.elements:
            bbox = element.get_bbox(transform=True)
            xmin = min(bbox.xmin, xmin)
            xmax = max(bbox.xmax, xmax)
            ymin = min(bbox.ymin, ymin)
            ymax = max(bbox.ymax, ymax)
        return BBox(xmin, ymin, xmax, ymax)

    def get_segments(self) -> list['Segment' | 'SegmentText' | 'SegmentArc' |
                                   'SegmentCircle' | 'SegmentPoly']:
        ''' Get flattened list of all segments in the drawing '''
        segments = []
        for element in self.elements:
            segments.extend([s.xform(element.transform, **element._cparams)
                             for s in element.segments])
        return segments

    def _repr_svg_(self):
        ''' SVG representation for Jupyter '''
        return self.draw().getimage('svg').decode()

    def _repr_png_(self):
        ''' PNG representation for Jupyter '''
        if Figure == mplFigure:
            return self.draw().getimage('png')
        return None

    def __iadd__(self, element: Element):
        ''' In-place add element, via += operator. '''
        self.add(element)
        return self

    def add(self, element: Element | Type[Element], **kwargs) -> Element:
        ''' Add an element to the drawing.

            Args:
                element: The element to add.
        '''
        # TODO: remove kwargs when deprecated dictionary elements are removed
        if not isinstance(element, Element):
            # Instantiate it (for support of legacy add method)
            element = element(**kwargs)
        elif len(kwargs) > 0:
            warnings.warn('kwargs to add method are ignored because element is already instantiated')

        dwgparams = ChainMap(self.dwgparams, schemdrawstyle)
        self.here, self.theta = element._place(self.here, self.theta,
                                               **dwgparams)
        self.elements.append(element)
        
        if self._interactive:
            if self.fig is None:
                self._initfig()
            element._draw(self.fig)
            self.fig.set_bbox(self.get_bbox())  # type: ignore
            self.fig.getimage()  # type: ignore
        else:
            self.fig = None  # Clear any existing figure
        return element

    def add_elements(self, *elements: Element) -> None:
        ''' Add multiple elements to the drawing '''
        for element in elements:
            self.add(element)

    def undo(self) -> None:
        ''' Removes previously added element '''
        self.elements.pop(-1)
        self.fig.clear()  # type: ignore
        for element in self.elements:
            element._draw(self.fig)
        self.here, self.theta = self.elements[-1].absdrop
        self.fig.set_bbox(self.get_bbox())  # type: ignore
        self.fig.getimage()  # type: ignore

    def move(self, dx: float, dy: float) -> None:
        ''' Move the current drawing position

            Args:
                dx: change in x position
                dy: change in y position
        '''
        self.here = Point((self.here[0] + dx, self.here[1] + dy))

    def push(self) -> None:
        ''' Push/save the drawing state.
            Drawing.here and Drawing.theta are saved.
        '''
        self._state.append((Point(self.here), self.theta))

    def pop(self) -> None:
        ''' Pop/load the drawing state. Location and angle are returned to
            previously pushed state.
        '''
        if len(self._state) > 0:
            self.here, self.theta = self._state.pop()

    def loopI(self, elm_list: list[Element], label: str='',
              d: Arcdirection='cw', theta1: float=35,
              theta2: float=-35, pad: float=.2, color: str=None) -> Element:
        ''' Draw an arc to indicate a loop current bordered by elements in list

            [DEPRECATED - use LoopCurrent element instead]

            Args:
                elm_list: Boundary elements in order of top, right, bot, left
                label: Text label to draw in center of loop
                d: Arc/arrow direction
                theta1: Start angle of arrow arc (degrees)
                theta2: End angle of arrow arc (degrees)
                pad: Distance between elements and arc
                color: Color for loop arrow
        '''
        warnings.warn('loopI function is deprecated. Add a LoopCurrent element instead.', DeprecationWarning)

        element = LoopCurrent(elm_list, theta1=theta1, theta2=theta2,
                              direction=d, pad=pad)
        element.label(label)
        if color:
            element.color(color)
        self.add(element)
        return element

    def labelI(self, elm: Element, label: str='', arrowofst: float=0.4,
               arrowlen: float=2, reverse: bool=False, top: bool=True,
               color: str=None) -> Element:
        ''' Add an arrow element along side another element

            [DEPRECATED - use CurrentLabel element instead]

            Args:
                elm: Element to add arrow to
                label: String or list of strings to evenly space along arrow
                arrowofst: Distance from element to arrow
                arrowlen: Length of arrow as multiple of Drawing.unit
                reverse: Reverse the arrow direction
                top: Draw arrow on top (True) or bottom (False) of element
                color: Color for label. Defaults to color of elm.
        '''
        warnings.warn('labelI function is deprecated. Add a CurrentLabel element instead.', DeprecationWarning)
        element = CurrentLabel(ofst=arrowofst, length=arrowlen,
                               top=top, reverse=reverse)
        element.at(elm.center).theta(elm.transform.theta)
        element.label(label)
        if color:
            element.color(color)
        self.add(element)
        return element

    def labelI_inline(self, elm: Element, label: str=None,
                      botlabel: str=None, d: BilateralDirection='in',
                      start: bool=True, ofst: float=.8,
                      color: str=None) -> Element:
        ''' Add an arrowhead for labeling current inline with leads.
            Works on Element2Term elements.

            [DEPRECATED - use CurrentLabelInline element instead]

            Args:
                elm: Element to add arrow to
                label: Text to draw above the arrowhead
                botlabel: Text to draw below the arrowhead
                d: Arrowhead direction, into or out of the element
                start: Place arrowhead near start (True) or
                    end (False) of element
                ofst: Offset from center of element
                color: Color for label. Defaults to color of elm.
        '''
        warnings.warn('labelI_inline function is deprecated. Add a CurrentLabelInline element instead.', DeprecationWarning)
        element = CurrentLabelInline(direction=d, ofst=ofst, start=start)
        element.at(elm.center).theta(elm.transform.theta).zorder(3)
        if label:
            element.label(label)
        if botlabel:
            element.label(botlabel, 'bot')
        if color:
            element.color(color)
        self.add(element)
        return element

    def _initfig(self, ax=None, backend: Backends=None, showframe: bool=False) -> None:
        figclass = {'matplotlib': mplFigure,
                    'svg': svgFigure}.get(backend, Figure)  # type: ignore
        fig = figclass(ax=ax,
                       bbox=self.get_bbox(),
                       inches_per_unit=self.inches_per_unit,
                       showframe=showframe)
        
        params = ChainMap(self.dwgparams, schemdrawstyle)
        if 'bgcolor' in params:
            fig.bgcolor(params['bgcolor'])
        self.fig = fig
    
    def draw(self, showframe: bool=False, show: bool=True,
             ax=None, backend: Backends=None):
        ''' Draw the schematic

            Args:
                showframe: Show axis frame. Useful for debugging a drawing.
                show: Show the schematic in a GUI popup window (when
                    outside of a Jupyter inline environment)
                ax: Existing axis to draw on. Should be set to equal
                    aspect for best results.

            Returns:
                schemdraw Figure object
        '''
        # Redraw only if needed. Otherwise, show/return what's already
        # been drawn on the figure
        if (self.fig is None or
            ax is not None or showframe != self.fig.showframe or
            backend is not None):
            self._initfig(ax=ax, backend=backend, showframe=showframe)
            for element in self.elements:
                element._draw(self.fig)

        if show:
            # Show figure in window if not inline/Jupyter mode            
            self.fig.show()  # type: ignore
        return self.fig  # Otherwise return Figure and let _repr_ display it

    def save(self, fname: str, transparent: bool=True, dpi: float=72) -> None:
        ''' Save figure to a file

            Args:
                fname: Filename to save. File type automatically determined
                    from extension (png, svg, jpg)
                transparent: Save as transparent background, if available
                dpi: Dots-per-inch for raster formats
        '''
        if self.fig is None:
            self.draw(show=False)
        self.fig.save(fname, transparent=transparent, dpi=dpi)  # type: ignore

    def get_imagedata(self, fmt: ImageFormat | ImageType) -> bytes:
        ''' Get image data as bytes array

            Args:
                fmt: Format or file extension of the image type

            Returns:
                Image data as bytes
        '''
        if Figure == svgFigure and fmt.lower() != 'svg':
            raise ValueError('Format not available in SVG backend.')
        if self.fig is None:
            self.draw(show=False)
        return self.fig.getimage(ext=fmt)  # type: ignore
