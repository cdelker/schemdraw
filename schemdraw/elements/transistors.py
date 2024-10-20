''' Transistor elements '''

from __future__ import annotations
from typing import Optional

__all__ = [
    'Bjt', 'Bjt2', 'BjtNpn', 'BjtNpn2', 'BjtPnp', 'BjtPnp2', 'BjtPnp2c', 'BjtPnp2c2',
    'JFet', 'JFet2', 'JFetN', 'JFetN2', 'JFetP', 'JFetP2',
    'NFet', 'NFet2', 'NMos', 'NMos2', 'PFet', 'PFet2', 'PMos', 'PMos2',
    "AnalogNFet", "AnalogPFet", "AnalogBiasedFet"]

from .elements import Element, Element2Term, gap
from .twoterm import reswidth
from ..segments import Segment, SegmentPoly, SegmentCircle
from ..types import Point


class _Mosfet(Element):
    '''Base Class for Metal Oxide Semiconductor Field Effect Transistors

        Args:
            variant: one of {'nmos', 'pmos'}
            diode: Draw body diode [default: False]
            circle: Draw circle around the mosfet [default: False]

        Anchors:
            * source
            * drain
            * gate

    Note: vertical orientation.  For horizontal orientation, see _Mosfet2.
    '''
    _element_defaults = {
        'diode': False,
        'circle': False
    }
    __variants = ['nmos', 'pmos']

    def __init__(self,
                 variant: str,
                 *,
                 diode: Optional[bool] = False,
                 circle: Optional[bool] = False,
                 **kwargs):
        if variant not in self.__variants:
            raise ValueError(
                "Parameter 'variant' must be one of {}, not {}.".format(
                    self.__variants, variant))

        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'right'  # Draw current labels on this side
        u = reswidth*0.5



        # ---
        self.segments.extend([
            Segment([(-3*u, -6.5*u), (-3*u, -7.5*u)]),
            Segment([(-3*u, -9.5*u), (-3*u, -10.5*u)]),
            Segment([(-3*u, -12.5*u), (-3*u, -13.5*u)]),
            ])

        # top lead
        self.segments.extend([
            Segment([(0, -7*u), (0, 0)]),
            Segment([(-3*u, -7*u), (0, -7*u)]),
            ])

        # bottom lead
        self.segments.extend([
            Segment([(0, -20*u), (0, -13*u)]),
            Segment([(-3*u, -13*u), (0, -13*u)]),
            ])

        if variant == 'nmos':
            # gate
            self.segments.extend([
            Segment([(-10*u, -14*u), (-5*u, -14*u)]),
            Segment([(-5*u, -14*u), (-5*u, -6*u)]),
            ])
            # source
            self.segments.extend([
                Segment(
                    [(-3*u, -10*u), (0, -10*u)],
                    arrow='<-', arrowwidth=2*u, arrowlength=2*u),
                Segment([(0, -10*u), (0, -13*u)]),
                ])

            self.anchors['drain'] = (0, 0)
            self.anchors['gate'] = (-10*u, -14*u)
            self.anchors['center'] = (0, -10*u)
            self.anchors['source'] = (0, -20*u)

        elif variant == 'pmos':
            # gate
            self.segments.extend([
            Segment([(-10*u, -6*u), (-5*u, -6*u)]),
            Segment([(-5*u, -6*u), (-5*u, -14*u)]),
            ])
            # source
            self.segments.extend([
                Segment(
                    [(-3*u, -10*u), (0, -10*u)],
                    arrow='->', arrowwidth=2*u, arrowlength=2*u),
                Segment([(0, -10*u), (0, -7*u)]),
                ])

            self.anchors['source'] = (0, 0)
            self.anchors['gate'] = (-10*u, -6*u)
            self.anchors['center'] = (0, -10*u)
            self.anchors['drain'] = (0, -20*u)

        self.elmparams['drop'] = (0, -20*u)
        self.elmparams['lblloc'] = 'rgt'

        if self.params['diode']:
            self.segments.extend([
                Segment([(0, -7*u), (3*u, -7*u)]),
                Segment([(3*u, -7*u), (3*u, -9*u)]),
                Segment([(2*u, -9*u), (4*u, -9*u)]),
                SegmentPoly([(3*u, -9*u), (2*u, -11*u), (4*u, -11*u)]),
                Segment([(3*u, -11*u), (3*u, -13*u)]),
                Segment([(3*u, -13*u), (0, -13*u)]),
                ])

        if self.params['circle']:
            self.segments.append(
                SegmentCircle((-1*u, -10*u), 7*u))


