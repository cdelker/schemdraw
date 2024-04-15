''' Twoport elements made from groups of other elements '''
from __future__ import annotations
from functools import partial

from .compound import ElementCompound
from ..import elements as elm
from ..types import Point, Linestyle
from ..segments import Segment, SegmentText, Segment
from typing import Optional


tp_arrowlen = 1
tp_termlen = 0.5  # terminal length


class ElementTwoport(ElementCompound):
    ''' Compound twoport element

        Args:
            input_element: The element forming the input branch of the twoport
            output_element: The element forming the output branch of the twoport
            bpadx: Horizontal padding from edge of either component
            bpady: Vertical padding from edge of either component
            minw: Margin around component if smaller than minw
            terminals: Draw with terminals extending past box
            unit: Length of input and output element
            width: Width of the twoport box
            box: Draw twoport outline
            boxfill: Color to fill the twoport if not None
            boxlw: Line width of twoport outline
            boxls: Line style of twoport outline '-', '--', ':', etc.

        Anchors:
            * in_p
            * in_n
            * out_p
            * out_n
            * center
    '''
    def __init__(self, input_element: type[elm.Element2Term],
                 output_element: type[elm.Element2Term],
                 boxpadx: float = .2, boxpady: float = .2, minw: float = .5,
                 terminals: bool = True, unit: float = 1.5, width: float = 2.15,
                 box: bool = True, boxfill: Optional[str] = None, boxlw: Optional[float] = None, boxls: Optional[Linestyle] = None, **kwargs):
        self.input_element = input_element
        self.output_element = output_element
        self.boxpadx = boxpadx
        self.boxpady = boxpady
        self.minw = minw
        self.terminals = terminals
        self.unit = unit
        self.width = width
        self.box = box
        self.boxfill = boxfill
        self.boxlw = boxlw
        self.boxls = boxls
        super().__init__(unit=unit, **kwargs)

    def setup(self):
        self.input_component = self.input_element().down()
        self.output_component = self.output_element().down()

        bbox_input = self.input_component.get_bbox()
        bbox_output = self.output_component.get_bbox()

        # since components are not yet placed, transform is not taken into account for bbox calculation
        # hence, use the height rather than the width. Also assumes symmetry
        in_w = max((bbox_input.ymax - bbox_input.ymin)/2,  self.minw / 2)
        out_w = max((bbox_output.ymax - bbox_output.ymin)/2, self.minw / 2)

        self.add(self.input_component.at((self.boxpadx + in_w, 0)))
        self.add(self.output_component.at((self.width-self.boxpadx - out_w, 0)))

        # draw outline
        bbox = self.get_bbox()
        if self.box:
            self.add(elm.Rect(theta=0, at=[0, 0],
                              corner1=(0, bbox.ymin - self.boxpady), corner2=(self.width, bbox.ymax + self.boxpady),
                              fill=self.boxfill, lw=self.boxlw, ls=self.boxls, zorder=0))

        bbox = self.get_bbox()

        out_p = self.add(elm.Line().at(self.output_component.start).tox(bbox.xmax).right())
        out_n = self.add(elm.Line().at(self.output_component.end).tox(bbox.xmax).right())
        in_p = self.add(elm.Line().at(self.input_component.start).tox(bbox.xmin).left())
        in_n = self.add(elm.Line().at(self.input_component.end).tox(bbox.xmin).left())

        self.anchors['in_p'] = in_p.end
        self.anchors['in_n'] = in_n.end
        self.anchors['out_p'] = out_p.end
        self.anchors['out_n'] = out_n.end
        self.anchors['center'] = ((bbox.xmin + bbox.xmax) / 2, (bbox.ymin + bbox.ymax) / 2)

        if self.terminals:
            for anchor in ['in_p', 'in_n', 'out_p', 'out_n']:
                if 'in' in anchor:
                    xadjust = -tp_termlen
                else:
                    xadjust = tp_termlen

                previous_anchor = self.anchors[anchor]
                new_anchor = (previous_anchor[0] + xadjust, previous_anchor[1])
                self.anchors[anchor] = new_anchor

                self.segments.append(Segment([previous_anchor, new_anchor]))


