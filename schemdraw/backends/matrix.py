''' Affine transformation matrix operations for SVG `transform` attributes '''
from __future__ import annotations
from typing import Sequence, Optional, Tuple
import math

from ..util import Point


Matrix3x3 = Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]


def matrix_translate(dx: float = 0, dy: float = 0) -> Matrix3x3:
    ''' Translation matrix '''
    return ((1., 0., dx),
            (0., 1., dy),
            (0., 0., 1.))


def matrix_rotate(theta: float = 0, cx: float = 0, cy: float = 0) -> Matrix3x3:
    ''' Rotation matrix, theta in degrees, about center (cx, cy) '''
    costh = math.cos(math.radians(theta))
    sinth = math.sin(math.radians(theta))
    return ((costh, -sinth, -cx*costh + cy*sinth + cx),
            (sinth, costh, -cx*sinth - cy*costh + cy),
            (0., 0., 1.))


def matrix_scale(kx: float = 1., ky: Optional[float] = None) -> Matrix3x3:
    ''' Scale matrix '''
    if ky is None:
        ky = kx
    return ((kx, 0., 0.),
            (0., ky, 0.),
            (0., 0., 1.))


def matrix_skewx(k: float = 1.) -> Matrix3x3:
    ''' X-Skew matrix '''
    return ((1., k,  0.),
            (0., 1., 0.),
            (0., 0., 1.))


def matrix_skewy(k: float = 1.) -> Matrix3x3:
    ''' Y-Skew matrix '''
    return ((1., 0., 0.),
            (k,  1., 0.),
            (0., 0., 1.))


def matrix(a: float = 1., b: float = 0., c: float = 0., d: float = 1., e: float = 0, f: float = 0) -> Matrix3x3:
    ''' Full matrix as defined by SVG transform '''
    return ((a, c, e),
            (b,  d, f),
            (0., 0., 1.))


def transform(point: Point, xform: Matrix3x3) -> Point:
    ''' Apply transform to point (matrix multiply) '''
    pt = [point[0], point[1], 1.]
    x = pt[0] * xform[0][0] + pt[1] * xform[0][1] + pt[2]*xform[0][2]
    y = pt[0] * xform[1][0] + pt[1] * xform[1][1] + pt[2]*xform[1][2]
    # z = pt[0] * xform[2][0] + pt[1] * xform[2][1] + pt[2]*xform[2][2]
    # assert math.isclose(z, 1)
    return Point((x, y))


def transform_all(pt, xform: Sequence[Matrix3x3]) -> Point:
    ''' Apply series of transforms to the point '''
    for xf in xform:
        pt = transform(pt, xf)
    return pt
