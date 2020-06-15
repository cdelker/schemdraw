''' Cable elements, coaxial and triaxial '''

import numpy as np
import warnings

from ..segments import Segment, SegmentArc
from .elements import Element2Term, gap
from ..adddocs import adddocs


@adddocs(Element2Term)
class Coax(Element2Term):
    ''' Coaxial cable element. Anchors: `shieldstart`, `shieldstart_top`,
        `shieldend`, `shieldend_top`, `shieldcenter`, `shieldcenter_top`.

        Parameters
        ----------
        length: float
            Total length of the cable
        radius: float
            Radius of shield
        leadlen: float
            Distance (x) from start of center conductor to
            start of shield.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        length = kwargs.get('length', 3)
        radius = kwargs.get('radius', 0.3)
        leadlen = kwargs.get('leadlen', 0.6)

        self.segments.append(Segment(    # Center conductor
                [[0, 0], [leadlen, 0], gap, [length-leadlen+radius/2, 0],
                 [length, 0]], **kwargs))
        self.segments.append(Segment(
            [[leadlen, radius], [length-leadlen, radius]]))   # Top
        self.segments.append(Segment([
            [leadlen, -radius], [length-leadlen, -radius]]))  # Bottom
        self.segments.append(SegmentArc(
            [leadlen, 0], width=radius, height=radius*2, theta1=0, theta2=360))
        self.segments.append(SegmentArc(
            [length-leadlen, 0], width=radius,
            height=radius*2, theta1=270, theta2=90))
        self.anchors['shieldstart'] = [leadlen, -radius]
        self.anchors['shieldstart_top'] = [leadlen, radius]
        self.anchors['shieldend'] = [length-leadlen, -radius]
        self.anchors['shieldend_top'] = [length-leadlen, radius]
        self.anchors['shieldcenter'] = [length/2, -radius]
        self.anchors['shieldcenter_top'] = [length/2, radius]

        if radius/2 > leadlen:
            warnings.warn('Coax leadlen < radius/2. Coax may be malformed.')
        if leadlen*2 > length:
            warnings.warn('Coax length < 2*leadlen. Coax may be malformed.')


@adddocs(Element2Term)
class Triax(Element2Term):
    ''' Triaxial cable element. Anchors: `shieldstart`, `shieldstart_top`,
        `shieldend`, `shieldend_top`, `shieldcenter`, `shieldcenter_top`,
        `guardstart`, `guardstart_top`, `guardend`, `guardend_top`.

        Parameters
        ----------
        length: float
            Total length of the cable
        radiusinner: float
            Radius of inner guard
        radiusouter: float
            Radius of outer shield
        leadlen: float
            Distance (x) from start of center conductor to
            start of guard.
        shieldofststart: float
            Distance from start of inner guard to start of outer shield
        shieldofstend: float
            Distance from end of outer shield to end of inner guard
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        length = kwargs.get('length', 3)
        leadlen = kwargs.get('leadlen', 0.6)
        radiusinner = kwargs.get('radiusinner', 0.3)
        radiusouter = kwargs.get('radiusouter', 0.6)
        shieldofststart = kwargs.get('shieldofststart', 0.3)
        shieldofstend = kwargs.get('shieldofstend', 0.45)

        if radiusouter < radiusinner:
            raise ValueError('Triax inner radius > outer radius')

        xshield = radiusouter/2 * np.sqrt(1 - radiusinner**2/radiusouter**2)
        if shieldofststart - xshield > -radiusinner/2:
            thetashield = 180 - np.rad2deg(np.arctan2(radiusinner, xshield))
        else:
            thetashield = 180

        if length - leadlen - shieldofstend + radiusouter < length:
            # Include the inner guard on output side
            self.segments.append(Segment(  # Center conductor (first)
                [[0, 0], [leadlen, 0], gap,
                 [length-leadlen+radiusinner/2, 0],
                 [length, 0]]))
            self.segments.append(Segment(
                [[length-leadlen-shieldofstend+xshield, radiusinner],
                 [length-leadlen, radiusinner]]))  # guard (inner) top/right
            self.segments.append(Segment(
                [[length-leadlen-shieldofstend+xshield, -radiusinner],
                 [length-leadlen, -radiusinner]]))  # guard (inner) bottom/right
            self.segments.append(SegmentArc(
                [length-leadlen, 0], width=radiusinner, height=radiusinner*2,
                theta1=270, theta2=90))
        else:
            # Don't include inner guard on output side
            self.segments.append(Segment(    # Center conductor
                [[0, 0], [leadlen, 0], gap,
                 [length-leadlen-shieldofstend+radiusouter/2, 0]]))

        # Start with shapes that are always shown...
        self.segments.append(Segment(  # guard (inner) top/left
            [[leadlen, radiusinner], [leadlen+shieldofststart+xshield, radiusinner]]))
        self.segments.append(Segment(  # guard (inner) bottom/left
            [[leadlen, -radiusinner], [leadlen+shieldofststart+xshield, -radiusinner]]))
        self.segments.append(Segment(  # shield (outer) top
            [[leadlen+shieldofststart, radiusouter],
             [length-leadlen-shieldofstend, radiusouter]]))
        self.segments.append(Segment(  # shield (outer) bottom
            [[leadlen+shieldofststart, -radiusouter],
             [length-leadlen-shieldofstend, -radiusouter]]))

        self.segments.append(SegmentArc(
            [leadlen, 0], width=radiusinner, height=radiusinner*2,
            theta1=0, theta2=360))
        self.segments.append(SegmentArc(
            [leadlen+shieldofststart, 0], width=radiusouter,
            height=radiusouter*2, theta1=-thetashield, theta2=thetashield))
        self.segments.append(SegmentArc(
            [length-leadlen-shieldofstend, 0], width=radiusouter,
            height=radiusouter*2, theta1=270, theta2=90))

        self.anchors['guardstart'] = [leadlen, -radiusinner]
        self.anchors['guardstart_top'] = [leadlen, radiusinner]
        self.anchors['guardend'] = [length-leadlen, -radiusinner]
        self.anchors['guardend_top'] = [length-leadlen, radiusinner]
        self.anchors['shieldstart'] = [leadlen+shieldofststart, -radiusouter]
        self.anchors['shieldstart_top'] = [leadlen+shieldofststart, radiusouter]
        self.anchors['shieldend'] = [length-leadlen-shieldofstend, -radiusouter]
        self.anchors['shieldend_top'] = [length-leadlen-shieldofstend, radiusouter]
        self.anchors['shieldcenter'] = [length/2, -radiusouter]
        self.anchors['shieldcenter_top'] = [length/2, radiusouter]

        if radiusouter <= radiusinner:
            warnings.warn('Triax outer radius < inner radius')

        if leadlen+shieldofststart > length-leadlen-shieldofstend:
            warnings.warn('Triax too short for outer radius')
