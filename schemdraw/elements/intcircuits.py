''' Integrated Circuit Element '''

from __future__ import annotations
from typing import Any, Optional, Sequence, Tuple, cast
from collections import namedtuple
import math
from dataclasses import dataclass, replace

from ..segments import Segment, SegmentText, SegmentCircle, SegmentPoly, SegmentType
from ..elements import Element
from ..util import linspace, Point
from ..types import XY, Side, Halign, Valign
from ..backends.svg import text_size
from .. import drawing_stack


@dataclass
class IcPin:
    ''' Integrated Circuit Pin

        Args:
            name: Input/output name (inside the box)
            pin: Pin name/number (outside the box)
            side: Side of box for the pin, 'left', 'right', 'top', 'bottom'
            pos: Pin position along the side, fraction from 0-1
            slot: Slot definition of pin location, given in 'X/Y' format.
                '2/4' is the second pin on a side with 4 pins.
            invert:Add an invert bubble to the pin
            invertradius: Radius of invert bubble
            color: Color for the pin and label
            rotation: Rotation for label text
            anchorname: Named anchor for the pin
     '''
    name: str | None = None
    pin: str | None = None
    side: Side = 'L'
    pos: float | None = None
    slot: str | None = None
    invert: bool = False
    invertradius: float = 0.15
    color: str | None = None
    rotation: float = 0
    anchorname: str | None = None
    lblsize: float | None = None
    pinlblsize: float | None = None


@dataclass
class IcSide:
    ''' Pin layout parameters for one side of an Ic '''
    spacing: float = 0.0  # 0 for auto
    pad: float = .25
    leadlen: float = 0.5
    label_ofst: float = 0.15
    label_size: float = 14.
    pinlabel_ofst: float = 0.05
    pinlabel_size: float = 11.


IcBox = namedtuple('IcBox', 'w h y1 y2')


