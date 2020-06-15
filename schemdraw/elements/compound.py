''' Compound elements made from groups of other elements '''

import numpy as np
import warnings

from ..import elements as elm
from ..adddocs import adddocs


@adddocs(elm.Element)
class ElementCompound(elm.Element):
    ''' Element onto which other elements can be added like a drawing '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dwgparams = {'unit': kwargs.get('unit', 3),
                          'font': kwargs.get('font', 'sans-serif'),
                          'fontsize': kwargs.get('fontsize', 14),
                          'lblofst': kwargs.get('lblofst', .1),
                          'color': kwargs.get('color', 'black'),
                          'lw': kwargs.get('lw', 2),
                          'ls': kwargs.get('ls', '-'),
                          'fill': kwargs.get('fill', False)}
        self._here = np.asarray([0, 0])
        self._theta = 0

    def add(self, element, **kwargs):
        ''' Add the element to the segments list '''
        if not isinstance(element, elm.Element):
            # Instantiate it (for support of legacy add method)            
            element = element(**kwargs)
        elif len(kwargs) > 0:
            warnings.warn('kwargs to add method are ignored because element is already instantiated')

        self._here, self._theta = element.place(self._here, self._theta, **self.dwgparams)
        self.segments.extend([s.xform(element.transform, **element.cparams)
                              for s in element.segments])
        return element


@adddocs(elm.Element)
class Optocoupler(ElementCompound):
    ''' Optocoupler element

        Parameters
        ----------
        box : bool
            Draw a box around the optocoupler
        boxfill : string
            Color to fill the box
        boxpad : float
            Padding between phototransistor and box
        base : bool
            Add a base contact to the phototransistor
    '''
    def __init__(self, *args, **kwargs):
        unit = 1.5
        super().__init__(*args, unit=unit, **kwargs)
        box = kwargs.get('box', True)
        boxfill = kwargs.get('boxfill', False)
        bpad = kwargs.get('boxpad', .2)
        base = kwargs.get('base', False)

        D = self.add(elm.Diode('d'))
        bjt = elm.BjtNpn('r', at=[1, -unit/2])
        bjt.segments.pop(0)  # Remove base contact
        B = self.add(bjt)
        self.add(elm.Arrow('r', at=[.5, -unit/2 + .2], l=.6,
                           headwidth=.15, headlength=.2))
        self.add(elm.Arrow('r', at=[.5, -unit/2 - .2], l=.6,
                           headwidth=.15, headlength=.2))

        bbox = self.get_bbox()
        if box:
            self.add(elm.Rect(
                'r', at=[0, 0],
                corner1=[bbox.xmin-bpad, bbox.ymin-bpad],
                corner2=[bbox.xmax+bpad, bbox.ymax+bpad],
                fill=boxfill, zorder=0))

        if base:
            self.add(elm.Line('l', at=[B.get_bbox(transform=True).xmin, D.center[1]], l=.15))
            E = self.add(elm.Line('d', toy=bbox.ymax+bpad))
            self.anchors['base'] = E.end

        A = self.add(elm.Line('r', at=B.collector, l=bpad))
        B = self.add(elm.Line('r', at=B.emitter, l=bpad))
        C = self.add(elm.Line('l', at=D.start, tox=bbox.xmin-bpad))
        D = self.add(elm.Line('l', at=D.end, tox=bbox.xmin-bpad))
        self.anchors['anode'] = C.end
        self.anchors['cathode'] = D.end
        self.anchors['emitter'] = B.end
        self.anchors['collector'] = A.end


@adddocs(elm.Element)
class Relay(ElementCompound):
    ''' Relay element with an inductor and switch

        Parameters
        ----------
        unit : float
            Unit length of the inductor
        cycloid : bool
            Use cycloid style inductor
        switch : string
            Switch style 'spst', 'spdt', 'dpst', 'dpdt'
        swreverse : bool
            Reverse the switch
        swflip : bool
            Flip the switch
        core : bool
            Show inductor core bar
        link : bool
            Show dotted line linking inductor and switch
        box : bool
            Draw a box around the relay
        boxfill : string
            Color to fill the box
        boxpad : float
            Spacing between components and box
    '''
    def __init__(self, *args, **kwargs):
        unit = kwargs.get('unit', 2)
        cycl = kwargs.get('cycloid', False)
        switch = kwargs.get('switch', 'spst').lower()
        core = kwargs.get('core', True)
        box = kwargs.get('box', True)
        boxfill = kwargs.get('boxfill', False)
        bpad = kwargs.get('boxpad', .25)
        swrev = kwargs.get('swreverse', False)
        swflip = kwargs.get('swflip', False)
        link = kwargs.get('link', True)

        super().__init__(*args, unit=unit, **kwargs)

        if cycl:
            L = self.add(elm.Inductor2('d'))
        else:
            L = self.add(elm.Inductor('d'))

        self.anchors['in1'] = L.start
        self.anchors['in2'] = L.end

        Lleft = L.get_bbox(transform=True).xmax
        swleft = Lleft + .6
        if core:
            self.add(elm.Line('d', at=[Lleft+.15, -unit/2],
                              anchor='center', l=1))
            swleft += .1

        if switch == 'spst':
            SW = elm.Switch('d', reverse=swrev, flip=swflip)
            bbox = SW.get_bbox()
            SW.userparams['at'] = [swleft-(-bbox.ymax if swflip else bbox.ymin), 0]
            self.add(SW)
            self.anchors['a'] = SW.start
            self.anchors['b'] = SW.end

        elif switch == 'spdt':
            SW = elm.SwitchSpdt2('d', reverse=swrev, flip=swflip)
            bbox = SW.get_bbox()
            SW.userparams['at'] = [swleft-(-bbox.ymax if swflip else bbox.ymin), -.5]
            self.add(SW)
            toy = -unit if swrev else 0
            a = self.add(elm.Line('d' if swrev else 'u', at=SW.a, toy=toy))
            toy = 0 if swrev else -unit
            b = self.add(elm.Line('u' if swrev else 'd', at=SW.b, toy=toy))
            c = self.add(elm.Line('u' if swrev else 'd', at=SW.c, toy=toy))
            self.anchors['a'] = a.end
            self.anchors['b'] = b.end
            self.anchors['c'] = c.end

        elif switch == 'dpst':
            SW = elm.SwitchDpst('d', link=False, reverse=swrev, flip=swflip)
            bbox = SW.get_bbox()
            SW.userparams['at'] = [swleft-(-bbox.ymax if swflip else bbox.ymin), -.5]
            self.add(SW)
            toy = 0 if swrev else -unit
            t1 = self.add(elm.Line('u' if swrev else 'd', at=SW.t1, toy=toy))
            t2 = self.add(elm.Line('u' if swrev else 'd', at=SW.t2, toy=toy))
            toy = -unit if swrev else 0
            p1 = self.add(elm.Line('d' if swrev else 'u', at=SW.p1, toy=toy))
            p2 = self.add(elm.Line('d' if swrev else 'u', at=SW.p2, toy=toy))
            self.anchors['t1'] = t1.end
            self.anchors['t2'] = t2.end
            self.anchors['p1'] = p1.end
            self.anchors['p2'] = p2.end

        elif switch == 'dpdt':
            SW = elm.SwitchDpdt('d', link=False, reverse=swrev, flip=swflip)
            bbox = SW.get_bbox()
            SW.userparams['at'] = [swleft-(-bbox.ymax if swflip else bbox.ymin), -.5]
            self.add(SW)
            toy = 0 if swrev else -unit
            t1 = self.add(elm.Line('u' if swrev else 'd', at=SW.t1, toy=toy))
            t2 = self.add(elm.Line('u' if swrev else 'd', at=SW.t2, toy=toy))
            t3 = self.add(elm.Line('u' if swrev else 'd', at=SW.t3, toy=toy))
            t4 = self.add(elm.Line('u' if swrev else 'd', at=SW.t4, toy=toy))
            toy = -unit if swrev else 0
            p1 = self.add(elm.Line('d' if swrev else 'u', at=SW.p1, toy=toy))
            p2 = self.add(elm.Line('d' if swrev else 'u', at=SW.p2, toy=toy))
            self.anchors['t1'] = t1.end
            self.anchors['t2'] = t2.end
            self.anchors['t3'] = t3.end
            self.anchors['t4'] = t4.end
            self.anchors['p1'] = p1.end
            self.anchors['p2'] = p2.end

        if link:
            tox = SW.get_bbox().ymax if swflip else SW.get_bbox().ymin
            self.add(elm.Line('r', at=[Lleft+.2, -unit/2], ls=':', tox=tox))

        if box:
            bbox = self.get_bbox()
            self.add(elm.Rect('r', at=[0, 0],
                              corner1=[bbox.xmin-bpad, bbox.ymin+.2],
                              corner2=[bbox.xmax+bpad, bbox.ymax-.2],
                              fill=boxfill, zorder=0))