class TwoPort(ElementTwoport):
    ''' Generic Twoport

        Args:
            bpadx: Horizontal padding from edge of either component
            bpady: Vertical padding from edge of either component
            minw: Margin around component if smaller than minw
            terminals: Draw with terminals extending past box
            component_offset: Offset between input and output element
            box: Draw twoport outline
            boxfill: Color to fill the twoport if not None
            boxlw: Line width of twoport outline
            boxls: Line style of twoport outline '-', '--', ':', etc.
            sign: Draw input and output terminal labels
            arrow: Draw arrow from input to output

        Anchors:
            * in_p
            * in_n
            * out_p
            * out_n
            * center
    '''
    def __init__(self, sign: bool = True, arrow: bool = True, reverse_output: bool = False, **kwargs):
        self.sign = sign
        self.arrow = arrow
        self.reverse_output = reverse_output
        super().__init__(input_element=elm.Gap, output_element=elm.Gap,
                         boxpadx=0, minw=0, component_offset=2, **kwargs)

    def setup(self):
        super().setup()
        if self.sign:
            # note the use of unicode − rather than usual - for better visual representation.
            self.segments.append(
                SegmentText(pos=Point((0.1, 0.1)) + self.input_component.end, label='−',
                            align=('left', 'center'), rotation_global=False))
            self.segments.append(
                SegmentText(pos=Point((0.1, -0.1)) + self.input_component.start, label='+',
                            align=('left', 'center'), rotation_global=False))

            if not self.reverse_output:
                self.segments.append(
                    SegmentText(pos=Point((-0.1, 0.1)) + self.output_component.end, label='−',
                                align=('right', 'center'), rotation_global=False))
                self.segments.append(
                    SegmentText(pos=Point((-0.1, -0.1)) + self.output_component.start, label='+',
                                align=('right', 'center'), rotation_global=False))
            else:
                self.segments.append(
                    SegmentText(pos=Point((-0.1, 0.1)) + self.output_component.end, label='+',
                                align=('right', 'center'), rotation_global=False))
                self.segments.append(
                    SegmentText(pos=Point((-0.1, -0.1)) + self.output_component.start, label='−',
                                align=('right', 'center'), rotation_global=False))

        if self.arrow:
            center_point = Point(self.anchors['center'])
            self.segments.append(
                Segment((center_point + Point((-tp_arrowlen / 2, 0)), center_point + Point((tp_arrowlen / 2, 0))),
                        arrow='->',
                        lw=2,
                        arrowwidth=0.3,
                        arrowlength=0.3,
                        ))


class VoltageTransactor(ElementTwoport):
    ''' Voltage transactor

        Args:
            bpadx: Horizontal padding from edge of either component
            bpady: Vertical padding from edge of either component
            minw: Margin around component if smaller than minw
            terminals: Draw with terminals extending past box
            component_offset: Offset between input and output element
            box: Draw twoport outline
            boxfill: Color to fill the twoport if not None
            boxlw: Line width of twoport outline
            boxls: Line style of twoport outline '-', '--', ':', etc.
            reverse_output: Switch direction of output source, defaults to False

        Anchors:
            * in_p
            * in_n
            * out_p
            * out_n
            * center
    '''
    def __init__(self, reverse_output: bool = False, **kwargs):
        output_element: type[elm.Element2Term] = elm.SourceControlledV
        if not reverse_output:
            # mypy doesn't like partials
            output_element = partial(output_element, reverse=True)  # type:ignore
        super().__init__(input_element=elm.Gap, output_element=output_element, **kwargs)

    def setup(self):
        super().setup()
        self.segments.append(
            SegmentText(pos=Point((0, 0.05)) + self.input_component.end, label='−',
                        align=('right', 'bottom'), rotation_global=False))
        self.segments.append(
            SegmentText(pos=Point((0, -0.05)) + self.input_component.start, label='+',
                        align=('right', 'top'), rotation_global=False))


class TransimpedanceTransactor(ElementTwoport):
    ''' Transimpedance transactor

        Args:
            bpadx: Horizontal padding from edge of either component
            bpady: Vertical padding from edge of either component
            minw: Margin around component if smaller than minw
            terminals: Draw with terminals extending past box
            component_offset: Offset between input and output element
            box: Draw twoport outline
            boxfill: Color to fill the twoport if not None
            boxlw: Line width of twoport outline
            boxls: Line style of twoport outline '-', '--', ':', etc.
            reverse_output: Switch direction of output source, defaults to False

        Anchors:
            * in_p
            * in_n
            * out_p
            * out_n
            * center
    '''
    def __init__(self, reverse_output: bool = False, **kwargs):
        output_element: type[elm.Element2Term] = elm.SourceControlledV
        if not reverse_output:
            # element is reversed in itself, so do a double reversal to cancel
            output_element = partial(output_element, reverse=True)   # type:ignore
        super().__init__(input_element=elm.Line, output_element=output_element, **kwargs)

    def setup(self):
        super().setup()
        current_label_inline = elm.CurrentLabelInline(ofst=-0.15, headlength=0.3)
        current_label_inline.at(self.input_component)
        self.add(current_label_inline)


