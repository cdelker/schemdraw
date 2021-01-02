''' Integrated Circuit Element '''

import math
from dataclasses import dataclass
from copy import copy
from typing import List, Optional, Literal, cast

from ..segments import Segment, SegmentText, SegmentCircle
from ..elements import Element
from ..util import linspace, Point
from ..types import XY, Align


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
    name: Optional[str] = None
    pin: Optional[str] = None
    side: Literal['left', 'right', 'top', 'bottom', 'L', 'R', 'T', 'B'] = 'L'
    pos: Optional[float] = None
    slot: Optional[str] = None
    invert: bool = False
    invertradius: float = 0.15
    color: Optional[str] = None
    rotation: float = 0
    anchorname: Optional[str] = None
    lblsize: Optional[float] = None


class Ic(Element):
    ''' Integrated Circuit element, or any other black-box element
        with arbitrary pins on any side.

        Args:
            size: (Width, Height) of box
            pins: List of IcPin instances defining the inputs/outputs
            pinspacing: Spacing between pins
            edgepadH: Padding between top/bottom and first pin
            edgepadW: Padding between left/right and first pin
            lofst: Offset between edge and label (inside box)
            lsize: Font size of labels (inside box)
            plblofst: Offset between edge and pin label (outside box)
            plblsize: Font size of pin labels (outside box)
            slant: Slant angle of top/bottom edges (e.g. for multiplexers)

        If a pin is named '>', it will be drawn as a proper clock signal input.

        Anchors:
            inL[X] - Each pin on left side
            inR[X] - Each pin on right side
            inT[X] - Each pin on top side
            inB[X] - Each pin on bottom side
            pinX - Each pin with a number
            CLK (if clock pin is defined with '>' name)

        Pins with names are also defined as anchors (if the name
        does not conflict with other attributes).
    '''
    def __init__(self,
                 size: XY=None,
                 pins: List[IcPin]=None,
                 pinspacing: float = 0.6,
                 edgepadH: float = 0.25,
                 edgepadW: float = 0.25,
                 leadlen: float = 0.5,
                 lofst: float = 0.15,
                 lsize: float = 14,
                 plblofst: float = 0.05,
                 plblsize: float = 11,
                 slant: float = 0,
                 w: float=None,
                 h: float=None,
                 **kwargs):
        super().__init__(**kwargs)

        # Sort pins by side
        if pins is None:
            pins = []
        pins = [copy(p) for p in pins]  # Make copy so user's IcPin instances don't change
        for pin in pins:
            # Convert pin designations to uppercase, single letter
            pin.side = pin.side[:1].upper()   # type: ignore
        sidepins = {}
        pincount = {}

        for side in ['L', 'R', 'T', 'B']:
            sidepins[side] = [p for p in pins if p.side == side]
            slotnames = [p.slot for p in sidepins[side]]
            # Add a 0 - can't max an empty list
            slots = [int(p.split('/')[1]) for p in slotnames if p is not None] + [0]
            pincount[side] = max(len(sidepins[side]), max(slots))

        if size is None:
            hcnt = max(pincount.get('L', 1), pincount.get('R', 1))
            wcnt = max(pincount.get('T', 1), pincount.get('B', 1))
            if h is None:
                try:
                    h = (hcnt-1)*pinspacing/(1-2/(hcnt+2)) + edgepadH*2
                except ZeroDivisionError:
                    h = 2 + edgepadH
            if w is None:
                try:
                    w = (wcnt-1)*pinspacing/(1-2/(wcnt+2)) + edgepadW*2
                except ZeroDivisionError:
                    w = 2 + edgepadW

            w = max(w, 2)  # Keep a minimum width for cases with 0-1 pins
            h = max(h, 2)
        else:
            w, h = size

        # Main box, adjusted for slant
        paths: List[List[Point]]
        if slant > 0:
            y1 = 0 - w * math.tan(math.radians(slant))
            y2 = h + w * math.tan(math.radians(slant))
            paths = [[Point((0, 0)), Point((w, y1)), Point((w, y2)), Point((0, h)), Point((0, 0))]]
        elif slant < 0:
            y1 = 0 + w * math.tan(math.radians(slant))
            y2 = h - w * math.tan(math.radians(slant))
            paths = [[Point((0, y1)), Point((w, 0)), Point((w, h)), Point((0, y2)), Point((0, y1))]]
        else:
            y1 = 0
            y2 = h
            paths = [[Point((0, 0)), Point((w, 0)), Point((w, h)), Point((0, h)), Point((0, 0))]]

        # Add each pin
        for side in sidepins.keys():
            if side in ['L', 'R']:
                sidelen = h-edgepadH*2
            else:
                sidelen = w-edgepadW*2

            leadext = {'L': Point((-leadlen, 0)),
                       'R': Point((leadlen, 0)),
                       'T': Point((0, leadlen)),
                       'B': Point((0, -leadlen))}.get(side, Point((0,0)))

            for i, pin in enumerate(sidepins[side]):
                # Determine pin position
                if pin.pos is not None:
                    z = pin.pos * sidelen
                elif pin.slot is None:
                    pin.slot = '{}/{}'.format(i+1, len(sidepins[side]))

                if pin.slot is not None:
                    num, tot = [int(k) for k in pin.slot.split('/')]
                    if tot == 1:
                        z = sidelen/2  # Single pin, center it
                    else:
                        # Evenly spaced along side
                        z = linspace(1/(tot+2), 1-1/(tot+2), num=tot)[num-1] * sidelen

                pinxy = {'L': Point((0, z+edgepadH)),
                         'R': Point((w, z+edgepadH)),
                         'T': Point((z+edgepadW, h)),
                         'B': Point((z+edgepadW, 0))}.get(side, Point((0,0)))

                # Adjust pin position for slant
                if side == 'T' and slant > 0:
                    pinxy = Point((pinxy[0], pinxy[1] - pinxy[0] * math.tan(-math.radians(slant))))
                elif side == 'T' and slant < 0:
                    pinxy = Point(((pinxy[0], pinxy[1] + (y2-h) - pinxy[0] * math.tan(-math.radians(slant)))))
                elif side == 'B' and slant < 0:
                    pinxy = Point((pinxy[0], pinxy[1] - (y2-h) - pinxy[0] * math.tan(math.radians(slant))))
                elif side == 'B' and slant > 0:
                    pinxy = Point((pinxy[0], pinxy[1] - pinxy[0] * math.tan(math.radians(slant))))

                if pin.name == '>':
                    # Draw clock pin
                    clkxy = pinxy
                    clkw, clkh = 0.4 * lsize/16, 0.2 * lsize/16
                    if side in ['T', 'B']:
                        clkh = math.copysign(clkh, leadext[1]) if leadext[1] != 0 else clkh
                        clkpath = [Point((clkxy[0]-clkw, clkxy[1])),
                                   Point((clkxy[0], clkxy[1]-clkh)),
                                   Point((clkxy[0]+clkw, clkxy[1]))]
                    else:
                        clkw = math.copysign(clkw, -leadext[0]) if leadext[0] != 0 else clkw
                        clkpath = [Point((clkxy[0], clkxy[1]+clkh)),
                                   Point((clkxy[0]+clkw, clkxy[1])),
                                   Point((clkxy[0], clkxy[1]-clkh))]
                    paths.append(clkpath)

                elif pin.name and pin.name != '':
                    # Add pin label
                    pofst = {'L': Point((lofst, 0)),
                             'R': Point((-lofst, 0)),
                             'T': Point((0, -lofst)),
                             'B': Point((0, lofst))}.get(side)

                    align = cast(Optional[Align], {'L': ('left', 'center'),
                             'R': ('right', 'center'),
                             'T': ('center', 'top'),
                             'B': ('center', 'bottom')}.get(side))

                    self.segments.append(SegmentText(pos=pinxy+pofst,
                                         label=pin.name,
                                         align=align,
                                         fontsize=pin.lblsize if pin.lblsize is not None else plblsize,
                                         color=pin.color,
                                         rotation=pin.rotation,
                                         rotation_mode='default')
                                        )

                # Add pin number outside the IC
                if pin.pin and pin.pin != '':
                    # Account for any invert-bubbles
                    invertradius = pin.invertradius * pin.invert
                    pofst = {'L': Point((-plblofst-invertradius*2, plblofst)),
                             'R': Point((plblofst+invertradius*2, plblofst)),
                             'T': Point((plblofst, plblofst+invertradius*2)),
                             'B': Point((plblofst, -plblofst-invertradius*2))
                             }.get(side)

                    align = cast(Optional[Align], {'L': ('right', 'bottom'),
                                                   'R': ('left', 'bottom'),
                                                   'T': ('left', 'bottom'),
                                                   'B': ('left', 'top')}.get(side))
                    self.segments.append(SegmentText(pos=pinxy+pofst,
                                                     label=pin.pin,
                                                     align=align,
                                                     fontsize=pin.lblsize if pin.lblsize is not None else plblsize
                                                    ))

                # Draw leads
                if leadlen > 0:
                    if pin.invert:
                        # Add invert-bubble
                        invertradius = pin.invertradius
                        invertofst = {'L': Point((-invertradius, 0)),
                                      'R': Point((invertradius, 0)),
                                      'T': Point((0, invertradius)),
                                      'B': Point((0, -invertradius))}.get(side, Point((0,0)))

                        self.segments.append(SegmentCircle(
                            pinxy+invertofst, invertradius))
                        paths.append([pinxy+invertofst*2, pinxy+leadext])
                    else:
                        paths.append([pinxy, pinxy+leadext])

                # Define anchors
                anchorpos = pinxy+leadext
                self.anchors['in{}{}'.format(side[0].upper(), i+1)] = anchorpos
                if pin.anchorname:
                    self.anchors[pin.anchorname] = anchorpos
                elif pin.name:
                    if pin.name == '>':
                        self.anchors['CLK'] = anchorpos
                    self.anchors[pin.name] = anchorpos
                if pin.pin:
                    self.anchors['pin{}'.format(pin.pin)] = anchorpos

        for p in paths:
            self.segments.append(Segment(p))
        self.params['lblloc'] = 'center'