class NMos(_Mosfet):
    ''' N-type Metal Oxide Semiconductor Field Effect Transistor

        Args:
            diode: Draw body diode
            circle: Draw circle around the mosfet

        Anchors:
            * source
            * drain
            * gate

    Note: vertical orientation.  For horizontal orientation, see NMos2.
    '''
    def __init__(self,
                 diode: Optional[bool] = False,
                 circle: Optional[bool] = False,
                 **kwargs):
        super().__init__(variant='nmos', diode=diode, circle=circle, **kwargs)


class PMos(_Mosfet):
    ''' P-type Metal Oxide Semiconductor Field Effect Transistor

        Args:
            diode: Draw body diode
            circle: Draw circle around the mosfet

        Anchors:
            * source
            * drain
            * gate

    Note: vertical orientation.  For horizontal orientation, see PMos2.
    '''

    def __init__(self,
                 diode: Optional[bool] = False,
                 circle: Optional[bool] = False,
                 **kwargs):
        super().__init__(variant='pmos', diode=diode, circle=circle, **kwargs)


class _Mosfet2(Element2Term):
    '''Base Class for Metal Oxide Semiconductor Field Effect Transistors

        Args:
            variant: one of {'nmos', 'pmos'}
            diode: Draw body diode
            circle: Draw circle around the mosfet

        Anchors:
            * source
            * drain
            * gate

    Note: horizontal orientation.  For vertical orientation, see _Mosfet.
    '''
    _element_defaults = {
        'diode': False,
        'circle': False
    }
    __variants = ['nmos', 'pmos']

    def __init__(self, variant: str, *,
                 diode: Optional[bool] = False,
                 circle: Optional[bool] = False,
                 **kwargs):
        if variant not in self.__variants:
            raise ValueError(
                "Parameter 'variant' must be one of {}, not {}.".format(
                    self.__variants, variant))

        super().__init__(**kwargs)
        self.variant = variant
        u = reswidth*0.5

        # top and bottom leads
        self.segments.append(
            Segment([
                (0, 0), (7*u, 0), (7*u, -3*u), gap,
                (13*u, -3*u), (13*u, 0), (20*u, 0),
                ]))



        # ---
        self.segments.extend([
            Segment([(6.5*u, -3*u), (7.5*u, -3*u)]),
            Segment([(9.5*u, -3*u), (10.5*u, -3*u)]),
            Segment([(12.5*u, -3*u), (13.5*u, -3*u)]),
            ])

        if variant == 'nmos':
            # gate
            self.segments.extend([
            Segment([(14*u, -10*u), (14*u, -5*u)]),
            Segment([(14*u, -5*u), (6*u, -5*u)]),
            ])
            # source
            self.segments.extend([
                Segment(
                    [(10*u, -3*u), (10*u, 0)],
                    arrow='<-', arrowwidth=2*u, arrowlength=2*u),
                Segment([(10*u, 0), (13*u, 0)]),
                ])

            self.anchors['drain'] = (0, 0)
            self.anchors['gate'] = (14*u, -10*u)
            self.anchors['source'] = (20*u, 0)

        elif variant == 'pmos':
            # gate
            self.segments.extend([
            Segment([(6*u, -10*u), (6*u, -5*u)]),
            Segment([(6*u, -5*u), (14*u, -5*u)]),
            ])

            # source
            self.segments.extend([
                Segment(
                    [(10*u, -3*u), (10*u, 0)],
                    arrow='->', arrowwidth=2*u, arrowlength=2*u),
                Segment([(10*u, 0), (7*u, 0)]),
                ])

            self.anchors['source'] = (0, 0)
            self.anchors['gate'] = (6*u, -10*u)
            self.anchors['drain'] = (20*u, 0)

        self.anchors['center'] = (10*u, 0)
        self.elmparams['drop'] = (20*u, 0)
        self.elmparams['lblloc'] = 'bottom'

        if self.params['diode']:
            self.segments.extend([
                Segment([(7*u, 0), (7*u, 3*u)]),
                Segment([(7*u, 3*u), (9*u, 3*u)]),
                Segment([(9*u, 2*u), (9*u, 4*u)]),
                SegmentPoly([(9*u, 3*u), (11*u, 2*u), (11*u, 4*u)]),
                Segment([(11*u, 3*u), (13*u, 3*u)]),
                Segment([(13*u, 3*u), (13*u, 0)]),
                ])

        if self.params['circle']:
            self.segments.append(
                SegmentCircle((10*u, -1*u), 7*u))


