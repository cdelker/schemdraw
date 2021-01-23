''' Outlets/Plugs from various countries

    Reference: https://www.worldstandards.eu/electricity/plugs-and-sockets/
'''
import math

from schemdraw.segments import Segment, SegmentPoly, SegmentCircle
from schemdraw.elements import Element
from schemdraw.util import linspace, rotate

_outletrad = 1.1


class OutletA(Element):
    ''' Outlet Style A (Ungrounded, North America)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        self._outletrad = 1.5
        th = linspace(math.pi*3/4, math.pi*5/4)
        xleft = [.15 + self._outletrad * math.cos(t) for t in th]
        yleft = [self._outletrad * math.sin(t) for t in th]
        xrght = [-.15 + -self._outletrad * math.cos(t) for t in th]
        yrght = [-self._outletrad * math.sin(t) for t in th]
        x = xleft + xrght
        y = yleft + yrght
        self.segments.append(SegmentPoly(list(zip(x, y))))

        pinw = self._outletrad/8
        pinh = pinw*3
        pinhn = pinh*1.25
        pintop = pinh/2
        pintopn = pinhn/2
        pinleft = self._outletrad/2.2
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentPoly(((-pinleft, pintopn),
                                          (-pinleft, pintopn-pinhn),
                                          (-pinleft+pinw, pintopn-pinhn),
                                          (-pinleft+pinw, pintopn)),
                                         fill=fill, zorder=3))
        self.segments.append(SegmentPoly(((pinleft, pintop),
                                          (pinleft, pintop-pinh),
                                          (pinleft-pinw, pintop-pinh),
                                          (pinleft-pinw, pintop)),
                                         fill=fill, zorder=3))
        self.anchors['hot'] = (pinleft-pinw/2, 0)
        self.anchors['neutral'] = (-pinleft+pinw/2, 0)
        self.params['drop'] = (pinleft-pinw/2, 0)


class OutletB(OutletA):
    ''' Outlet Style B (Grounded, North America)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, plug=plug, **kwargs)
        gndw = self._outletrad/4
        gndy = -self._outletrad/2.5
        x = [-gndw/2, -gndw/2, gndw/2, gndw/2]  # Flat part
        y = [gndy, gndy-gndw/2, gndy-gndw/2, gndy]
        theta = linspace(0, math.pi)
        xarc = [gndw/2 * math.cos(t) for t in theta]
        yarc = [gndy + gndw/2 * math.sin(t) for t in theta]
        x.extend(xarc)
        y.extend(yarc)
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentPoly((list(zip(x, y))), fill=fill, zorder=3))
        # Move prongs up a bit
        dy = gndw/2
        self.segments[1].verts = [(x, y+dy) for x, y in self.segments[1].verts]  # type: ignore
        self.segments[2].verts = [(x, y+dy) for x, y in self.segments[2].verts]  # type: ignore
        self.anchors['hot'] = self.anchors['hot'][0], self.anchors['hot'][1] + dy
        self.anchors['neutral'] = self.anchors['neutral'][0], self.anchors['neutral'][1] + dy
        self.anchors['ground'] = (0, gndy)


class OutletC(Element):
    ''' Outlet Style C (Ungrounded, Europe, South America, Asia)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentCircle((0, 0), _outletrad))
        prad = _outletrad/8
        x = _outletrad/2
        self.segments.append(SegmentCircle((-x, 0), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((x, 0), prad, fill=fill, zorder=3))
        self.anchors['hot'] = (x, 0)
        self.anchors['neutral'] = (-x, 0)
        self.params['drop'] = self.anchors['hot']

class OutletD(Element):
    ''' Outlet Style D (India)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentCircle((0, 0), _outletrad))
        prad = _outletrad/8
        x = _outletrad/2
        y = -_outletrad/4
        y2 = _outletrad/2.5
        self.segments.append(SegmentCircle((-x, y), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((x, y), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((0, y2), prad*1.2, fill=fill, zorder=3))
        self.anchors['hot'] = (x, y)
        self.anchors['neutral'] = (-x, y)
        self.anchors['ground'] = (0, y2)
        self.params['drop'] = self.anchors['ground']


class OutletE(Element):
    ''' Outlet Style D (France, Belgium, Poland, ...)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentCircle((0, 0), _outletrad))
        prad = _outletrad/8
        x = _outletrad/2
        y = 0
        y2 = _outletrad/2
        self.segments.append(SegmentCircle((-x, y), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((x, y), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((0, y2), prad, fill=fill, zorder=3))
        self.anchors['hot'] = (x, y)
        self.anchors['neutral'] = (-x, y)
        self.anchors['ground'] = (0, y2)
        self.params['drop'] = self.anchors['neutral']


class OutletF(OutletC):
    ''' Outlet Style F (Europe, Russia)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, plug=plug, **kwargs)
        fill = 'black' if plug else 'bg'
        notchw = _outletrad/8
        notchH = _outletrad/6
        y = _outletrad - .05
        y2 = -_outletrad + .05
        self.segments.append(Segment(((-notchw, y), (-notchw, y-notchH),
                                      (notchw, y-notchH), (notchw, y)),
                                     fill=fill, zorder=3))
        self.segments.append(Segment(((-notchw, y2), (-notchw, y2+notchH),
                                      (notchw, y2+notchH), (notchw, y2)),
                                     fill=fill, zorder=3))


class OutletG(Element):
    ''' Outlet Style G (U.K.)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentCircle((0, 0), _outletrad))
        pinw = _outletrad/6
        pinh = pinw*3
        gndw = _outletrad/5
        gndtop = _outletrad*3/4
        y = -_outletrad/2.5
        pinleft = pinw
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentPoly(((-gndw/2, gndtop), (-gndw/2, gndtop-pinh),
                                          (gndw/2, gndtop-pinh), (gndw/2, gndtop)),
                                        fill=fill, zorder=3))
        self.segments.append(SegmentPoly(((-pinleft, y), (-pinleft, y-pinw),
                                          (-pinleft-pinh, y-pinw), (-pinleft-pinh, y)),
                                         fill=fill, zorder=3))
        self.segments.append(SegmentPoly(((pinleft, y), (pinleft, y-pinw),
                                          (pinleft+pinh, y-pinw), (pinleft+pinh, y)),
                                         fill=fill, zorder=3))
        self.anchors['hot'] = (pinleft+pinh/2, y-pinw/2)
        self.anchors['neutral'] = (-pinleft-pinh/2, y-pinw/2)
        self.anchors['ground'] = (0, gndtop-pinh/2)
        self.params['drop'] = self.anchors['hot']


class OutletH(Element):
    ''' Outlet Style H (Israel)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentCircle((0, 0), _outletrad))
        pinw = _outletrad/8
        pinh = pinw*3
        gndtop = -pinw*2
        verts = ((-pinw/2, gndtop), (-pinw/2, gndtop-pinh), (pinw/2, gndtop-pinh), (pinw/2, gndtop))
        hotverts = [rotate(v, 120) for v in verts]
        neutverts = [rotate(v, -120) for v in verts]
        self.segments.append(SegmentPoly(verts, fill=fill, zorder=3))
        self.segments.append(SegmentPoly(hotverts, fill=fill, zorder=3))
        self.segments.append(SegmentPoly(neutverts, fill=fill, zorder=3))
        self.anchors['hot'] = (hotverts[1])
        self.anchors['neutral'] = (neutverts[2])
        self.anchors['ground'] = (0, gndtop-pinh)
        self.params['drop'] = self.anchors['hot']


