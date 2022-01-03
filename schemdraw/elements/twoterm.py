''' Two-terminal element definitions '''

from __future__ import annotations
import math
from typing import Sequence

from .elements import Element, Element2Term, gap
from ..util import Point, linspace
from ..segments import Segment, SegmentArc, SegmentText, SegmentCircle, SegmentPoly


resheight = 0.25      # Resistor height
reswidth = 1.0 / 6   # Full (inner) length of resistor is 1.0 data unit


class ResistorIEEE(Element2Term):
    ''' Resistor (IEEE/U.S. style) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(
            [(0, 0), (0.5*reswidth, resheight), (1.5*reswidth, -resheight),
             (2.5*reswidth, resheight), (3.5*reswidth, -resheight),
             (4.5*reswidth, resheight), (5.5*reswidth, -resheight), (6*reswidth, 0)]))


class ResistorIEC(Element2Term):
    ''' Resistor as box (IEC/European style) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(
            [(0, 0), (0, resheight), (reswidth*6, resheight),
             (reswidth*6, -resheight), (0, -resheight), (0, 0),
             gap, (reswidth*6, 0)]))



class ResistorVarIEEE(ResistorIEEE):
    ''' Variable resistor (U.S. style) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        super().__init__(**kwargs)
        self.segments.append(Segment([(1.5*reswidth, -resheight*2), (4.5*reswidth, reswidth*3.5)],
                                     arrow='->', arrowwidth=.16, arrowlength=.2))


class ResistorVarIEC(ResistorIEC):
    ''' Variable resistor (European style) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(1*reswidth, -resheight*2), (5*reswidth, reswidth*3.5)],
                                     arrow='->', arrowwidth=.16, arrowlength=.2))


class Thermistor(ResistorIEC):
    ''' Thermistor '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, -resheight-.2), (.2, -resheight-.2), (1, resheight+.2)]))


class PhotoresistorIEEE(ResistorIEEE):
    ''' Photo-resistor (U.S. style) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(.7, .75), (.4, .4)], arrow='->',
                                     arrowwidth=.16, arrowlength=.2))
        self.segments.append(Segment([(1, .75), (.7, .4)], arrow='->',
                                     arrowwidth=.16, arrowlength=.2))


class PhotoresistorIEC(ResistorIEC):
    ''' Photo-resistor (European style) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(.7, .75), (.4, .4)], arrow='->', 
                                     arrowwidth=.16, arrowlength=.2))
        self.segments.append(Segment([(1, .75), (.7, .4)], arrow='->',
                                     arrowwidth=.16, arrowlength=.2))


class Capacitor(Element2Term):
    ''' Capacitor (flat plates)

        Args:
            polar: Add polarity + sign
    '''
    def __init__(self, *d, polar: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        capgap = 0.18
        self.segments.append(Segment([(0, 0), gap, (0, resheight), (0, -resheight), gap,
                                     (capgap, resheight), (capgap, -resheight), gap,
                                     (capgap, 0)]))
        if polar:
            self.segments.append(SegmentText((-capgap*1.2, capgap), '+'))


class Capacitor2(Element2Term):
    ''' Capacitor (curved bottom plate)

        Args:
            polar: Add polarity + sign
    '''
    def __init__(self, *d, polar: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        capgap = 0.18
        self.segments.append(Segment([(0, 0), gap, (0, resheight),
                                     (0, -resheight), gap, (capgap, 0)]))
        self.segments.append(SegmentArc((capgap*1.5, 0), width=capgap*1.5,
                                        height=resheight*2.5, theta1=105, theta2=-105))

        if polar:
            self.segments.append(SegmentText((-capgap*1.2, capgap), '+'))


class CapacitorVar(Capacitor):
    ''' Variable capacitor '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(-2*reswidth, -resheight), (3*reswidth, reswidth*2)],
                                     arrow='->', arrowwidth=.2, arrowlength=.2))


