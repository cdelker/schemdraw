''' Two-terminal element definitions '''

from collections import ChainMap
import numpy as np

from .elements import Element, gap
from ..transform import Transform
from ..segments import *


def angle(a, b):
    ''' Compute angle from coordinate a to b '''
    theta = np.degrees(np.arctan2(b[1] - a[1], (b[0] - a[0])))
    return theta


def distance(a, b):
    ''' Compute distance from A to B '''
    r = np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return r


class Element2Term(Element):
    ''' Two terminal element, with automatic lead extensions to result in the
        desired length
    
        Keyword Arguments
        -----------------
        to : [x, y] float array
            The end coordinate of the element
        tox : float
            x-value of end coordinate. y-value will be same as start
        toy : float
            y-value of end coordinate. x-value will be same as start
        l : float
            Total length of element
        endpts: tuple of 2 [x, y] float arrays
            The start and end points of the element. Overrides other
            2-terminal placement parameters.
            
        Attributes
        ----------
        anchors: start, center, end
    '''
    def place(self, dwgxy, dwgtheta, **dwgparams):
        ''' Place the element, adding lead extensions '''
        self.dwgparams = dwgparams
        if self.cparams is None:
            self.buildparams()
        
        totlen = self.cparams.get('l', self.cparams.get('unit', 3))
        endpts = self.cparams.get('endpts', None)
        to = self.cparams.get('to', None)
        tox = self.cparams.get('tox', None)
        toy = self.cparams.get('toy', None)
        anchor = self.cparams.get('anchor', None)
        zoom = self.cparams.get('zoom', 1)
        xy = np.asarray(self.cparams.get('at', dwgxy))

        # set up transformation
        theta = self.cparams.get('theta', dwgtheta)
        if endpts is not None:
            theta = angle(endpts[0], endpts[1])
        elif self.cparams.get('d') is not None:
            theta = {'u': 90, 'r': 0, 'l': 180, 'd': 270}[self.cparams.get('d')[0].lower()]
        elif to is not None:
            theta = angle(xy, np.asarray(to))

        # Get offset to element position within drawing (global shift)
        if endpts is not None:
            xy = endpts[0]
        
        if endpts is not None:
            totlen = distance(endpts[0], endpts[1])
        elif to is not None:
            # Move until X or Y position is 'end'. Depends on direction
            totlen = distance(xy, np.asarray(to))
        elif tox is not None:
            # Allow either full coordinate (only keeping x), or just an x value
            if isinstance(tox, float) or isinstance(tox, int):
                x = float(tox)
            else:
                x = tox[0]
            endpt = [x, xy[1]]
            totlen = distance(xy, endpt)
        elif toy is not None:
            # Allow either full coordinate (only keeping y), or just a y value
            if isinstance(toy, float) or isinstance(toy, int):
                y = toy
            else:
                y = toy[1]
            endpt = [xy[0], y]
            totlen = distance(xy, endpt)
        
        self.localshift = 0
        if self.cparams.get('extend', True):
            in_path = np.array(self.segments[0].path)
            dz = in_path[-1]-in_path[0]   # Defined delta of path
            in_len = np.sqrt(dz[0]*dz[0]+dz[1]*dz[1])   # Defined length of path
            lead_len = (totlen - in_len)/2
            
            if lead_len > 0:  # Don't make element shorter
                start = in_path[0] - np.array([lead_len, 0])
                end = in_path[-1] + np.array([lead_len, 0])
                self.localshift = -start
                params = self.cparams.copy()
                params.update({'color': self.segments[0].color,
                               'lw': self.segments[0].lw,
                               'ls': self.segments[0].ls})
                              
                self.segments.append(Segment([start, in_path[0]], **params))
                self.segments.append(Segment([in_path[-1], end], **params))
            else:
                start = in_path[0]
                end = in_path[-1]
                self.localshift = 0

        self.anchors['start'] = start
        self.anchors['end'] = end
        self.anchors['center'] = (start+end)/2
                
        if anchor is not None:
            self.localshift = -np.asarray(self.anchors[anchor])
        transform = Transform(theta, xy, self.localshift, zoom)

        self.absanchors = {}
        if len(self.segments) == 0:
            self.absanchors['start'] =  transform.transform(np.array([0, 0]))
            self.absanchors['end'] = transform.transform(np.array([0, 0]))
            self.absanchors['center'] = transform.transform(np.array([0, 0]))
        else:
            self.absanchors['start'] = transform.transform(start)
            self.absanchors['end'] = transform.transform(end)
            self.absanchors['center'] = transform.transform((start+end)/2)

        self.params['drop'] = end
        return super().place(xy, theta, **dwgparams)
    
