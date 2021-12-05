''' Timing Diagrams, based on WaveJSON format '''

import re
import io
import ast
import tokenize
from collections import namedtuple

from ..elements import Element
from ..segments import Segment, SegmentText, SegmentPoly
from ..backends.svg import text_size
from ..types import BBox
from .timingwaves import Wave0, Wave1, WaveL, WaveH, Wavez, WaveV, WaveU, WaveD, WaveClk, getsplit


LabelInfo = namedtuple('LabelInfo', ['name', 'row', 'height', 'level'])

PTS_TO_UNITS = 2/72


def state_level(state: str, ud: bool=False, np: bool=False) -> str:
    ''' Get level of wave state (0, 1, V, z, -) '''
    state = re.sub(r'[2-9]|\=|x', 'V', state)
    state = re.sub('u', '1', state)
    state = re.sub('d', '0', state)
    state = re.sub('n|N', '1', state)
    state = re.sub('p|P', '0', state)
    state = re.sub('l|L', '0', state)
    state = re.sub('h|H', '1', state)
    return state


def flatten(S):
    ''' Flatten the signals list so only individual rows (dicts) are included '''
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    if isinstance(S[0], str):
        return flatten(S[1:])
    return S[:1] + flatten(S[1:])


def max_depth(sig) -> int:
    ''' Get maximum group depth of the signal list '''
    return isinstance(sig, list) and max(map(max_depth, sig))+1


def get_nrows(sig) -> int:
    ''' Get the number of signal rows in the signal list '''
    if isinstance(sig, dict):
        return 1
    elif isinstance(sig[0], list):
        return sum(map(get_nrows, sig[0]))
    elif isinstance(sig[0], str):
        return sum(map(get_nrows, sig[1:]))
    return 0


def getlabels(sig, row: int=0, level: int=0) -> list[LabelInfo]:
    ''' Get a list of group label info '''
    if isinstance(sig, dict) or sig == []:
        return []
    elif all(isinstance(s, dict) for s in sig):
        return []
    elif isinstance(sig[0], str):
        lbl = [LabelInfo(sig[0], row, get_nrows(sig), level)]
        n = 0
        for s in sig[1:]:
            lbl.extend(getlabels(s, row=row+n, level=level+1))
            n += get_nrows(s)
        return lbl
    else:
        lbl = []
        n = 0
        for s in sig:
            lbl.extend(getlabels(s, row=row+n, level=level+1))
            n += get_nrows(s)
        return lbl


