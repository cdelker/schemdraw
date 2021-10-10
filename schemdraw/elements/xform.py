''' Transformer element definitions '''

from ..segments import Segment, SegmentArc
from .elements import Element
from .twoterm import cycloid
from ..types import XformTap


class Transformer(Element):
    ''' Transformer

        Add taps to the windings on either side using
        the `.taps` method.
        
        Args:
            t1: Turns on primary (left) side
            t2: Turns on secondary (right) side
            core: Draw the core (parallel lines)
            loop: Use spiral/cycloid (loopy) style

        Anchors:
            * p1: primary side 1
            * p2: primary side 2
            * s1: secondary side 1
            * s2: secondary side 2
            * Other anchors defined by `taps` method
    '''
    def __init__(self, *d,
                 t1: int=4, t2: int=4, core: bool=True,
                 loop: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        ind_w = .4
        lbot = 0.
        ltop = t1*ind_w
        rtop = (ltop+lbot)/2 + t2*ind_w/2
        rbot = (ltop+lbot)/2 - t2*ind_w/2

        # Adjust for loops or core
        ind_gap = .75
        if loop:
            ind_gap = ind_gap + .4
        if core:
            ind_gap = ind_gap + .25

        ltapx = 0.
        rtapx = ind_gap

        # Draw coils
        if loop:
            c1 = cycloid(loops=t1, ofst=(0, 0), norm=False, vertical=True)
            c2 = cycloid(loops=t2, ofst=(ind_gap, -rtop+ltop), norm=False,
                         flip=True, vertical=True)
            ltapx = min([i[0] for i in c1])
            rtapx = max([i[0] for i in c2])
            ltop = c1[-1][1]
            rtop = c2[-1][1]
            self.segments.append(Segment(c1))
            self.segments.append(Segment(c2))
        else:
            for i in range(t1):
                self.segments.append(SegmentArc(
                    [0, ltop-(i*ind_w+ind_w/2)],
                    theta1=270, theta2=90, width=ind_w, height=ind_w))
            for i in range(t2):
                self.segments.append(SegmentArc(
                    [ind_gap, rtop-(i*ind_w+ind_w/2)],
                    theta1=90, theta2=270, width=ind_w, height=ind_w))
        # Add the core
        if core:
            top = max(ltop, rtop)
            bot = min(lbot, rbot)
            center = ind_gap/2
            core_w = ind_gap/10
            self.segments.append(Segment(
                [(center-core_w, top), (center-core_w, bot)]))
            self.segments.append(Segment(
                [(center+core_w, top), (center+core_w, bot)]))

        self.anchors['p1'] = (0, ltop)
        self.anchors['p2'] = (0, lbot)
        self.anchors['s1'] = (ind_gap, rtop)
        self.anchors['s2'] = (ind_gap, rbot)

        self._ltapx = ltapx  # Save these for adding taps
        self._rtapx = rtapx
        self._ltop = ltop
        self._rtop = rtop
        self._ind_w = ind_w

        if 'ltaps' in kwargs:
            for name, pos in kwargs['ltaps'].items():
                self.tap(name, pos, 'primary')
        if 'rtaps' in kwargs:
            for name, pos in kwargs['rtaps'].items():
                self.tap(name, pos, 'secondary')

    def tap(self, name: str, pos: int, side: XformTap='primary'):
        ''' Add a tap

            A tap is simply a named anchor definition along one side
            of the transformer.

            Args:
                name: Name of the tap/anchor
                pos: Turn number from the top of the tap
                side: Primary (left) or Secondary (right) side
        '''
        if side in ['left', 'primary']:
            self.anchors[name] = (self._ltapx, self._ltop - pos * self._ind_w)
        elif side in ['right', 'secondary']:
            self.anchors[name] = (self._rtapx, self._rtop - pos * self._ind_w)
        else:
            raise ValueError(f'Undefined tap side {side}')
        return self