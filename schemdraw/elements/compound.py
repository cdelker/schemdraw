''' Compound elements made from groups of other elements '''

from __future__ import annotations
from typing import Optional, Sequence, Union

from ..import elements as elm
from ..types import Point
from .. import drawing_stack


class ElementCompound(elm.Element):
    ''' Element onto which other elements can be added like a drawing '''
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.dwgparams = {'unit': kwargs.get('unit', 3),
                          'font': kwargs.get('font', None),
                          'fontsize': kwargs.get('fontsize', 14),
                          'lblofst': kwargs.get('lblofst', .1),
                          'color': kwargs.get('color', 'black'),
                          'lw': kwargs.get('lw', 2),
                          'ls': kwargs.get('ls', '-'),
                          'fill': kwargs.get('fill', 'none')}
        self._here: Point = Point((0, 0))
        self._theta: float = 0
        self.elements: list[elm.Element] = []

        pause_state = drawing_stack.pause
        drawing_stack.pause = True
        self.setup()
        drawing_stack.pause = pause_state

    def __contains__(self, element):
        return element in self.elements
        
    def move_from(self, xy: Point, dx: float = 0, dy: float = 0, theta: Optional[float] = None) -> None:
        ''' Move relative to xy position '''
        xy = Point(xy)
        self._here = Point((xy.x + dx, xy.y + dy))
        if theta is not None:
            self._theta = theta

    def move(self, dx: float = 0, dy: float = 0) -> None:
        ''' Move relative to current position '''
        self._here = Point((self._here.x + dx, self._here.y + dy))

    def add(self, element: elm.Element) -> elm.Element:
        ''' Add an element to the segments list '''
        self.elements.append(element)
        self._here, self._theta = element._place(self._here, self._theta, **self.dwgparams)
        self.segments.extend([s.xform(element.transform, **element.params)
                              for s in element.segments])
        return element


class Optocoupler(ElementCompound):
    ''' Optocoupler element

        Args:
            box: Draw a box around the optocoupler
            boxfill: Color to fill the box
            boxpad: Padding between phototransistor and box
            base: Add a base contact to the phototransistor

        Anchors:
            * anode
            * cathode
            * emitter
            * collector
            * base (if base==True)
    '''
    def __init__(self, box: bool = True, boxfill: str = 'none',
                 boxpad: float = 0.2, base: bool = False, **kwargs):
        self.unit = 1.5
        self.box = box
        self.boxfill = boxfill
        self.boxpad = boxpad
        self.base = base
        super().__init__(unit=self.unit, **kwargs)
    
    def setup(self):
        D = self.add(elm.Diode(d='d'))
        bjt = elm.BjtNpn(d='r', at=(1, -self.unit/2))
        bjt.segments.pop(0)  # Remove base contact
        B = self.add(bjt)
        self.add(elm.Arrow(d='r', at=(.5, -self.unit/2 + .2), l=.6,
                           arrowwidth=.15, arrowlength=.2))
        self.add(elm.Arrow(d='r', at=(.5, -self.unit/2 - .2), l=.6,
                           arrowwidth=.15, arrowlength=.2))

        bbox = self.get_bbox()
        if self.box:
            self.add(elm.Rect(
                d='r', at=(0, 0),
                corner1=(bbox.xmin-self.boxpad, bbox.ymin-self.boxpad),
                corner2=(bbox.xmax+self.boxpad, bbox.ymax+self.boxpad),
                fill=self.boxfill, zorder=0))

        if self.base:
            self.add(elm.Line(d='l', at=Point((B.get_bbox(transform=True).xmin, D.center[1])), l=.15))  # type: ignore
            E = self.add(elm.Line(d='d', toy=bbox.ymax+self.boxpad))
            self.anchors['base'] = E.end

        A = self.add(elm.Line(d='r', at=bjt.collector, l=self.boxpad))
        B = self.add(elm.Line(d='r', at=bjt.emitter, l=self.boxpad))
        C = self.add(elm.Line(d='l', at=D.start, tox=bbox.xmin-self.boxpad))
        D = self.add(elm.Line(d='l', at=D.end, tox=bbox.xmin-self.boxpad))
        self.anchors['anode'] = C.end
        self.anchors['cathode'] = D.end
        self.anchors['emitter'] = B.end
        self.anchors['collector'] = A.end