resheight = 0.25      # Resistor height
reswidth = 1.0 / 6   # Full (inner) length of resistor is 1.0 data unit
            
    
class Line(Element2Term):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0,0]], **kwargs))

    
class Resistor(Element2Term):
    def setup(self, **kwargs):
        self.segments = [Segment([[0, 0], [0.5*reswidth, resheight], [1.5*reswidth, -resheight], [2.5*reswidth, resheight],
                                  [3.5*reswidth, -resheight], [4.5*reswidth, resheight], [5.5*reswidth, -resheight], [6*reswidth, 0]], **kwargs)]
    

class ResistorBox(Element2Term):
    def setup(self, **kwargs):
        self.segments = [Segment([[0, 0], [0, resheight], [reswidth*6, resheight], [reswidth*6, -resheight],
                                  [0, -resheight], [0, 0], gap, [reswidth*6, 0]], **kwargs)]

class ResistorVar(Resistor):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentArrow([1.5*reswidth, -resheight*2], [4.5*reswidth, reswidth*3.5],
                                          headwidth=.12, headlength=.2, **kwargs))
        self.segments.append(Segment([[1.5*reswidth, -resheight*2], [4.5*reswidth, reswidth*3.5]], **kwargs))

    
    
class Capacitor(Element2Term):
    ''' Capacitor 2-terminal element.
    
        Parameters
        ----------
        polar : bool
            Add polarity + sign
            
        Keyword Arguments
        -----------------
        See schemdraw.Element2Term
    '''
    def setup(self, **kwargs):
        capgap = 0.18
        self.segments = [Segment([[0, 0], gap, [0, resheight], [0, -resheight], gap,
                                  [capgap, resheight], [capgap, -resheight], gap,
                                  [capgap, 0]], **kwargs)]
        if kwargs.get('polar', False):
            kwargs = dict(kwargs)
            kwargs.pop('label', None)  # Remove existing element label from kwargs
            self.segments.append(SegmentText([-capgap*1.2, capgap], '+', **kwargs))


class Capacitor2(Element2Term):
    ''' Capacitor 2-terminal element, with curved side.
    
        Parameters
        ----------
        polar : bool
            Add polarity + sign

        Keyword Arguments
        -----------------
        See schemdraw.Element2Term
    '''    
    def setup(self, **kwargs):
        capgap = 0.18        
        self.segments = [Segment([[0, 0], gap, [0, resheight], [0, -resheight], gap, [capgap, 0]], **kwargs),
                         SegmentArc([capgap*1.5, 0], width=capgap*1.5, height=resheight*2.5, theta1=105, theta2=-105, **kwargs)]
        
        if kwargs.get('polar', False):
            self.segments.append(SegmentText([-capgap*1.2, capgap], '+', **kwargs))
        

class CapacitorVar(Capacitor):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentArrow([-2*reswidth, -resheight], [3*reswidth, reswidth*2],
                                          headwidth=.12, headlength=.2, **kwargs))

                             
class Crystal(Element2Term):
    def setup(self, **kwargs):
        xgap = 0.2
        self.segments = [Segment([[0, 0], gap, [0, resheight], [0, -resheight], gap,
                                  [xgap/2, resheight], [xgap/2, -resheight], [xgap*1.5, -resheight],
                                  [xgap*1.5, resheight], [xgap/2, resheight], gap,
                                  [xgap*2, resheight], [xgap*2, -resheight], gap, [xgap*2, 0]], **kwargs)]
        
        
class Diode(Element2Term):
    def setup(self, **kwargs):
        self.segments = [Segment([[0, 0], gap, [resheight*1.4, resheight], [resheight*1.4, -resheight], gap, [resheight*1.4, 0]], **kwargs),
                         SegmentPoly([[0, resheight], [resheight*1.4, 0], [0, -resheight]], **kwargs)]


class Schottky(Diode):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        schottky_width = 0.1
        self.segments.append(Segment([[resheight*1.4, resheight], [resheight*1.4-schottky_width, resheight],  [resheight*1.4-schottky_width, resheight-schottky_width]], **kwargs))
        self.segments.append(Segment([[resheight*1.4, -resheight], [resheight*1.4+schottky_width, -resheight], [resheight*1.4+schottky_width, -resheight+schottky_width]], **kwargs))


