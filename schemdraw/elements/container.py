''' Container Element '''
import math
from typing import Union, TYPE_CHECKING

from .elements import Element
from ..segments import Segment, SegmentPoly, BBox

if TYPE_CHECKING:
    from ..schemdraw import Drawing


class Container(Element):
    ''' Container element - a group of elements surrounded by a box '''
    def __init__(self, drawing: Union['Drawing', 'Container'], cornerradius: float = .3,
                 padx: float = .75, pady: float = .75):
        super().__init__()
        self.drawing = drawing
        self.elements: list[Element] = []
        self.padx = padx
        self.pady = pady
        self.cornerradius = cornerradius
        self.params['lblloc'] = 'NW'
        self.params['lblofst'] = (.1, -.1)
        self.params['lblalign'] = ('left', 'top')
        self.params['theta'] = 0
        self.params['anchor'] = 'NW'

    def container(self, cornerradius: float = .3,
                  padx: float = .75, pady: float = .75) -> 'Container':
        ''' Add a container to the container

            Args:
                cornerradius: radius for box corners
                padx: space between contents and border in x direction
                pady: space between contents and border in y direction
        '''
        return Container(self, cornerradius, padx, pady)

    def __iadd__(self, element: Element) -> 'Container':
        return self.add(element)

    def add(self, element: Element) -> 'Container':
        ''' Add an element to the container '''
        self.elements.append(element)
        self.drawing.add(element)
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.drawing.add(self)

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
        return BBox(bbox.xmin-self.padx,
                    bbox.ymin-self.pady,
                    bbox.xmax+self.padx,
                    bbox.ymax+self.pady)

    def _place(self, dwgxy, dwgtheta, **dwgparams):
        bbox = self.container_bbox()
        w = bbox.xmax - bbox.xmin + self.padx*2
        h = bbox.ymax - bbox.ymin + self.pady*2
        bbox = BBox(bbox.xmin-self.padx,
                    bbox.ymin-self.pady,
                    bbox.xmax+self.padx,
                    bbox.ymax+self.pady)
        self.at((bbox.xmin, bbox.ymax))
        if self.cornerradius > 0:
            self.segments = [SegmentPoly(
                [(0, h/2), (w, h/2), (w, -h/2), (0, -h/2)],
                cornerradius=self.cornerradius)]
        else:
            self.segments.append(Segment([(0, 0), (0, h/2), (w, h/2),
                                          (w, -h/2), (0, -h/2), (0, 0)]))
        self.anchors['center'] = (w/2, 0)
        self.anchors['N'] = (w/2, h/2)
        self.anchors['E'] = (w, 0)
        self.anchors['S'] = (w/2, -h/2)
        self.anchors['W'] = (0, 0)
        k = self.cornerradius - self.cornerradius*math.sqrt(2)/2
        self.anchors['NE'] = (w-k, h/2-k)
        self.anchors['NW'] = (k, h/2-k)
        self.anchors['SE'] = (w-k, -h/2+k)
        self.anchors['SW'] = (k, -h/2+k)
        self.anchors['NNE'] = (3*w/4 if self.cornerradius < w/4 else w-self.cornerradius, h/2)
        self.anchors['NNW'] = (w/4 if self.cornerradius < w/4 else self.cornerradius, h/2)
        self.anchors['SSE'] = (3*w/4 if self.cornerradius < w/4 else w-self.cornerradius, -h/2)
        self.anchors['SSW'] = (w/4 if self.cornerradius < w/4 else self.cornerradius, -h/2)
        self.anchors['ENE'] = (w, h/4 if self.cornerradius < h/4 else h/2-self.cornerradius)
        self.anchors['ESE'] = (w, -h/4 if self.cornerradius < h/4 else -h/2+self.cornerradius)
        self.anchors['WNW'] = (0, h/4 if self.cornerradius < h/4 else h/2-self.cornerradius)
        self.anchors['WSW'] = (0, -h/4 if self.cornerradius < h/4 else -h/2+self.cornerradius)
        return super()._place(dwgxy, dwgtheta, **dwgparams)
