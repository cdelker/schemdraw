''' Schemdraw transformations for converting local element definition to
    global position within the drawing
'''

from typing import List, Sequence, Literal

from .util import Point


class Transform(object):
    ''' Class defining transformation matrix

        Parameters
        ----------
        theta: float
            Rotation angle in degrees
        globalshift: (x, y) iterable
            X-Y shift (applied after zoom and rotation)
        localshift: (x, y) iterable
            Local X-Y shift (applied before zoom and rotation)
        zoom: float
            Zoom factor
    '''
    def __init__(self, theta: float, globalshift: Sequence[float], localshift: Sequence[float]=(0, 0), zoom: float=1):
        self.theta = theta
        self.shift = Point(globalshift)
        self.localshift = Point(localshift)
        self.zoom = zoom

    def __repr__(self):
        return 'Transform: xy={}; theta={}; scale={}'.format(self.shift, self.theta, self.zoom)

    def transform(self, pt: Sequence[float], ref: Literal['start', 'end']=None) -> Point:
        ''' Apply the transform to the point

            Parameters
            ----------
            pt: (x, y) iterable
                Original coordinates
            ref: string
                'start', 'end', or None, transformation reference
                (whether to apply localshift)

            Returns
            -------
            pt: (x, y) iterable
                Transformed coordinates
        '''
        lshift = {'start': Point((0, 0)),
                  'end': self.localshift*2}.get(ref, self.localshift)  # type: ignore
        return ((Point(pt) + lshift) * self.zoom).rotate(self.theta) + self.shift

    def transform_array(self, pts: List[Sequence[float]]) -> List[Point]:
        ''' Apply the transform to multiple points

            Parameters
            ----------
            pts: array
                List of (x,y) points to transform
        '''
        return [self.transform(pt) for pt in pts]