class Ic(Element):
    _element_defaults = {
        'pinspacing': 0.0,
        'edgepadH': 0.5,
        'edgepadW': 0.5,
        'leadlen': 0.5,
        'lsize': 14,
        'lofst': 0.15,
        'plblofst': 0.075,
        'plblsize': 11
    }
    def __init__(self,
                 size: Optional[XY] = None,
                 pins: Optional[Sequence[IcPin]] = None,
                 slant: float = 0,
                 **kwargs):
        super().__init__(**kwargs)
        self.size = size if size is not None else self.params.get('size')
        self._sizeauto: Optional[tuple[float, float]] = None
        self.slant = slant
        self.pins: dict[Side, list[IcPin]] = {'L': [], 'R': [], 'T': [], 'B': []}
        self.usersides: dict[Side, IcSide] = {}
        self.sides: dict[Side, IcSide] = {}
        self._dflt_side = IcSide(
            self.params.get('pinspacing', 0),
            self.params.get('edgepadH', .25),
            self.params.get('leadlen', .5),
            self.params.get('lofst', .15),
            self.params.get('lsize', 14),
            self.params.get('plblofst', .05),
            self.params.get('plblsize', 11))

        if pins is not None:
            for pin in pins:
                side = cast(Side, pin.side[0].upper())
                self.pins[side].append(pin)

        self._icbox = IcBox(0,0,0,0)
        self._setsize()

    def __getattr__(self, name: str) -> Any:
        ''' Allow getting anchor position as attribute '''
        anchornames = ['start', 'end', 'center', 'istart', 'iend',
                       'N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW',
                       'NNE', 'NNW', 'ENE', 'WNW', 'SSE', 'SSW', 'ESE', 'WSW']
        anchornames += list(vars(self).get('anchors', {}).keys())
        anchornames += self.pinnames
        anchornames += [f'pin{p.pin}' for p in self.pins.get('L', [])]
        anchornames += [f'pin{p.pin}' for p in self.pins.get('R', [])]
        anchornames += [f'pin{p.pin}' for p in self.pins.get('T', [])]
        anchornames += [f'pin{p.pin}' for p in self.pins.get('B', [])]
        if (name in anchornames and not name in vars(self).get('absanchors', {})):
                # Not placed yet
                drawing_stack.push_element(self)

        if name in vars(self).get('absanchors', {}):
            return vars(self).get('absanchors')[name]  # type: ignore
        raise AttributeError(f'{name} not defined in Element')

    @property
    def pinnames(self) -> list[str]:
        ''' List of all pin names '''
        names: list[str] = []
        for _, pins in self.pins.items():
            names.extend(p.name for p in pins if p.name)
        return names

    def pin(self,
            side: Side = 'L',
            name: str | None = None,
            pin: str | None = None,
            pos: float | None = None,
            slot: str | None = None,
            invert: bool = False,
            invertradius: float = 0.15,
            color: str | None = None,
            rotation: float = 0,
            anchorname: str | None = None,
            lblsize: float | None = None):
        ''' Add a pin to the IC

            Args:
                name: Input/output name (inside the box)
                pin: Pin name/number (outside the box)
                side: Side of box for the pin, 'left', 'right', 'top', 'bottom'
                pos: Pin position along the side, fraction from 0-1
                slot: Slot definition of pin location, given in 'X/Y' format.
                    '2/4' is the second pin on a side with 4 pins.
                invert:Add an invert bubble to the pin
                invertradius: Radius of invert bubble
                color: Color for the pin and label
                rotation: Rotation for label text
                anchorname: Named anchor for the pin
                lblsize: Font size for label
        '''
        side = cast(Side, side[0].upper())
        self.pins[side].append(IcPin(name, pin, side, pos, slot, invert,
                                    invertradius, color, rotation, anchorname, lblsize))
        self._setsize()
        return self

    def side(self,
             side: Side = 'L',
             spacing: float = 0,
             pad: float = 0.5,
             leadlen: float = .5,
             label_ofst: float = 0.15,
             label_size: float = 14.,
             pinlabel_ofst: float = 0.05,
             pinlabel_size: float = 11.):
        ''' Set parameters for spacing/layout of one side

            Args:
                side: Side of box to define
                spacing: Distance between pins
                pad: Distance from box edge to first pin
                leadlen: Length of pin lead extensions
                label_ofst: Offset between box and label (inside box)
                label_size: Font size of label (inside box)
                pinlabel_ofst: Offset between box and pin label (outside box)
                pinlabel_size: Font size of pin label (outside box)
        '''
        side = cast(Side, side[0].upper())
        self.usersides[side] = IcSide(spacing, pad, leadlen,
                                      label_ofst, label_size,
                                      pinlabel_ofst, pinlabel_size)
        self._setsize()
        return self

    def _countpins(self) -> dict[Side, int]:
        ''' Count the number of pins (or slots) on each side '''
        pincount = {}
        for side, pins in self.pins.items():
            slotnames = [p.slot for p in pins]
            # Add a 0 - can't max an empty list
            slots = [int(p.split('/')[1]) for p in slotnames if p is not None] + [0]
            pincount[side] = max(len(pins), max(slots))
        return pincount

    def _autosize(self) -> None:
        ''' Determine size of box if not provided '''
        lengths: dict[str, float] = {}
        labelwidths: dict[str, float] = {}

        # Determine length of each side given spacing and pad
        for side in ['L', 'R', 'T', 'B']:
            side = cast(Side, side)
            sideparam = replace(self.usersides.get(side, self._dflt_side))
            self.sides[side] = sideparam
            if sideparam.spacing == 0:
                sideparam.spacing = 0.6
            lengths[side] = sideparam.pad * 2 + sideparam.spacing * (self.pincount[side] - 1)

            # Expand to fit pin labels if necessary
            labelw = 0.
            for p in self.pins[side]:
                if p.name:
                    lblsize = p.lblsize if p.lblsize else self.params['lsize']
                    labelw = max(labelw, text_size(p.name, size=lblsize)[0]/72*2)
            labelwidths[side] = labelw

        # Box is larger of the two sides, with minimum of 2
        labelw = labelwidths['L'] + labelwidths['R'] + 4*self.params['lofst']
        boxh = max(lengths.get('L', 0.), lengths.get('R', 0.), 2+self.params['edgepadH'])
        boxw = max(lengths.get('T', 0.), lengths.get('B', 0.), 2+self.params['edgepadW'], labelw)
        self._sizeauto = boxw, boxh

        # Adjust pad for the shorter of the two parallel sides
        for side in ['L', 'R']:
            side = cast(Side, side)
            sideparam = self.sides.get(side, self._dflt_side)
            sideparam.pad = (boxh - sideparam.spacing * (self.pincount[side] - 1)) / 2

        for side in ['T', 'B']:
            side = cast(Side, side)
            sideparam = self.sides.get(side, self._dflt_side)
            sideparam.pad = (boxw - sideparam.spacing * (self.pincount[side] - 1)) / 2

    def _autopinlayout(self) -> None:
        ''' Determine pin layout when box size is specified '''
        for side in ['L', 'R', 'T', 'B']:
            side = cast(Side, side)
            sideparam = replace(self.usersides.get(side, self._dflt_side))
            self.sides[side] = sideparam
            length = self.size[0] if side in ['T', 'B'] else self.size[1]
            pad = sideparam.pad
            if sideparam.spacing == 0:
                #use PAD to evenly space pins over (length-2*pad)
                if self.pincount[side] > 1:
                    sideparam.spacing = (length - 2*pad) / (self.pincount[side] - 1)
                else:
                    sideparam.pad = length/2
            else:
                # Addjust PAD center the group of pins
                sideparam.pad = (length - sideparam.spacing*(self.pincount[side]-1)) / 2

    def _drawbox(self) -> IcBox:
        ''' Draw main box and return its size '''
        if self.size:
            w, h = self.size
        elif self._sizeauto:
            w, h = self._sizeauto
        else:
            w, h = (2, 3)

        tanslant = w * math.tan(math.radians(self.slant))
        if self.slant > 0:
            y1 = 0 - tanslant
            y2 = h + tanslant
            path = [Point((0, 0)), Point((w, y1)), Point((w, y2)), Point((0, h)), Point((0, 0))]
        elif self.slant < 0:
            y1 = 0 + tanslant
            y2 = h - tanslant
            path = [Point((0, y1)), Point((w, 0)), Point((w, h)), Point((0, y2)), Point((0, y1))]
        else:
            y1 = 0
            y2 = h
            path = [Point((0, 0)), Point((w, 0)), Point((w, h)), Point((0, h)), Point((0, 0))]
        self.segments.append(Segment(path))
        return IcBox(w, h, y1, y2)

    def _pinpos(self, side: Side, pin: IcPin, num: int) -> Point:
        ''' Get XY position of pin '''
        sidesetup = self.sides.get(side, self._dflt_side)
        spacing = sidesetup.spacing if sidesetup.spacing > 0 else 0.6
        if pin.slot:
            num = int(pin.slot.split('/')[0]) - 1
        z = sidesetup.pad + num*spacing
        if pin.pos:
            z = sidesetup.pad + pin.pos * (self.pincount[side]-1)*spacing
        xy = {'L': Point((0, z)),
              'R': Point((self._icbox.w, z)),
              'T': Point((z, self._icbox.h)),
              'B': Point((z, 0))
              }.get(side, Point((0, 0)))

        # Adjust pin position for slant
        if side == 'T' and self.slant > 0:
            xy = Point((xy[0], xy[1] - xy[0] * math.tan(-math.radians(self.slant))))
        elif side == 'T' and self.slant < 0:
            xy = Point(((xy[0], xy[1] + (self._icbox.y2-self._icbox.h) - xy[0] * math.tan(-math.radians(self.slant)))))
        elif side == 'B' and self.slant < 0:
            xy = Point((xy[0], xy[1] - (self._icbox.y2-self._icbox.h) - xy[0] * math.tan(math.radians(self.slant))))
        elif side == 'B' and self.slant > 0:
            xy = Point((xy[0], xy[1] - xy[0] * math.tan(math.radians(self.slant))))
        return xy

    def _drawpin(self, side: Side, pin: IcPin, num: int) -> None:
        ''' Draw one pin and its labels '''
        # num is index of where pin is along side
        sidesetup = self.sides.get(side, self._dflt_side)
        xy = self._pinpos(side, pin, num)
        leadext = {'L': Point((-sidesetup.leadlen, 0)),
                   'R': Point((sidesetup.leadlen, 0)),
                   'T': Point((0, sidesetup.leadlen)),
                   'B': Point((0, -sidesetup.leadlen))}.get(side, Point((0, 0)))

        # Anchor
        anchorpos = xy+leadext
        self.anchors[f'in{side[0].upper()}{num+1}'] = anchorpos
        if pin.anchorname:
            self.anchors[pin.anchorname] = anchorpos
        elif pin.name:
            if pin.name == '>':
                self.anchors['CLK'] = anchorpos
            self.anchors[pin.name] = anchorpos
        if pin.pin:
            self.anchors[f'pin{pin.pin}'] = anchorpos

        # Lead        
        if sidesetup.leadlen > 0:
            if pin.invert:  # Add invert-bubble
                invertradius = pin.invertradius
                invertofst = {'L': Point((-invertradius, 0)),
                              'R': Point((invertradius, 0)),
                              'T': Point((0, invertradius)),
                              'B': Point((0, -invertradius))}.get(side, Point((0, 0)))
                self.segments.append(SegmentCircle(
                    xy+invertofst, invertradius))
                self.segments.append(Segment([xy+invertofst*2, xy+leadext]))
            else:
                self.segments.append(Segment([xy, xy+leadext]))

        # Pin Number (outside the box)
        if pin.pin and pin.pin != '':
            # Account for any invert-bubbles
            invertradius = pin.invertradius * pin.invert
            plbl = sidesetup.pinlabel_ofst
            pofst = {'L': Point((-plbl-invertradius*2, plbl)),
                     'R': Point((plbl+invertradius*2, plbl)),
                     'T': Point((plbl, plbl+invertradius*2)),
                     'B': Point((plbl, -plbl-invertradius*2))
                     }.get(side)

            align = cast(Optional[Tuple[Halign, Valign]],
                         {'L': ('right', 'bottom'),
                          'R': ('left', 'bottom'),
                          'T': ('left', 'bottom'),
                          'B': ('left', 'top')}.get(side))
            self.segments.append(SegmentText(
                pos=xy+pofst,
                label=pin.pin,
                align=align,
                fontsize=pin.pinlblsize if pin.pinlblsize is not None else sidesetup.pinlabel_size))

        if pin.name == '>':
            self._drawclkpin(xy, leadext, side, pin, num)
            return

        # Label (inside the box)
        if pin.name and pin.name != '':
            pofst = {'L': Point((sidesetup.label_ofst, 0)),
                     'R': Point((-sidesetup.label_ofst, 0)),
                     'T': Point((0, -sidesetup.label_ofst)),
                     'B': Point((0, sidesetup.label_ofst))}.get(side)

            align = cast(Optional[Tuple[Halign, Valign]],
                         {'L': ('left', 'center'),
                          'R': ('right', 'center'),
                          'T': ('center', 'top'),
                          'B': ('center', 'bottom')}.get(side))

            self.segments.append(SegmentText(
                pos=xy+pofst,
                label=pin.name,
                align=align,
                fontsize=pin.lblsize if pin.lblsize is not None else sidesetup.label_size,
                color=pin.color,
                rotation=pin.rotation,
                rotation_mode='default'))

    def _drawclkpin(self, xy: Point, leadext: Point,
                    side: Side, pin: IcPin, num: int) -> None:
        ''' Draw clock pin > '''
        sidesetup = self.sides.get(side, self._dflt_side)
        sidesetup.label_size
        clkw, clkh = 0.4 * sidesetup.label_size/16, 0.2 * sidesetup.label_size/16
        if side in ['T', 'B']:
            clkw = math.copysign(clkw, leadext[1]) if leadext[1] != 0 else clkw
            clkpath = [Point((xy[0]-clkh, xy[1])),
                        Point((xy[0], xy[1]-clkw)),
                        Point((xy[0]+clkh, xy[1]))]
        else:
            clkw = math.copysign(clkw, -leadext[0]) if leadext[0] != 0 else clkw
            clkpath = [Point((xy[0], xy[1]+clkh)),
                        Point((xy[0]+clkw, xy[1])),
                        Point((xy[0], xy[1]-clkh))]
        self.segments.append(Segment(clkpath))

    def _drawpins(self) -> None:
        ''' Draw all the pins '''
        for side, pins in self.pins.items():
            for i, pin in enumerate(pins):
                self._drawpin(side, pin, i)

    def _setsize(self) -> None:
        ''' Set size based on pins added so far '''
        self.pincount = self._countpins()
        if self.size is None:
            self._autosize()
        else:
            self._autopinlayout()
        self.pinspacing = {'L': self.sides['L'].spacing,
                           'R': self.sides['R'].spacing,
                           'T': self.sides['T'].spacing,
                           'B': self.sides['B'].spacing}

    def _place(self, dwgxy: XY, dwgtheta: float, **dwgparams) -> tuple[Point, float]:
        self._icbox = self._drawbox()
        self._drawpins()
        self.elmparams['lblloc'] = 'center'
        self.anchors['center'] = (self._icbox.w/2, self._icbox.h/2)
        return super()._place(dwgxy, dwgtheta, **dwgparams)