class TimingDiagram(Element):
    ''' Logic Timing Diagram

        Draw timing diagrams compatible with WaveJSON format
        See https://wavedrom.com/ for details. Use `from_json`
        to use WaveJSON strings copied from the site (since they
        can't be copied as proper Python dicts due to lack of
        quoting).

        Args:
            wave: WaveJSON as a Python dict

        Keyword Args:
            yheight: Height of one waveform
            ygap: Separation between two waveforms
            risetime: Rise/fall time for wave transitions
            fontsize: Size of label fonts
            nodesize: Size of node labels
            namecolor: Color for wave names
            datacolor: Color for wave data text
            nodecolor: Color for node text
            gridcolor: Color of background grid
    '''
    def __init__(self, waved: dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.wave = waved

        kwargs.setdefault('lw', 1)
        yheight = kwargs.pop('yheight', .5)
        ygap = kwargs.pop('ygap', .3)
        risetime = kwargs.pop('risetime', .15)
        fontsize = kwargs.pop('fontsize', 12)
        nodesize = kwargs.pop('nodesize', 8)
        namecolor = kwargs.pop('namecolor', 'blue')
        datacolor = kwargs.pop('datacolor', None)  # default: get color from theme
        nodecolor = kwargs.pop('nodecolor', None)
        gridcolor = kwargs.pop('gridcolor', '#DDDDDD')

        signals = self.wave.get('signal', [])  # type: ignore
        signals_flat = flatten(signals)
        config = self.wave.get('config', {})  # type: ignore
        hscale = config.get('hscale', 1)  # type: ignore

        totheight = (yheight+ygap)*len(signals_flat)
        totperiods = max(len(w.get('wave', [])) for w in signals_flat)
        for p in range(totperiods+1):
            self.segments.append(
                Segment([(p*2*yheight*hscale, yheight+ygap/2),
                         (p*2*yheight*hscale, yheight-totheight)],
                        ls=':', lw=1, color=gridcolor, zorder=0))

        clipbox = BBox(0, yheight, totperiods*yheight*2*hscale, -totheight)
        kwargs['clip'] = clipbox

        labelwidth = 0.
        y0 = 0.
        for signal in signals_flat:
            name = signal.get('name', '')
            wave = signal.get('wave', '')
            data = signal.get('data', [])
            nodes = signal.get('node', [])
            phase = signal.get('phase', 0)
            period = 2*yheight*signal.get('period', 1) * hscale
            textpad = .2

            if not isinstance(data, list):
                data = data.split()  # Sometimes it's a space-separated string...

            x = 0.
            y1 = y0 + yheight
            i = 0
            pstate = '-'

            labelwidth = max(labelwidth, text_size(name, size=12)[0])
            self.segments.append(
                SegmentText((x-textpad, y0), name, align=('right', 'bottom'),
                            fontsize=fontsize, color=namecolor))
            x -= period*phase
            while i < len(wave):
                state = wave[i]
                splits = []
                periods = 1
                k = i+1
                while k < len(wave) and wave[k] in '|.':
                    if wave[k] == '|':
                        splits.append(periods)
                    periods += 1
                    k += 1
                nstate = wave[k] if k < len(wave) else '-'

                xend = x+periods*period
                params = {'state': state,
                          'pstate': pstate,
                          'nstate': nstate,
                          'plevel': state_level(pstate),
                          'nlevel': state_level(nstate),
                          'periods': periods,
                          'period': period,
                          'x0': x,
                          'xend': xend,
                          'y0': y0,
                          'y1': y1,
                          'rise': risetime,
                          'data': data,
                          'datacolor': datacolor,
                          'kwargs': kwargs}

                wavecls = {'0': Wave0,
                           '1': Wave1,
                           'H': WaveH,
                           'h': WaveH,
                           'L': WaveL,
                           'l': WaveL,
                           'z': Wavez,
                           'u': WaveU,
                           'd': WaveD,
                           'n': WaveClk,
                           'p': WaveClk,
                           'N': WaveClk,
                           'P': WaveClk,
                           }.get(state, WaveV)

                self.segments.extend(wavecls(params).segments())
                
                for split in splits:
                    self.segments.extend(
                        getsplit(x + (split+1)*period-period/2, y0, y1))

                pstate = state
                x += periods*period
                i = k

            # Draw nodes and define anchors
            x = 0
            for j, node in enumerate(nodes):
                if node == '.': continue
                w, h, _ = text_size(node, size=nodesize)
                w, h = w*PTS_TO_UNITS*2.5, h*PTS_TO_UNITS*2.5
                ycenter = (y0+y1)/2
                xnode = j*period + risetime/2
                if not node.isupper():  # Only uppercase nodes and symbols are drawn
                    self.segments.append(SegmentPoly([(xnode-w/2, ycenter-h/2), (xnode-w/2, ycenter+h/2),
                                                      (xnode+w/2, ycenter+h/2), (xnode+w/2, ycenter-h/2)],
                                                     color='none', fill='bg', zorder=3))
                    self.segments.append(
                        SegmentText((xnode, ycenter), node, align=('center', 'center'),
                                    fontsize=nodesize, color=nodecolor))
                self.anchors[f'node_{node}'] = (xnode, ycenter)

            y0 -= (yheight+ygap)

        # Add the group labels
        nlevels = max_depth(signals)
        edgelen = .05
        levelwidth = 0.5
        for label in getlabels(signals):
            xval = -(labelwidth*PTS_TO_UNITS) - (nlevels-label.level)*levelwidth
            ytop = -label.row*(yheight+ygap) + yheight - edgelen
            ybot = ytop - label.height * (yheight+ygap) + ygap/2 + edgelen
            ycenter = (ytop+ybot)/2
            xtext = xval - .1
            self.segments.append(
                Segment([(xval+edgelen, ybot-edgelen), (xval, ybot),
                         (xval, ytop), (xval+edgelen, ytop+edgelen)],
                        color=namecolor, lw=1))
            self.segments.append(
                SegmentText((xtext, ycenter), label.name, rotation=90,
                            align=('center', 'bottom'), color=namecolor,
                            fontsize=fontsize))

    @classmethod
    def from_json(cls, wave: str, **kwargs):
        ''' Create timing diagram from string WaveJSON. '''
        # Source for cleaning up JSON: https://stackoverflow.com/a/61783377/13826284
        tokens = tokenize.generate_tokens(io.StringIO(wave).readline)
        modified_tokens = (
            (tokenize.STRING, repr(token.string)) if token.type == tokenize.NAME else token[:2]
            for token in tokens)

        fixed_input = tokenize.untokenize(modified_tokens)
        return cls(ast.literal_eval(fixed_input), **kwargs)
