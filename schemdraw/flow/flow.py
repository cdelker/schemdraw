''' Flowcharting element definitions '''

import numpy as np

from ..segments import Segment, SegmentCircle, SegmentText
from ..elements import Element


class Box(Element):
    ''' Flowchart box

        Parameters
        ----------
        w, h : float
            Width and height of box

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = kwargs.get('w', 3)
        h = kwargs.get('h', 2)
        self.segments.append(Segment([[0, 0], [0, w/2], [h, w/2],
                                      [h, -w/2], [0, -w/2], [0, 0]]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = [h, 0]
        self.anchors['W'] = [h/2, -w/2]
        self.anchors['E'] = [h/2, w/2]
        self.anchors['S'] = [h, 0]
        self.anchors['N'] = [0, 0]


class Subroutine(Element):
    ''' Flowchart subroutine (box with extra vertical lines
        near sides)

        Parameters
        ----------
        w, h : float
            Width and height of box
        s : float
            Spacing of side lines

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = kwargs.get('w', 3.5)
        h = kwargs.get('h', 2)
        s = kwargs.get('s', 0.3)
        self.segments.append(Segment([[0, 0], [0, w/2], [h, w/2],
                                      [h, -w/2], [0, -w/2], [0, 0]]))
        self.segments.append(Segment([[0, w/2-s], [h, w/2-s]]))
        self.segments.append(Segment([[0, -w/2+s], [h, -w/2+s]]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = [h, 0]
        self.anchors['W'] = [h/2, -w/2]
        self.anchors['E'] = [h/2, w/2]
        self.anchors['S'] = [h, 0]
        self.anchors['N'] = [0, 0]


class Data(Element):
    ''' Flowchart data box (parallelogram)

        Parameters
        ----------
        w, h : float
            Width and height of box
        s : float
            Slant of sides

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = kwargs.get('w', 3)
        h = kwargs.get('h', 2)
        s = kwargs.get('s', 0.5)
        self.segments.append(Segment([[0, 0], [0, w/2+s/2], [h, w/2-s/2],
                                      [h, -w/2-s/2], [0, -w/2+s/2], [0, 0]]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = [h, 0]
        self.anchors['W'] = [h/2, -w/2]
        self.anchors['E'] = [h/2, w/2]
        self.anchors['S'] = [h, 0]
        self.anchors['N'] = [0, 0]


class Start(Element):
    ''' Flowchart start/stop box (ellipse)

        Parameters
        ----------
        w, h : float
            Width and height of box

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = kwargs.get('w', 3)
        h = kwargs.get('h', 2)

        # There's no ellipse Segment type, so draw one with a path Segment
        t = np.linspace(0, np.pi*2, num=50)
        y = (w/2) * np.cos(t)
        x = (h/2) * np.sin(t) + h/2
        x[-1] = x[0]
        y[-1] = y[0]  # Ensure the path is actually closed
        self.segments.append(Segment(np.transpose(np.vstack((x, y)))))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = [h, 0]
        self.anchors['W'] = [h/2, -w/2]
        self.anchors['E'] = [h/2, w/2]
        self.anchors['S'] = [h, 0]
        self.anchors['N'] = [0, 0]


class Decision(Element):
    ''' Flowchart decision (diamond)

        Parameters
        ----------
        w, h : float
            Width and height of box
        N, E, S, W : string
            Labels for each decision branch

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        w = kwargs.get('w', 4)
        h = kwargs.get('h', 2)
        self.segments.append(Segment([[0, 0], [h/2, w/2], [h, 0],
                                      [h/2, -w/2], [0, 0]]))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = [h, 0]
        self.anchors['W'] = [h/2, -w/2]
        self.anchors['E'] = [h/2, w/2]
        self.anchors['S'] = [h, 0]
        self.anchors['N'] = [0, 0]

        lblargs = dict(kwargs)
        lblargs.pop('label', None)  # Take out element label before passing to SegmentText
        for loc in ['N', 'E', 'S', 'W']:
            if loc in kwargs:
                lblofst = .13
                pos = {'N': [0, lblofst],
                       'S': [h, lblofst],
                       'E': [h/2, w/2+lblofst],
                       'W': [h/2, -w/2-lblofst]}.get(loc)
                align = {'N': ('left', 'bottom'),
                         'S': ('left', 'top'),
                         'E': ('left', 'bottom'),
                         'W': ('right', 'bottom')}.get(loc)
                self.segments.append(SegmentText(pos, kwargs.get(loc), align=align, **lblargs))


class Connect(Element):
    ''' Flowchart connector (circle)

        Parameters
        ----------
        r : float
            Radius of box

        Keyword Arguments
        -----------------
        See schemdraw.Element
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        r = kwargs.get('r', 0.75)
        self.segments.append(SegmentCircle([r, 0], r))
        self.params['lblloc'] = 'center'
        self.params['lblofst'] = 0
        self.params['theta'] = -90
        self.params['drop'] = [2*r, 0]
        self.anchors['W'] = [r, -r]
        self.anchors['E'] = [r, r]
        self.anchors['S'] = [2*r, 0]
        self.anchors['N'] = [0, 0]
