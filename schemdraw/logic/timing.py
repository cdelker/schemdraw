''' Timing Diagrams, based on WaveJSON format '''

from __future__ import annotations
import re
import io
import ast
import tokenize
import math
from collections import namedtuple, ChainMap

from ..elements import Element
from ..segments import Segment, SegmentText, SegmentPoly, SegmentBezier
from ..backends.svg import text_size
from ..types import BBox
from ..util import Point
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

        Schemdraw provides a few additional extensions to the
        WaveJSON dictionary, including asynchronous waveforms
        and configuration options (color, lw) on each wave.
        See documentation for full specification.

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
    _wavelookup = {'0': Wave0,
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
                   }

    def __init__(self, waved: dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.wave = waved

        self.yheight = kwargs.pop('yheight', .5)
        self.ygap = kwargs.pop('ygap', .3)
        self.risetime = kwargs.pop('risetime', .15)
        self.fontsize = kwargs.pop('fontsize', 12)
        self.nodesize = kwargs.pop('nodesize', 8)
        self.namecolor = kwargs.pop('namecolor', 'blue')
        self.datacolor = kwargs.pop('datacolor', None)  # default: get color from theme
        self.nodecolor = kwargs.pop('nodecolor', None)
        self.gridcolor = kwargs.pop('gridcolor', '#DDDDDD')
        self.edgecolor = kwargs.pop('edgecolor', 'blue')
        self.grid = kwargs.pop('grid', True)
        self.kwargs = kwargs

        signals = self.wave.get('signal', [])  # type: ignore
        signals_flat = flatten(signals)
        config = self.wave.get('config', {})  # type: ignore
        self.hscale = config.get('hscale', 1)  # type: ignore

        height = (self.yheight+self.ygap)*len(signals_flat)
        periods = max(len(w.get('wave', [])) for w in signals_flat)
        if self.grid:
            self._drawgrid(periods, height)

        # phase shifts that go off screen will be clipped by this rect
        clipbox = BBox(0, self.yheight, periods*self.yheight*2*self.hscale, -height)
        self.kwargs['clip'] = clipbox

        labelwidth = 0.
        y0 = 0.
        for signal in signals_flat:
            name = signal.get('name', '')
            _width = self._drawname(name, y0)
            labelwidth = max(labelwidth, _width)

            if 'async' in signal:
                self._drawasync(signal, y0)
            else:
                self._drawwave(signal, y0=y0)
            self._drawnodes(signal, y0=y0)
            y0 -= (self.yheight+self.ygap)

        self._drawedges()
        self._drawgroups(signals, labelwidth)

    def _drawgrid(self, periods, height):
        ''' Draw grid (vertical dotted lines) '''
        for p in range(periods+1):
            self.segments.append(
                Segment([(p*2*self.yheight*self.hscale, self.yheight+self.ygap/2),
                         (p*2*self.yheight*self.hscale, self.yheight-height)],
                        ls=':', lw=1, color=self.gridcolor, zorder=0))

    def _drawname(self, name, y0):
        ''' Draw name of one wave. Returns calculated unit width of the string. '''
        textpad = .2
        self.segments.append(
            SegmentText((-textpad, y0), name, align=('right', 'bottom'),
                        fontsize=self.fontsize, color=self.namecolor))
        return text_size(name, size=self.fontsize)[0] * PTS_TO_UNITS

    def _drawwave(self, signal, y0=0):
        ''' Draw one wave.

            Args:
                signal: Dictionary defining the signal to draw
                y0: Vertical position
        '''
        wave = signal.get('wave', '')
        phase = signal.get('phase', 0)
        waverise = signal.get('risetime', None)
        wavekwargs = ChainMap({'color': signal.get('color', None),
                               'lw': signal.get('lw', 1)}, self.kwargs)

        data = signal.get('data', [])
        if not isinstance(data, list):
            data = data.split()  # Sometimes it's a space-separated string...

        period = 2*self.yheight*signal.get('period', 1) * self.hscale
        y1 = y0 + self.yheight
        i = 0
        pstate = '-'

        x = -period*phase
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
                      'rise': waverise if waverise is not None else self.risetime,
                      'data': data,
                      'datacolor': self.datacolor,
                      'kwargs': wavekwargs}

            wavecls = self._wavelookup.get(state, WaveV)
            self.segments.extend(wavecls(params).segments())

            for split in splits:
                self.segments.extend(
                    getsplit(x + (split+1)*period-period/2, y0, y1))

            pstate = state
            x += periods*period
            i = k

    def _drawasync(self, signal, y0):
        ''' Draw asynchronous wave

            Args:
                signal: Dictionary defining the signal to draw
                y0: Vertical position
        '''
        times = signal.get('async', '')
        wave = signal.get('wave', '')
        waverise = signal.get('risetime', None)
        wavekwargs = ChainMap({'color': signal.get('color', None),
                               'lw': signal.get('lw', 1)}, self.kwargs)
        rise = waverise if waverise is not None else self.risetime

        data = signal.get('data', [])
        if not isinstance(data, list):
            data = data.split()  # Sometimes it's a space-separated string...
        if not isinstance(times, list):
            times = [float(f) for f in times.split()]

        if len(wave) + 1 != len(times):
            raise ValueError('len(times) must be one more than len(wave).')

        period = 2*self.yheight*signal.get('period', 1) * self.hscale
        y1 = y0 + self.yheight
        pstate = '-'
        for i in range(len(wave)):
            state = wave[i]
            t0 = times[i]
            t1 = times[i+1]
            nstate = wave[i+1] if i<len(wave)-1 else '-'
            x = t0*period
            xend = t1*period
            params = {'state': state,
                      'pstate': pstate,
                      'nstate': nstate,
                      'plevel': state_level(pstate),
                      'nlevel': state_level(nstate),
                      'periods': 0,
                      'period': period,
                      'x0': x,
                      'xend': xend,
                      'y0': y0,
                      'y1': y1,
                      'rise': rise,
                      'data': data,
                      'datacolor': self.datacolor,
                      'kwargs': wavekwargs}

            wavecls = self._wavelookup.get(state, WaveV)
            self.segments.extend(wavecls(params).segments())
            x = xend
            pstate = state

    def _drawnodes(self, signal, y0):
        ''' Draw nodes (labels along the wave) and define anchors for each

            Args:
                signal: Dictionary defining the signal to draw
                y0: Vertical position
        '''
        nodes = signal.get('node', '')
        phase = signal.get('phase', 0)
        period = 2*self.yheight*signal.get('period', 1) * self.hscale

        y1 = y0 + self.yheight
        for j, node in enumerate(nodes):
            if node == '.': continue
            w, h, _ = text_size(node, size=self.nodesize)
            w, h = w*PTS_TO_UNITS*2.5, h*PTS_TO_UNITS*2.5
            ycenter = (y0+y1)/2
            xnode = j*period + self.risetime/2 - period*phase
            if not node.isupper():  # Only uppercase nodes and symbols are drawn
                self.segments.append(SegmentPoly([(xnode-w/2, ycenter-h/2), (xnode-w/2, ycenter+h/2),
                                                  (xnode+w/2, ycenter+h/2), (xnode+w/2, ycenter-h/2)],
                                                 color='none', fill='bg', zorder=3))
                self.segments.append(
                    SegmentText((xnode, ycenter), node, align=('center', 'center'),
                                fontsize=self.nodesize, color=self.nodecolor, zorder=3))
            self.anchors[f'node_{node}'] = (xnode, ycenter)

    def _drawedges(self):
        edges = self.wave.get('edge', [])  # type: ignore
        chrrad = self.nodesize / 60
        caplen = .1
        period = 2*self.yheight * self.hscale

        for edge in edges:
            label = ''
            if ' ' in edge:
                edge, label = edge.split(maxsplit=1)
            style = re.findall(r'{(.*)}', edge)
            edge = re.sub(r'{(.*)}', '', edge)
            nodes = re.findall(r'\[(.+?)\]', edge)
            if len(nodes) == 0:
                # Single letter node names, WaveDrom style
                mode = edge[1:-1]
                p0 = Point(self.anchors[f'node_{edge[0]}'])
                pn = Point(self.anchors[f'node_{edge[-1]}'])

            else:
                # Extended node naming - [WaveNumber:Xposition]
                assert len(nodes) == 2
                mode = re.subn(r'\[(.+?)\]', '', edge)[0]
                endpoints = []
                for node in nodes:
                    nodewave, nodet = node.split(':')
                    nodet = float(nodet)  # number periods into wave
                    ofst = self.yheight/2
                    if '^' in nodewave:
                        ofst = self.yheight + caplen*2
                    elif 'v' in nodewave:
                        ofst = -caplen*2
                    nodewave = nodewave.replace('^', '').replace('v', '')
                    wavenum = int(nodewave)
                    endpoints.append(
                        Point((nodet*period+self.risetime/2,
                               -wavenum*(self.yheight + self.ygap) + ofst)))
                p0, pn = endpoints

            color = self.edgecolor
            ls = '-'
            if style:
                style = style[0].split(',')
                color = style[0]
                ls = '-' if len(style) == 1 else style[1]

            if '<' in edge and '>' in edge:
                arrow = '<>'
            elif '<' in edge:
                arrow = '>'
            elif '>' in edge:
                arrow = '<'
            else:
                arrow = None

            mode = mode.strip('<>')
            center = Point(((p0.x+pn.x)/2, (p0.y+pn.y)/2))
            if mode == '-':  # Straight line
                center = Point(((p0.x+pn.x)/2, (p0.y+pn.y)/2))
                th0 = math.atan2((pn.y-p0.y), (pn.x-p0.x))
                p0 = Point((p0.x + chrrad * math.cos(th0), p0.y + chrrad * math.sin(th0)))
                pn = Point((pn.x - chrrad * math.cos(th0), pn.y - chrrad * math.sin(th0)))
                self.segments.append(Segment([pn, p0], lw=1, ls=ls, color=color,
                                             arrow=arrow, zorder=3))

            elif mode == '+':  # Straight line with endcaps, full length
                center = Point(((p0.x+pn.x)/2, (p0.y+pn.y)/2))
                th0 = math.atan2(-(pn.x-p0.x), (pn.y-p0.y))
                self.segments.append(Segment((p0, pn), lw=1, ls=ls, color=color))
                cap1 = [(p0.x + caplen*math.cos(th0), p0.y + caplen*math.sin(th0)),
                        (p0.x - caplen*math.cos(th0), p0.y - caplen*math.sin(th0))]
                cap2 = [(pn.x + caplen*math.cos(th0), pn.y + caplen*math.sin(th0)),
                        (pn.x - caplen*math.cos(th0), pn.y - caplen*math.sin(th0))]
                self.segments.append(Segment(cap1, lw=1, color=color))
                self.segments.append(Segment(cap2, lw=1, color=color))

            elif mode == '|-':
                center = Point((p0.x, (p0.y+pn.y)/2))
                dy = 1 if p0.y > pn.y else -1
                dx = 1 if p0.x < pn.x else -1
                p0 = p0 - Point((0, chrrad*dy))
                pn = pn - Point((chrrad*dx, 0))
                p1 = Point((p0.x, pn.y))
                self.segments.append(Segment((p0, p1, pn), lw=1, ls=ls, color=color, zorder=3, arrow=arrow))

            elif mode == '-|':
                center = Point((pn.x, (p0.y+pn.y)/2))
                dy = -1 if p0.y > pn.y else 1
                dx = -1 if p0.x < pn.x else 1
                p0 = p0 - Point((chrrad*dx, 0))
                pn = pn - Point((0, chrrad*dy))
                p1 = Point((pn.x, p0.y))
                self.segments.append(Segment((p0, p1, pn), lw=1, ls=ls, color=color, arrow=arrow, zorder=3))

            elif mode == '-|-':
                center = (p0+pn)/2
                dx = -1 if pn.x < p0.x else 1
                p0 = p0 + Point((chrrad*dx, 0))
                p1 = Point((center.x, p0.y))
                p2 = Point((center.x, pn.y))
                pn = pn - Point((chrrad*dx, 0))
                self.segments.append(Segment((p0, p1, p2, pn), lw=1, ls=ls, color=color, arrow=arrow, zorder=3))

            elif mode == '~':  # S-curve, start and end horizontally
                center = Point(((p0.x+pn.x)/2, (p0.y+pn.y)/2))
                p0 = p0 + Point((chrrad, 0))
                p3 = pn - Point((chrrad, 0))
                dx = p3.x - p0.x
                p1 = p0 + Point((dx*.6, 0))
                p2 = p3 - Point((dx*.6, 0))
                self.segments.append(SegmentBezier([p0, p1, p2, p3], lw=1, ls=ls,
                                                   color=color, arrow=arrow, zorder=3))

            elif mode == '-~':  # C curve, horizontal at start
                center = Point((p0.x+0.8*(pn.x-p0.x), p0.y + (pn.y-p0.y)/2))
                dx = pn.x - p0.x
                p1 = p0 + Point((dx*.7, 0))
                th0 = math.atan2((p1.y-p0.y), (p1.x-p0.x))
                th2 = math.atan2((p1.y-pn.y), (p1.x-pn.x))
                p0 = Point((p0.x + chrrad * math.cos(th0), p0.y + chrrad * math.sin(th0)))
                pn = Point((pn.x - chrrad * math.cos(th0), pn.y + chrrad * math.sin(th2)))
                self.segments.append(SegmentBezier(
                    [p0, p1, pn], lw=1, ls=ls, color=color, arrow=arrow, zorder=3))

            elif mode == '~-':
                center = Point((p0.x+0.25*(pn.x-p0.x), (p0.y+pn.y)/2))
                dx = pn.x - p0.x
                p1 = pn - Point((dx*.6, 0))
                th0 = math.atan2((p1.y-p0.y), (p1.x-p0.x))
                th2 = math.atan2((p1.y-pn.y), (p1.x-pn.x))
                p0 = Point((p0.x + chrrad * math.cos(th0), p0.y + chrrad * math.sin(th0)))
                pn = Point((pn.x + chrrad * math.cos(th2), pn.y + chrrad * math.sin(th2)))
                self.segments.append(SegmentBezier(
                    [p0, p1, pn], lw=1, ls=ls, color=color, arrow=arrow, zorder=3))

            if label:
                w, h, _ = text_size(label, size=self.nodesize)
                w, h = w*PTS_TO_UNITS*1.5, h*PTS_TO_UNITS*1.5
                self.segments.append(SegmentPoly([(center.x-w/2, center.y-h/2),
                                                  (center.x-w/2, center.y+h/2),
                                                  (center.x+w/2, center.y+h/2),
                                                  (center.x+w/2, center.y-h/2)],
                                     color='none', fill='bg', zorder=4))
                self.segments.append(SegmentText(center, label, fontsize=self.nodesize,
                                                 color=self.nodecolor, align=('center', 'center'),
                                                 zorder=4))

    def _drawgroups(self, signals, labelwidth):
        ''' Draw group labels

            Args:
                signals: List of dictionaries defining the signals
                labelwidth: Max text width (drawing units) of signal names
        '''
        nlevels = max_depth(signals)
        edgelen = .05
        levelwidth = 0.5
        for label in getlabels(signals):
            xval = -(labelwidth) - (nlevels-label.level)*levelwidth
            ytop = -label.row*(self.yheight+self.ygap) + self.yheight - edgelen
            ybot = ytop - label.height * (self.yheight+self.ygap) + self.ygap/2 + edgelen
            ycenter = (ytop+ybot)/2
            xtext = xval - .1
            self.segments.append(
                Segment([(xval+edgelen, ybot-edgelen), (xval, ybot),
                         (xval, ytop), (xval+edgelen, ytop+edgelen)],
                        color=self.namecolor, lw=1))
            self.segments.append(
                SegmentText((xtext, ycenter), label.name, rotation=90,
                            align=('center', 'bottom'), color=self.namecolor,
                            fontsize=self.fontsize))

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