class Relay(ElementCompound):
    ''' Relay element with an inductor and switch

        Args:
            unit: Unit length of the inductor
            cycloid: Use cycloid style inductor
            switch: Switch style 'spst', 'spdt', 'dpst', 'dpdt'
            swreverse: Reverse the switch
            swflip: Flip the switch up/down
            core: Show inductor core bar
            link: Show dotted line linking inductor and switch
            box: Draw a box around the relay
            boxfill: Color to fill the box
            boxpad: Spacing between components and box
    '''
    def __init__(self, unit: float = 2, cycl: bool = False, switch: str = 'spst',
                 core: bool = True, box: bool = True, boxfill: str = 'none',
                 boxpad: float = .25, swreverse: bool = False,
                 swflip: bool = False, link: bool = True, **kwargs):
        self.unit = unit
        self.cycl = cycl
        self.switch = switch
        self.core = core
        self.box = box
        self.boxfill = boxfill
        self.boxpad = boxpad
        self.swreverse = swreverse
        self.swflip = swflip
        self.link = link
        super().__init__(unit=unit, **kwargs)

    def setup(self) -> None:
        if self.cycl:
            L = self.add(elm.Inductor2(d='d'))
        else:
            L = self.add(elm.Inductor(d='d'))

        self.anchors['in1'] = L.start
        self.anchors['in2'] = L.end

        Lleft = L.get_bbox(transform=True).xmax
        swleft = Lleft + .6
        if self.core:
            self.add(elm.Line(d='d', at=(Lleft+.15, -self.unit/2),
                              anchor='center', l=1))
            swleft += .1

        SW: Union[elm.Switch, elm.SwitchSpdt2, elm.SwitchDpst, elm.SwitchDpdt]
        if self.switch == 'spst':
            SW = elm.Switch(d='d', reverse=self.swreverse, flip=self.swflip)
            bbox = SW.get_bbox()
            SW._userparams['at'] = (swleft-(-bbox.ymax if self.swflip else bbox.ymin), 0)
            self.add(SW)
            self.anchors['a'] = SW.start
            self.anchors['b'] = SW.end

        elif self.switch == 'spdt':
            SW = elm.SwitchSpdt2(d='d', reverse=self.swreverse, flip=self.swflip)
            bbox = SW.get_bbox()
            SW._userparams['at'] = (swleft-(-bbox.ymax if self.swflip else bbox.ymin), -.5)
            self.add(SW)
            toy = -self.unit if self.swreverse else 0
            a = self.add(elm.Line(d='d' if self.swreverse else 'u', at=SW.a, toy=toy))
            toy = 0 if self.swreverse else -self.unit
            b = self.add(elm.Line(d='u' if self.swreverse else 'd', at=SW.b, toy=toy))
            c = self.add(elm.Line(d='u' if self.swreverse else 'd', at=SW.c, toy=toy))
            self.anchors['a'] = a.end
            self.anchors['b'] = b.end
            self.anchors['c'] = c.end

        elif self.switch == 'dpst':
            SW = elm.SwitchDpst(d='d', link=False, reverse=self.swreverse, flip=self.swflip)
            bbox = SW.get_bbox()
            SW._userparams['at'] = (swleft-(-bbox.ymax if self.swflip else bbox.ymin), -.5)
            self.add(SW)
            toy = 0 if self.swreverse else -self.unit
            t1 = self.add(elm.Line(d='u' if self.swreverse else 'd', at=SW.t1, toy=toy))
            t2 = self.add(elm.Line(d='u' if self.swreverse else 'd', at=SW.t2, toy=toy))
            toy = -self.unit if self.swreverse else 0
            p1 = self.add(elm.Line(d='d' if self.swreverse else 'u', at=SW.p1, toy=toy))
            p2 = self.add(elm.Line(d='d' if self.swreverse else 'u', at=SW.p2, toy=toy))
            self.anchors['t1'] = t1.end
            self.anchors['t2'] = t2.end
            self.anchors['p1'] = p1.end
            self.anchors['p2'] = p2.end

        elif self.switch == 'dpdt':
            SW = elm.SwitchDpdt(d='d', link=False, reverse=self.swreverse, flip=self.swflip)
            bbox = SW.get_bbox()
            SW._userparams['at'] = (swleft-(-bbox.ymax if self.swflip else bbox.ymin), -.5)
            self.add(SW)
            toy = 0 if self.swreverse else -self.unit
            t1 = self.add(elm.Line(d='u' if self.swreverse else 'd', at=SW.t1, toy=toy))
            t2 = self.add(elm.Line(d='u' if self.swreverse else 'd', at=SW.t2, toy=toy))
            t3 = self.add(elm.Line(d='u' if self.swreverse else 'd', at=SW.t3, toy=toy))
            t4 = self.add(elm.Line(d='u' if self.swreverse else 'd', at=SW.t4, toy=toy))
            toy = -self.unit if self.swreverse else 0
            p1 = self.add(elm.Line(d='d' if self.swreverse else 'u', at=SW.p1, toy=toy))
            p2 = self.add(elm.Line(d='d' if self.swreverse else 'u', at=SW.p2, toy=toy))
            self.anchors['t1'] = t1.end
            self.anchors['t2'] = t2.end
            self.anchors['t3'] = t3.end
            self.anchors['t4'] = t4.end
            self.anchors['p1'] = p1.end
            self.anchors['p2'] = p2.end

        if self.link:
            tox = SW.get_bbox().ymax if self.swflip else SW.get_bbox().ymin
            self.add(elm.Line(d='r', at=(Lleft+.2, -self.unit/2), ls=':', tox=tox))

        if self.box:
            bbox = self.get_bbox()
            self.add(elm.Rect(d='r', at=(0, 0),
                              corner1=(bbox.xmin-self.boxpad, bbox.ymin+.2),
                              corner2=(bbox.xmax+self.boxpad, bbox.ymax-.2),
                              fill=self.boxfill, zorder=0))


