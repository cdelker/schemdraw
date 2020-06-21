''' Transformer element definitions '''

from ..segments import Segment, SegmentArc
from .elements import Element
from .twoterm import cycloid
from ..adddocs import adddocs


@adddocs(Element)
class Transformer(Element):
    ''' Transformer Element
        Anchors: `p1`, `p2`, `s1`, `s2` (primary and secondary sides)

        Parameters
        ----------
        t1, t2 : int
            Turns on primary (left) and scondary (right) sides
        core : bool
            Draw the core (parallel lines)
        ltaps : dict
            Dictionary of name:position pairs, position is the turn number
            from the top to tap. Each tap defines an anchor point but does
            not draw anything.
        rtaps : dict
            Same as ltaps, on right side
        loop : bool
            Use spiral/cycloid (loopy) style
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        t1 = kwargs.get('t1', 4)
        t2 = kwargs.get('t2', 4)
        core = kwargs.get('core', True)
        ltaps = kwargs.get('ltaps', None)
        rtaps = kwargs.get('rtaps', None)
        loop = kwargs.get('loop', False)
        # Set initial parameters
        ind_w = .4
        lbot = 0
        ltop = t1*ind_w
        rtop = (ltop+lbot)/2 + t2*ind_w/2
        rbot = (ltop+lbot)/2 - t2*ind_w/2

        # Adjust for loops or core
        ind_gap = .75
        if loop:
            ind_gap = ind_gap + .4
        if core:
            ind_gap = ind_gap + .25

        ltapx = 0
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
            self.segments.append(Segment(c1, **kwargs))
            self.segments.append(Segment(c2, **kwargs))
        else:
            for i in range(t1):
                self.segments.append(SegmentArc([0, ltop-(i*ind_w+ind_w/2)],
                                                theta1=270, theta2=90,
                                                width=ind_w, height=ind_w))
            for i in range(t2):
                self.segments.append(SegmentArc([ind_gap, rtop-(i*ind_w+ind_w/2)],
                                                theta1=90, theta2=270,
                                                width=ind_w, height=ind_w))
        # Add the core
        if core:
            top = max(ltop, rtop)
            bot = min(lbot, rbot)
            center = ind_gap/2
            core_w = ind_gap/10
            self.segments.append(Segment([[center-core_w, top], [center-core_w, bot]]))
            self.segments.append(Segment([[center+core_w, top], [center+core_w, bot]]))

        self.anchors['p1'] = [0, ltop]
        self.anchors['p2'] = [0, lbot]
        self.anchors['s1'] = [ind_gap, rtop]
        self.anchors['s2'] = [ind_gap, rbot]

        if ltaps:
            for name, pos in ltaps.items():
                self.anchors[name] = [ltapx, ltop - pos * ind_w]
        if rtaps:
            for name, pos in rtaps.items():
                self.anchors[name] = [rtapx, rtop - pos * ind_w]