class CapacitorTrim(Capacitor):
    ''' Trim capacitor '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        capgap = 0.18
        # Line endpoints
        p1 = Point((-1.8*reswidth, -resheight))
        p2 = Point((1.8*reswidth+capgap, resheight))
        dx = p2.x - p1.x
        dy = p2.y - p1.y

        self.segments.append(Segment([p1, p2]))

        tlen = .14
        theta = math.atan2(dy, dx) + math.radians(90)
        t1 = Point((p2.x + tlen * math.cos(theta),
                    p2.y + tlen * math.sin(theta)))
        t2 = Point((p2.x + tlen * math.cos(theta-math.pi),
                    p2.y + tlen * math.sin(theta-math.pi)))
        self.segments.append(Segment([t1, t2]))


class Crystal(Element2Term):
    ''' Crystal oscillator '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        xgap = 0.2
        self.segments.append(Segment(
            [(0, 0), gap, (0, resheight), (0, -resheight), gap,
             (xgap/2, resheight), (xgap/2, -resheight), (xgap*1.5, -resheight),
             (xgap*1.5, resheight), (xgap/2, resheight), gap,
             (xgap*2, resheight), (xgap*2, -resheight), gap, (xgap*2, 0)]))


class Diode(Element2Term):
    ''' Diode '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), gap, (resheight*1.4, resheight),
                                      (resheight*1.4, -resheight), gap, (resheight*1.4, 0)]))
        self.segments.append(SegmentPoly([(0, resheight), (resheight*1.4, 0), (0, -resheight)]))


class Schottky(Diode):
    ''' Schottky Diode '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        schottky_width = 0.1
        self.segments.append(Segment(
            [(resheight*1.4, resheight),
             (resheight*1.4-schottky_width, resheight),
             (resheight*1.4-schottky_width, resheight-schottky_width)]))
        self.segments.append(Segment(
            [(resheight*1.4, -resheight),
             (resheight*1.4+schottky_width, -resheight),
             (resheight*1.4+schottky_width, -resheight+schottky_width)]))


class DiodeTunnel(Diode):
    ''' Tunnel Diode '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        tunnel_width = 0.1
        self.segments.append(Segment([(resheight*1.4, resheight),
                                      (resheight*1.4-tunnel_width, resheight)]))
        self.segments.append(Segment([(resheight*1.4, -resheight),
                                      (resheight*1.4-tunnel_width, -resheight)]))


class DiodeShockley(Element2Term):
    ''' Shockley Diode '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (resheight*1.4, 0), (resheight*1.4, resheight),
                                      (resheight*1.4, -resheight), gap, (resheight*1.4, 0)]))
        self.segments.append(Segment([(0, -resheight), (0, resheight), (resheight*1.4, 0)]))


class Zener(Diode):
    ''' Zener Diode '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        zener_width = 0.1
        self.segments.append(Segment([(resheight*1.4, resheight),
                                      (resheight*1.4+zener_width, resheight+zener_width)]))
        self.segments.append(Segment([(resheight*1.4, -resheight),
                                      (resheight*1.4-zener_width, -resheight-zener_width)]))


class Varactor(Element2Term):
    ''' Varactor Diode/Varicap/Variable Capacitance Diode '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        capgap = .13
        self.segments.append(Segment([(0, 0), gap, 
                                     (resheight*1.4, resheight), (resheight*1.4, -resheight),
                                     gap,
                                     (resheight*1.4+capgap, resheight), (resheight*1.4+capgap, -resheight),
                                     gap,
                                     (resheight*1.4+capgap, 0)]))
        self.segments.append(SegmentPoly([(0, resheight), (resheight*1.4, 0), (0, -resheight)]))


