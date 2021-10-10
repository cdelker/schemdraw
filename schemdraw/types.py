''' Data types for schemdraw '''

import sys
if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

from typing import Union, Tuple, Sequence, Optional
from collections import namedtuple
from enum import Enum, unique

from .util import Point

BBox = namedtuple('BBox', ['xmin', 'ymin', 'xmax', 'ymax'])

# matplotlib uses 'projecting' to be the same as 'square' in svg.
Capstyle = Literal['butt', 'round', 'square', 'projecting']
Joinstyle = Literal['bevel', 'miter', 'round']
Linestyle = Literal['-', ':', '--', '-.']
Direction = Union[Literal['up', 'down', 'left', 'right',
                          'u', 'd', 'l', 'r'], int]
Halign = Literal['center', 'left', 'right']
Valign = Literal['center', 'top', 'bottom']
Align = Tuple[Optional[Halign], Optional[Valign]]
Arcdirection = Literal['cw', 'ccw']
Side = Literal['top', 'bot', 'lft', 'rgt', 'bottom', 'left', 'right', 'L', 'R', 'T', 'B']
LabelLoc = Union[Side, str]
XY = Union[Sequence[float], Point]
RotationMode = Literal['anchor', 'default']
TextMode = Literal['path', 'text']

BilateralDirection = Literal['in', 'out']
EndRef = Literal['start', 'end']
ActionType = Optional[Literal['open', 'close']]
HeaderStyle = Literal['round', 'square', 'screw']
HeaderNumbering = Literal['lr', 'ud', 'ccw']
XformTap = Literal['primary', 'secondary', 'left', 'right']

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


ImageType = Literal['eps', 'jpg', 'pdf', 'pgf', 'png', 'ps',
                    'raw', 'rgba', 'svg', 'tif']
