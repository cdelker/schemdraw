''' Transistor elements '''

from .elements import Element, Element2Term
from .twoterm import reswidth
from ..segments import Segment, SegmentCircle
from ..types import Point


fetw = reswidth*4
feth = reswidth*5
fetl = feth/2
fetgap = reswidth
fetr = reswidth*.7  # Radius of "not" bubble


class NFet(Element):
    ''' N-type Field Effect Transistor

        Args:
            bulk: Draw bulk contact

        Anchors:
            * source
            * drain
            * gate
    '''
    def __init__(self, *d, bulk: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
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
        self.params['drop'] = (0, -2*fetl-fetw)
        self.params['lblloc'] = 'lft'
        if bulk:
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
    '''
    def __init__(self, *d, bulk: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
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
        self.params['drop'] = (0, -2*fetl-fetw)
        self.params['lblloc'] = 'lft'
        if bulk:
            self.segments.append(Segment([(0, -fetl-fetw/2), (fetw, -fetl-fetw/2)],
                                         arrow='->', arrowwidth=.2))
            self.anchors['bulk'] = (0, -fetl-fetw/2)


class NFet2(Element2Term):
    ''' N-type Field Effect Transistor which extends
        source/drain leads to the desired length

        Args:
            bulk: Draw bulk contact

        Anchors:
            * source
            * drain
            * gate
    '''
    def __init__(self, *d, bulk: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (fetl, 0), (fetl, fetw),
                                      (fetl+fetw, fetw), (fetl+fetw, 0), (2*fetl+fetw, 0)]))
        self.segments.append(Segment([(fetl, fetw+fetgap), (fetl+fetw, fetw+fetgap)]))
        self.segments.append(Segment([(fetl+fetw/2, fetw+fetgap), (fetl+fetw/2, fetw+fetgap+fetr+fetl)]))
        self.anchors['isource'] = (2*fetl+fetw, 0)
        self.anchors['idrain'] = (0, 0)
        self.anchors['gate'] = (fetl+fetw/2, fetw+fetgap+fetr+fetl)
        self.params['lblloc'] = 'bottom'
        if bulk:
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
            bulk: Draw bulk contact

        Anchors:
            * source
            * drain
            * gate
    '''
    def __init__(self, *d, bulk: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (fetl, 0), (fetl, fetw),
                                      (fetl+fetw, fetw), (fetl+fetw, 0), (2*fetl+fetw, 0)]))
        self.segments.append(Segment([(fetl, fetw+fetgap), (fetl+fetw, fetw+fetgap)]))
        self.segments.append(SegmentCircle((fetl+fetw/2, fetw+fetgap+fetr), fetr))
        self.segments.append(Segment([(fetl+fetw/2, fetw+fetgap+fetr*2), (fetl+fetw/2, fetw+fetgap+fetr+fetl)]))
        self.anchors['isource'] = (2*fetl+fetw, 0)
        self.anchors['idrain'] = (0, 0)
        self.anchors['gate'] = (fetl+fetw/2, fetw+fetgap+fetr+fetl)
        self.params['lblloc'] = 'bottom'
        if bulk:
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


# Junction FETs
fete = fetw*.2  # JFET extension
jfetw = reswidth*3


class JFet(Element):
    ''' Junction Field Effect Transistor (untyped)

        Anchors:
            * source
            * drain
            * gate
    '''
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(
            [(0, 0), (0, -fetl), (jfetw, -fetl), (jfetw, -fetl+fete),
             (jfetw, -fetl-jfetw-fete), (jfetw, -fetl-jfetw),
             (0, -fetl-jfetw), (0, -2*fetl-jfetw)]))
        self.segments.append(Segment([(jfetw, -fetl-jfetw), (jfetw+fetl, -fetl-jfetw)]))
        self.params['drop'] = (jfetw+fetl, -fetl-jfetw)
        self.anchors['source'] = (0, -2*fetl-jfetw)
        self.anchors['drain'] = (0, 0)
        self.anchors['gate'] = (jfetw+fetl, -fetl-jfetw)
        self.params['lblloc'] = 'lft'
        if circle:
            self.segments.append(SegmentCircle((jfetw/2, -fetw), fetw*1.1))


class JFetN(JFet):
    ''' N-type Junction Field Effect Transistor

        Args:
            circle: Draw circle around the transistor

        Anchors:
            * source
            * drain
            * gate
    '''
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([
            (0, 0), (fetl, 0), (fetl, jfetw), (fetl+jfetw, jfetw),
            (fetl+jfetw, 0), (2*fetl+jfetw, 0)]))
        self.segments.append(Segment([(fetl-fete, jfetw), (fetl+jfetw+fete, jfetw)]))
        self.segments.append(Segment([(fetl+jfetw, jfetw), (fetl+jfetw, jfetw+fetl)]))
        self.anchors['isource'] = (2*fetl+jfetw, 0)
        self.anchors['idrain'] = (0, 0)
        self.anchors['gate'] = (fetl+jfetw, jfetw+fetl)
        self.params['lblloc'] = 'bottom'
        
        if circle:
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
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    '''
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    '''
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment([(0, 0), (bjt_v, 0)]))
        self.segments.append(Segment([(bjt_v, bjt_v_len/2), (bjt_v, -bjt_v_len/2)]))
        self.segments.append(Segment([(bjt_v, bjt_a), (bjt_emx, bjt_emy),
                                      (bjt_emx, bjt_emy+bjt_a)]))
        self.segments.append(Segment([(bjt_v, -bjt_a), (bjt_emx, -bjt_emy),
                                      (bjt_emx, -bjt_emy-bjt_a)]))
        if circle:
            self.segments.append(SegmentCircle((bjt_r, 0), bjt_r))
        self.params['drop'] = (bjt_emx, bjt_emy+bjt_a)
        self.params['lblloc'] = 'rgt'
        self.anchors['base'] = (0, 0)
        self.anchors['collector'] = (bjt_emx, bjt_emy+bjt_a)
        self.anchors['emitter'] = (bjt_emx, -bjt_emy-bjt_a)
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
    '''
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    '''
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    '''
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, **kwargs)
        self.segments.append(Segment(((0, 0),
                                      (bjt_width/2-bjt_diag_ofst, bjt_base_h),
                                      (bjt_width/2+bjt_diag_ofst, bjt_base_h),
                                      (bjt_width, 0))))  # Diagonals and lead ends
        self.segments.append(Segment(((bjt_width/2-bjt_base_w/2, bjt_base_h),
                                      (bjt_width/2+bjt_base_w/2, bjt_base_h))))  # Base bar
        self.segments.append(Segment(((bjt_width/2, bjt_base_h),
                                      (bjt_width/2, bjt_base_h+bjt_base_w/2))))  # Base lead
        if circle:
            self.segments.append(SegmentCircle((bjt_width/2, bjt_r/2), bjt_r))
        self.params['lblloc'] = 'bottom'
        self.params['lblofst'] = .1
        self.anchors['base'] = (bjt_width/2, bjt_base_h+bjt_base_w/2)
        self.anchors['icollector'] = (bjt_width, 0)
        self.anchors['iemitter'] = (0, 0)
        self.params['theta'] = 90

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
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
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
    def __init__(self, *d, circle: bool=False, **kwargs):
        super().__init__(*d, circle=circle, **kwargs)
        bjt_2c_dy = .25
        self.segments.append(Segment([(bjt_2c_dy, 0),
                                      (bjt_2c_dy+bjt_width/2-bjt_diag_ofst, bjt_base_h)]))
        self.anchors['C2'] = (bjt_2c_dy, 0)
        self.C2: Point