class LED(Diode):
    ''' Light emitting diode '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(resheight, resheight*1.5), (resheight*2, resheight*3.25)],
                                     arrow='->', arrowwidth=.16, arrowlength=.2))
        self.segments.append(Segment([(resheight*.1, resheight*1.5), (resheight*1.1, resheight*3.25)],
                                     arrow='->', arrowwidth=.16, arrowlength=.2))
        self.params['lblloc'] = 'bot'


class LED2(Diode):
    ''' Light emitting diode (curvy light lines) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        x = linspace(-1, 1)
        y = [-x0*(x0-.7)*(x0+.7)/2 + resheight*2.5 for x0 in x]
        x = linspace(resheight*.75, resheight*1.25)
        
        theta = 20
        p = [Point((x0, y0)).rotate(theta) for x0, y0 in zip(x, y)]
        p2 = [Point((x0-.2, y0)).rotate(theta) for x0, y0 in zip(x, y)]
        
        pa = Point((x[0], y[0]+.1)).rotate(theta)
        pa2 = Point((x[0]-.2, y[0]+.1)).rotate(theta)
        
        self.segments.append(Segment(p))
        self.segments.append(Segment(p2))
        self.segments.append(Segment((p[1], pa), arrow='->', arrowwidth=.15, arrowlength=.2))
        self.segments.append(Segment((p2[1], pa2), arrow='->', arrowwidth=.15, arrowlength=.2))
        self.params['lblloc'] = 'bot'


class Photodiode(Diode):
    ''' Photo-sensitive diode '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        x = linspace(-1, 1)
        y = [-x0*(x0-.7)*(x0+.7)/2 + resheight*2.5 for x0 in x]
        x = linspace(resheight*.75, resheight*1.25)
        theta = 20
        p = [Point((x0, y0)).rotate(theta) for x0, y0 in zip(x, y)]
        p2 = [Point((x0-.2, y0)).rotate(theta) for x0, y0 in zip(x, y)]

        pa = Point((x[-1], y[-1]-.1)).rotate(theta)
        pa2 = Point((x[-1]-.2, y[-1]-.1)).rotate(theta)
        self.segments.append(Segment(p))
        self.segments.append(Segment(p2))
        self.segments.append(Segment((p[-2], pa), arrow='->', arrowwidth=.15, arrowlength=.2))
        self.segments.append(Segment((p2[-2], pa2), arrow='->', arrowwidth=.15, arrowlength=.2))
        self.params['lblloc'] = 'bot'


class PotentiometerIEEE(ResistorIEEE):
    ''' Potentiometer (U.S. style)

        Anchors:
            tap
    '''
    # Ok, this has three terminals, but is works like a two-term with lead extension
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        potheight = .72
        self.anchors['tap'] = (reswidth*3, potheight)
        self.params['lblloc'] = 'bot'
        self.segments.append(Segment([(reswidth*3, potheight), (reswidth*3, reswidth*1.5)],
                                     arrow='->', arrowwidth=.15, arrowlength=.25))


class PotentiometerIEC(ResistorIEC):
    ''' Potentiometer (European style)

        Anchors:
            tap
    '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        potheight = .72
        self.anchors['tap'] = (reswidth*3, potheight)
        self.params['lblloc'] = 'bot'
        self.segments.append(Segment([(reswidth*3, potheight), (reswidth*3, reswidth*2)],
                                     arrow='->', arrowwidth=.15, arrowlength=.22))


class Diac(Element2Term):
    ''' Diac (diode for alternating current) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(
            [(0, 0), gap, (resheight*1.4, resheight*1.8),
             (resheight*1.4, -resheight*1.8), gap,
             (0, resheight*1.8), (0, -resheight*1.8), gap, (resheight*1.4, 0)]))
        self.segments.append(SegmentPoly([(0, -resheight-.25), (resheight*1.4, -.25),
                                          (0, -resheight+.25)]))
        self.segments.append(SegmentPoly([(resheight*1.4, resheight+.25), (0, .25),
                                          (resheight*1.4, resheight-.25)]))


class Triac(Diac):
    ''' Triac

        Anchors:
            gate
    '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(resheight*1.4, .25), (resheight*1.4+.5, .5)]))
        self.anchors['gate'] = (resheight*1.4+.5, .5)


