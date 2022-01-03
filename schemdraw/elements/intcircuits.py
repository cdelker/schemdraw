''' Integrated Circuit Element '''

from __future__ import annotations

import sys
from typing import Optional, Sequence, cast
import math
from dataclasses import dataclass
from copy import copy

from ..segments import Segment, SegmentText, SegmentCircle, SegmentPoly, SegmentType
from ..elements import Element
from ..util import linspace, Point
from ..types import XY, Align, Side


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
            * inL[X] - Each pin on left side
            * inR[X] - Each pin on right side
            * inT[X] - Each pin on top side
            * inB[X] - Each pin on bottom side
            * pin[X] - Each pin with a number
            * CLK (if clock pin is defined with '>' name)

        Pins with names are also defined as anchors (if the name
        does not conflict with other attributes).
    '''
    def __init__(self,
                 size: XY=None,
                 pins: list[IcPin]=None,
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
        paths: list[list[Point]]
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
                        clkw = math.copysign(clkw, leadext[1]) if leadext[1] != 0 else clkw
                        clkpath = [Point((clkxy[0]-clkh, clkxy[1])),
                                   Point((clkxy[0], clkxy[1]-clkw)),
                                   Point((clkxy[0]+clkh, clkxy[1]))]
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
        self.anchors['center'] = (w/2, h/2)


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
                 size: XY=None,
                 pins: list[IcPin]=None,
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


class IcDIP(Element):
    ''' Dual-inline Package Integrated Circuit.

        Args:
            pins: number of pins
            names: List of names for each pin to display inside the box
            notch: Show the notch at top of box
            width: Width of the box
            pinw: Width and height of each pin
            spacing: Distance between each pin
            number: Show pin numbers inside each pin
            fontsize: Size for pin name labels
            pfontsize: Size for pin number labels

        Anchors:
            * p[x]  - Each pin
            * p[x]_in  - Inside contact for each pin

        If signal names are provided, they will also be added as anchors
        along with _in inside variants.
    '''
    def __init__(self, *d, pins: int=8, 
                 names: Sequence[str]=None,
                 notch: bool=True,
                 width: float=3,
                 pinw: float=0.6,
                 spacing: float=0.5,
                 number: bool=True,
                 fontsize: float=12,
                 pfontsize: float=10,         
                 **kwargs):
        super().__init__(*d, **kwargs)
        if pins % 2 == 1:
            raise ValueError('pins must be even')

        height = pins/2*pinw + spacing*(pins/2+1)    
        self.segments.append(SegmentPoly(((0, 0), (width, 0), (width, height), (0, height))))
        
        if notch:
            c = width/2
            theta = linspace(-math.pi, 0)
            notchr = pinw/2
            notchx = [c + notchr * math.cos(t) for t in theta]
            notchy = [height + notchr * math.sin(t) for t in theta]
            self.segments.append(Segment(list(zip(notchx, notchy))))
        
        for i in range(pins//2):
            y1 = spacing + spacing*i+i*pinw
            y2 = spacing + spacing*i+(i+1)*pinw
            ymid = (y1+y2)/2

            # Left
            self.segments.append(SegmentPoly(((0, y1), (0, y2), (-pinw, y2), (-pinw, y1))))
            pnum = pins//2 - i
            self.anchors[f'p{pnum}'] = (-pinw, ymid)
            self.anchors[f'p{pnum}_in'] = (0, ymid)
            if number:
                self.segments.append(SegmentText((-pinw/2, ymid), str(pnum), fontsize=pfontsize))
            if names:
                self.segments.append(SegmentText((.1, ymid), names[pnum-1], align=('left', 'center'), fontsize=fontsize))
                self.anchors[names[pnum-1]] = (-pinw, ymid)
                self.anchors[f'{names[pnum-1]}_in'] = (0, ymid)
                
            # Right
            self.segments.append(SegmentPoly(((width, y1), (width, y2), (width+pinw, y2), (width+pinw, y1))))
            pnum = pins//2 + i + 1
            self.anchors[f'p{pnum}'] = (width+pinw, ymid)
            self.anchors[f'p{pnum}_in'] = (width, ymid)
            if number:
                self.segments.append(SegmentText((width+pinw/2, ymid), str(pnum), fontsize=pfontsize))
            if names:
                self.segments.append(SegmentText((width-.1, ymid), names[pnum-1], align=('right', 'center'), fontsize=fontsize))
                self.anchors[names[pnum-1]] = (width+pinw, ymid)
                self.anchors[f'{names[pnum-1]}_in'] = (width, ymid)


class DFlipFlop(Ic):
    ''' D-Type Flip Flop

        Args:
            preclr: Show preset and clear inputs
            preclrinvert: Add invert bubble to preset and clear inputs
            size: Size of the box

        Anchors:
            * D
            * CLK
            * Q
            * Qbar
            * PRE
            * CLR
    '''
    def __init__(self, *d, preclr: bool=False, preclrinvert: bool=True, size=(2, 3), **kwargs):
        pins=[IcPin('D', side='left', slot='2/2'),
              IcPin('>', side='left', slot='1/2'),
              IcPin('Q', side='right', slot='2/2'),
              IcPin('$\overline{Q}$', side='right', slot='1/2', anchorname='Qbar')]

        if preclr:
            pins.extend([IcPin('PRE', side='top', invert=preclrinvert),
                         IcPin('CLR', side='bottom', invert=preclrinvert)])

        super().__init__(pins=pins, size=size)
        

class JKFlipFlop(Ic):
    ''' J-K Flip Flop

        Args:
            preclr: Show preset and clear inputs
            preclrinvert: Add invert bubble to preset and clear inputs
            size: Size of the box

        Anchors:
            * J
            * K
            * CLK
            * Q
            * Qbar
            * PRE
            * CLR
    '''
    def __init__(self, *d, preclr: bool=False, preclrinvert: bool=True, size=(2, 3), **kwargs):
        pins=[IcPin('J', side='left', slot='3/3'),
              IcPin('>', side='left', slot='2/3'),
              IcPin('K', side='left', slot='1/3'),
              IcPin('Q', side='right', slot='3/3'),
              IcPin('$\overline{Q}$', side='right', slot='1/3', anchorname='Qbar')]

        if preclr:
            pins.extend([IcPin('PRE', side='top', invert=preclrinvert),
                         IcPin('CLR', side='bottom', invert=preclrinvert)])

        super().__init__(pins=pins, size=size)


class VoltageRegulator(Ic):
    ''' Voltage regulator

        Args:
            size: Size of the box

        Anchors:
            * in
            * out
            * gnd
    '''
    def __init__(self, *d, size=(2, 1.5), **kwargs):
        pins=[IcPin('in', side='left', slot='3/3'),
              IcPin('out', side='right', slot='3/3'),
              IcPin('gnd', side='bottom')]
        super().__init__(pins=pins, size=size)


class Ic555(Ic):
    def __init__(self, *d, **kwargs):
        pins=[IcPin(name='TRG', side='left', pin='2'),
              IcPin(name='THR', side='left', pin='6'),
              IcPin(name='DIS', side='left', pin='7'),
              IcPin(name='CTL', side='right', pin='5'),
              IcPin(name='OUT', side='right', pin='3'),
              IcPin(name='RST', side='top', pin='4'),
              IcPin(name='Vcc', side='top', pin='8'),
              IcPin(name='GND', side='bot', pin='1')]
        super().__init__(pins=pins,
                         edgepadW=.5,
                         edgepadH=1,
                         pinspacing=1.5,
                         leadlen=1,
                         label='555')
        
        
def sevensegdigit(bottom: float=0, left: float=0,
                  seglen: float=1.5, segw: float=0.3, spacing: float=0.12,                  
                  decimal: bool=False, digit: int | str=8, 
                  segcolor: str='red', tilt: float=10, labelsegments: bool=True) -> list[SegmentType]:
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
    halfw = segw/2 # Half segment width
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
    segAlabel = (seglen/2 + halfspace, seglen*2+halfw)
    segGlabel = (seglen/2 + halfspace, seglen+halfw)
    segDlabel = (seglen/2 + halfspace, halfw)
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

        Args:
            decimal: Show decimal point segment
            digit: Number to display
            segcolor: Color of segments
            tilt: Tilt angle in degrees
            labelsegments: Add a-g labels to each segment
            anode: Add common anode pin
            cathode: Add common cathode pin
            size: Total size of the box

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
    def __init__(self, *d, decimal: bool=False,
                 digit: int | str=8, 
                 segcolor: str='red',
                 tilt: float=10,
                 labelsegments: bool=True,
                 anode: bool=False,
                 cathode: bool=False,
                 size=(2, 1.5), **kwargs):
        
        if decimal:
            slots = '8'
            boxheight = 5.9
        else:
            slots = '7'
            boxheight = 5.3
        
        pins=[IcPin(pin='a', side='left', slot=f'{7+decimal}/{slots}', anchorname='a'),
              IcPin(pin='b', side='left', slot=f'{6+decimal}/{slots}', anchorname='b'),
              IcPin(pin='c', side='left', slot=f'{5+decimal}/{slots}', anchorname='c'),
              IcPin(pin='d', side='left', slot=f'{4+decimal}/{slots}', anchorname='d'),
              IcPin(pin='e', side='left', slot=f'{3+decimal}/{slots}', anchorname='e'),
              IcPin(pin='f', side='left', slot=f'{2+decimal}/{slots}', anchorname='f'),
              IcPin(pin='g', side='left', slot=f'{1+decimal}/{slots}', anchorname='g')]
        if decimal:
            pins.append(IcPin(pin='dp', side='left', slot=f'1/{slots}', anchorname='dp'))
        if anode:
            pins.append(IcPin(pin='ca', side='top', anchorname='anode'))
        if cathode:
            pins.append(IcPin(pin='cc', side='bottom', anchorname='cathode'))

        super().__init__(pins=pins, w=3)

        left = 0.8
        seglen = 1.5
        bot = (boxheight-seglen*2)/2
        
        segments = sevensegdigit(left=0.8, bottom=bot, decimal=decimal, digit=digit,
                                 segcolor=segcolor, tilt=tilt, labelsegments=labelsegments)
        self.segments.extend(segments)