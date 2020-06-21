''' Operation amplifier '''

import numpy as np

from .elements import Element, gap
from ..segments import Segment
from ..adddocs import adddocs


oa_back = 2.5
oa_xlen = oa_back * np.sqrt(3)/2
oa_lblx = oa_xlen/8
oa_pluslen = .2


@adddocs(Element)
class Opamp(Element):
    ''' Operational Amplifier. Anchors: `in1`, `in2`, `out`, `vd`,
        `vs`, `n1`, `n2`, `n1a`, `n2a`.

        Parameters
        ----------
        sign : bool
            Draw +/- sign labels at each input
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment(
            [[0, 0], [0, oa_back/2], [oa_xlen, 0], [0, -oa_back/2], [0, 0],
             gap, [oa_xlen, 0]]))

        if kwargs.get('sign', True):
            self.segments.append(Segment(
                [[oa_lblx-oa_pluslen/2, oa_back/4],
                 [oa_lblx+oa_pluslen/2, oa_back/4]]))
            self.segments.append(Segment(
                [[oa_lblx-oa_pluslen/2, -oa_back/4],
                 [oa_lblx+oa_pluslen/2, -oa_back/4]]))
            self.segments.append(Segment(
                [[oa_lblx, -oa_back/4-oa_pluslen/2],
                 [oa_lblx, -oa_back/4+oa_pluslen/2]]))

        self.anchors['center'] = [oa_xlen/2, 0]
        self.anchors['in1'] = [0, oa_back/4]
        self.anchors['in2'] = [0, -oa_back/4]
        self.anchors['out'] = [oa_xlen, 0]
        self.anchors['vd'] = [oa_xlen/3, .84]
        self.anchors['vs'] = [oa_xlen/3, -.84]
        self.anchors['n1'] = [oa_xlen*2/3, -.42]
        self.anchors['n2'] = [oa_xlen*2/3, .42]
        self.anchors['n1a'] = [oa_xlen*.9, -.13]
        self.anchors['n2a'] = [oa_xlen*.9, .13]
        self.params['drop'] = [oa_xlen, 0]
