''' Karnaugh Map '''

from typing import Sequence, Union

import math

from ..segments import Segment, SegmentText, SegmentPoly
from ..elements import Element


class Kmap(Element):
    ''' Karnaugh Map

        Draws a K-Map with 2, 3, or 4 variables.

        Args:
            names: 2, 3, or 4-character string defining names of
                the inputs
            truthtable: list defining values to display in each
                box of the K-Map. First element is string of 2, 3,
                or 4 logic 0's and 1's, and last element is the string
                to display for that input. Example: ('0000', '1')
                displays a '1' when all inputs are 0.
            groups: dictionary of style parameters for circling groups
                of inputs. Dictionary key must be same length as names,
                and defines which elements are circled using '0', '1',
                or '.' in each position. For example, '1...' circles
                every box where A=1, and '.11.' circles every box where
                both B and C are 1. Value of dictionary pair is another
                dictionary containing style of box (e.g. color, fill, lw,
                and ls).
            default: string to display in boxes that don't have a truthtable
                entry defined

        Anchors:
            * cellXXXX - Center of each cell in the grid, where X is 0 or 1
    '''
    def __init__(self,
                 names: str='ABCD',
                 truthtable: Sequence[Sequence[Union[int, str]]]=None,
                 groups: dict=None,
                 default: str='0',
                 **kwargs):
        super().__init__(**kwargs)
        truthtable = [] if truthtable is None else truthtable
        groups = {} if groups is None else groups
        kwargs.setdefault('lw', 1.25)

        if len(names) == 4:
            rows = cols = 4
        elif len(names) == 3:
            rows, cols = 2, 4
        elif len(names) == 2:
            rows = cols = 2
        else:
            raise ValueError('Kmap requires 2 to 4 variable names')

        boxw = 1
        w = cols * boxw
        h = rows * boxw
        order = [0, 1, 3, 2]  # 00, 01, 11, 10
        
        # Frame
        self.segments.append(Segment([(0, 0), (w, 0), (w, h), (0, h), (0, 0)], **kwargs))
        for row in range(rows):
            self.segments.append(Segment([(0, row*boxw), (w, row*boxw)], **kwargs))
        for col in range(cols):
            self.segments.append(Segment([(col*boxw, 0), (col*boxw, h)], **kwargs))
        diag = boxw / math.sqrt(2)
        self.segments.append(Segment([(0, h), (-diag, h+diag)], **kwargs))
        
        # Labels
        rowfmt = '02b' if rows > 2 else '01b'
        colfmt = '02b' if cols > 2 else '01b'
        topnames = names[:2] if len(names) > 2 else names[0]
        leftnames = names[2:] if len(names) > 2 else names[1]
        self.segments.append(SegmentText((0, h+3*diag/4), topnames, align=('right', 'bottom'), fontsize=12))
        self.segments.append(SegmentText((-3*diag/4, h), leftnames, align=('right', 'bottom'), fontsize=12))
        for i, col in enumerate(order[:cols]):
            self.segments.append(SegmentText((col*boxw+boxw/2, h+boxw/20), format(i, colfmt),
                                             align=('center', 'bottom'), fontsize=10))
        for j, row in enumerate(order[:rows]):
            self.segments.append(SegmentText((-boxw/10, h-row*boxw-boxw/2), format(j, rowfmt),
                                             align=('right', 'center'), fontsize=10))

        # Logic values
        ttable_in = [k[0] for k in truthtable]
        ttable_out = [k[1] for k in truthtable]
        for i, col in enumerate(order[:cols]):
            for j, row in enumerate(order[:rows]):
                invalue = ''.join([k for k in format(i, colfmt)] + [k for k in format(j, rowfmt)])
                try:
                    idx = ttable_in.index(invalue)
                except ValueError:
                    valstr = default
                else:
                    valstr = str(ttable_out[idx])
                self.segments.append(SegmentText((col*boxw+boxw/2, h-row*boxw-boxw/2), valstr,
                                                 align=('center', 'center'), fontsize=12))
                self.anchors['cell'+''.join(str(k) for k in invalue)] = col*boxw+boxw/2, h-row*boxw-boxw/2

        # Group circles
        gpad = .1
        for group, style in groups.items():
            tlen = len(topnames)
            llen = len(leftnames)
            gwidth = int(2**tlen / (2**(group[:tlen].count('0') + group[:tlen].count('1'))))
            gheight = int(2**llen / (2**(group[tlen:].count('0') + group[tlen:].count('1'))))
            rowlookup = {'0': 0, '1': 1, '.': 0,
                         '..': 0, '00': 0, '01': 1, '10': 3, '11': 2, '.0': 3, '.1': 1, '0.': 0, '1.': 2}
            col = rowlookup.get(group[:tlen], 0)
            row = rowlookup.get(group[tlen:], 0)

            x1 = col*boxw
            x2 = x1 + gwidth*boxw
            y1 = h - row*boxw
            y2 = y1 - gheight*boxw
            verts = []
            if col+gwidth <= cols and row+gheight <= rows:
                # No wrapping, just one rect
                verts = [[(x1+gpad, y1-gpad), (x2-gpad, y1-gpad), (x2-gpad, y2+gpad), (x1+gpad, y2+gpad)]]
            elif row+gheight <= rows:
                # Wrap left-right
                verts = [[(x1+gpad, y1-gpad), (x1+boxw+gpad, y1-gpad), (x1+boxw+gpad, y2+gpad), (x1+gpad, y2+gpad)],
                         [(-gpad, y1-gpad), (boxw-gpad, y1-gpad), (boxw-gpad, y2+gpad), (-gpad, y2+gpad)]]
            elif col+gwidth <= cols:
                # Wrap top-bottom
                verts = [[(x1+gpad, y1-gpad), (x2-gpad, y1-gpad), (x2-gpad, y1-boxw-gpad), (x1+gpad, y1-boxw-gpad)],
                         [(x1+gpad, h+gpad), (x2-gpad, h+gpad), (x2-gpad, h-boxw+gpad), (x1+gpad, h-boxw+gpad)]]
            else:
                # Wrap four corners
                verts = [[(x1+gpad, y1-gpad), (x1+boxw+gpad, y1-gpad), (x1+boxw+gpad, y1-boxw-gpad), (x1+gpad, y1-boxw-gpad)],
                         [(-gpad, y1-gpad), (boxw-gpad, y1-gpad), (boxw-gpad, y1-boxw-gpad), (-gpad, y1-boxw-gpad)],
                         [(-gpad, h+gpad), (boxw-gpad, h+gpad), (boxw-gpad, h-boxw+gpad), (-gpad, h-boxw+gpad)],
                         [(x1+gpad, h+gpad), (x1+boxw+gpad, h+gpad), (x1+boxw+gpad, h-boxw+gpad), (x1+gpad, h-boxw+gpad)]]

            style.setdefault('lw', 1)
            for vert in verts:
                self.segments.append(SegmentPoly(vert, cornerradius=.25, **style))