class Multiplexer(Ic):
    ''' Multiplexer

        Args:
            demux: Draw as demultiplexer
            size: (Width, Height) of box
            pins: List of IcPin instances defining the inputs/outputs
            slant: Slant angle of top/bottom edges

        Keyword Args:            
            pinspacing: Spacing between pins [default: 0.6]
            edgepadH: Padding between top/bottom and first pin [default: 0.25]
            edgepadW: Padding between left/right and first pin [default: 0.25]
            lofst: Offset between edge and label (inside box) [default: 0.15]
            lsize: Font size of labels (inside box) [default: 14]
            plblofst: Offset between edge and pin label (outside box) [default: 0.05]
            plblsize: Font size of pin labels (outside box) [default: 11]

        If a pin is named '>', it will be drawn as a proper clock signal input.

        Anchors:
            * inL[X] - Each pin on left side
            * inR[X] - Each pin on right side
            * inT[X] - Each pin on top side
            * inB[X] - Each pin on bottom side
            * pin[X] - Each pin with a number
            * CLK (if clock pin is defined with '>' name)

        Pins with names are also defined as anchors (if the name does
        not conflict with other attributes).
    '''
    def __init__(self,
                 demux: bool = False,
                 size: Optional[XY] = None,
                 pins: Optional[Sequence[IcPin]] = None,
                 slant: float = 25,
                 **kwargs):
        slant = -slant if not demux else slant
        super().__init__(size=size,
                         pins=pins,
                         slant=slant,
                         **kwargs)