class Wheatstone(ElementCompound):
    ''' Wheatstone Resistor Bridge

        Args:
            vout: draw output terminals inside the bridge
            labels: Labels to draw on each resistor

        Anchors:
            * N
            * S
            * E
            * W
            * vo1 (if vout==True)
            * vo2 (if vout==True)
    '''
    def __init__(self, vout: bool = False, labels: Optional[Sequence[str]] = None, **kwargs):
        self.vout = vout
        self.labels = labels
        super().__init__(**kwargs)

    def setup(self):
        A = elm.Resistor().theta(45)
        B = elm.Resistor().theta(-45)
        C = elm.Resistor().theta(-135)
        D = elm.Resistor().theta(135)

        locs = ['top', 'top', 'bottom', 'bottom']
        if self.labels:
            for label, r, loc in zip(self.labels, [A, B, C, D], locs):
                r.label(label, loc)

        self.add(A)
        self.add(B)
        self.add(C)
        self.add(D)
        if self.vout:
            self.add(elm.Line().right().at(A.start).length(1))
            vo1 = self.add(elm.Dot(open=True))
            self.add(elm.Line().left().at(C.start).length(1))
            vo2 = self.add(elm.Dot(open=True))
            self.anchors['vo1'] = vo1.center
            self.anchors['vo2'] = vo2.center

        self.anchors['W'] = A.start
        self.anchors['N'] = B.start
        self.anchors['E'] = C.start
        self.anchors['S'] = D.start
        self.params['theta'] = 0


class Rectifier(ElementCompound):
    ''' Diode Rectifier Bridge

        Args:
            fill: Fill the didoes
            labels: Labels to draw on each resistor

        Anchors:
            * N
            * S
            * E
            * W
    '''
    def __init__(self, fill=False, labels=None, **kwargs):
        self.fill = fill
        self.labels = labels
        super().__init__(**kwargs)

    def setup(self):
        A = elm.Diode(fill=self.fill).theta(45)
        B = elm.Diode(fill=self.fill).theta(-45)
        C = elm.Diode(fill=self.fill).theta(-135).reverse()
        D = elm.Diode(fill=self.fill).theta(135).reverse()

        locs = ['top', 'top', 'bottom', 'bottom']
        if self.labels:
            for label, d, loc in zip(self.labels, [A, B, C, D], locs):
                d.label(label, loc)

        self.add(A)
        self.add(B)
        self.add(C)
        self.add(D)
        self.anchors['W'] = A.start
        self.anchors['N'] = B.start
        self.anchors['E'] = C.start
        self.anchors['S'] = D.start
        self.params['theta'] = 0
