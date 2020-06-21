''' Two-terminal element definitions '''

import numpy as np

from .elements import Element2Term, gap
from ..segments import Segment, SegmentArrow, SegmentArc, SegmentText, SegmentCircle, SegmentPoly
from ..adddocs import adddocs


resheight = 0.25      # Resistor height
reswidth = 1.0 / 6   # Full (inner) length of resistor is 1.0 data unit


class Resistor(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment(
            [[0, 0], [0.5*reswidth, resheight], [1.5*reswidth, -resheight],
             [2.5*reswidth, resheight], [3.5*reswidth, -resheight],
             [4.5*reswidth, resheight], [5.5*reswidth, -resheight], [6*reswidth, 0]]))


class RBox(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment(
            [[0, 0], [0, resheight], [reswidth*6, resheight],
             [reswidth*6, -resheight], [0, -resheight], [0, 0],
             gap, [reswidth*6, 0]]))


class ResistorVar(Resistor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([1.5*reswidth, -resheight*2],
                                          [4.5*reswidth, reswidth*3.5],
                                          headwidth=.12, headlength=.2))


class RBoxVar(RBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([1*reswidth, -resheight*2],
                                          [5*reswidth, reswidth*3.5],
                                          headwidth=.12, headlength=.2))


class Thermistor(RBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, -resheight-.2], [.2, -resheight-.2], [1, resheight+.2]]))


class Photoresistor(Resistor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([.7, .75], [.4, .4],
                                          headwidth=.12, headlength=.2))
        self.segments.append(SegmentArrow([1, .75], [.7, .4],
                                          headwidth=.12, headlength=.2))


class PhotoresistorBox(RBox):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([.7, .75], [.4, .4],
                                          headwidth=.12, headlength=.2))
        self.segments.append(SegmentArrow([1, .75], [.7, .4],
                                          headwidth=.12, headlength=.2))

@adddocs(Element2Term)
class Capacitor(Element2Term):
    ''' Capacitor 2-terminal element.

        Parameters
        ----------
        polar : bool
            Add polarity + sign
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        capgap = 0.18
        self.segments = [Segment([[0, 0], gap, [0, resheight], [0, -resheight], gap,
                                  [capgap, resheight], [capgap, -resheight], gap,
                                  [capgap, 0]])]
        if kwargs.get('polar', False):
            kwargs = dict(kwargs)
            kwargs.pop('label', None)  # Remove existing element label from kwargs
            self.segments.append(SegmentText([-capgap*1.2, capgap], '+'))


@adddocs(Element2Term)
class Capacitor2(Element2Term):
    ''' Capacitor 2-terminal element, with curved side.

        Parameters
        ----------
        polar : bool
            Add polarity + sign
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        capgap = 0.18
        self.segments = [Segment([[0, 0], gap, [0, resheight],
                                  [0, -resheight], gap, [capgap, 0]]),
                         SegmentArc([capgap*1.5, 0], width=capgap*1.5,
                                    height=resheight*2.5, theta1=105, theta2=-105)]

        if kwargs.get('polar', False):
            self.segments.append(SegmentText([-capgap*1.2, capgap], '+'))


class CapacitorVar(Capacitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([-2*reswidth, -resheight],
                                          [3*reswidth, reswidth*2],
                                          headwidth=.12, headlength=.2))


