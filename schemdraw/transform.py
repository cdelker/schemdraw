''' Schemdraw transformations for converting local element definition to
    global position within the drawing
'''

from __future__ import annotations

import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from typing import Sequence

from .util import Point


class Transform:
    ''' Class defining transformation matrix

        Args:
            theta: Rotation angle in degrees
            globalshift: X-Y shift (applied after zoom and rotation)
            localshift: Local X-Y shift (applied before zoom and rotation)
            zoom: Zoom factor
    '''
    def __init__(self, theta: float, globalshift: Sequence[float],
                 localshift: Sequence[float]=(0, 0), zoom: float=1):
        self.theta = theta
        self.shift = Point(globalshift)
        self.localshift = Point(localshift)
        self.zoom = zoom

    def __repr__(self):
        return 'Transform: xy={}; theta={}; scale={}'.format(
            self.shift, self.theta, self.zoom)

    def transform(self, pt: Sequence[float], ref: Literal['start', 'end']=None) -> Point:
        ''' Apply the transform to the point

            Args:
            pt: Original (x, y) coordinates
            ref: 'start', 'end', or None, transformation reference
                (whether to apply localshift)

            Returns:
                Transformed (x, y) coordinates
        '''
        lshift = {'start': Point((0, 0)),
                  'end': self.localshift*2}.get(ref, self.localshift)  # type: ignore
        return ((Point(pt) + lshift) * self.zoom).rotate(self.theta) + self.shift

    def transform_array(self, pts: list[Sequence[float]]) -> list[Point]:
        ''' Apply the transform to multiple points

            Args:
                pts: List of (x,y) points to transform

            Returns:
                List of transformed (x, y) points
        '''
        return [self.transform(pt) for pt in pts]