class DiodeTunnel(Diode):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        tunnel_width = 0.1
        self.segments.append(Segment([[resheight*1.4, resheight], [resheight*1.4-tunnel_width, resheight]], **kwargs))
        self.segments.append(Segment([[resheight*1.4, -resheight], [resheight*1.4-tunnel_width, -resheight]], **kwargs))

        
class Zener(Diode):    
    def setup(self, **kwargs):
        super().setup(**kwargs)
        zener_width = 0.1
        self.segments.append(Segment([[resheight*1.4, resheight], [resheight*1.4+zener_width, resheight+zener_width]], **kwargs))
        self.segments.append(Segment([[resheight*1.4, -resheight], [resheight*1.4-zener_width, -resheight-zener_width]], **kwargs))
        
        
class LED(Diode):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentArrow([resheight, resheight*1.5], [resheight*2, resheight*3.25], headwidth=.12, headlength=.2, **kwargs))
        self.segments.append(SegmentArrow([resheight*.1, resheight*1.5], [resheight*1.1, resheight*3.25], headwidth=.12, headlength=.2, **kwargs))
        self.params['lblloc'] = 'bot'


class LED2(Diode):  # LED with squiggly light lines
    def setup(self, **kwargs):
        super().setup(**kwargs)
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
        self.segments.append(Segment(p, **kwargs))
        self.segments.append(Segment(p2, **kwargs))        
        self.segments.append(SegmentArrow(p[1], p[0], headwidth=.07, headlength=.08, **kwargs))
        self.segments.append(SegmentArrow(p2[1], p2[0], headwidth=.07, headlength=.08, **kwargs))
        self.params['lblloc'] = 'bot'

        
class Photodiode(Diode):
    def setup(self, **kwargs):
        super().setup(**kwargs)
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
        self.segments.append(Segment(p, **kwargs))
        self.segments.append(Segment(p2, **kwargs))
        self.segments.append(SegmentArrow(p[-2], p[-1], headwidth=.07, headlength=.08, **kwargs))
        self.segments.append(SegmentArrow(p2[-2], p2[-1], headwidth=.07, headlength=.08, **kwargs))
        self.params['lblloc'] = 'bot'
        
        
class Potentiometer(Resistor):
    # Ok, this has three terminals, but is works like a two-term with lead extension
    def setup(self, **kwargs):
        super().setup(**kwargs)
        potheight = .72
        self.anchors = {'tap': [reswidth*3, potheight]}
        self.params['lblloc'] = 'bot'
        self.segments.append(SegmentArrow([reswidth*3, potheight], [reswidth*3, reswidth*1.5],
                                          headwidth=.15, headlength=.25, **kwargs))


class Diac(Element2Term):
    def setup(self, **kwargs):
        self.segments = [Segment([[0, 0], gap, [resheight*1.4, resheight*1.8], [resheight*1.4, -resheight*1.8], gap,
                                  [0, resheight*1.8], [0, -resheight*1.8], gap, [resheight*1.4, 0]], **kwargs),
                         SegmentPoly([[0, -resheight-.25], [resheight*1.4, -.25], [0, -resheight+.25]], **kwargs),
                         SegmentPoly([[resheight*1.4, resheight+.25], [0, .25], [resheight*1.4, resheight-.25]], **kwargs)]


class Triac(Diac):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(Segment([[resheight*1.4, .25], [resheight*1.4+.5, .5]], **kwargs))
        self.anchors['gate'] = [resheight*1.4+.5, .5]


class SCR(Diode):
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(Segment([[resheight*1.4, 0], [resheight*1.4+.3, -.3], [resheight*1.4+.3, -.5]], **kwargs))
        self.anchors['gate'] = [resheight*1.4+.3, -.5]


class Memristor(Element2Term):
    def setup(self, **kwargs):
        mr = 0.2
        self.segments.append(Segment([[0, 0], [mr, 0], [mr, -mr*.75], [mr*2, -mr*.75], [mr*2, mr*.75], [mr*3, mr*.75], [mr*3, -mr*.75], [mr*4, -mr*.75], [mr*4, 0], [mr*5, 0]], **kwargs))
        self.segments.append(Segment([[0, mr*1.25], [mr*5, mr*1.25], [mr*5, mr*-1.25], [0, mr*-1.25], [0, mr*1.25]], **kwargs))
        args = ChainMap({'fill': 'black'}, kwargs)
        self.segments.append(SegmentPoly([[0, mr*1.25], [0, -mr*1.25], [mr/2, -mr*1.25], [mr/2, mr*1.25]], **args))


