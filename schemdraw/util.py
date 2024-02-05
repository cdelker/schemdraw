''' Utility functions for point geometry '''
from __future__ import annotations
from typing import Union, Tuple

import math
from operator import mul
from itertools import starmap

XY = Union[Tuple[float, float], 'Point']


class Point(Tuple[float, float]):
    ''' An (x, y) tuple that can do math operations '''
    @property
    def x(self) -> float:
        ''' X value of point '''
        return self[0]

    @property
    def y(self) -> float:
        ''' Y value of point '''
        return self[1]

    def __repr__(self):
        return f'Point({self.x},{self.y})'

    def __add__(self, a):
        try:
            return Point((self.x+a.x, self.y+a.y))
        except AttributeError:
            return Point((self.x+a, self.y+a))

    def __sub__(self, a):
        try:
            return Point((self.x-a.x, self.y-a.y))
        except AttributeError:
            return Point((self.x-a, self.y-a))

    def __rsub__(self, a):
        try:
            return Point((a.x-self.x, a.y-self.y))
        except AttributeError:
            return Point((a-self.x, a-self.y))

    def __mul__(self, a):
        try:
            return Point((a.x*self.x, a.y*self.y))
        except AttributeError:
            return Point((a*self.x, a*self.y))

    def __truediv__(self, a):
        try:
            return Point((self.x/a.x, self.y/a.y))
        except AttributeError:
            return Point((self.x/a, self.y/a))

    def __neg__(self):
        return Point((-self.x, -self.y))

    __radd__ = __add__
    __rmul__ = __mul__

    def rotate(self, angle: float, center: XY = (0, 0)) -> 'Point':
        ''' Rotate the point by angle degrees about the center '''
        return Point(rotate(self, angle, center=Point(center)))

    def mirrorx(self, centerx: float = 0) -> 'Point':
        ''' Mirror in x direction about the centerx point '''
        return Point(mirrorx(self, centerx))

    def flip(self) -> 'Point':
        ''' Flip the point vertically '''
        return Point(flip(self))


def dot(a: XY, b: Tuple[Tuple[float, float], Tuple[float, float]]) -> Point:
    ''' Dot product of iterables a and b '''
    return Point([sum(starmap(mul, zip(a, col))) for col in zip(*b)])


def linspace(start: float, stop: float, num: int = 50) -> list[float]:
    ''' List of evenly spaced numbers '''
    step = (stop - start) / (num - 1)
    return [start+step*i for i in range(num)]


def rotate(xy: XY,
           angle: float,
           center: XY = (0, 0)) -> Point:
    ''' Rotate the xy point by angle degrees '''
    co = math.cos(math.radians(angle))
    so = math.sin(math.radians(angle))
    center = Point(center)
    m = ((co, so), (-so, co))  # rotation matrix
    b = Point(xy) - center
    b = dot(b, m)
    b = b + center
    return b


def mirrorx(xy, centerx=0) -> Point:
    ''' Mirror the point horizontally '''
    return Point((-(xy[0]-centerx)+centerx, xy[1]))


def flip(xy: XY) -> Point:
    ''' Flip the point vertically '''
    return Point((xy[0], -xy[1]))


def delta(a: XY, b: XY) -> Point:
    ''' Delta between points a and b '''
    return Point((b[0] - a[0], b[1] - a[1]))


def angle(a: XY, b: XY) -> float:
    ''' Compute angle from point a to b '''
    theta = math.degrees(math.atan2(b[1] - a[1], b[0] - a[0]))
    return theta


def dist(a: XY, b: XY) -> float:
    ''' Get distance from point a to b.

        Same as math.dist in Python 3.8+.
    '''
    try:
        # Python 3.8+
        return math.dist(a, b)  # type: ignore
    except AttributeError:
        return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
