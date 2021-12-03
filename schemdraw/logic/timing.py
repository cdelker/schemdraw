import re
import io
import ast
import json
import math
import tokenize

from ..elements import Element
from ..segments import Segment, SegmentPoly, SegmentText

from .. import util
from ..types import BBox


def state_level(state, ud=False, np=False):
    ''' Get level of wave state (0, 1, V, z, -) '''
    state = re.sub('[2-9]|\=|x', 'V', state)
    state = re.sub('u', '1', state)
    state = re.sub('d', '0', state)
    state = re.sub('n|N', '1', state)
    state = re.sub('p|P', '0', state)
    state = re.sub('l|L', '0', state)
    state = re.sub('h|H', '1', state)
    return state

def expcurve(height):
    xcurve = util.linspace(0, 1, 10)
    ycurve = [height * math.exp(-v*6) for v in xcurve]
    return xcurve, ycurve

def getsplit(x0, y0, y1, **kwargs):
    ''' Splits are filled in the middle to cover/hide the wave underneath '''
    sig = Doublesigmoid(x0, y0, y1, **kwargs)
    leftx, lefty = sig.curve(side='left')
    rghtx, rghty = sig.curve(side='right')
    left = list(zip(leftx, lefty))
    right = list(zip(rghtx, rghty))
    segments = [Segment(left, lw=1, zorder=3),
                Segment(right, lw=1, zorder=3),
                SegmentPoly(left+right[::-1], zorder=2, color='none', fill='white', lw=1, closed=False)]
    return segments


class Doublesigmoid:
    def __init__(self, x0, y0, y1, extend=0.1, gap=.2, **kwargs):
        self.x0 = x0  # Center
        self.y0 = y0
        self.y1 = y1
        self.extend = extend  # Over/under y0 and y1 lines, relative to height
        self.gap = gap  # Distance from first to second curve, relative to height
        self.kwargs = kwargs

        self.rate = 25  # Adjust curvature
        self.height = self.y1-self.y0
        self.curve1x = self.x0 - self.gap*self.height/2
        self.curve2x = self.x0 + self.gap*self.height/2
        self.top = self.y1 + self.height * self.extend
        self.bot = self.y0 - self.height * self.extend

    def segments(self):
        segments = []
        x, y = self.curve(side='left')
        segments.append(Segment(list(zip(x, y)), **self.kwargs))
        x, y = self.curve(side='right')
        segments.append(Segment(list(zip(x, y)), **self.kwargs))
        return segments

    def intersect(self, y0):
        # Get x0, x1, values that intersect y
        fullh = self.height * (1 + self.extend*2)
        drop = self.height * self.extend

        x = math.log(1 / (y0 - self.y0 + drop) * fullh - 1) / -self.rate
        return self.x0 - self.gap*height/2 + x, self.x0 + self.gap*height/2 + x

    def curve(self, side='left', crop=False, ofst=0):
        fullh = self.height * (1 + self.extend*2)
        drop = self.height * self.extend

        # Base sigmoid
        sigx = util.linspace(-0.15, 0.15)
        sigy = [1/(1+math.exp(-x*self.rate)) * fullh - drop for x in sigx]
        
        if crop:
            sigx = [x for i, x in enumerate(sigx) if 0 <= sigy[i] < self.height]
            sigy = [y for i, y in enumerate(sigy) if 0 <= sigy[i] < self.height]

        # Move to position
        x0 = self.curve1x if side == 'left' else self.curve2x
        sigx = [x+x0+ofst for x in sigx]
        sigy = [y+self.y0 for y in sigy]
        
        return sigx, sigy

class Wave0:
    def __init__(self, params):
        self.params = params
        self.x0 = self.params.get('x0', 0)
        self.xend = self.params.get('xend', 1)
        self.y0 = self.params.get('y0', 0)
        self.y1 = self.params.get('y1', .5)
        self.pstate = self.params.get('pstate', '-')
        self.nstate = self.params.get('nstate', '-')
        self.plevel = self.params.get('plevel', '-')
        self.nlevel = self.params.get('nlevel', '-')
        self.rise = self.params.get('rise', 0.1)

        self.xrise = self.x0 + self.rise
        self.xrisehalf = self.x0 + self.rise / 2
        self.yhalf = (self.y0 + self.y1)/2
        self.xcenter = (self.x0 + self.xend)/2
        self.xtext = self.xcenter + self.rise / 2

        self.kwargs = self.params.get('kwargs', {'lw': 1})
        
    def verts_in(self):
        verts = {'-': [(self.x0, self.y0)],
                 '|': [(self.x0, self.y0)],
                 '0': [(self.x0, self.y0), (self.xrisehalf, self.yhalf), (self.xrise, self.y0)],
                 '1': [(self.x0, self.y1), (self.xrise, self.y0)],
                 'z': [(self.x0, self.yhalf), (self.xrisehalf, self.y0)],
                 'V': [(self.xrise, self.y0)]
                }.get(self.plevel)
        return verts

    def verts_out(self):
        return [(self.xend, self.y0)]
    
    def segments(self):
        verts = self.verts_in() + self.verts_out()
        return [Segment(verts, **self.kwargs)]
        
