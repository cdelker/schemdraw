from .elements import Element
from ..segments import SegmentImage
from ..util import Point


class ElementImage(Element):
    def __init__(self, image, width=None, height=None, xy=Point((0, 0)), **kwargs):
        super().__init__(**kwargs)
        zorder = kwargs.get('zorder', 1)
        self.segments.append(SegmentImage(image=image, xy=xy, width=width, height=height, zorder=zorder))
        self.elmparams['theta'] = 0