class Multiplexer(Ic):
    ''' Multiplexer

        Args:
            demux: Draw as demultiplexer
            size: (Width, Height) of box
            pins: List of IcPin instances defining the inputs/outputs
            pinspacing: Spacing between pins
            edgepadH: Padding between top/bottom and first pin
            edgepadW: Padding between left/right and first pin
            lofst: Offset between edge and label (inside box)
            lsize: Font size of labels (inside box)
            plblofst: Offset between edge and pin label (outside box)
            plblsize: Font size of pin labels (outside box)
            slant: Slant angle of top/bottom edges

        If a pin is named '>', it will be drawn as a proper clock signal input.

        Anchors:
            inL[X] - Each pin on left side
            inR[X] - Each pin on right side
            inT[X] - Each pin on top side
            inB[X] - Each pin on bottom side
            pinX - Each pin with a number
            CLK (if clock pin is defined with '>' name)

        Pins with names are also defined as anchors (if the name does
        not conflict with other attributes).
    '''
    def __init__(self,
                 demux: bool = False,
                 size: XY=None,
                 pins: List[IcPin]=None,
                 pinspacing: float = 0.6,
                 edgepadH: float = 0.25,
                 edgepadW: float = 0.25,
                 leadlen: float = 0.5,
                 lofst: float = 0.15,
                 lsize: float = 14,
                 plblofst: float = 0.05,
                 plblsize: float = 11,
                 slant: float = 25,
                 **kwargs):
        slant = -slant if not demux else slant
        super().__init__(size=size,
                         pins=pins,
                         pinspacing=pinspacing,
                         edgepadH=edgepadH,
                         edgepadW=edgepadW,
                         leadlen=leadlen,
                         lofst=lofst,
                         lsize=lsize,
                         plblofst=plblofst,
                         plblsize=plblsize,
                         slant=slant,
                         **kwargs)
