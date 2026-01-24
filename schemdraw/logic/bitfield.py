''' Draw Bit Fields compatible with WaveDrom '''
from __future__ import annotations
import io
import ast
import tokenize

from ..elements import Element
from ..segments import Segment, SegmentText, SegmentPoly

SCALE = 2/72 * 3/4  # Roughly match WaveDrom pixels
COLORS = {
    '1': '#dadada',
    '2': '#f2dbdc',
    '3': '#ecf2da',
    '4': '#e2f2ee',
    '5': '#f2eddb',
    '6': '#e2f2db',
    '7': '#dee5f2',
    '8': '#f2d6ff',
    '9': '#feffdb',
}


class BitField(Element):
    ''' Draw a Bit Field compatible with WaveDrom syntax.
        For reg parameters and examples, see https://github.com/wavedrom/bitfield.

        Args:
            reg: The register dictionary. See below and https://github.com/wavedrom/bitfield.
            bitheight: Height of a bit register box in drawing units
            width: Full width of the register box in drawing units
            fontsize: Size of all text labels
            lw: Line width for borders
            ygap: Distance between lanes. Omit to auto-space based on label heights
            vflip: Flip order of bits
            hflip: Flip order of lanes
            compact: Remove whitespace between lanes

        The reg dictionary may have two keys. 'reg' is a list bitfields, and 'config' tha
        defines configuration options.
        Items in the reg list are dictionaries that may include:
            * name: Text to display within the bit group
            * bits: Number of bits within the group
            * attr: Label to show below the group. May be a string, or integer. If integer,
                the binary representation is shown. May also be a list of multiple lines.
            * type: 0-9 code to fill the bit group. Or may be any valid color string.

        The config list may include:
            * lanes: Number of lanes (bit words stacked vertically)
            * hflip: Reverse order of lanes
            * vflip: Reverse order of bits
            * compact: Remove whitespace between lanes
            * bits: Total number of bits to include (padded out if not included in the `reg` list)
            * label: Dictionary of either 'left' or 'right' and text to display left or right of the lanes.

        Schemdraw's implementation has these known differences:
            * 'type' parameter, which is used to specify a fill color, can
                be the 0-9 code as in WaveDrom, or any valid color string
            * hspace defines the full width of the register in pixels, without including any labels
            * vspace defines the full width of a register in pixels, without including any labels or padding
            * margins are ignored (but can be set by adding the BitField to a schemdraw Drawing)
    '''
    _element_defaults = {
        'bitheight': 0.625,
        'width': 15,    # Width of register box
        'fontsize': 12,
        'lw': 1,
        'ygap': None,  # Vertical spacing between lanes
        'vflip': False,
        'hflip': False,
        'compact': False,
    }

    def __init__(self, reg: dict, **kwargs):
        super().__init__(**kwargs)
        self.regdict = reg
        self.anchors['origin'] = (0, 0)

        reg = self.regdict.get('reg', [])
        config = self.regdict.get('config', {})
        fontsize = config.get('fontsize', self.params['fontsize'])
        hflip = config.get('hflip', self.params['hflip']) in [True, 1, 'true', 'True']
        vflip = config.get('vflip', self.params['vflip']) in [True, 1, 'true', 'True']
        compact = config.get('compact', self.params['compact']) in [True, 1, 'true', 'True']
        totalbits = sum(b.get('bits') for b in reg)
        lblofst = self.params.get('lblofst', .1)

        if 'vspace' in config:
            height = config.get('vspace', 30) * SCALE
        else:
            height = self.params['bitheight']

        if 'hspace' in config:
            lanewidth = config.get('hspace', 800) * SCALE
        else:
            lanewidth = self.params['width']

        lanes = config.get('lanes', 1)

        ygap = self.params['ygap']
        if ygap is None:
            ygap = 0
            for r in reg:
                attr = r.get('attr', [])
                if isinstance(attr, (int, str)):
                    attr = [attr]
                textheight = (len(attr)+1.5) * SCALE * 1.5 * fontsize
                ygap = max(ygap, textheight)

        if 'bits' in config:
            totalbits = config['bits']
            bitsperlane = totalbits // lanes
        elif lanes > 1:
            if totalbits % 2 != 0:
                totalbits += 1
            bitsperlane = config.get('bits', totalbits // lanes)
        else:
            bitsperlane = totalbits

        # Extract labels on left/right side
        leftlabels = None
        rightlabels = None
        if labelconfig := config.get('label'):
            if 'left' in labelconfig:
                if isinstance(labelconfig['left'], int):
                    leftlabels = [str(i+labelconfig['left']) for i in range(lanes)]

                elif isinstance(labelconfig['left'], str):
                    leftlabels = [labelconfig['left']] * lanes

                else:
                    num = len(labelconfig['left'])
                    leftlabels = labelconfig['left'] + [str(i+num) for i in range(lanes-num)]

            if 'right' in labelconfig:
                if isinstance(labelconfig['right'], int):
                    rightlabels = [str(i+labelconfig['right']) for i in range(lanes)]

                elif isinstance(labelconfig['right'], str):
                    rightlabels = [labelconfig['right']] * lanes

                else:
                    num = len(labelconfig['right'])
                    rightlabels = labelconfig['right'] + [str(i+num) for i in range(lanes-num)]

        bitwidth = lanewidth / bitsperlane
        bitheight = height
        leftoverbits = 0
        tickh = bitheight / 8
        bg = 0
        dx = -1 if vflip else 1
        y = 0

        for lane in range(lanes):

            # Main box and ticks
            self.segments.append(
                SegmentPoly(((0, y), (lanewidth, y), (lanewidth, y+bitheight), (0, y+bitheight)), closed=True, lw=self.params['lw'])
            )
            for b in range(bitsperlane-1):
                x = (b+1) * bitwidth
                self.segments.append(
                    Segment(((x, y+bitheight), (x, y+bitheight-tickh)), lw=self.params['lw'])
                )
                self.segments.append(
                    Segment(((x, y), (x, y+tickh)), lw=self.params['lw'])
                )

            # Labels on left/right side
            if leftlabels:
                self.segments.append(SegmentText(
                    (0-lblofst, y+bitheight/2), leftlabels[lane],
                    fontsize=fontsize, align=('right', 'center'))
                )
            if rightlabels:
                self.segments.append(SegmentText(
                    (lanewidth+lblofst, y+bitheight/2), rightlabels[lane],
                    fontsize=fontsize, align=('left', 'center'))
                )

            # Details of each lane
            x = lanewidth if not vflip else 0
            centery = y + bitheight/2
            rowbit = 0
            while rowbit < bitsperlane and bg < len(reg):
                bitgroup = reg[bg]
                groupbits = int(bitgroup.get('bits', 1))  # Whole bit group
                nbits = groupbits if not leftoverbits else leftoverbits  # Bits that fit in this lane
                attr = bitgroup.get('attr', None)
                rotate = bitgroup.get('rotate', 0)
                name = bitgroup.get('name', '')
                color = bitgroup.get('type', None)

                if nbits + rowbit > bitsperlane:
                    nbits, leftoverbits = bitsperlane - rowbit, nbits - (bitsperlane-rowbit)
                else:
                    leftoverbits = 0

                # Draw bitgroup edges and fill
                centerx = x - dx*nbits*bitwidth/2
                x0 = x
                x -= nbits*bitwidth*dx
                self.segments.append(
                    Segment(((x, y+bitheight), (x, y)), lw=self.params['lw'])
                )
                if color or not name:
                    if color is None or len(str(color)) == 1:
                        color = COLORS.get(str(color), '#dadada')
                    self.segments.append(
                        SegmentPoly(((x, y+bitheight), (x, y), (x0, y), (x0, y+bitheight)),
                                    lw=0, color='none', fill=color,
                                    zorder=0,
                                    )
                    )

                # Draw name in center of bits
                if name:
                    self.segments.append(
                        SegmentText(
                            (centerx, centery), name,
                            fontsize=fontsize,
                            align=('center', 'center'),
                            rotation=-rotate
                        )
                    )

                # Draw bit numbers above
                if (hflip and lane == 0) or (not hflip and lane == lanes-1) or not compact:
                    self.segments.append(
                        SegmentText((x0-dx*bitwidth/2, y+bitheight+lblofst), str(lane*bitsperlane+rowbit),
                                    fontsize=fontsize,
                                    align=('center', 'bottom')
                                    )
                    )
                    self.segments.append(
                        SegmentText((x+dx*bitwidth/2, y+bitheight+lblofst), str(lane*bitsperlane+rowbit+nbits-1),
                                    fontsize=fontsize,
                                    align=('center', 'bottom')
                                    )
                    )

                # Draw attributes below
                if attr is not None:
                    if isinstance(attr, (str, int)):
                        attr = [attr]

                    if isinstance(attr[0], str):
                        # String label
                        text = '\n'.join(attr)
                        self.segments.append(SegmentText(
                            (centerx, y-lblofst), text,
                            fontsize=fontsize, align=('center', 'top'))
                        )

                    else:
                        # Number - label bit values as 0 or 1
                        values = [v if v >= 0 else v+(1 << groupbits) for v in attr]  # 2's complement negative ints
                        binaries = [f'{v:0{groupbits}b}' for v in values]
                        for bit in range(nbits):
                            n = nbits+leftoverbits-bit-1
                            column = [b[n] for b in binaries]
                            columnstr = '\n'.join(column)
                            self.segments.append(SegmentText(
                                (x0 - dx*bitwidth*bit - dx*bitwidth/2, y-lblofst), columnstr,
                                fontsize=fontsize, align=('center', 'top'))
                            )

                rowbit += nbits
                if not leftoverbits:
                    bg += 1

            dy = bitheight if compact else bitheight + ygap
            if hflip:
                y -= dy
            else:
                y += dy

    @classmethod
    def from_json(cls, wave: str, **kwargs):
        ''' Create bitfield diagram from string WaveJSON. '''
        tokens = tokenize.generate_tokens(io.StringIO(wave).readline)
        modified_tokens = (
            (tokenize.STRING, repr(token.string)) if token.type == tokenize.NAME else token[:2]
            for token in tokens)

        fixed_input = tokenize.untokenize(modified_tokens)
        return cls(ast.literal_eval(fixed_input), **kwargs)
