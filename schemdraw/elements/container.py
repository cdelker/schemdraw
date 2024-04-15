''' Container Element '''
from __future__ import annotations
import math
from typing import Union, Optional, TYPE_CHECKING

from .elements import Element
from ..segments import Segment, SegmentPoly, BBox
from .. import drawing_stack

if TYPE_CHECKING:
    from ..schemdraw import Drawing


class Container(Element):
    ''' Container element - a group of elements surrounded by a box
    
        Args:
            drawing: The schemdraw Drawing or another Container to contain
            cornerradius: Radius to round the corners of the box [default: 0.3]
            padx: Spacing from element to box in x direction [default: 0.75]
            pady: Spacing from element to box in y direction [default: 0.75]
    '''
    _element_defaults = {
        'cornerradius': 0.3,
        'padx': 0.75,
        'pady': 0.75,
        'lblloc': 'NW',
        'lblofst': (.1, -.1),
        'lblalign': ('left', 'top'),
        'theta': 0,
        'anchor': 'boxNW'
    }
    def __init__(self,
                 drawing: Union['Drawing', 'Container'],
                 *,
                 cornerradius: Optional[float] = None,
                 padx: Optional[float] = None,
                 pady: Optional[float] = None):
        super().__init__()
        self.drawing = drawing
        self.elements: list[Element] = []

    def container(self,
                  cornerradius: Optional[float] = None,
                  padx: Optional[float] = None,
                  pady: Optional[float] = None) -> 'Container':
        ''' Add a container to the container. Use as a context manager,
            such that elemnents inside the `with` are surrounded by
            the container.
            
            >>> with container.container():
            >>>    elm.Resistor()
            >>>    ...

            Args:
            cornerradius: Radius to round the corners of the box [default: 0.3]
            padx: Spacing from element to box in x direction [default: 0.75]
            pady: Spacing from element to box in y direction [default: 0.75]
        '''
        return Container(self, cornerradius=cornerradius, padx=padx, pady=pady)

    def __iadd__(self, element: Element) -> 'Container':
        return self.add(element)

    def add(self, element: Element) -> 'Container':
        ''' Add an element to the container '''
        self.elements.append(element)
        self.drawing.add(element)
        return self

    def __enter__(self):
        drawing_stack.push_drawing(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        drawing_stack.push_element(self)
        drawing_stack.pop_drawing(self)

    def __contains__(self, element):
        return element in self.elements

    def container_bbox(self, transform: bool = True) -> BBox:
        ''' Bounding box of the contents only '''
        xmin = math.inf
        xmax = -math.inf
        ymin = math.inf
        ymax = -math.inf
        for element in self.elements:
            bbox = element.get_bbox(transform=transform)
            xmin = min(bbox.xmin, xmin)
            xmax = max(bbox.xmax, xmax)
            ymin = min(bbox.ymin, ymin)
            ymax = max(bbox.ymax, ymax)
        return BBox(xmin, ymin, xmax, ymax)

    def get_bbox(self, transform: bool = False, includetext: bool = True) -> BBox:
        ''' Bounding box including border '''
        bbox = self.container_bbox(transform=transform)
        return BBox(bbox.xmin-self.params['padx'],
                    bbox.ymin-self.params['pady'],
                    bbox.xmax+self.params['padx'],
                    bbox.ymax+self.params['pady'])

    def _place(self, dwgxy, dwgtheta, **dwgparams):
        bbox = self.container_bbox()
        w = bbox.xmax - bbox.xmin + self.params['padx']*2
        h = bbox.ymax - bbox.ymin + self.params['pady']*2
        cornerradius = self.params['cornerradius']
        bbox = BBox(bbox.xmin-self.params['padx'],
                    bbox.ymin-self.params['pady'],
                    bbox.xmax+self.params['padx'],
                    bbox.ymax+self.params['pady'])
        self.at((bbox.xmin, bbox.ymax))
        if cornerradius > 0:
            self.segments = [SegmentPoly(
                [(0, h/2), (w, h/2), (w, -h/2), (0, -h/2)],
                 cornerradius=cornerradius)]
        else:
            self.segments.append(Segment([(0, 0), (0, h/2), (w, h/2),
                                          (w, -h/2), (0, -h/2), (0, 0)]))
        self.anchors['center'] = (w/2, 0)
        self.anchors['boxNW'] = (0, h/2)
        self.anchors['N'] = (w/2, h/2)
        self.anchors['E'] = (w, 0)
        self.anchors['S'] = (w/2, -h/2)
        self.anchors['W'] = (0, 0)
        k = cornerradius - cornerradius*math.sqrt(2)/2
        self.anchors['NE'] = (w-k, h/2-k)
        self.anchors['NW'] = (k, h/2-k)
        self.anchors['SE'] = (w-k, -h/2+k)
        self.anchors['SW'] = (k, -h/2+k)
        self.anchors['NNE'] = (3*w/4 if cornerradius < w/4 else w-cornerradius, h/2)
        self.anchors['NNW'] = (w/4 if cornerradius < w/4 else cornerradius, h/2)
        self.anchors['SSE'] = (3*w/4 if cornerradius < w/4 else w-cornerradius, -h/2)
        self.anchors['SSW'] = (w/4 if cornerradius < w/4 else cornerradius, -h/2)
        self.anchors['ENE'] = (w, h/4 if cornerradius < h/4 else h/2-cornerradius)
        self.anchors['ESE'] = (w, -h/4 if cornerradius < h/4 else -h/2+cornerradius)
        self.anchors['WNW'] = (0, h/4 if cornerradius < h/4 else h/2-cornerradius)
        self.anchors['WSW'] = (0, -h/4 if cornerradius < h/4 else -h/2+cornerradius)
        return super()._place(dwgxy, dwgtheta, **dwgparams)