class WaveL(Wave0):
    def verts_in(self):
        if self.params['pstate'] in 'pP':
            return [(self.x0, self.y0)]
        else:
            return [(self.x0, self.y1), (self.x0, self.y0)]

    def segments(self):
        segments = super().segments()
        if self.params['state'] == 'L':
            hlength = .25
            hwidth = .12
            yhead = self.yhalf - hlength/2
            ytail = self.yhalf + hlength/2
            segments.append(SegmentArrow((self.x0, ytail), (self.x0, yhead),
                                        headwidth=hwidth, headlength=hlength))
        return segments
    
    
class Wave1(Wave0):
    def verts_in(self):
        verts = {'-': [(self.x0, self.y1)],
                 'h': [(self.x0, self.y1)],
                 'H': [(self.x0, self.y1)],
                 'l': [(self.x0, self.y1)],
                 'L': [(self.x0, self.y1)],
                 '0': [(self.x0, self.y0), (self.xrise, self.y1)],
                 '1': [(self.x0, self.y1), (self.xrisehalf, self.yhalf), (self.xrise, self.y1)],
                 'z': [(self.x0, self.yhalf), (self.xrisehalf, self.y1)],
                 'V': [(self.xrise, self.y1)]
                }.get(self.plevel)
        return verts

    def verts_out(self):
        return [(self.xend, self.y1)]

class WaveH(Wave1):
    def verts_in(self):
        if self.params['pstate'] in 'nN':
            return [(self.x0, self.y1)]
        else:
            return [(self.x0, self.y0), (self.x0, self.y1)]
    
    def segments(self):
        segments = super().segments()
        if self.params['state'] == 'H':
            hlength = .25
            hwidth = .12
            ytail = self.yhalf - hlength/2
            yhead = self.yhalf + hlength/2
            segments.append(SegmentArrow((self.x0, ytail), (self.x0, yhead),
                                        headwidth=hwidth, headlength=hlength))
        return segments

    
class Wavez(Wave0):
    def verts_in(self):
        xcurve, yexp = expcurve((self.y1-self.y0)/2)
        ycurve = [self.yhalf + yc for yc in yexp]
        ycurveflip = [self.yhalf - yc for yc in yexp]
        xcurve = [self.x0+xc*self.rise*6 for xc in xcurve]
        verts = {'-': [(self.x0, self.yhalf)],
                 '0': list(zip(xcurve, ycurveflip)),
                 '1': list(zip(xcurve, ycurve)),
                 'z': [(self.x0, self.yhalf)],
                 'V': [(self.xrise+self.rise, self.yhalf)],   # V gets curves on its output
                }.get(self.plevel)
        return verts

    def verts_out(self):
        return [(self.xend, self.yhalf)]


