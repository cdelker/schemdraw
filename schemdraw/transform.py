''' Schemdraw transformations for converting local element definition to
    global position within the drawing
'''

from __future__ import annotations
from typing import Sequence

from .util import Point
from .types import XY


class Transform:
    ''' Class defining transformation matrix

        Args:
            theta: Rotation angle in degrees
            globalshift: X-Y shift (applied after zoom and rotation)
            localshift: Local X-Y shift (applied before zoom and rotation)
            zoom: Zoom factor
    '''
    def __init__(self, theta: float, globalshift: XY,
                 localshift: XY = (0, 0), zoom: XY | float = Point((1, 1))):
        self.theta = theta
        self.shift = Point(globalshift)
        self.localshift = Point(localshift)
        if isinstance(zoom, (int, float)):
            zoom = Point((zoom, zoom))
        self.zoom = zoom

    def __repr__(self):
        return f'Transform: xy={self.shift}; theta={self.theta}; scale={self.zoom}; lshift={self.localshift}'

    def transform(self, pt: XY) -> Point:
        ''' Apply the transform to the point

            Args:
            pt: Original (x, y) coordinates

            Returns:
                Transformed (x, y) coordinates
        '''
        return ((Point(pt) + self.localshift) * self.zoom).rotate(self.theta) + self.shift

    def transform_array(self, pts: Sequence[XY]) -> list[Point]:
        ''' Apply the transform to multiple points

            Args:
                pts: List of (x,y) points to transform

            Returns:
                List of transformed (x, y) points
        '''
        return [self.transform(pt) for pt in pts]
