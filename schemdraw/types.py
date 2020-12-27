
from typing import Literal, Union, Tuple, TypedDict, Sequence
from collections import namedtuple
from enum import Enum, unique

from .util import Point

BBox = namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])

Capstyle = Literal['butt', 'round', 'square']
Joinstyle = Literal['bevel', 'miter', 'round']
Linestyle = Literal['-', ':', '--', '-.']
Direction = Literal['up', 'down', 'left', 'right', 'u', 'd', 'l', 'r']
Arcdirection = Literal['cw', 'ccw']
XY = Union[Tuple[float, float], Point]

Backends = Literal['svg', 'matplotlib']


    
@unique
class ImageFormat(str, Enum):
    ''' Known Matplotlib image formats '''
    EPS = 'eps'
    JPG = 'jpg'
    PDF = 'pdf'
    PGF = 'pgf'
    PNG = 'png'
    PS = 'ps'
    RAW = 'raw'
    RGBA = 'rgba'
    SVG = 'svg'
    TIF = 'tif'