class OutletI(OutletH):
    ''' Outlet Style I (Australia, New Zealand, China)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, plug=plug, **kwargs)
        hotcenter = (.4, .3)
        neutcenter = (-.4, .3)
        self.segments[2].verts = [rotate(v, 90, center=hotcenter) for v in self.segments[2].verts]  # type: ignore
        self.segments[3].verts = [rotate(v, -90, center=neutcenter) for v in self.segments[3].verts]  # type: ignore
        self.anchors['hot'] = rotate(self.anchors['hot'], 90, center=hotcenter)
        self.anchors['neutral'] = rotate(self.anchors['neutral'], -90, center=neutcenter)


class OutletJ(Element):
    ''' Outlet Style J (Switzerland)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'black' if plug else 'bg'
        fullh = _outletrad*1.5
        fullw = fullh*2
        dw = fullw/5
        self.segments.append(SegmentPoly(((-fullw/2, 0), (-fullw/2+dw, fullh/2),
                                          (fullw/2-dw, fullh/2), (fullw/2, 0),
                                          (fullw/2-dw, -fullh/2),
                                          (-fullw/2+dw, -fullh/2))))
        prad = _outletrad/8
        self.segments.append(SegmentCircle((-fullw/4, 0), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((0, -prad*2), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((fullw/4, 0), prad, fill=fill, zorder=3))
        self.anchors['hot'] = (fullw/4, 0)
        self.anchors['neutral'] = (-fullw/4, 0)
        self.anchors['ground'] = (0, -prad*2)
        self.params['drop'] = self.anchors['hot']


class OutletK(Element):
    ''' Outlet Style K (Denmark, Greenland)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'black' if plug else 'bg'
        self.segments.append(SegmentCircle((0, 0), _outletrad))
        prad = _outletrad/8
        prongx = _outletrad/2
        self.segments.append(SegmentCircle((-prongx, 0), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((prongx, 0), prad, fill=fill, zorder=3))
        self.anchors['hot'] = (prongx, 0)
        self.anchors['neutral'] = (-prongx, 0)
        self.params['drop'] = (prongx, 0)
        gndw = _outletrad/4
        gndy = -_outletrad/2
        x = [-gndw/2, -gndw/2, gndw/2, gndw/2]  # Flat part
        y = [gndy, gndy+gndw/2, gndy+gndw/2, gndy]
        theta = linspace(0, math.pi)
        xarc = [gndw/2 * math.cos(t) for t in theta]
        yarc = [gndy - gndw/2 * math.sin(t) for t in theta]
        x.extend(xarc)
        y.extend(yarc)
        self.segments.append(SegmentPoly(list(zip(x, y)), fill=fill, zorder=3))
        self.anchors['ground'] = (0, gndy)


class OutletL(Element):
    ''' Outlet Style L (Italy, Chile)

        Args:
            plug: Fill the prongs

        Anchors:
            * hot
            * neutral
            * ground
    '''
    def __init__(self, *d, plug: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        fill = 'black' if plug else 'bg'
        fullh = _outletrad*1.2
        fullw = fullh*2.25
        self.segments.append(SegmentPoly(((-fullw/2, fullh/2), (fullw/2, fullh/2),
                                          (fullw/2, -fullh/2), (-fullw/2, -fullh/2))))
        prad = _outletrad/8
        self.segments.append(SegmentCircle((-fullw/4, 0), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((0, 0), prad, fill=fill, zorder=3))
        self.segments.append(SegmentCircle((fullw/4, 0), prad, fill=fill, zorder=3))
        self.anchors['hot'] = (fullw/4, 0)
        self.anchors['neutral'] = (-fullw/4, 0)
        self.anchors['ground'] = (0, 0)
        self.params['drop'] = self.anchors['hot']