class NMos2(_Mosfet2):
    ''' N-type Metal Oxide Semiconductor Field Effect Transistor

        Args:
            diode: Draw body diode
            circle: Draw circle around the mosfet

        Anchors:
            * source
            * drain
            * gate

    Note: horizontal orientation.  For vertical orientation, see NMos.
    '''
    def __init__(self,
                 diode: Optional[bool] = False,
                 circle: Optional[bool] = False,
                 **kwargs):
        super().__init__(variant='nmos', diode=diode, circle=circle, **kwargs)


class PMos2(_Mosfet2):
    ''' P-type Metal Oxide Semiconductor Field Effect Transistor

        Args:
            diode: Draw body diode
            circle: Draw circle around the mosfet

        Anchors:
            * source
            * drain
            * gate

    Note: horizontal orientation.  For vertical orientation, see PMos.
    '''
    def __init__(self,
                 diode: Optional[bool] = False,
                 circle: Optional[bool] = False,
                 **kwargs):
        super().__init__(variant='pmos', diode=diode, circle=circle, **kwargs)


fetw = reswidth * 4
feth = reswidth * 5
fetl = feth / 2
fetgap = reswidth
fetr = reswidth * .7  # Radius of "not" bubble


class NFet(Element):
    ''' N-type Field Effect Transistor

        Args:
            bulk: Draw bulk contact [default: False]

        Anchors:
            * source
            * drain
            * gate
            * center
    '''
    _element_defaults = {
        'bulk': False
    }
    def __init__(self, *, bulk: Optional[bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'left'  # Draw current labels on this side

        self.segments.append(Segment([(0, 0), (0, -fetl), (fetw, -fetl),
                                      (fetw, -fetl-fetw), (0, -fetl-fetw),
                                      (0, -2*fetl-fetw)]))
        self.segments.append(Segment([(fetw+fetgap, -fetl),
                                      (fetw+fetgap, -fetl-fetw)]))
        self.segments.append(Segment([(fetw+fetgap, -fetl-fetw/2),
                                      (fetw+fetgap+fetl+fetr, -fetl-fetw/2)]))
        self.anchors['source'] = (0, -2*fetl-fetw)
        self.anchors['drain'] = (0, 0)
        self.anchors['gate'] = (fetw+fetgap+fetl+fetr, -fetl-fetw/2)
        self.anchors['center'] = (0, -fetl - fetw/2)
        self.elmparams['drop'] = (0, -2*fetl-fetw)
        self.elmparams['lblloc'] = 'lft'
        if self.params['bulk']:
            self.segments.append(Segment([(0, -fetl-fetw/2), (fetw, -fetl-fetw/2)],
                                         arrow='->', arrowwidth=.2))
            self.anchors['bulk'] = (0, -fetl-fetw/2)


class PFet(Element):
    ''' P-type Field Effect Transistor

        Args:
            bulk: Draw bulk contact

        Anchors:
            source
            drain
            gate
            center
    '''
    _element_defaults = {
        'bulk': False
    }
    def __init__(self, *, bulk: Optional[bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'left'  # Draw current labels on this side

        self.segments.append(Segment([(0, 0), (0, -fetl), (fetw, -fetl),
                                      (fetw, -fetl-fetw), (0, -fetl-fetw),
                                      (0, -2*fetl-fetw)]))
        self.segments.append(Segment([(fetw+fetgap, -fetl),
                                      (fetw+fetgap, -fetl-fetw)]))
        self.segments.append(Segment([(fetw+fetgap+fetr*2, -fetl-fetw/2),
                                      (fetw+fetgap+fetl+fetr, -fetl-fetw/2)]))
        self.segments.append(SegmentCircle((fetw+fetgap+fetr, -fetl-fetw/2), fetr))

        self.anchors['source'] = (0, 0)
        self.anchors['drain'] = (0, -2*fetl-fetw)
        self.anchors['gate'] = (fetw+fetgap+fetl+fetr, -fetl-fetw/2)
        self.anchors['center'] = (0, -fetl - fetw / 2)
        self.elmparams['drop'] = (0, -2*fetl-fetw)
        self.elmparams['lblloc'] = 'lft'
        if self.params['bulk']:
            self.segments.append(Segment([(0, -fetl-fetw/2), (fetw, -fetl-fetw/2)],
                                         arrow='->', arrowwidth=.2))
            self.anchors['bulk'] = (0, -fetl-fetw/2)


class NFet2(Element2Term):
    ''' N-type Field Effect Transistor which extends
        source/drain leads to the desired length

        Args:
            bulk: Draw bulk contact [default: False]

        Anchors:
            * source
            * drain
            * gate
    '''
    _element_defaults = {
        'bulk': False
        }
    def __init__(self, *, bulk: Optional[bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'bottom'  # Draw current labels on this side

        self.segments.append(Segment([(0, 0), (fetl, 0), (fetl, fetw),
                                      (fetl+fetw, fetw), (fetl+fetw, 0), (2*fetl+fetw, 0)]))
        self.segments.append(Segment([(fetl, fetw+fetgap), (fetl+fetw, fetw+fetgap)]))
        self.segments.append(Segment([(fetl+fetw/2, fetw+fetgap), (fetl+fetw/2, fetw+fetgap+fetr+fetl)]))
        self.anchors['isource'] = (2*fetl+fetw, 0)
        self.anchors['idrain'] = (0, 0)
        self.anchors['gate'] = (fetl+fetw/2, fetw+fetgap+fetr+fetl)
        self.elmparams['lblloc'] = 'bottom'
        if self.params['bulk']:
            self.segments.append(Segment([(fetl+fetw/2, 0), (fetl+fetw/2, fetw)],
                                         arrow='->', arrowwidth=.2))
            self.anchors['bulk'] = (fetl+fetw/2, 0)

    def _place_anchors(self, start, end):
        ''' Allow positioning anchors relative to extended endpoints
            before the element is placed
        '''
        super()._place_anchors(start, end)
        self.anchors['source'] = self.anchors['end']
        self.anchors['drain'] = self.anchors['start']
        if self._userparams.get('reverse', False):
            self.anchors['source'] = self.anchors['start']
            self.anchors['drain'] = self.anchors['end']


class PFet2(Element2Term):
    ''' P-type Field Effect Transistor which extends
        source/drain leads to the desired length

        Args:
            bulk: Draw bulk contact [default: False]

        Anchors:
            * source
            * drain
            * gate
    '''
    _element_defaults = {
        'bulk': False
    }
    def __init__(self, *, bulk: Optional[bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'bottom'  # Draw current labels on this side

        self.segments.append(Segment([(0, 0), (fetl, 0), (fetl, fetw),
                                      (fetl+fetw, fetw), (fetl+fetw, 0), (2*fetl+fetw, 0)]))
        self.segments.append(Segment([(fetl, fetw+fetgap), (fetl+fetw, fetw+fetgap)]))
        self.segments.append(SegmentCircle((fetl+fetw/2, fetw+fetgap+fetr), fetr))
        self.segments.append(Segment([(fetl+fetw/2, fetw+fetgap+fetr*2), (fetl+fetw/2, fetw+fetgap+fetr+fetl)]))
        self.anchors['isource'] = (2*fetl+fetw, 0)
        self.anchors['idrain'] = (0, 0)
        self.anchors['gate'] = (fetl+fetw/2, fetw+fetgap+fetr+fetl)
        self.elmparams['lblloc'] = 'bottom'
        if self.params['bulk']:
            self.segments.append(Segment([(fetl+fetw/2, 0), (fetl+fetw/2, fetw)],
                                         arrow='->', arrowwidth=.2))
            self.anchors['bulk'] = (fetl+fetw/2, 0)

    def _place_anchors(self, start, end):
        ''' Allow positioning anchors relative to extended endpoints
            before the element is placed
        '''
        super()._place_anchors(start, end)
        self.anchors['source'] = self.anchors['end']
        self.anchors['drain'] = self.anchors['start']
        if self._userparams.get('reverse', False):
            self.anchors['source'] = self.anchors['start']
            self.anchors['drain'] = self.anchors['end']


# Analog style FETs
afetw = reswidth * 2.5
afeth = afetw * 2
afetl = afeth * 0.5
afetgap = afetw * 0.2
afeti = afeth * 0.1   # gate inset
afetb = afeti * 0.75  # bias dot radius
afeta = 0.25          # fet arrow head width


class _AnalogFet(Element):
    _element_defaults = {
        'bulk': False,
        'offset_gate': True,
        'arrow': True
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'left'  # Draw current labels on this side


class AnalogNFet(_AnalogFet):
    ''' N-type Field Effect Transistor, analog style

        Args:
            bulk: Draw bulk contact
            offset_gate: Draw gate on the source side of the transistor, rather than middle
            arrow: Draw source arrow on the transistor if bulk arrow is not drawn

        Anchors:
            source
            drain
            gate
            bulk (if bulk=True)
            center
    '''
    def __init__(self, *,
                 bulk: Optional[bool] = None,
                 offset_gate: Optional[bool] = None,
                 arrow: Optional[bool] = None,
                 **kwargs):
        super().__init__(**kwargs)
        _arrow = self.params['arrow'] if not self.params['bulk'] else False
        self.segments.append(Segment([(0, 0), (0, -afetl), (afetw, -afetl),
                                      (afetw, -afetl - afeth), (0, -afetl - afeth),
                                      (0, -2 * afetl - afeth)]))
        if _arrow:
            self.segments.append(Segment([(afetw, -afetl - afeth), (0, -afetl - afeth)],
                                         arrow='->', arrowwidth=afeta, arrowlength=afeta))
        self.segments.append(Segment([(afetw + afetgap, -afetl - afeti),
                                      (afetw + afetgap, -afetl - afeth + afeti)]))

        if self.params['offset_gate']:
            self.segments.append(Segment([(afetw + afetgap, -afetl - afeth + afeti),
                                          (afetw + afetgap + afetl, -afetl - afeth + afeti)]))
            self.anchors['gate'] = (afetw + afetgap + afetl, -afetl - afeth + afeti)
        else:
            self.segments.append(Segment([(afetw + afetgap, -afetl - afeth / 2),
                                          (afetw + afetgap + afetl, -afetl - afeth / 2)]))
            self.anchors['gate'] = (afetw + afetgap + afetl, -afetl - afeth / 2)

        self.anchors['source'] = (0, -2 * afetl - afeth)
        self.anchors['drain'] = (0, 0)
        self.anchors['center'] = (0, -afetl - afeth / 2)
        self.elmparams['drop'] = (0, -2 * afetl - afeth)
        self.elmparams['lblloc'] = 'lft'

        if self.params['bulk']:
            self.segments.append(Segment([(0, -afetl - afeth / 2), (afetw, -afetl - afeth / 2)],
                                         arrow='->', arrowwidth=afeta, arrowlength=afeta))
            self.anchors['bulk'] = (0, -afetl - afeth / 2)


class AnalogPFet(_AnalogFet):
    ''' P-type Field Effect Transistor, analog style

        Args:
            bulk: Draw bulk contact
            offset_gate: Draw gate on the source side of the transistor, rather than middle
            arrow: Draw source arrow on the transistor if bulk arrow is not drawn

        Anchors:
            source
            drain
            gate
            bulk (if bulk=True)
            center
    '''
    def __init__(self, *,
                 bulk: Optional[bool] = None,
                 offset_gate: Optional[bool] = None,
                 arrow: Optional[bool] = None,
                 **kwargs):
        super().__init__(**kwargs)
        _arrow = self.params['arrow'] if not self.params['bulk'] else False
        self.segments.append(Segment([(0, 0), (0, -afetl), (afetw, -afetl),
                                      (afetw, -afetl - afeth), (0, -afetl - afeth),
                                      (0, -2 * afetl - afeth)]))
        if _arrow:
            self.segments.append(Segment([(0, -afetl), (afetw, -afetl)],
                                         arrow='->', arrowwidth=afeta, arrowlength=afeta))
        self.segments.append(Segment([(afetw + afetgap, -afetl - afeti),
                                      (afetw + afetgap, -afetl - afeth + afeti)]))
        if self.params['offset_gate']:
            self.segments.append(Segment([(afetw + afetgap, -afetl - afeti),
                                          (afetw + afetgap + afetl, -afetl - afeti)]))
            self.anchors['gate'] = (afetw + afetgap + afetl, -afetl - afeti)
        else:
            self.segments.append(Segment([(afetw + afetgap, -afetl - afeth / 2),
                                          (afetw + afetgap + afetl, -afetl - afeth / 2)]))
            self.anchors['gate'] = (afetw + afetgap + afetl, -afetl - afeth / 2)

        self.anchors['source'] = (0, 0)
        self.anchors['drain'] = (0, -2 * afetl - afeth)
        self.anchors['center'] = (0, -afetl - afeth / 2)
        self.elmparams['drop'] = (0, -2 * afetl - afeth)
        self.elmparams['lblloc'] = 'lft'
        if self.params['bulk']:
            self.segments.append(Segment([(afetw, -afetl - afeth / 2), (0, -afetl - afeth / 2)],
                                         arrow='->', arrowwidth=afeta, arrowlength=afeta))
            self.anchors['bulk'] = (0, -afetl - afeth / 2)


class AnalogBiasedFet(_AnalogFet):
    ''' Generic biased small-signal Field Effect Transistor, analog style

        Args:
            bulk: Draw bulk contact
            offset_gate: Draw gate on the source side of the transistor, rather than middle
            arrow: Draw source dot on the transistor if bulk dot is not drawn

        Anchors:
            source
            drain
            gate
            bulk (if bulk=True)
            center
    '''
    def __init__(self, *,
                 bulk: Optional[bool] = None,
                 offset_gate: Optional[bool] = None,
                 arrow: Optional[bool] = None,
                 **kwargs):
        super().__init__(**kwargs)
        _arrow = self.params['arrow'] if not self.params['bulk'] else False
        self.segments.append(Segment([(0, 0), (0, -afetl), (afetw, -afetl),
                                      (afetw, -afetl - afeth), (0, -afetl - afeth),
                                      (0, -2 * afetl - afeth)]))
        if _arrow:
            self.segments.append(SegmentCircle(center=(afetb * 2, -afetl - afeth), radius=afetb, fill=True))
        self.segments.append(Segment([(afetw + afetgap, -afetl - afeti),
                                      (afetw + afetgap, -afetl - afeth + afeti)]))

        if self.params['offset_gate']:
            self.segments.append(Segment([(afetw + afetgap, -afetl - afeth + afeti),
                                          (afetw + afetgap + afetl, -afetl - afeth + afeti)]))
            self.anchors['gate'] = (afetw + afetgap + afetl, -afetl - afeth + afeti)
        else:
            self.segments.append(Segment([(afetw + afetgap, -afetl - afeth / 2),
                                          (afetw + afetgap + afetl, -afetl - afeth / 2)]))
            self.anchors['gate'] = (afetw + afetgap + afetl, -afetl - afeth / 2)

        self.anchors['source'] = (0, -2 * afetl - afeth)
        self.anchors['drain'] = (0, 0)
        self.anchors['center'] = (0, -afetl - afeth / 2)
        self.elmparams['drop'] = (0, -2 * afetl - afeth)
        self.elmparams['lblloc'] = 'lft'
        if self.params['bulk']:
            self.segments.append(Segment([(0, -afetl - afeth / 2),
                                          (afetw, -afetl - afeth / 2)]))
            self.segments.append(SegmentCircle(center=(afetw - afetb * 2, -afetl - afeth / 2), radius=afetb, fill=True))
            self.anchors['bulk'] = (0, -afetl - afeth / 2)


# Junction FETs
fete = fetw*.2  # JFET extension
jfetw = reswidth*3


class JFet(Element):
    ''' Junction Field Effect Transistor (untyped)

        Anchors:
            * source
            * drain
            * gate
            * center
    '''
    _element_defaults = {
        'circle': False,
        'lblloc': 'lft'
    }
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'left'  # Draw current labels on this side
        self.segments.append(Segment(
            [(0, 0), (0, -fetl), (jfetw, -fetl), (jfetw, -fetl+fete),
             (jfetw, -fetl-jfetw-fete), (jfetw, -fetl-jfetw),
             (0, -fetl-jfetw), (0, -2*fetl-jfetw)]))
        self.segments.append(Segment([(jfetw, -fetl-jfetw), (jfetw+fetl, -fetl-jfetw)]))
        self.elmparams['drop'] = (jfetw+fetl, -fetl-jfetw)
        self.anchors['source'] = (0, -2*fetl-jfetw)
        self.anchors['drain'] = (0, 0)
        self.anchors['gate'] = (jfetw+fetl, -fetl-jfetw)
        self.anchors['center'] = (0, -fetl-jfetw/2)
        if self.params['circle']:
            self.segments.append(SegmentCircle((jfetw/2, -fetw), fetw*1.1))


class JFetN(JFet):
    ''' N-type Junction Field Effect Transistor

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * source
            * drain
            * gate
            * center
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        self.segments.append(Segment([(jfetw+.1, -fetl-jfetw), (jfetw+.3, -fetl-jfetw)],
                                     arrow='->', arrowwidth=.2, arrowlength=.2))


class JFet2(Element2Term):
    ''' Junction Field Effect Transistor (untyped) which extends
        collector/emitter leads to the desired length

        Anchors:
            * source
            * drain
            * gate
    '''
    _element_defaults = {
        'circle': False,
        'lblloc': 'bottom'
    }
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'bottom'  # Draw current labels on this side

        self.segments.append(Segment([
            (0, 0), (fetl, 0), (fetl, jfetw), (fetl+jfetw, jfetw),
            (fetl+jfetw, 0), (2*fetl+jfetw, 0)]))
        self.segments.append(Segment([(fetl-fete, jfetw), (fetl+jfetw+fete, jfetw)]))
        self.segments.append(Segment([(fetl+jfetw, jfetw), (fetl+jfetw, jfetw+fetl)]))
        self.anchors['isource'] = (2*fetl+jfetw, 0)
        self.anchors['idrain'] = (0, 0)
        self.anchors['gate'] = (fetl+jfetw, jfetw+fetl)

        if self.params['circle']:
            self.segments.append(SegmentCircle((fetl+jfetw/2, jfetw/2), fetw*1.1))

    def _place_anchors(self, start, end):
        ''' Allow positioning anchors relative to extended endpoints
            before the element is placed
        '''
        super()._place_anchors(start, end)
        self.anchors['source'] = self.anchors['end']
        self.anchors['drain'] = self.anchors['start']
        if self._userparams.get('reverse', False):
            self.anchors['source'] = self.anchors['start']
            self.anchors['drain'] = self.anchors['end']


class JFetN2(JFet2):
    ''' N-type Junction Field Effect Transistor which extends
        collector/emitter leads to the desired length

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * source
            * drain
            * gate
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        self.segments.append(Segment([(fetl+jfetw, jfetw), (fetl+jfetw, jfetw+0.3)],
                                     arrow='->', arrowwidth=.2, arrowlength=.2))


class JFetP2(JFet2):
    ''' P-type Junction Field Effect Transistor which extends
        collector/emitter leads to the desired length

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * source
            * drain
            * gate
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        self.segments.append(Segment([(fetl+jfetw, jfetw+0.3), (fetl+jfetw, jfetw)],
                                     arrow='->', arrowwidth=.2, arrowlength=.2))


class JFetP(JFet):
    ''' P-type Junction Field Effect Transistor

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * source
            * drain
            * gate
            * center
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        self.segments.append(Segment([(jfetw+.25, -fetl-jfetw), (jfetw, -fetl-jfetw)],
                                     arrow='->', arrowwidth=.2, arrowlength=.2))


# BJT transistors
bjt_r = reswidth*3.3   # Radius of BJT circle
bjt_v = bjt_r*2/3  # x coord of vertical line
bjt_v_len = bjt_r*4/3  # height of vertical line
bjt_a = bjt_v_len/4    # Intercept of emitter/collector lines
bjt_emx = bjt_v + bjt_r*.7  # x-coord of emitter exiting circle
bjt_emy = bjt_v_len*.7    # y-coord of emitter exiting circle


class Bjt(Element):
    ''' Bipolar Junction Transistor (untyped)

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * collector
            * emitter
            * base
            * center
    '''
    _element_defaults = {
        'circle': False,
        'lblloc': 'rgt'
    }
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'right'  # Draw current labels on this side

        self.segments.append(Segment([(0, 0), (bjt_v, 0)]))
        self.segments.append(Segment([(bjt_v, bjt_v_len/2), (bjt_v, -bjt_v_len/2)]))
        self.segments.append(Segment([(bjt_v, bjt_a), (bjt_emx, bjt_emy),
                                      (bjt_emx, bjt_emy+bjt_a)]))
        self.segments.append(Segment([(bjt_v, -bjt_a), (bjt_emx, -bjt_emy),
                                      (bjt_emx, -bjt_emy-bjt_a)]))
        if self.params['circle']:
            self.segments.append(SegmentCircle((bjt_r, 0), bjt_r))
        self.elmparams['drop'] = (bjt_emx, bjt_emy+bjt_a)
        self.anchors['base'] = (0, 0)
        self.anchors['collector'] = (bjt_emx, bjt_emy+bjt_a)
        self.anchors['emitter'] = (bjt_emx, -bjt_emy-bjt_a)
        self.anchors['center'] = (bjt_emx, 0)
        self.base: Point
        self.collector: Point
        self.emitter: Point


class BjtNpn(Bjt):
    ''' NPN Bipolar Junction Transistor

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * collector
            * emitter
            * base
            * center
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        self.segments.append(Segment([(bjt_v, -bjt_a), (bjt_emx, -bjt_emy)],
                                     arrow='->', arrowwidth=.2))


class BjtPnp(Bjt):
    ''' PNP Bipolar Junction Transistor

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * collector
            * emitter
            * base
            * center
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        self.segments.append(Segment([(bjt_emx, bjt_emy), (bjt_v, bjt_a)], arrow='->', arrowwidth=.2))
        self.anchors['base'] = (0, 0)
        self.anchors['collector'] = (bjt_emx, -bjt_emy-bjt_a)
        self.anchors['emitter'] = (bjt_emx, bjt_emy+bjt_a)


class BjtPnp2c(BjtPnp):
    ''' PNP Bipolar Junction Transistor with 2 collectors

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * collector
            * emitter
            * base
            * C2
            * center
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        bjt_2c_dy = -.25
        self.segments.append(Segment([(bjt_v, -bjt_a-bjt_2c_dy),
                                      (bjt_emx, -bjt_emy-bjt_2c_dy)]))
        self.anchors['C2'] = (bjt_emx, -bjt_emy-bjt_2c_dy)
        self.C2: Point


bjt_r = .55  # BJT circle radius
bjt_lead_dflt = 0.18  # Default lead length
bjt_diag_ofst = 0.2  # Distance from base to diagonals
bjt_base_w = .75  # Length of base bar
bjt_base_h = .42  # Height of base bar above leads
bjt_width = 1.1   # Distance between leads


class Bjt2(Element2Term):
    ''' Bipolar Junction Transistor (untyped) which extends
        collector/emitter leads to the desired length

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * collector
            * emitter
            * base
    '''
    _element_defaults = {
        'circle': False,
        'lblloc': 'bottom',
        'lblofst': 0.1,
        'theta': 90
    }
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(**kwargs)
        self.elmparams['ilabel'] = 'bottom'  # Draw current labels on this side
        self.segments.append(Segment(((0, 0),
                                      (bjt_width/2-bjt_diag_ofst, bjt_base_h),
                                      (bjt_width/2+bjt_diag_ofst, bjt_base_h),
                                      (bjt_width, 0))))  # Diagonals and lead ends
        self.segments.append(Segment(((bjt_width/2-bjt_base_w/2, bjt_base_h),
                                      (bjt_width/2+bjt_base_w/2, bjt_base_h))))  # Base bar
        self.segments.append(Segment(((bjt_width/2, bjt_base_h),
                                      (bjt_width/2, bjt_base_h+bjt_base_w/2))))  # Base lead
        if self.params['circle']:
            self.segments.append(SegmentCircle((bjt_width/2, bjt_r/2), bjt_r))
        self.anchors['base'] = (bjt_width/2, bjt_base_h+bjt_base_w/2)
        self.anchors['icollector'] = (bjt_width, 0)
        self.anchors['iemitter'] = (0, 0)

    def _place_anchors(self, start, end):
        ''' Allow positioning anchors relative to extended endpoints
            before the element is placed
        '''
        super()._place_anchors(start, end)
        self.anchors['emitter'] = self.anchors['start']
        self.anchors['collector'] = self.anchors['end']
        if self._userparams.get('reverse', False):
            self.anchors['emitter'] = self.anchors['end']
            self.anchors['collector'] = self.anchors['start']


class BjtNpn2(Bjt2):
    ''' NPN Bipolar Junction Transistor which extends
        collector/emitter leads to the desired length

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * collector
            * emitter
            * base
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        self.segments.append(Segment([(0, 0), (bjt_width/2-bjt_diag_ofst, bjt_base_h)],
                                     arrow='<-', arrowwidth=.2))


class BjtPnp2(Bjt2):
    ''' PNP Bipolar Junction Transistor which extends
        collector/emitter leads to the desired length

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * collector
            * emitter
            * base
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        self.segments.append(Segment([(bjt_width/2+bjt_diag_ofst, bjt_base_h),
                                      (bjt_width, 0)],
                                     arrow='<-', arrowwidth=.2))
        self.anchors['icollector'], self.anchors['iemitter'] = self.anchors['iemitter'], self.anchors['icollector']

    def _place_anchors(self, start, end):
        ''' Allow positioning anchors relative to extended endpoints
            before the element is placed
        '''
        super()._place_anchors(start, end)
        self.anchors['emitter'] = self.anchors['end']
        self.anchors['collector'] = self.anchors['start']
        if self._userparams.get('reverse', False):
            self.anchors['emitter'] = self.anchors['start']
            self.anchors['collector'] = self.anchors['end']


class BjtPnp2c2(BjtPnp2):
    ''' 2-Collector PNP Bipolar Junction Transistor which extends
        collector/emitter leads to the desired length

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * collector
            * emitter
            * base
            * C2
    '''
    def __init__(self, *, circle: Optional[bool] = None, **kwargs):
        super().__init__(circle=circle, **kwargs)
        bjt_2c_dy = .25
        self.segments.append(Segment([(bjt_2c_dy, 0),
                                      (bjt_2c_dy+bjt_width/2-bjt_diag_ofst, bjt_base_h)]))
        self.anchors['C2'] = (bjt_2c_dy, 0)
        self.C2: Point
