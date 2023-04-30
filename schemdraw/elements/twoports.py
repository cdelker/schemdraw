''' Twoport elements made from groups of other elements '''

from typing import Sequence, Union

from .compound import ElementCompound
from ..import elements as elm
from ..types import Point
from ..segments import SegmentArrow, Segment
from .elements import Label

# tp_back = 2.5
# tp_xlen = 1.2*tp_back
# tp_lblx = 3*tp_back/16
# tp_lbly = 3*tp_back/16
tp_arrowlen = 1
# tp_pluslen = .2
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

    def __init__(self, input_element: elm.Element2Term, output_element: elm.Element2Term, *d,
                 boxpadx: float = .2, boxpady: float = .2, minw: float = .5,
                 terminals: bool = True, unit: float = 1.5, width: float = 2.15,
                 box: bool = True, boxfill: str = None, boxlw: float = None, boxls: float = None, **kwargs):
        super().__init__(*d, unit=unit, **kwargs)

        input_component  = input_element.down()
        output_component = output_element.down()

        bbox_input  = input_component.get_bbox()
        bbox_output = output_component.get_bbox()

        # since components are not yet placed, transform is not taken into account for bbox calculation
        # hence, use the height rather than the width. Also assumes symmetry
        in_w  = max((bbox_input.ymax - bbox_input.ymin)/2,  minw / 2)
        out_w = max((bbox_output.ymax - bbox_output.ymin)/2, minw / 2)

        input_component  = self.add(input_component.at((boxpadx + in_w, 0)))
        output_component = self.add(output_component.at((width-boxpadx - out_w, 0)))

        # expose input components to outside manipulation
        self.input_component  = input_component
        self.output_component = output_component

        # draw outline
        bbox = self.get_bbox()
        if box:
            self.add(elm.Rect('r', at=[0, 0],
                corner1=(0, bbox.ymin - boxpady), corner2=(width, bbox.ymax + boxpady),
                fill=boxfill, lw=boxlw, ls=boxls, zorder=0))

        bbox = self.get_bbox()

        out_p = self.add(elm.Line('r', at=output_component.start, tox=bbox.xmax))
        out_n = self.add(elm.Line('r', at=output_component.end,   tox=bbox.xmax))
        in_p  = self.add(elm.Line('l', at=input_component.start,  tox=bbox.xmin))
        in_n  = self.add(elm.Line('l', at=input_component.end,    tox=bbox.xmin))

        self.anchors['in_p']   = in_p.end
        self.anchors['in_n']   = in_n.end
        self.anchors['out_p']  = out_p.end
        self.anchors['out_n']  = out_n.end
        self.anchors['center'] = ((bbox.xmin + bbox.xmax) / 2, (bbox.ymin + bbox.ymax) / 2)

        tp_termlen = 0.5
        if terminals:
            for anchor in ['in_p', 'in_n', 'out_p', 'out_n']:
                if 'in' in anchor:
                    xadjust = -tp_termlen
                else:
                    xadjust = tp_termlen

                previous_anchor = self.anchors[anchor]
                new_anchor = (previous_anchor[0] + xadjust, previous_anchor[1])
                self.anchors[anchor] = new_anchor

                self.segments.append(Segment([previous_anchor, new_anchor]))


''' The generic twoport and voltage input transactors feature + and - texts that should rotate with the components.
However, the SegmentText class is designed for fixed rotations in the world frame, not segments that rotate with the
component. Hence, this quick hack effectively places labels that contain the text. Alternate solutions could be to add a
rotation_global flag to the SegmentText class or create a new segment type for these applications. However, those
changes touch a lot of code and could thus cause problems.'''
def _add_rotating_text_at(self, location, text, align=None):
    center_coord = Point(self.anchors['center'])
    self._userlabels.append(
        Label(label=text, loc='center', ofst=location - center_coord, align=align, rotate=True, fontsize=None,
              font=None, mathfont=None, color=None))

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

    def __init__(self, sign: bool = True, arrow: bool = True, reverse_output: bool = False, *d, **kwargs):
        super().__init__(*d, input_element=elm.Gap(), output_element=elm.Gap(),
                         boxpadx=0, minw=0, component_offset=2, **kwargs)

        if sign:
            # note the use of unicode − rather than usual - for better visual representation.
            _add_rotating_text_at(self, Point(( 0.1, 0.1)) + self.input_component.end,    '−', align=('left', 'center'))
            _add_rotating_text_at(self, Point(( 0.1,-0.1)) + self.input_component.start,  '+', align=('left', 'center'))
            if not reverse_output:
                _add_rotating_text_at(self, Point((-0.1, 0.1)) + self.output_component.end,   '−', align=('right','center'))
                _add_rotating_text_at(self, Point((-0.1,-0.1)) + self.output_component.start, '+', align=('right','center'))
            else:
                _add_rotating_text_at(self, Point((-0.1, 0.1)) + self.output_component.end,   '+', align=('right','center'))
                _add_rotating_text_at(self, Point((-0.1,-0.1)) + self.output_component.start, '−', align=('right','center'))

        if arrow:
            center_point = Point(self.anchors['center'])
            self.segments.append(
                SegmentArrow(center_point + Point((-tp_arrowlen / 2, 0)), center_point + Point((tp_arrowlen / 2, 0)),
                             lw=2,
                             headwidth=0.3,
                             headlength=0.3,
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

    def __init__(self, *d, reverse_output: bool = False, **kwargs):
        output_element = elm.SourceControlledV()
        if not reverse_output:
            output_element = output_element.reverse()  # element is reversed in itself, so do a double reversal to cancel
        super().__init__(*d, input_element=elm.Gap(), output_element=output_element, **kwargs)

        _add_rotating_text_at(self, Point((0,  0.05)) + self.input_component.end,   '−', align=('right', 'bottom'))
        _add_rotating_text_at(self, Point((0, -0.05)) + self.input_component.start, '+', align=('right', 'top'))


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

    def __init__(self, *d, reverse_output: bool = False, **kwargs):
        output_element = elm.SourceControlledV()
        if not reverse_output:
            output_element = output_element.reverse()  # element is reversed in itself, so do a double reversal to cancel
        super().__init__(*d, input_element=elm.Line(), output_element=output_element, **kwargs)

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

    def __init__(self, *d, reverse_output: bool = False, **kwargs):
        output_element = elm.SourceControlledI()
        if not reverse_output:
            output_element = output_element.reverse()  # element is reversed in itself, so do a double reversal to cancel
        super().__init__(*d, input_element=elm.Line(), output_element=output_element, **kwargs)

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

    def __init__(self, *d, reverse_output: bool = False, **kwargs):
        output_element = elm.SourceControlledI()
        if not reverse_output:
            output_element = output_element.reverse()  # element is reversed in itself, so do a double reversal to cancel
        super().__init__(*d, input_element=elm.Gap(), output_element=output_element, **kwargs)

        _add_rotating_text_at(self, Point((0,  0.05)) + self.input_component.end,   '−', align=('right', 'bottom'))
        _add_rotating_text_at(self, Point((0, -0.05)) + self.input_component.start, '+', align=('right', 'top'))


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

    def __init__(self, *d, **kwargs):
        super().__init__(*d, input_element=elm.Nullator(), output_element=elm.Norator(), boxpadx=0.3, **kwargs)

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

    def __init__(self, *d, **kwargs):
        super().__init__(*d, input_element=elm.VoltageMirror(), output_element=elm.CurrentMirror(), boxpadx=0.3, **kwargs)