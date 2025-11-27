''' Transformer element definitions '''
from __future__ import annotations
from typing import Optional, Sequence
import math

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
            core: Draw the core (parallel lines) [default: True]
            loop: Use spiral/cycloid (loopy) style [default: False]

        Anchors:
            * p1: primary side 1
            * p2: primary side 2
            * s1: secondary side 1
            * s2: secondary side 2
            * Other anchors defined by `taps` method
    '''
    _element_defaults = {
        'core': True,
        'loop': False,
        'corewidth': 0.75,
        'phasegap': 0.4,
        'arcwidth': 0.4,  # For non-loop inductors
    }
    def __init__(self,
                 t1: int|Sequence[int] = 4,
                 t2: int|Sequence[int] = 4,
                 *,
                 core: Optional[bool] = None,
                 loop: Optional[bool] = None,
                 align: str = 'center',
                 **kwargs):
        super().__init__(**kwargs)

        if isinstance(t1, int):
            t1 = [t1]
        if isinstance(t2, int):
            t2 = [t2]

        self._t1, self._t2 = t1, t2

        phase_gap = self.params['phasegap']
        corewidth = self.params['corewidth']
        if self.params['loop']:
            corewidth = corewidth + .4
        if self.params['core']:
            corewidth = corewidth + .25
        self._corewidth = corewidth

        def right_position():
            if align == 'center':
                right_bot = left_height/2 - right_height/2
                right_top = right_bot + right_height
            elif align == 'bottom':
                right_bot = 0
                right_top = right_height
            else:
                right_top = left_height
                right_bot = right_top - right_height
            return right_bot, right_top

        if self.params['loop']:
            left_cycloids = [cycloid(n, norm=False, vertical=True) for n in t1]
            right_cycloids = [cycloid(n, ofst=(corewidth, 0), norm=False, vertical=True, flip=True) for n in t2]
            left_height = sum(c[-1][1] for c in left_cycloids) + phase_gap * (len(left_cycloids)-1)
            right_height = sum(c[-1][1] for c in right_cycloids) + phase_gap * (len(right_cycloids)-1)

            left_bot = 0
            left_top = left_height
            right_bot, right_top = right_position()

            a, b = .06, .19
            yint = math.acos(a/b)
            period = math.pi*2*a
            ofst = period - (a*yint - b*math.sin(yint))
            resheight = 0.25
            tapxofst = (a-b)/2/resheight

            y = left_bot
            tapnum = 0
            for i, cyc in enumerate(left_cycloids):
                height = cyc[-1][1]
                cyc_y = [(c[0], c[1]+y) for c in cyc]  # Shift to vertical position
                self.segments.append(Segment(cyc_y))
                self.anchors[f'p{i*2+1}'] = cyc_y[0]
                self.anchors[f'p{i*2+2}'] = cyc_y[-1]
                left_top = cyc_y[-1][1]

                for k in range(0, t1[i]):
                    self.anchors[f'tapP{tapnum+k+1}'] = (tapxofst, cyc_y[0][1] + k*period + ofst)

                tapnum += k+1
                y += height + phase_gap


            y = right_bot
            tapnum = 0
            for i, cyc in enumerate(right_cycloids):
                height = cyc[-1][1]
                cyc_y = [(c[0], c[1]+y) for c in cyc]  # Shift to vertical position
                self.segments.append(Segment(cyc_y))
                self.anchors[f's{i*2+1}'] = cyc_y[0]
                self.anchors[f's{i*2+2}'] = cyc_y[-1]
                right_top = cyc_y[-1][1]
                for k in range(0, t2[i]):
                    self.anchors[f'tapS{tapnum+k+1}'] = (corewidth-tapxofst, cyc_y[0][1] + k*period + ofst)
                tapnum += k+1

                y += height + phase_gap

        else:  # Not loop
            arcw = self.params['arcwidth']

            left_height = sum(t1)*arcw + phase_gap*(len(t1)-1)
            right_height = sum(t2)*arcw + phase_gap*(len(t2)-1)
            left_bot = 0
            left_top = left_height
            right_bot, right_top = right_position()

            y = left_bot
            tapnum = 0
            for i, turns in enumerate(t1):
                self.anchors[f'p{i*2+2}'] = (0, y)
                self.anchors[f'p{i*2+1}'] = (0, y+turns*arcw)
                for k in range(turns):
                    self.segments.append(SegmentArc(
                        (0, y+arcw/2), theta1=270, theta2=90, width=arcw, height=arcw))
                    if k < turns-1:
                        self.anchors[f'tapP{tapnum+k+1}'] = (0, y+arcw)
                    y += arcw
                tapnum += turns-1
                y += phase_gap

            y = right_bot
            tapnum = 0
            for i, turns in enumerate(t2):
                self.anchors[f's{i*2+2}'] = (corewidth, y)
                self.anchors[f's{i*2+1}'] = (corewidth, y+turns*arcw)
                for k in range(turns):
                    self.segments.append(SegmentArc(
                        (corewidth, y+arcw/2), theta1=90, theta2=270, width=arcw, height=arcw))
                    if k < turns-1:
                        self.anchors[f'tapS{tapnum+k+1}'] = (corewidth, y+arcw)
                    y += arcw
                tapnum += turns-1
                y += phase_gap

        if self.params['core']:
            top = max(left_top, right_top)
            bot = min(left_bot, right_bot)
            center = corewidth/2
            core_w = corewidth/10
            self.segments.append(Segment(
                [(center-core_w, top), (center-core_w, bot)]))
            self.segments.append(Segment(
                [(center+core_w, top), (center+core_w, bot)]))

        self._left_top = left_top
        self._right_top = right_top

    def tap(self, name: str, pos: int, side: XformTap = 'primary') -> 'Transformer':
        ''' Add a tap

            A tap is simply a named anchor definition along one side
            of the transformer.

            Args:
                name: Name of the tap/anchor
                pos: Turn number from the top of the tap
                side: Primary (left) or Secondary (right) side
        '''
        s = 'P' if side == 'primary' else 'S'
        if pos == 0:
            tap = self.anchors.get(f'{s.lower()}1', None)
        else:
            tap = self.anchors.get(f'tap{s}{pos}', None)


        if tap:
            self.anchors[name] = tap
        else:
            raise ValueError(f'No tap at position {pos}')
        return self
