''' Integrated Circuit Element '''

import numpy as np

from ..segments import Segment, SegmentText, SegmentCircle
from ..elements import Element
from .lines import Line
from ..adddocs import adddocs


class IcPin(dict):
    ''' Integrated Circuit Pin

        Keyword Arguments
        -----------------
        name : string
            Input/output name (inside the box)
        pin : string
            Pin name/number (outside the box)
        side : string
            Side of box for the pin, 'left', 'right', 'top', 'bottom'
        pos : float
            Pin position along the side, fraction from 0-1
        slot : string
            Slot definition of pin location, given in 'X/Y' format.
            '2/4' is the second pin on a side with 4 pins.
        invert : bool
            Add an invert bubble to the pin
        invertradius : float
            Radius of invert bubble
        color : string or RGB tuple
            Color for the pin and label
        rotation : float
            Rotation for label text
        anchorname : string
            Named anchor for the pin
     '''


@adddocs(Element)
class Ic(Element):
    ''' Integrated Circuit element

        Parameters
        ----------
        size: tuple
            (Width, Height) of box
        pins : list
            List of IcPin instances defining the inputs/outputs
        pinspacing : float
            Spacing between pins [1.25]
        edgepadH : float
            Padding between top/bottom and first pin [.25]
        edgepadW : float
            Padding between left/right and first pin [.25]
        lofst : float
            Offset between edge and label (inside box) [.15]
        lsize : float
            Font size of labels (inside box) [14]
        plblofst : float
            Offset between edge and pin label (outside box) [.05]
        plblsize : float
            Font size of pin labels (outside box) [11]
        slant : float
            Slant angle of top/bottom edges (e.g. for multiplexers) [0]
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pins = kwargs.get('pins', [])  # List of IcPin objects
        pinspacing = kwargs.get('pinspacing', 0.6)
        edgepadH = kwargs.get('edgepadH', .25)
        edgepadW = kwargs.get('edgepadW', .25)
        lblofst = kwargs.get('lofst', .15)   # lblofst would conflict with main IC label
        lblsize = kwargs.get('lsize', 14)
        leadlen = kwargs.get('leadlen', 0.5)
        plblofst = kwargs.get('plblofst', .05)
        plblsize = kwargs.get('plblsize', 11)
        slant = kwargs.get('slant', 0)

        # Sort pins by side
        pins = [p.copy() for p in pins]  # Make copy so user's dicts don't change
        for pin in pins:
            # Convert pin designations to uppercase, single letter            
            pin['side'] = pin.get('side', 'L')[:1].upper()
        sidepins = {}
        pincount = {}

        for side in ['L', 'R', 'T', 'B']:
            sidepins[side] = [p for p in pins if p['side'] == side]
            slots = [p.get('slot', None) for p in sidepins[side]]
            # Add a 0 - can't max an empty list            
            slots = [int(p.split('/')[1]) for p in slots if p is not None] + [0]
            pincount[side] = max(len(sidepins[side]), max(slots))

        if 'size' not in kwargs:
            hcnt = max(pincount.get('L', 1), pincount.get('R', 1))
            wcnt = max(pincount.get('T', 1), pincount.get('B', 1))
            try:
                h = (hcnt-1)*pinspacing/(1-2/(hcnt+2)) + edgepadH*2
            except ZeroDivisionError:
                h = 2 + edgepadH
            try:
                w = (wcnt-1)*pinspacing/(1-2/(wcnt+2)) + edgepadW*2
            except ZeroDivisionError:
                w = 2 + edgepadW

            w = max(w, 2)  # Keep a minimum width for cases with 0-1 pins
            h = max(h, 2)
            w = kwargs.get('w', w)
            h = kwargs.get('h', h)
        else:
            w, h = kwargs.get('size')

        # Main box, adjusted for slant
        if slant > 0:
            y1 = 0 - w * np.tan(np.deg2rad(slant))
            y2 = h + w * np.tan(np.deg2rad(slant))
            paths = [[[0, 0], [w, y1], [w, y2], [0, h], [0, 0]]]
        elif slant < 0:
            y1 = 0 + w * np.tan(np.deg2rad(slant))
            y2 = h - w * np.tan(np.deg2rad(slant))
            paths = [[[0, y1], [w, 0], [w, h], [0, y2], [0, y1]]]
        else:
            y1 = 0
            y2 = h
            paths = [[[0, 0], [w, 0], [w, h], [0, h], [0, 0]]]

        # Add each pin
        for side in sidepins.keys():
            if side in ['L', 'R']:
                sidelen = h-edgepadH*2
            else:
                sidelen = w-edgepadW*2

            leadext = {'L': np.array([-leadlen, 0]),
                       'R': np.array([leadlen, 0]),
                       'T': np.array([0, leadlen]),
                       'B': np.array([0, -leadlen])}.get(side)

            for i, pin in enumerate(sidepins[side]):
                # Determine pin position
                if 'pos' in pin:
                    z = pin['pos'] * sidelen
                elif 'slot' not in pin:
                    pin['slot'] = '{}/{}'.format(i+1, len(sidepins[side]))

                if 'slot' in pin:
                    num, tot = pin['slot'].split('/')
                    num = int(num)
                    tot = int(tot)
                    if tot == 1:
                        z = sidelen/2  # Single pin, center it
                    else:
                        # Evenly spaced along side
                        z = np.linspace(1/(tot+2), 1-1/(tot+2), num=tot)[num-1] * sidelen

                pin['pos'] = np.asarray({'L': [0, z+edgepadH],
                                         'R': [w, z+edgepadH],
                                         'T': [z+edgepadW, h],
                                         'B': [z+edgepadW, 0]}.get(side))

                # Adjust pin position for slant
                if side == 'T' and slant > 0:
                    pin['pos'] = [pin['pos'][0], pin['pos'][1] - pin['pos'][0] * np.tan(-np.deg2rad(slant))]
                elif side == 'T' and slant < 0:
                    pin['pos'] = [pin['pos'][0], pin['pos'][1] + (y2-h) - pin['pos'][0] * np.tan(-np.deg2rad(slant))]
                elif side == 'B' and slant < 0:
                    pin['pos'] = [pin['pos'][0], pin['pos'][1] - (y2-h) - pin['pos'][0] * np.tan(np.deg2rad(slant))]
                elif side == 'B' and slant > 0:
                    pin['pos'] = [pin['pos'][0], pin['pos'][1] - pin['pos'][0] * np.tan(np.deg2rad(slant))]

                if pin.get('name', '') == '>':
                    # Draw clock pin
                    clkxy = np.array(pin['pos'])
                    clkw, clkh = 0.4 * lblsize/16, 0.2 * lblsize/16
                    if side in ['T', 'B']:
                        clkh = clkh * np.sign(leadext[1]) if leadext[1] != 0 else clkh
                        clkpath = [[clkxy[0]-clkw, clkxy[1]],
                                   [clkxy[0], clkxy[1]-clkh],
                                   [clkxy[0]+clkw, clkxy[1]]]
                    else:
                        clkw = clkw * -np.sign(leadext[0]) if leadext[0] != 0 else clkw
                        clkpath = [[clkxy[0], clkxy[1]+clkh],
                                   [clkxy[0]+clkw, clkxy[1]],
                                   [clkxy[0], clkxy[1]-clkh]]
                    paths.append(clkpath)

                elif pin.get('name', '') != '':
                    # Add pin label
                    pofst = np.asarray({'L': [lblofst, 0],
                                        'R': [-lblofst, 0],
                                        'T': [0, -lblofst],
                                        'B': [0, lblofst]}.get(side))

                    align = {'L': ('left', 'center'),
                             'R': ('right', 'center'),
                             'T': ('center', 'top'),
                             'B': ('center', 'bottom')}.get(side)

                    label = {'label': pin['name'],
                             'pos': pin['pos'] + pofst,
                             'align': align,
                             'size': pin.get('size', lblsize)}
                    if 'color' in pin:
                        label['color'] = pin['color']

                    if 'rotation' in pin:
                        label['rotation'] = pin['rotation']
                        label['rotation_mode'] = 'default'

                    self.segments.append(SegmentText(**label))

                # Add pin number outside the IC
                if pin.get('pin', '') != '':
                    # Account for any invert-bubbles
                    invertradius = pin.get('invertradius', .15) * pin.get('invert', 0)
                    pofst = np.asarray({'L': [-plblofst-invertradius*2, plblofst],
                                        'R': [plblofst+invertradius*2, plblofst],
                                        'T': [plblofst, plblofst+invertradius*2],
                                        'B': [plblofst, -plblofst-invertradius*2]
                                        }.get(side))

                    align = {'L': ('right', 'bottom'),
                             'R': ('left', 'bottom'),
                             'T': ('left', 'bottom'),
                             'B': ('left', 'top')}.get(side)
                    label = {'label': pin['pin'],
                             'pos': pin['pos'] + pofst,
                             'align': align,
                             'fontsize': pin.get('psize', plblsize)}
                    self.segments.append(SegmentText(**label))

                # Draw leads 
                if leadlen > 0:
                    if pin.get('invert', False):
                        # Add invert-bubble
                        invertradius = pin.get('invertradius', .15)
                        invertofst = {'L': np.array([-invertradius, 0]),
                                      'R': np.array([invertradius, 0]),
                                      'T': np.array([0, invertradius]),
                                      'B': np.array([0, -invertradius])}.get(side)

                        self.segments.append(SegmentCircle(
                            np.asarray(pin['pos'])+invertofst, invertradius))
                        paths.append([pin['pos']+invertofst*2, pin['pos']+leadext])
                    else:
                        paths.append([pin['pos'], pin['pos']+leadext])

                # Define anchors
                anchorpos = pin['pos']+leadext
                self.anchors['in{}{}'.format(side[0].upper(), i+1)] = anchorpos
                if pin.get('anchorname'):
                    self.anchors[pin.get('anchorname')] = anchorpos
                elif pin.get('name'):
                    if pin.get('name') == '>':
                        self.anchors['CLK'] = anchorpos
                    self.anchors[pin.get('name')] = anchorpos
                if pin.get('pin'):
                    self.anchors['pin{}'.format(pin.get('pin'))] = anchorpos

        for p in paths:
            self.segments.append(Segment(p))
        self.params['lblloc'] = 'center'


@adddocs(Ic)
class Multiplexer(Ic):
    ''' Multiplexer

        Parameters
        ----------
        slant : float
            Slant of top/bottom edges
        demux : bool
            Draw as demultiplexer
    '''
    def __init__(self, *args, **kwargs):
        slant = kwargs.pop('slant', 25)
        demux = kwargs.pop('demux', False)
        slant = -slant if not demux else slant
        super().__init__(*args, slant=slant, **kwargs)