class IcDIP(Element):
    ''' Dual-inline Package Integrated Circuit.

        Args:
            names: List of names for each pin to display inside the box

        Keyword Args:
            pins: number of pins [default: 8]
            notch: Show the notch at top of box [default: True]
            width: Width of the box [default: 3]
            pinw: Width and height of each pin [default: 0.6]
            spacing: Distance between each pin [default: 0.5]
            number: Show pin numbers inside each pin [default: True]
            fontsize: Size for pin name labels [default: 12]
            pfontsize: Size for pin number labels [default: 10]

        Anchors:
            * p[x]  - Each pin
            * p[x]_in  - Inside contact for each pin

        If signal names are provided, they will also be added as anchors
        along with _in inside variants.
    '''
    _element_defaults = {
        'pins': 8,
        'notch': True,
        'width': 3.,
        'pinw': 0.6,
        'spacing': 0.5,
        'number': True,
        'fontsize': 12,
        'pfontsize': 10
    }
    def __init__(self, *,
                 pins: Optional[int] = None,
                 names: Optional[Sequence[str]] = None,
                 notch: Optional[bool] = None,
                 width: Optional[float] = None,
                 pinw: Optional[float] = None,
                 spacing: Optional[float] = None,
                 number: Optional[bool] = None,
                 fontsize: Optional[float]= None,
                 pfontsize: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        w: float = self.params['width']
        pw: float = self.params['pinw']
        space: float = self.params['spacing']
        if self.params['pins'] % 2 == 1:
            raise ValueError('pins must be even')

        height = self.params['pins']/2*pw + space*(self.params['pins']/2+1)
        self.segments.append(SegmentPoly(((0, 0), (w, 0), (w, height), (0, height))))

        if self.params['notch']:
            c = w/2
            theta = linspace(-math.pi, 0)
            notchr = pw/2
            notchx = [c + notchr * math.cos(t) for t in theta]
            notchy = [height + notchr * math.sin(t) for t in theta]
            self.segments.append(Segment(list(zip(notchx, notchy))))

        for i in range(self.params['pins']//2):
            y1 = space + space*i+i*pw
            y2 = space + space*i+(i+1)*pw
            ymid = (y1+y2)/2

            # Left
            self.segments.append(SegmentPoly(((0, y1), (0, y2), (-pw, y2), (-pw, y1))))
            pnum = self.params['pins']//2 - i
            self.anchors[f'p{pnum}'] = (-pw, ymid)
            self.anchors[f'p{pnum}_in'] = (0, ymid)
            if self.params['number']:
                self.segments.append(SegmentText((-pw/2, ymid), str(pnum), fontsize=self.params['pfontsize']))
            if names:
                self.segments.append(SegmentText(
                    (.1, ymid), names[pnum-1], align=('left', 'center'), fontsize=self.params['fontsize']))
                self.anchors[names[pnum-1]] = (-pw, ymid)
                self.anchors[f'{names[pnum-1]}_in'] = (0, ymid)

            # Right
            self.segments.append(SegmentPoly(((w, y1), (w, y2), (w+pw, y2), (w+pw, y1))))
            pnum = self.params['pins']//2 + i + 1
            self.anchors[f'p{pnum}'] = (w+pw, ymid)
            self.anchors[f'p{pnum}_in'] = (w, ymid)
            if self.params['number']:
                self.segments.append(SegmentText((w+pw/2, ymid), str(pnum), fontsize=self.params['pfontsize']))
            if names:
                self.segments.append(SegmentText(
                    (w-.1, ymid), names[pnum-1], align=('right', 'center'), fontsize=self.params['fontsize']))
                self.anchors[names[pnum-1]] = (w+pw, ymid)
                self.anchors[f'{names[pnum-1]}_in'] = (w, ymid)


class DFlipFlop(Ic):
    ''' D-Type Flip Flop

        Args:
            preclr: Show preset and clear inputs
            preclrinvert: Add invert bubble to preset and clear inputs

        Keyword Args:
            size: Size of the box [default: (2, 3)]

        Anchors:
            * D
            * CLK
            * Q
            * Qbar
            * PRE
            * CLR
    '''
    _element_defaults = {
        'size': (2, 3)
    }
    def __init__(self, preclr: bool = False, preclrinvert: bool = True, **kwargs):
        pins = [IcPin('D', side='left', slot='2/2'),
                IcPin('>', side='left', slot='1/2'),
                IcPin('Q', side='right', slot='2/2'),
                IcPin(r'$\overline{Q}$', side='right', slot='1/2', anchorname='Qbar')]

        if preclr:
            pins.extend([IcPin('PRE', side='top', invert=preclrinvert),
                         IcPin('CLR', side='bottom', invert=preclrinvert)])
        super().__init__(pins=pins, **kwargs)


class JKFlipFlop(Ic):
    ''' J-K Flip Flop

        Args:
            preclr: Show preset and clear inputs
            preclrinvert: Add invert bubble to preset and clear inputs
            
        Keyword Args:
            size: Size of the box [default: (2, 3)]

        Anchors:
            * J
            * K
            * CLK
            * Q
            * Qbar
            * PRE
            * CLR
    '''
    _element_defaults = {
        'size': (2, 3)
    }
    def __init__(self, preclr: bool = False, preclrinvert: bool = True, **kwargs):
        pins = [IcPin('J', side='left', slot='3/3'),
                IcPin('>', side='left', slot='2/3'),
                IcPin('K', side='left', slot='1/3'),
                IcPin('Q', side='right', slot='3/3'),
                IcPin(r'$\overline{Q}$', side='right', slot='1/3', anchorname='Qbar')]

        if preclr:
            pins.extend([IcPin('PRE', side='top', invert=preclrinvert),
                         IcPin('CLR', side='bottom', invert=preclrinvert)])

        super().__init__(pins=pins, **kwargs)


class VoltageRegulator(Ic):
    ''' Voltage regulator

        Keyword Args:
            size: Size of the box [default: (2, 1.5)]

        Anchors:
            * in
            * out
            * gnd
    '''
    _element_defaults = {
        'size': (2, 1.5)
    }
    def __init__(self, **kwargs):
        pins = [IcPin('in', side='left', slot='3/3'),
                IcPin('out', side='right', slot='3/3'),
                IcPin('gnd', side='bottom')]
        super().__init__(pins=pins, **kwargs)


class Ic555(Ic):
    _element_defaults = {
        'edgepadW': 0.5,
        'edgepadH': 1,
        'pinspacing': 1.5,
        'leadlen': 1
    }
    def __init__(self, **kwargs):
        pins = [IcPin(name='TRG', side='left', pin='2'),
                IcPin(name='THR', side='left', pin='6'),
                IcPin(name='DIS', side='left', pin='7'),
                IcPin(name='CTL', side='right', pin='5'),
                IcPin(name='OUT', side='right', pin='3'),
                IcPin(name='RST', side='top', pin='4'),
                IcPin(name='Vcc', side='top', pin='8'),
                IcPin(name='GND', side='bot', pin='1')]
        super().__init__(pins=pins, label='555')


def sevensegdigit(bottom: float = 0, left: float = 0,
                  seglen: float = 1.5, segw: float = 0.3, spacing: float = 0.12,
                  decimal: bool = False, digit: int | str = 8,
                  segcolor: str = 'red', tilt: float = 10, labelsegments: bool = True) -> list[SegmentType]:
    ''' Generate drawing segments for a 7-segment display digit. Use for
        building new elements incorporating a 7-segment display.

        Args:
            bottom: Location of bottom of digit
            left: Location of left side of digit
            seglen: Length of one segment
            segw: Width of one segment
            spacing: Distance between segments in corners
            decimal: Show decimal point segment
            digit: Number to display
            segcolor: Color of segments
            tilt: Tilt angle in degrees
            labelsegments: Add a-g labels to each segment
            anode: Add common anode pin
            cathode: Add common cathode pin
            size: Total size of the box

        Returns:
            List of Segments making the digit
    '''
    halfw = segw/2  # Half segment width
    marginy = segw/5  # Margin between label and segment
    halfspace = spacing/2
    tilt = math.radians(tilt)

    # Straight (non-tilted) segments - Horizontal
    segDx = [halfspace, halfspace+halfw, seglen-halfspace-halfw,
             seglen-halfspace, seglen-halfspace-halfw, halfspace+halfw]
    segDy = [0, halfw, halfw, 0, -halfw, -halfw]
    segAx = segDx
    segGx = segDx
    segAy = [k + seglen*2 for k in segDy]
    segGy = [k + seglen for k in segDy]
    # - Vertical
    segEx = [0, halfw, halfw, 0, -halfw, -halfw]
    segEy = [halfspace, halfspace+halfw, seglen-halfspace-halfw,
             seglen-halfspace,  seglen-halfspace-halfw, halfspace+halfw]
    segFx = segEx
    segFy = [k + seglen for k in segEy]
    segBx = [k + seglen for k in segEx]
    segBy = segFy
    segCx = segBx
    segCy = segEy

    # Label positions
    segAlabel = (seglen/2 + halfspace, seglen*2+halfw+marginy)
    segGlabel = (seglen/2 + halfspace, seglen+halfw+marginy)
    segDlabel = (seglen/2 + halfspace, halfw+marginy)
    segBlabel = (seglen + halfw + halfspace, seglen*1.5)
    segClabel = (seglen + halfw + halfspace, seglen*.5)
    segElabel = (-halfw - halfspace, seglen*.5)
    segFlabel = (-halfw - halfspace, seglen*1.5)

    # Apply shear
    if tilt != 0:
        lam = math.sin(tilt)
        segAx = [k + lam*i for k, i in zip(segAx, segAy)]
        segBx = [k + lam*i for k, i in zip(segBx, segBy)]
        segCx = [k + lam*i for k, i in zip(segCx, segCy)]
        segDx = [k + lam*i for k, i in zip(segDx, segDy)]
        segEx = [k + lam*i for k, i in zip(segEx, segEy)]
        segFx = [k + lam*i for k, i in zip(segFx, segFy)]
        segGx = [k + lam*i for k, i in zip(segGx, segGy)]
        def shiftlabel(label):
            return label[0] + label[1]*lam, label[1]
        segAlabel = shiftlabel(segAlabel)
        segGlabel = shiftlabel(segGlabel)
        segDlabel = shiftlabel(segDlabel)
        segBlabel = shiftlabel(segBlabel)
        segClabel = shiftlabel(segClabel)
        segElabel = shiftlabel(segElabel)
        segFlabel = shiftlabel(segFlabel)
        left -= lam*seglen

    # Translate to final position
    segDx = [k + left for k in segDx]
    segDy = [k + bottom for k in segDy]
    segGx = [k + left for k in segGx]
    segGy = [k + bottom for k in segGy]
    segAx = [k + left for k in segAx]
    segAy = [k + bottom for k in segAy]
    segEx = [k + left for k in segEx]
    segEy = [k + bottom for k in segEy]
    segFx = [k + left for k in segFx]
    segFy = [k + bottom for k in segFy]
    segBx = [k + left for k in segBx]
    segBy = [k + bottom for k in segBy]
    segCx = [k + left for k in segCx]
    segCy = [k + bottom for k in segCy]
    segAlabel = (segAlabel[0] + left, segAlabel[1] + bottom)
    segGlabel = (segGlabel[0] + left, segGlabel[1] + bottom)
    segDlabel = (segDlabel[0] + left, segDlabel[1] + bottom)
    segBlabel = (segBlabel[0] + left, segBlabel[1] + bottom)
    segClabel = (segClabel[0] + left, segClabel[1] + bottom)
    segElabel = (segElabel[0] + left, segElabel[1] + bottom)
    segFlabel = (segFlabel[0] + left, segFlabel[1] + bottom)

    # Fill based on digit parameter
    fillA = segcolor if str(digit).lower() in ['2', '3', '5', '6', '7', '8', '9', '0', 'a', 'c', 'e', 'f'] else None
    fillB = segcolor if str(digit).lower() in ['1', '2', '3', '4', '7', '8', '9', '0', 'a', 'd'] else None
    fillC = segcolor if str(digit).lower() in ['1', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'd'] else None
    fillD = segcolor if str(digit).lower() in ['2', '3', '5', '6', '8', '9', '0', 'b', 'c', 'd', 'e'] else None
    fillE = segcolor if str(digit).lower() in ['2', '6', '8', '0', 'a', 'b', 'c', 'd', 'e', 'f'] else None
    fillF = segcolor if str(digit).lower() in ['4', '5', '6', '8', '9', '0', 'a', 'b', 'c', 'e', 'f'] else None
    fillG = segcolor if str(digit).lower() in ['2', '3', '4', '5', '6', '8', '9', 'a', 'b', 'd', 'e', 'f'] else None

    segments: list[SegmentType] = []
    segments.append(SegmentPoly(list(zip(segAx, segAy)), color='gray', fill=fillA, lw=.5))
    segments.append(SegmentPoly(list(zip(segBx, segBy)), color='gray', fill=fillB, lw=.5))
    segments.append(SegmentPoly(list(zip(segCx, segCy)), color='gray', fill=fillC, lw=.5))
    segments.append(SegmentPoly(list(zip(segDx, segDy)), color='gray', fill=fillD, lw=.5))
    segments.append(SegmentPoly(list(zip(segEx, segEy)), color='gray', fill=fillE, lw=.5))
    segments.append(SegmentPoly(list(zip(segFx, segFy)), color='gray', fill=fillF, lw=.5))
    segments.append(SegmentPoly(list(zip(segGx, segGy)), color='gray', fill=fillG, lw=.5))
    if labelsegments:
        segments.append(SegmentText(segAlabel, 'a', align=('center', 'bottom'), fontsize=10))
        segments.append(SegmentText(segGlabel, 'g', align=('center', 'bottom'), fontsize=10))
        segments.append(SegmentText(segDlabel, 'd', align=('center', 'bottom'), fontsize=10))
        segments.append(SegmentText(segBlabel, 'b', align=('left', 'center'), fontsize=10))
        segments.append(SegmentText(segClabel, 'c', align=('left', 'center'), fontsize=10))
        segments.append(SegmentText(segElabel, 'e', align=('right', 'center'), fontsize=10))
        segments.append(SegmentText(segFlabel, 'f', align=('right', 'center'), fontsize=10))

    if decimal:
        dotrad = .15
        segments.append(SegmentCircle((left+seglen+segw+dotrad/2, bottom),
                                      radius=dotrad, color='gray', fill=segcolor, lw=.5))
    return segments


class SevenSegment(Ic):
    ''' A seven-segment display digit.

        Keyword Args:
            decimal: Show decimal point segment [default: False]
            digit: Number to display [default: 8]
            segcolor: Color of segments [default: red]
            tilt: Tilt angle in degrees [default: 10]
            labelsegments: Add a-g labels to each segment [default: True]
            anode: Add common anode pin [default: False]
            cathode: Add common cathode pin [default: False]

        Anchors:
            * a
            * b
            * c
            * d
            * e
            * f
            * g
            * dp
            * cathode
            * anode
    '''
    _element_defaults = {
        'decimal': False,
        'digit': 8,
        'segcolor': 'red',
        'tilt': 10,
        'labelsegments': True,
        'anode': False,
        'cathode': False,
        'pinspacing': 0.6
    }
    def __init__(self, *,
                 decimal: Optional[bool] = None,
                 digit: Optional[int | str] = None,
                 segcolor: Optional[str] = None,
                 tilt: Optional[float] = None,
                 labelsegments: Optional[bool] = None,
                 anode: Optional[bool] = None,
                 cathode: Optional[bool] = None,
                 **kwargs) -> None:

        dec = self.params['decimal']
        boxwidth = 3
        if dec:
            slots = '8'
            boxheight = 5.9
        else:
            slots = '7'
            boxheight = 5.3
        size = self.params.get('size', (boxwidth, boxheight))

        pins = [IcPin(pin='a', side='left', slot=f'{7+dec}/{slots}', anchorname='a'),
                IcPin(pin='b', side='left', slot=f'{6+dec}/{slots}', anchorname='b'),
                IcPin(pin='c', side='left', slot=f'{5+dec}/{slots}', anchorname='c'),
                IcPin(pin='d', side='left', slot=f'{4+dec}/{slots}', anchorname='d'),
                IcPin(pin='e', side='left', slot=f'{3+dec}/{slots}', anchorname='e'),
                IcPin(pin='f', side='left', slot=f'{2+dec}/{slots}', anchorname='f'),
                IcPin(pin='g', side='left', slot=f'{1+dec}/{slots}', anchorname='g')]
        if dec:
            pins.append(IcPin(pin='dp', side='left', slot=f'1/{slots}', anchorname='dp'))
        if self.params['anode']:
            pins.append(IcPin(pin='ca', side='top', anchorname='anode'))
        if self.params['cathode']:
            pins.append(IcPin(pin='cc', side='bottom', anchorname='cathode'))

        super().__init__(pins=pins, size=size)

        left = 0.8
        seglen = 1.5
        bot = (boxheight-seglen*2)/2

        segments = sevensegdigit(left=left, bottom=bot,
                                 decimal=dec,
                                 digit=self.params['digit'],
                                 segcolor=self.params['segcolor'],
                                 tilt=self.params['tilt'],
                                 labelsegments=self.params['labelsegments'])
        self.segments.extend(segments)
