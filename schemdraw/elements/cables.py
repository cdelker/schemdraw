''' Cable elements, coaxial and triaxial '''
from __future__ import annotations
from typing import Optional
import math
import warnings

from ..segments import Segment, SegmentArc
from .elements import Element2Term, gap


class Coax(Element2Term):
    ''' Coaxial cable element.

        Args:
            length: Total length of the cable, excluding lead extensions. [default: 3]
            radius: Radius of shield [default: 0.3]
            leadlen: Distance (x) from start of center conductor to
                start of shield. [default: 0.6]

        Anchors:
            * shieldstart
            * shieldstart_top
            * shieldend
            * shieldend_top
            * shieldcenter
            * shieldcenter_top
    '''
    _element_defaults = {
        'length': 3,
        'leadlen': 0.6,
        'radius': 0.3,
    }
    def __init__(self, *,
                 length: Optional[float] = None,
                 radius: Optional[float] = None,
                 leadlen: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        _leadlen = self.params['leadlen']
        _length = self.params['length']
        _radius = self.params['radius']
        self.segments.append(Segment(    # Center conductor
                [(0, 0), (_leadlen, 0), gap, (_length-_leadlen+_radius/2, 0),
                 (_length, 0)]))
        self.segments.append(Segment(
            [(_leadlen, _radius), (_length-_leadlen, _radius)]))   # Top
        self.segments.append(Segment(
            [(_leadlen, -_radius), (_length-_leadlen, -_radius)]))  # Bottom
        self.segments.append(SegmentArc(
            (_leadlen, 0), width=_radius, height=_radius*2, theta1=0, theta2=360))
        self.segments.append(SegmentArc(
            (_length-_leadlen, 0), width=_radius,
            height=_radius*2, theta1=270, theta2=90))
        self.anchors['shieldstart'] = (_leadlen, -_radius)
        self.anchors['shieldstart_top'] = (_leadlen, _radius)
        self.anchors['shieldend'] = (_length-_leadlen, -_radius)
        self.anchors['shieldend_top'] = (_length-_leadlen, _radius)
        self.anchors['shieldcenter'] = (_length/2, -_radius)
        self.anchors['shieldcenter_top'] = (_length/2, _radius)

        if _radius/2 > _leadlen:
            warnings.warn('Coax leadlen < radius/2. Coax may be malformed.')
        if _leadlen*2 > _length:
            warnings.warn('Coax length < 2*leadlen. Coax may be malformed.')


class Triax(Element2Term):
    ''' Triaxial cable element.

        Args:
            length: Total length of the cable [default: 3]
            radiusinner: Radius of inner guard [default: 0.3]
            radiusouter: Radius of outer shield [default: 0.6]
            leadlen: Distance (x) from start of center conductor to
                start of guard. [default: 0.6]
            shieldofststart: Distance from start of inner guard to start
                of outer shield [default: 0.3]
            shieldofstend: Distance from end of outer shield to end
                of inner guard [default: 0.3]

        Anchors:
            * shieldstart
            * shieldstart_top
            * shieldend
            * shieldend_top
            * shieldcenter
            * shieldcenter_top
            * guardstart
            * guardstart_top
            * guardend
            * guardend_top
    '''
    _element_defaults = {
        'length': 3,
        'leadlen': 0.6,
        'radiusinner': 0.3,
        'radiusouter': 0.6,
        'shieldofststart': 0.3,
        'shieldofstend': 0.3
    }
    def __init__(self, *,
                 length: Optional[float] = None,
                 leadlen: Optional[float] = None,
                 radiusinner: Optional[float] = None,
                 radiusouter: Optional[float] = None,
                 shieldofststart: Optional[float] = None,
                 shieldofstend: Optional[float] = None,
                 **kwargs):
        super().__init__(**kwargs)
        r1 = self.params['radiusinner']
        r2 = self.params['radiusouter']
        _length = self.params['length']
        _leadlen = self.params['leadlen']
        _shieldofstend = self.params['shieldofstend']
        _shieldofststart = self.params['shieldofststart']

        if r2 < r1:
            raise ValueError('Triax inner radius > outer radius')

        xshield = r2/2 * math.sqrt(1 - r1**2/r2**2)
        if _shieldofststart - xshield > -r1/2:
            thetashield = 180 - math.degrees(math.atan2(r1, xshield))
        else:
            thetashield = 180

        if _length - _leadlen - _shieldofstend + r2 < _length:
            # Include the inner guard on output side
            self.segments.append(Segment(  # Center conductor (first)
                [(0, 0), (_leadlen, 0), gap,
                 (_length-_leadlen+r1/2, 0),
                 (_length, 0)]))
            self.segments.append(Segment(
                [(_length-_leadlen-_shieldofstend+xshield, r1),
                 (_length-_leadlen, r1)]))  # guard (inner) top/right
            self.segments.append(Segment(
                [(_length-_leadlen-_shieldofstend+xshield, -r1),
                 (_length-_leadlen, -r1)]))  # guard (inner) bottom/right
            self.segments.append(SegmentArc(
                (_length-_leadlen, 0), width=r1, height=r1*2,
                theta1=270, theta2=90))
        else:
            # Don't include inner guard on output side
            self.segments.append(Segment(    # Center conductor
                [(0, 0), (_leadlen, 0), gap,
                 (_length-_leadlen-_shieldofstend+r2/2, 0)]))

        # Start with shapes that are always shown...
        self.segments.append(Segment(  # guard (inner) top/left
            [(_leadlen, r1), (_leadlen+_shieldofststart+xshield, r1)]))
        self.segments.append(Segment(  # guard (inner) bottom/left
            [(_leadlen, -r1), (_leadlen+_shieldofststart+xshield, -r1)]))
        self.segments.append(Segment(  # shield (outer) top
            [(_leadlen+_shieldofststart, r2),
             (_length-_leadlen-_shieldofstend, r2)]))
        self.segments.append(Segment(  # shield (outer) bottom
            [(_leadlen+_shieldofststart, -r2),
             (_length-_leadlen-_shieldofstend, -r2)]))

        self.segments.append(SegmentArc(
            (_leadlen, 0), width=r1, height=r1*2,
            theta1=0, theta2=360))
        self.segments.append(SegmentArc(
            (_leadlen+_shieldofststart, 0), width=r2,
            height=r2*2, theta1=-thetashield, theta2=thetashield))
        self.segments.append(SegmentArc(
            (_length-_leadlen-_shieldofstend, 0), width=r2,
            height=r2*2, theta1=270, theta2=90))

        self.anchors['guardstart'] = (_leadlen, -r1)
        self.anchors['guardstart_top'] = (_leadlen, r1)
        self.anchors['guardend'] = (_length-_leadlen, -r1)
        self.anchors['guardend_top'] = (_length-_leadlen, r1)
        self.anchors['shieldstart'] = (_leadlen+_shieldofststart, -r2)
        self.anchors['shieldstart_top'] = (_leadlen+_shieldofststart, r2)
        self.anchors['shieldend'] = (_length-_leadlen-_shieldofstend, -r2)
        self.anchors['shieldend_top'] = (_length-_leadlen-_shieldofstend, r2)
        self.anchors['shieldcenter'] = (_length/2, -r2)
        self.anchors['shieldcenter_top'] = (_length/2, r2)

        if r2 <= r1:
            warnings.warn('Triax outer radius < inner radius')

        if _leadlen+_shieldofststart > _length-_leadlen-_shieldofstend:
            warnings.warn('Triax too short for outer radius')
