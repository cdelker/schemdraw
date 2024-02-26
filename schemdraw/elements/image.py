''' Elements based on images '''
from __future__ import annotations
from typing import Optional, BinaryIO

from .elements import Element
from ..segments import SegmentImage
from ..util import Point


class ElementImage(Element):
    ''' Element from an Image file

        Args:
            image: Image filename or open file pointer
            width: Width to draw image in Drawing
            height: Height to draw image in Drawing
            xy: Origin (lower left corner)
    '''
    def __init__(self, image: str | BinaryIO,
                 width: float,
                 height: float,
                 xy: Point = Point((0, 0)),
                 imgfmt: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)
        zorder = kwargs.get('zorder', 1)
        self.segments.append(SegmentImage(image=image, xy=xy, width=width, height=height,
                                          zorder=zorder, imgfmt=imgfmt))
        self.elmparams['theta'] = 0