class SCR(Diode):
    ''' Silicon controlled rectifier (or thyristor)

        Anchors:
            gate
    '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(
            [(resheight*1.4, 0), (resheight*1.4+.3, -.3), (resheight*1.4+.3, -.5)]))
        self.anchors['gate'] = (resheight*1.4+.3, -.5)


class Memristor(Element2Term):
    ''' Memristor (resistor with memory) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        mr = 0.2
        self.segments.append(Segment(
            [(0, 0), (mr, 0), (mr, -mr*.75), (mr*2, -mr*.75), (mr*2, mr*.75),
             (mr*3, mr*.75), (mr*3, -mr*.75), (mr*4, -mr*.75), (mr*4, 0),
             (mr*5, 0)]))
        self.segments.append(Segment(
            [(0, mr*1.25), (mr*5, mr*1.25), (mr*5, mr*-1.25), (0, mr*-1.25),
             (0, mr*1.25)]))
        self.segments.append(SegmentPoly(
            [(0, mr*1.25), (0, -mr*1.25), (mr/2, -mr*1.25), (mr/2, mr*1.25)],
            fill='black'))


class Memristor2(Element2Term):
    ''' Memristor (resistor with memory), alternate style '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        mr = 0.2
        mrv = .25
        self.segments.append(Segment(
            [(0, 0), (0, mrv), (mr, mrv), (mr, -mrv), (mr*2, -mrv), (mr*2, mrv),
             (mr*3, mrv), (mr*3, -mrv), (mr*4, -mrv), (mr*4, mrv),
             (mr*5, mrv), (mr*5, -mrv), (mr*6, -mrv), (mr*6, 0),
             (mr*7, 0)]))


class Josephson(Element2Term):
    ''' Josephson Junction '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(
            [(0, 0), gap, (-resheight, resheight), (resheight, -resheight),
             gap, (resheight, resheight), (-resheight, -resheight),
             gap, (0, 0)]))


class FuseUS(Element2Term):
    ''' Fuse (U.S. Style)

        Args:
            dots: Show dots on connections to fuse
    '''
    def __init__(self, *d, dots: bool=True, **kwargs):
        super().__init__(*d, **kwargs)
        fuser = .12
        fusex = linspace(fuser*2, 1+fuser)
        fusey = [math.sin(x) * resheight for x in linspace(0, 2*math.pi)]
        self.segments.append(Segment(list(zip(fusex, fusey))))
        self.segments.append(Segment([(0, 0), gap, (1+fuser*3, 0)]))
        if dots:
            self.fill(kwargs.get('fill', 'bg'))

    def fill(self, color: bool | str=True) -> 'Element':
        ''' Set element fill '''
        fuser = .12
        self.segments.append(SegmentCircle(
            (fuser, 0), fuser, zorder=4, fill=color))
        self.segments.append(SegmentCircle(
            (fuser*2+1, 0), fuser, zorder=4, fill=color))
        super().fill(color)
        return self


