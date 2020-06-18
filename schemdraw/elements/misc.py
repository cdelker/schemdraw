''' Other elements '''

from .elements import Element, Element2Term, gap
from .twoterm import resheight
from ..segments import Segment, SegmentPoly, SegmentArc, SegmentCircle, SegmentArrow
from ..adddocs import adddocs


@adddocs(Element)
class Speaker(Element):
    ''' Speaker element with two inputs. Anchors: `in1`, `in2`. '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sph = .5
        self.segments.append(Segment([[0, 0], [resheight, 0]]))
        self.segments.append(Segment([[0, -sph], [resheight, -sph]]))
        self.segments.append(SegmentPoly(
            [[resheight, sph/2], [resheight, -sph*1.5],
             [resheight*2, -sph*1.5], [resheight*2, sph/2]]))
        self.segments.append(SegmentPoly(
            [[resheight*2, sph/2], [resheight*3.5, sph*1.25],
             [resheight*3.5, -sph*2.25], [resheight*2, -sph*1.5]], closed=False))
        self.anchors['in1'] = [0, 0]
        self.anchors['in2'] = [0, -sph]
        self.params['drop'] = [0, -sph]


@adddocs(Element)
class Mic(Element):
    ''' Microphone element with two inputs. Anchors: `in1`, `in2`. '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        sph = .5
        self.segments.append(Segment(  # Upper lead
            [[0, 0], [resheight, 0]]))
        self.segments.append(Segment(  # Lower lead
            [[0, -sph], [resheight, -sph]]))
        self.segments.append(Segment(  # Vertical flat
            [[-resheight*2, resheight], [-resheight*2, -resheight*3]]))
        self.segments.append(SegmentArc(
            [-resheight*2, -resheight], theta1=270, theta2=90,
            width=resheight*4, height=resheight*4))
        self.anchors['in1'] = [resheight, 0]
        self.anchors['in2'] = [resheight, -sph]
        self.params['drop'] = [0, -sph]


class Motor(Element2Term):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        mw = .22
        self.segments.append(Segment(
            [[-mw, 0], [-mw, 0], gap, [1+mw, 0], [1+mw, 0]]))
        self.segments.append(Segment(
            [[0, -mw], [0-mw, -mw], [0-mw, mw], [0, mw]]))
        self.segments.append(Segment(
            [[1, -mw], [1+mw, -mw], [1+mw, mw], [1, mw]]))
        self.segments.append(SegmentCircle([0.5, 0], 0.5))


class AudioJack(Element):
    ''' Audio Jack with 2 or 3 connectors and optional switches.
        Anchors: tip, sleeve, ring, ringswitch, tipswitch
    
        Parameters
        ----------
        ring : bool
            Show ring (third conductor) contact
        switch : bool
            Show switch on tip contact
        ringswitch : bool
            Show switch on ring contact
        dots : bool
            Show connector dots
        radius : float
            Radius of connector dots
    
        Anchors
    
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        radius = kwargs.get('radius', 0.075)
        ring = kwargs.get('ring', False)
        dots = kwargs.get('dots', True)
        switch = kwargs.get('switch', False)
        ringswitch = kwargs.get('ringswitch', False)
        fill = kwargs.get('fill', 'white' if kwargs.get('open', True) else True)

        length = 2
        ringlen = .75
        tiplen = .55
        swidth=.2
        sleeveheight = 1
        tipy = 1
        ringy = .1
        sleevey = .35
        swdy = .4
        swlen = .5
        
        if switch:
            tipy += .2

        if ring and ringswitch:
            sleevey += .2
            ringy -= .2

        if ring:
            if dots:
                self.segments.append(SegmentCircle([0, -sleevey], radius, fill=fill, zorder=4))
            self.segments.append(Segment([[-radius, -sleevey], [-length, -sleevey], [-length, 0],
                                          [-length, sleeveheight], [-length-swidth, sleeveheight],
                                          [-length-swidth, 0], [-length, 0]]))
            self.anchors['sleeve'] = [0, -sleevey]

            if dots:
                self.segments.append(SegmentCircle([0,  ringy], radius, fill=fill, zorder=4))            
            self.segments.append(Segment([[-radius, ringy], [-length*.75, ringy],
                                          [-length*ringlen-2*radius, ringy+2*radius],
                                          [-length*ringlen-radius*4, ringy]]))
            self.anchors['ring'] = [0, ringy]

        else:
            if dots:
                self.segments.append(SegmentCircle([0, 0], radius, fill=fill, zorder=4))
            self.segments.append(Segment([[-radius, 0], [-length, 0], [-length, sleeveheight],
                                          [-length+swidth, sleeveheight], [-length+swidth, 0]]))
            self.anchors['sleeve'] = [0, 0]
            
        if dots:
            self.segments.append(SegmentCircle([0, tipy], radius, fill=fill, zorder=4))
        self.segments.append(Segment([[-radius, tipy], [-length*.55, tipy],
                                      [-length*tiplen-2*radius, tipy-2*radius],
                                      [-length*tiplen-radius*4, tipy]]))
        self.anchors['tip'] = [0, tipy]

        if switch:
            if dots:
                self.segments.append(SegmentCircle([0, tipy-swdy], radius, fill=fill, zorder=4))
            self.segments.append(Segment([[0, tipy-swdy], [-swlen, tipy-swdy]]))
            self.segments.append(SegmentArrow([-swlen, tipy-swdy], [-swlen, tipy]))
            self.anchors['tipswitch'] = [0, tipy-swdy]

        if ring and ringswitch:
            if dots:
                self.segments.append(SegmentCircle([0, ringy+swdy], radius, fill=fill, zorder=4))
            self.segments.append(Segment([[0, ringy+swdy], [-swlen, ringy+swdy]]))
            self.segments.append(SegmentArrow([-swlen, ringy+swdy], [-swlen, ringy]))
            self.anchors['ringswitch'] = [0, ringy+swdy]