class WaveV(Wave0):
    def verts_in(self):
        xcurve, yexp = expcurve((self.y1-self.y0)/2)
        ycurve = [self.yhalf + yc for yc in yexp]
        ycurveflip = [self.yhalf - yc for yc in yexp]
        xcurve = [self.x0+xc*self.rise*6 for xc in xcurve]

        verts = {'-': [(self.x0, self.y1), (self.x0, self.y0)],
                 '|': [(self.x0, self.y1), (self.x0, self.y0)],
                 '0': [(self.xrise, self.y1), (self.x0, self.y0)],
                 '1': [(self.x0, self.y1), (self.xrise, self.y0)],
                 'z': [(self.xrise, self.y1), (self.xrisehalf, self.yhalf), (self.xrise, self.y0)],  # CCW
                 'V': [(self.xrise, self.y1), (self.xrisehalf, self.yhalf), (self.xrise, self.y0)],  # CCW
                 }.get(self.plevel)
        return verts

    def verts_out(self):
        xcurve, yexp = expcurve((self.y1-self.y0))
        xcurve = [self.xend+xc*self.rise*6 for xc in xcurve]
        ycurve = [self.y0+yc for yc in yexp]     # Exp fall
        ycurveh = [self.y0+yc/2 for yc in yexp]  # Half exp fall
        ycurvef = [self.y1-yc for yc in yexp]    # Flipped
        ycurvehf = [self.y1-yc/2 for yc in yexp] # Flipped half

        nstate = 'V' if self.nstate in '=23456789x' else self.nstate

        sig = Doublesigmoid(self.xcenter, self.y0, self.y1)

        verts = {
            '0': [(self.xend+self.rise, self.y0), (self.xend, self.y1)],  # Fall
            'L': [(self.xend, self.y0), (self.xend, self.y1)],
            'l': [(self.xend, self.y0), (self.xend, self.y1)],
            '1': [(self.xend, self.y0), (self.xend, self.y1)],  # Rise
            'H': [(self.xend, self.y0), (self.xend, self.y1)],
            'h': [(self.xend, self.y0), (self.xend, self.y1)],
            'z': list(zip(xcurve, [yc-(self.y1-self.y0)/2 for yc in ycurvehf])) + list(zip(xcurve[::-1], [yc+(self.y1-self.y0)/2 for yc in ycurveh[::-1]])),
            'V': [(self.xend, self.y0), (self.xend+self.rise/2, self.yhalf), (self.xend, self.y1)],
            'd': list(zip(xcurve, ycurve))[::-1],
            'u': list(zip(xcurve, ycurvef)),
            '-': [(self.xend, self.y0), (self.xend, self.y1)],
            'n': [(self.xend, self.y0), (self.xend, self.y1)],
            'p': [(self.xend, self.y0), (self.xend, self.y1)],
            'N': [(self.xend, self.y0), (self.xend, self.y1)],
            'P': [(self.xend, self.y0), (self.xend, self.y1)],
            }.get(nstate)
        return verts

    def fillcolor(self):
        fill = {#'x': '#DDDDDD',   # TODO: HATCH
                '3': '#feffc2',
                '4': '#ffe2ba',
                '5': '#abd9ff',
                '6': '#bdfbff',
                '7': '#bdffcb',
                '8': '#e3a5fa',
                '9': '#f7b7bd'}.get(self.params.get('state', '2'), None)
        ukwargs = self.kwargs.copy()
        ukwargs['fill'] = fill
        return ukwargs

    def segments(self):
        ukwargs = self.fillcolor()
        if self.params['state'] == 'x':
            ukwargs['hatch'] = True

        segments = []
        if self.nstate in '-|' and self.pstate in '-|':  # Open both ends. Draw two lines and a poly
            ukwargs['color'] = 'none'
            segments.append(Segment([(self.x0, self.y0), (self.xend, self.y0)], **self.kwargs))
            segments.append(Segment([(self.x0, self.y1), (self.xend, self.y1)], **self.kwargs))
            segments.append(SegmentPoly([(self.x0, self.y0), (self.xend, self.y0),
                                              (self.xend, self.y1), (self.x0, self.y1)], **ukwargs))
        elif self.pstate in '-|':  # Open left end
            segments.append(SegmentPoly([(self.x0, self.y0)] + self.verts_out() + [(self.x0, self.y1)], closed=False, **ukwargs))

        elif self.nstate in '-|':  # Open right end
            segments.append(SegmentPoly([(self.xend, self.y1)] + self.verts_in() + [(self.xend, self.y0)], closed=False, **ukwargs))

        else:
            segments.append(SegmentPoly(self.verts_in()+self.verts_out(), **ukwargs))

        if self.params.get('data', None) and self.params.get('state', None) != 'x':
            segments.append(SegmentText((self.xtext, self.yhalf), self.params['data'][0],
                                         fontsize=11, align=('center', 'center')))
            self.params['data'].pop(0)
        return segments
    
    
class WaveU(Wave1):
    def verts_in(self):
        xcurve, yexp = expcurve((self.y1-self.y0))
        xcurve = [self.x0+xc*self.rise*6 for xc in xcurve]
        ycurvef = [self.y1-yc for yc in yexp]    # Flipped
        ycurvehf = [self.y1-yc/2 for yc in yexp] # Flipped half
        verts = {'-': [(self.x0, self.y1)],
                 '0': list(zip(xcurve, ycurvef)),
                 '1': [(self.x0, self.y1)],
                 'z': list(zip(xcurve, ycurvehf)),
                 'V': [(self.xrise, self.y1)],   # V gets the curve on output
                }.get(self.plevel)
        return verts

    def segments(self):
        verts = self.verts_in()
        segments = [
            Segment(verts, **self.kwargs),
            Segment([verts[-1], (self.xend, self.y1)], ls=':', **self.kwargs)]
        return segments