class Memristor2(Element2Term):
    def setup(self, **kwargs):
        mr = 0.2        
        mrv = .25
        self.segments.append(Segment([[0, 0], [0, mrv], [mr, mrv], [mr, -mrv], [mr*2, -mrv], [mr*2, mrv],
               [mr*3, mrv], [mr*3, -mrv], [mr*4, -mrv], [mr*4, mrv],
               [mr*5, mrv], [mr*5, -mrv], [mr*6, -mrv], [mr*6, 0],
               [mr*7, 0]], **kwargs))

        
class Josephson(Element2Term):
    def setup(self, **kwargs):
        self.segments.append(Segment([[0, 0], gap, [-resheight, resheight], [resheight, -resheight], gap, [resheight, resheight], [-resheight, -resheight], gap, [0, 0]], **kwargs))


class Fuse(Element2Term):
    def setup(self, **kwargs):
        fuser = .15
        fusex = np.linspace(fuser*2, 1+fuser)
        fusey = np.sin(np.linspace(0, 1)*2*np.pi) * resheight
        self.segments.append(Segment(np.transpose(np.vstack((fusex, fusey))), **kwargs))
        self.segments.append(Segment([[0, 0], gap, [1+fuser*3, 0]], **kwargs))
        if 'fill' not in kwargs or kwargs['fill'] is None:
            fill = 'white' if kwargs.get('open', False) else True
            kwargs = ChainMap({'fill': fill}, kwargs)
        kwargs = ChainMap({'zorder': 4}, kwargs)    
        self.segments.append(SegmentCircle([fuser, 0], fuser, **kwargs))
        self.segments.append(SegmentCircle([fuser*2+1, 0], fuser, **kwargs))


class Arrow(Line):
    ''' Arrow element
    
        Parameters
        ----------
        double : bool
            Show arrowhead on both ends
            
        Keyword Arguments
        -----------------
        See schemdraw.Element2Term
    '''
    def setup(self, **kwargs):
        super().setup(**kwargs)
        self.segments.append(SegmentArrow([-.3, 0], [0, 0], headwidth=.3, headlength=.3, ref='end', **kwargs))
        if kwargs.get('double', False):
            self.segments.append(SegmentArrow([.3, 0], [0, 0], headwidth=.3, headlength=.3, ref='start', **kwargs))


class LineDot(Line):
    ''' Line with a dot at the end
    
        Parameters
        ----------
        double : bool
            Show dot on both ends

        Keyword Arguments
        -----------------
        See schemdraw.Element2Term
    '''    
    def setup(self, **kwargs):
        super().setup(**kwargs)
        radius = kwargs.get('radius', 0.075)
        fill = kwargs.pop('fill', 'white' if kwargs.get('open', False) else 'black')
        args = ChainMap({'fill': fill, 'zorder': 4}, kwargs)
        self.segments.append(SegmentCircle([0, 0], radius, ref='end', **args))
        if kwargs.get('double', False):
            self.segments.append(SegmentCircle([0, 0], radius, ref='start', **args))


class Gap(Element2Term):
    def setup(self, **kwargs):
        kwargs['color'] = self.userparams.get('color', 'white')
        self.segments.append(Segment([[0, 0], gap, [1, 0]], **kwargs))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['zorder'] = 0
    

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
    def setup(self, **kwargs):        
        ind_w = .25
        self.segments.append(Segment([[0, 0], gap, [1, 0]], **kwargs))
        for i in range(4):
            self.segments.append(SegmentArc([(i*2+1)*ind_w/2, 0], theta1=0, theta2=180, width=ind_w, height=ind_w, **kwargs))


class Inductor2(Element2Term):
    ''' Inductor, drawn as cycloid
    
        Parameters
        ----------
        loops : int
            Number of inductor loops

        Keyword Arguments
        -----------------
        See schemdraw.Element2Term
    '''
    def setup(self, **kwargs):
        loops = kwargs.get('loops', 4)
        self.segments.append(Segment(cycloid(loops=loops), **kwargs))