class FuseIEEE(ResistorIEC):
    ''' Fuse (IEEE Style) '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (reswidth*6, 0)]))


class FuseIEC(ResistorIEC):
    ''' Fuse (IEC Style) '''    
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        dx = resheight*.66
        self.segments.append(Segment([(dx, resheight), (dx, -resheight)]))
        self.segments.append(Segment([(6*reswidth-dx, resheight),
                                      (6*reswidth-dx, -resheight)]))            


class Breaker(Element2Term):
    ''' Circuit breaker

        Args:
            dots: Show connection dots
    '''
    def __init__(self, *d, dots: bool=True, **kwargs):
        super().__init__(*d, **kwargs)
        theta1 = 25 if dots else 10
        theta2 = 155 if dots else 170
        self.segments.append(Segment(
            [(0, 0), gap, (1, 0)]))
        self.segments.append(SegmentArc(
            (.5, 0), 1, .65, theta1=theta1, theta2=theta2))
        if dots:
            rad = .12
            self.segments.append(SegmentCircle((rad, 0), rad, zorder=4))
            self.segments.append(SegmentCircle((1-rad, 0), rad, zorder=4))


def cycloid(loops: int=4, ofst: Sequence[float]=(0, 0),
            a:float=.06, b:float=.19, norm:bool=True,
            vertical:bool=False,
            flip:bool=False) -> list[tuple[float, float]]:
    ''' Generate a prolate cycloid (inductor spiral) that
        will always start and end at y=0.

        Args:
            loops: Number of loops
            a, b: Parameters. b>a for prolate (loopy) cycloid
            norm: Normalize the length to 1
            vertical: draw vertically (swap x, y)
            flip: flip orientation (invert y)

        Returns:
            List of (x, y) coordinates defining the cycloid
    '''
    yint = math.acos(a/b)  # y-intercept
    t = linspace(yint, 2*(loops+1)*math.pi-yint, num=loops*50)
    x = [a*t0 - b*math.sin(t0) for t0 in t]
    y = [a - b*math.cos(t0) for t0 in t]
    x = [xx - x[0] for xx in x]  # Shift to start at 0,0

    if norm:
        x = [xx / (x[-1]-x[0]) for xx in x]  # Normalize length to 1

    if flip:
        y = [-yy for yy in y]

    y = [yy * (max(y)-min(y))/(resheight) for yy in y]  # Normalize to resistor width

    if vertical:
        x, y = y, x

    x = [xx + ofst[0] for xx in x]
    y = [yy + ofst[1] for yy in y]

    path = list(zip(x, y))
    return path


class Inductor(Element2Term):
    ''' Inductor '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        ind_w = .25
        self.segments.append(Segment([(0, 0), gap, (1, 0)]))
        for i in range(4):
            self.segments.append(SegmentArc(
                [(i*2+1)*ind_w/2, 0], theta1=0, theta2=180,
                width=ind_w, height=ind_w))


class Inductor2(Element2Term):
    ''' Inductor, drawn as cycloid (loopy)

        Args:
            loops: Number of inductor loops
    '''
    def __init__(self, *d, loops: int=4, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(cycloid(loops=loops)))


class CPE(Element2Term):
    ''' Constant Phase Element '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        capgap = 0.25
        offset = 0.25
        self.segments.append(Segment([(0, 0), (-offset, 0), gap, (offset, 0),
                                      (0, -resheight), gap, (capgap, 0)]))
        self.segments.append(Segment([(0, 0), (-offset, 0), gap, (offset, 0),
                                      (0, resheight), gap, (capgap, 0)]))
        self.segments.append(Segment([(0, 0), (-offset, resheight), gap,
                                      (0, -resheight), gap, (capgap, 0)]))
        self.segments.append(Segment([(0, 0), (-offset, -resheight), gap,
                                      (0, -resheight), gap, (capgap, 0)]))


class SparkGap(Element2Term):
    ''' Spark Gap '''
    def __init__(self, *d, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (.3, 0), gap, (.7, 0), (1, 0)]))
        # Arrow coords overlap a bit since default arrow is offset by linewidth
        self.segments.append(Segment([(.3, 0), (.52, 0)], arrow='->', arrowwidth=.2))
        self.segments.append(Segment([(.7, 0), (.48, 0)], arrow='->', arrowwidth=.2))

        
# default to IEEE style
Resistor = ResistorIEEE
ResistorVar = ResistorVarIEEE
Photoresistor = PhotoresistorIEEE
Potentiometer = PotentiometerIEEE
Fuse = FuseIEEE

# Old names
RBox = ResistorIEC
RBoxVar = ResistorVarIEC
PotBox = PotentiometerIEC
PhotoresistorBox = PhotoresistorIEC