class WaveD(Wave0):
    def verts_in(self):
        xcurve, yexp = expcurve((self.y1-self.y0))
        xcurve = [self.x0+xc*self.rise*6 for xc in xcurve]
        ycurve = [self.y0+yc for yc in yexp]     # Exp fall
        ycurveh = [self.y0+yc/2 for yc in yexp]  # Half exp fall
        ycurvef = [self.y1-yc for yc in yexp]    # Flipped
        ycurvehf = [self.y1-yc/2 for yc in yexp] # Flipped half
        verts = {'-': [(self.x0, self.y0)],
                 '0': [(self.x0, self.y0)],
                 '1': list(zip(xcurve, ycurve)),
                 'z': list(zip(xcurve, ycurveh)),
                 'V': [(self.x0, self.y0)],
                }.get(self.plevel)
        return verts

    def segments(self):
        verts = self.verts_in()
        segments = [
            Segment(verts, **self.kwargs),
            Segment([verts[-1], (self.xend, self.y0)], ls=':', **self.kwargs)]
        return segments
    
    
class WaveClk(Wave0):
    def verts_in(self):
        state = self.params['state']
        period = self.params['period']
        yh, yl = self.y1, self.y0
        if state in 'nN': yh, yl = yl, yh

        verts = []
        for p in range(self.params['periods']):            
            verts.extend([(self.x0+period*p, yl), (self.x0+period*p, yh),
                          (self.x0+period*p+period/2, yh), (self.x0+period*p+period/2, yl),
                         ])
        if ((self.params['state'] in 'nN' and self.params['pstate'] in 'lL') or
            (self.params['state'] in 'pP' and self.params['pstate'] in 'hH')):
            verts = verts[1:]  # No blip at beginning
        return verts

    def verts_out(self):
        yh, yl = self.y1, self.y0
        if self.params['state'] in 'nN': yh, yl = yl, yh
        return [(self.xend, yl)]

    def segments(self):
        segments = super().segments()
        if self.params['state'] in 'NP':
            period = self.params['period']
            periods = self.params['periods']
            hlength = .25
            hwidth = .12
            yhead = self.yhalf - hlength/2
            ytail = self.yhalf + hlength/2
            if self.params['state'] == 'P':
                yhead, ytail = ytail, yhead
            for p in range(periods):
                xcenter = self.x0 + period*p
                segments.append(SegmentArrow((xcenter, ytail), (xcenter, yhead),
                                        headwidth=hwidth, headlength=hlength))
        return segments
        
    
class TimingDiagram(Element):
    def __init__(self, wave: dict[str, str], **kwargs):
        super().__init__(**kwargs)
        self.wave = wave

        kwargs.setdefault('lw', 1)
        width = .5
        ysep = .3
        risetime = .15
        
        signals = self.wave.get('signal', [])

        totheight = (width+ysep)*len(signals)
        totperiods = max(len(w.get('wave', [])) for w in signals)
        for p in range(totperiods+1):
            self.segments.append(Segment([(p*2*width, width+ysep/2), (p*2*width, width-totheight)],
                                         ls=':', lw=1, color='#DDDDDD', zorder=0))

        clipbox = BBox(0, width, totperiods*width*2, -totheight)
        kwargs['clip'] = clipbox

        y0 = 0
        for signal in signals:            
            name = signal.get('name', '')
            wave = signal.get('wave', '')
            data = signal.get('data', [])
            phase = signal.get('phase', 0)
            period = 2*width*signal.get('period', 1)
            halfperiod = period/2
            textpad = .2
            
            if not isinstance(data, list):
                data = data.split()  # Sometimes it's a space-separated string...

            x = 0
            y1 = y0 + width
            i = 0
            pstate = '-'

            self.segments.append(SegmentText((x-textpad, y0), name, align=('right', 'bottom'),
                                             fontsize=12, color='blue'))
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
                nstate = wave[k] if k<len(wave) else '-'

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
                    self.segments.extend(getsplit(x + (split+1)*period-period/2, y0, y1))

                pstate = state # if not split else pstate
                x += periods*period
                i = k
            y0 -= (width+ysep)
                                              
    @classmethod
    def from_json(cls, wave: str):
        # Source for cleaning up JSON: https://stackoverflow.com/a/61783377/13826284
        tokens = tokenize.generate_tokens(io.StringIO(wave).readline)
        modified_tokens = (
            (tokenize.STRING, repr(token.string)) if token.type == tokenize.NAME else token[:2]
            for token in tokens)

        fixed_input = tokenize.untokenize(modified_tokens)
        return cls(ast.literal_eval(fixed_input))
        

                