class CapacitorTrim(Capacitor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        capgap = 0.18
        self.segments.append(SegmentArrow([-1.8*reswidth, -resheight], [1.8*reswidth+capgap, resheight],
                                         headlength=.0001, headwidth=.3))


class Crystal(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        xgap = 0.2
        self.segments = [Segment(
            [[0, 0], gap, [0, resheight], [0, -resheight], gap,
             [xgap/2, resheight], [xgap/2, -resheight], [xgap*1.5, -resheight],
             [xgap*1.5, resheight], [xgap/2, resheight], gap,
             [xgap*2, resheight], [xgap*2, -resheight], gap, [xgap*2, 0]])]


class Diode(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments = [Segment([[0, 0], gap, [resheight*1.4, resheight],
                                  [resheight*1.4, -resheight], gap, [resheight*1.4, 0]]),
                         SegmentPoly([[0, resheight], [resheight*1.4, 0], [0, -resheight]])]


class Schottky(Diode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        schottky_width = 0.1
        self.segments.append(Segment(
            [[resheight*1.4, resheight],
             [resheight*1.4-schottky_width, resheight],
             [resheight*1.4-schottky_width, resheight-schottky_width]]))
        self.segments.append(Segment(
            [[resheight*1.4, -resheight],
             [resheight*1.4+schottky_width, -resheight],
             [resheight*1.4+schottky_width, -resheight+schottky_width]]))


class DiodeTunnel(Diode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        tunnel_width = 0.1
        self.segments.append(Segment([[resheight*1.4, resheight],
                                      [resheight*1.4-tunnel_width, resheight]]))
        self.segments.append(Segment([[resheight*1.4, -resheight],
                                      [resheight*1.4-tunnel_width, -resheight]]))


class DiodeShockley(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[0, 0], [resheight*1.4, 0], [resheight*1.4, resheight],
                                      [resheight*1.4, -resheight], gap, [resheight*1.4, 0]]))
        self.segments.append(Segment([[0, -resheight], [0, resheight], [resheight*1.4, 0]]))


class Zener(Diode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        zener_width = 0.1
        self.segments.append(Segment([[resheight*1.4, resheight],
                                      [resheight*1.4+zener_width, resheight+zener_width]]))
        self.segments.append(Segment([[resheight*1.4, -resheight],
                                      [resheight*1.4-zener_width, -resheight-zener_width]]))


class LED(Diode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(SegmentArrow([resheight, resheight*1.5],
                                          [resheight*2, resheight*3.25],
                                          headwidth=.12, headlength=.2))
        self.segments.append(SegmentArrow([resheight*.1, resheight*1.5],
                                          [resheight*1.1, resheight*3.25],
                                          headwidth=.12, headlength=.2))
        self.params['lblloc'] = 'bot'


class LED2(Diode):  # LED with squiggly light lines
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x = np.linspace(-1, 1)
        y = -x*(x-.7)*(x+.7)/2 + resheight*2.5
        x = np.linspace(resheight*.75, resheight*1.25)
        theta = 20
        c = np.cos(np.radians(theta))
        s = np.sin(np.radians(theta))
        m = np.array([[c, s], [-s, c]])
        p = np.transpose(np.vstack((x, y)))
        p = np.dot(p, m)
        p2 = np.transpose(np.vstack((x-.2, y)))
        p2 = np.dot(p2, m)
        self.segments.append(Segment(p))
        self.segments.append(Segment(p2))
        self.segments.append(SegmentArrow(p[1], p[0], headwidth=.07, headlength=.08))
        self.segments.append(SegmentArrow(p2[1], p2[0], headwidth=.07, headlength=.08))
        self.params['lblloc'] = 'bot'


class Photodiode(Diode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x = np.linspace(-1, 1)
        y = -x*(x-.7)*(x+.7)/2 + resheight*2.5
        x = np.linspace(resheight*.75, resheight*1.25)
        theta = 20
        c = np.cos(np.radians(theta))
        s = np.sin(np.radians(theta))
        m = np.array([[c, s], [-s, c]])
        p = np.transpose(np.vstack((x, y)))
        p = np.dot(p, m)
        p2 = np.transpose(np.vstack((x-.2, y)))
        p2 = np.dot(p2, m)
        self.segments.append(Segment(p))
        self.segments.append(Segment(p2))
        self.segments.append(SegmentArrow(p[-2], p[-1], headwidth=.07, headlength=.08))
        self.segments.append(SegmentArrow(p2[-2], p2[-1], headwidth=.07, headlength=.08))
        self.params['lblloc'] = 'bot'


@adddocs(Element2Term)
class Potentiometer(Resistor):
    ''' Potentiometer element. Anchors: `tap` '''
    # Ok, this has three terminals, but is works like a two-term with lead extension
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        potheight = .72
        self.anchors['tap'] = [reswidth*3, potheight]
        self.params['lblloc'] = 'bot'
        self.segments.append(SegmentArrow([reswidth*3, potheight], [reswidth*3, reswidth*1.5],
                                          headwidth=.15, headlength=.25))


@adddocs(Element2Term)
class PotBox(RBox):
    ''' Potentiometer using box resistor element. Anchors: `tap` '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        potheight = .72
        self.anchors['tap'] = [reswidth*3, potheight]
        self.params['lblloc'] = 'bot'
        self.segments.append(SegmentArrow([reswidth*3, potheight], [reswidth*3, reswidth*2],
                                          headwidth=.15, headlength=.22))

class Diac(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment(
            [[0, 0], gap, [resheight*1.4, resheight*1.8],
             [resheight*1.4, -resheight*1.8], gap,
             [0, resheight*1.8], [0, -resheight*1.8], gap, [resheight*1.4, 0]]))
        self.segments.append(SegmentPoly([[0, -resheight-.25], [resheight*1.4, -.25],
                                          [0, -resheight+.25]]))
        self.segments.append(SegmentPoly([[resheight*1.4, resheight+.25], [0, .25],
                                          [resheight*1.4, resheight-.25]]))


@adddocs(Element2Term)
class Triac(Diac):
    ''' Triac element. Anchors: `gate` '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment([[resheight*1.4, .25], [resheight*1.4+.5, .5]]))
        self.anchors['gate'] = [resheight*1.4+.5, .5]


@adddocs(Element2Term)
class SCR(Diode):
    ''' Silicon controlled rectifier (or thyristor) element. Anchors: `gate` '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment(
            [[resheight*1.4, 0], [resheight*1.4+.3, -.3], [resheight*1.4+.3, -.5]]))
        self.anchors['gate'] = [resheight*1.4+.3, -.5]


class Memristor(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mr = 0.2
        self.segments.append(Segment(
            [[0, 0], [mr, 0], [mr, -mr*.75], [mr*2, -mr*.75], [mr*2, mr*.75],
             [mr*3, mr*.75], [mr*3, -mr*.75], [mr*4, -mr*.75], [mr*4, 0], [mr*5, 0]]))
        self.segments.append(Segment(
            [[0, mr*1.25], [mr*5, mr*1.25], [mr*5, mr*-1.25], [0, mr*-1.25], [0, mr*1.25]]))
        self.segments.append(SegmentPoly(
            [[0, mr*1.25], [0, -mr*1.25], [mr/2, -mr*1.25], [mr/2, mr*1.25]],
            fill='black'))


class Memristor2(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mr = 0.2
        mrv = .25
        self.segments.append(Segment(
            [[0, 0], [0, mrv], [mr, mrv], [mr, -mrv], [mr*2, -mrv], [mr*2, mrv],
             [mr*3, mrv], [mr*3, -mrv], [mr*4, -mrv], [mr*4, mrv],
             [mr*5, mrv], [mr*5, -mrv], [mr*6, -mrv], [mr*6, 0],
             [mr*7, 0]]))


class Josephson(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.segments.append(Segment(
            [[0, 0], gap, [-resheight, resheight], [resheight, -resheight],
             gap, [resheight, resheight], [-resheight, -resheight], gap, [0, 0]]))


class Fuse(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fuser = .12
        fusex = np.linspace(fuser*2, 1+fuser)
        fusey = np.sin(np.linspace(0, 1)*2*np.pi) * resheight
        self.segments.append(Segment(np.transpose(np.vstack((fusex, fusey)))))
        self.segments.append(Segment([[0, 0], gap, [1+fuser*3, 0]]))
        if kwargs.get('dots', True):
            fill = kwargs.get('fill', 'white')
            self.segments.append(SegmentCircle([fuser, 0], fuser, zorder=4, fill=fill))
            self.segments.append(SegmentCircle([fuser*2+1, 0], fuser, zorder=4, fill=fill))


class Breaker(Element2Term):
    ''' Circuit breaker

        Parameters
        ----------
        dots : bool
            Show connection dots
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        dots = kwargs.get('dots', True)
        theta1 = 25 if dots else 10
        theta2 = 155 if dots else 170
        self.segments.append(Segment([[0, 0], gap, [1, 0]]))
        self.segments.append(SegmentArc([.5, 0], 1, .65, theta1=theta1, theta2=theta2))
        if dots:
            fill = kwargs.get('fill', 'white')
            rad = .12
            self.segments.append(SegmentCircle([rad, 0], rad, zorder=4, fill=fill))
            self.segments.append(SegmentCircle([1-rad, 0], rad, zorder=4, fill=fill))


def cycloid(loops=4, ofst=(0, 0), a=.06, b=.19, norm=True, vertical=False, flip=False):
    ''' Generate a prolate cycloid (inductor spiral) that
        will always start and end at y=0.

        Parameters
        ----------
        loops : int
            Number of loops
        a, b : float
            Parameters. b>a for prolate (loopy) cycloid
        norm : bool
            Normalize the length to 1
        vertical, flip : bool
            Control the orientation of cycloid

        Returns
        -------
        path : array
            List of [x, y] coordinates defining the cycloid
    '''
    yint = np.arccos(a/b)  # y-intercept
    t = np.linspace(yint, 2*(loops+1)*np.pi-yint, num=loops*50)
    x = a*t - b*np.sin(t)
    y = a - b*np.cos(t)
    x = x - x[0]  # Shift to start at 0,0

    if norm:
        x = x / (x[-1]-x[0])      # Normalize length to 1

    if flip:
        y = -y

    y = y * (max(y)-min(y))/(resheight)  # Normalize to resistor width

    if vertical:
        x, y = y, x

    x = x + ofst[0]
    y = y + ofst[1]

    path = np.transpose(np.vstack((x, y)))
    return path


class Inductor(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ind_w = .25
        self.segments.append(Segment([[0, 0], gap, [1, 0]]))
        for i in range(4):
            self.segments.append(SegmentArc(
                [(i*2+1)*ind_w/2, 0], theta1=0, theta2=180,
                width=ind_w, height=ind_w))


@adddocs(Element2Term)
class Inductor2(Element2Term):
    ''' Inductor, drawn as cycloid

        Parameters
        ----------
        loops : int
            Number of inductor loops
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loops = kwargs.get('loops', 4)
        self.segments.append(Segment(cycloid(loops=loops)))