class CurrentTransactor(ElementTwoport):
    ''' Current transactor

        Args:
            bpadx: Horizontal padding from edge of either component
            bpady: Vertical padding from edge of either component
            minw: Margin around component if smaller than minw
            terminals: Draw with terminals extending past box
            component_offset: Offset between input and output element
            box: Draw twoport outline
            boxfill: Color to fill the twoport if not None
            boxlw: Line width of twoport outline
            boxls: Line style of twoport outline '-', '--', ':', etc.
            reverse_output: Switch direction of output source, defaults to False

        Anchors:
            * in_p
            * in_n
            * out_p
            * out_n
            * center
    '''

    def __init__(self, reverse_output: bool = False, **kwargs):
        output_element: type[elm.Element2Term] = elm.SourceControlledI
        if not reverse_output:
            # element is reversed in itself, so do a double reversal to cancel
            output_element = partial(output_element, reverse=True)  # type:ignore
        super().__init__(input_element=elm.Line, output_element=output_element, **kwargs)

    def setup(self):
        super().setup()
        current_label_inline = elm.CurrentLabelInline(ofst=-0.15, headlength=0.3)
        current_label_inline.at(self.input_component)
        self.add(current_label_inline)


class TransadmittanceTransactor(ElementTwoport):
    ''' Transadmittance transactor

        Args:
            bpadx: Horizontal padding from edge of either component
            bpady: Vertical padding from edge of either component
            minw: Margin around component if smaller than minw
            terminals: Draw with terminals extending past box
            component_offset: Offset between input and output element
            box: Draw twoport outline
            boxfill: Color to fill the twoport if not None
            boxlw: Line width of twoport outline
            boxls: Line style of twoport outline '-', '--', ':', etc.
            reverse_output: Switch direction of output source, defaults to False

        Anchors:
            * in_p
            * in_n
            * out_p
            * out_n
            * center
    '''

    def __init__(self, reverse_output: bool = False, **kwargs):
        output_element: type[elm.Element2Term] = elm.SourceControlledI
        self.reverse_output = reverse_output
        if not reverse_output:
            # element is reversed in itself, so do a double reversal to cancel
            output_element = partial(output_element, reverse=True)  # type:ignore
        super().__init__(input_element=elm.Gap, output_element=output_element, **kwargs)

    def setup(self):
        super().setup()
        self.segments.append(
            SegmentText(pos=Point((0, 0.05)) + self.input_component.end, label='−',
                        align=('right', 'bottom'), rotation_global=False))
        self.segments.append(
            SegmentText(pos=Point((0, -0.05)) + self.input_component.start, label='+',
                        align=('right', 'top'), rotation_global=False))


class Nullor(ElementTwoport):
    ''' Nullor

        Args:
            bpadx: Horizontal padding from edge of either component
            bpady: Vertical padding from edge of either component
            minw: Margin around component if smaller than minw
            terminals: Draw with terminals extending past box
            component_offset: Offset between input and output element
            box: Draw twoport outline
            boxfill: Color to fill the twoport if not None
            boxlw: Line width of twoport outline
            boxls: Line style of twoport outline '-', '--', ':', etc.

        Anchors:
            * in_p
            * in_n
            * out_p
            * out_n
            * center
    '''
    def __init__(self, **kwargs):
        super().__init__(input_element=elm.Nullator, output_element=elm.Norator, boxpadx=0.3, **kwargs)


class VMCMPair(ElementTwoport):
    ''' Nullor

        Args:
            bpadx: Horizontal padding from edge of either component
            bpady: Vertical padding from edge of either component
            minw: Margin around component if smaller than minw
            terminals: Draw with terminals extending past box
            component_offset: Offset between input and output element
            box: Draw twoport outline
            boxfill: Color to fill the twoport if not None
            boxlw: Line width of twoport outline
            boxls: Line style of twoport outline '-', '--', ':', etc.

        Anchors:
            * in_p
            * in_n
            * out_p
            * out_n
            * center
    '''
    def __init__(self, **kwargs):
        super().__init__(input_element=elm.VoltageMirror, output_element=elm.CurrentMirror,
                         boxpadx=0.3, **kwargs)
