''' Functions for generating flowchart symbols. These do 
not have "leads" like electrical elements to accomodate
connections from any direction.
'''

import numpy as _np

from .elements import ARROWHEAD, LINE, DOT


def box(w=3, h=2):
    ''' Create flowchart block
    
        Parameters
        ----------
        w: float
            Width of box
        h: float
            Height of box
            
        Anchors: N, S, E, W
    '''
    elem = {'name': 'FLOWBOX', 'extend': False, 'lblloc': 'center', 'lblofst': 0, 'theta': -90}
    elem['paths'] = [[[0, 0], [0, w/2], [h, w/2], [h, -w/2], [0, -w/2], [0, 0]]]
    elem['anchors'] = {'W': [h/2, -w/2], 'E': [h/2, w/2], 'S': [h, 0], 'N': [0, 0]}
    elem['drop'] = [h, 0]
    return elem


def sub(w=3.5, h=2, s=.3):
    ''' Create flowchart subprocess (block with extra vertical lines)
        
        Parameters
        ----------
        w: float
            Width of box
        h: float
            Height of box
        s: float
            Spacing of side lines
            
        Anchors: N, S, E, W
    '''
    elem = {'name': 'FLOWSUB', 'extend': False, 'lblloc': 'center', 'lblofst': 0, 'theta': -90}
    elem['paths'] = [[[0, 0], [0, w/2], [h, w/2], [h, -w/2], [0, -w/2], [0, 0]],
                     [[0, w/2-s], [h, w/2-s]],
                     [[0, -w/2+s], [h, -w/2+s]],
                    ]
    elem['anchors'] = {'W': [h/2, -w/2], 'E': [h/2, w/2], 'S': [h, 0], 'N': [0, 0]}
    elem['drop'] = [h, 0]
    return elem


def data(w=3, h=2, s=.5):
    ''' Create flowchart data or I/O block (parallelogram)    
        
        Parameters
        ----------
        w: float
            Width of box
        h: float
            Height of box
        s: float
            Slant of parallelogram
        
        Anchors: N, S, E, W
    '''
    elem = {'name': 'FLOWDATA', 'extend': False, 'lblloc': 'center', 'lblofst': 0, 'theta': -90}
    elem['paths'] = [[[0, 0], [0, w/2+s/2], [h, w/2-s/2], [h, -w/2-s/2], [0, -w/2+s/2], [0, 0]]]
    elem['anchors'] = {'W': [h/2, -w/2], 'E': [h/2, w/2], 'S': [h, 0], 'N': [0, 0]}
    elem['drop'] = [h, 0]
    return elem


def start(w=3, h=2):
    ''' Create flowchart oval (start block)
        
        Parameters
        ----------
        w: float
            Width of box
        h: float
            Height of box
            
        Anchors: N, S, E, W
    '''
    # We could change base schemdraw code to take "ellipse" as a shape, or just make one
    # mathematically here.
    elem = {'name': 'FLOWSTART', 'extend': False, 'lblloc': 'center', 'lblofst': 0, 'theta': -90}
    t = _np.linspace(0, _np.pi*2, num=50)
    y = (w/2) * _np.cos(t)
    x = (h/2) * _np.sin(t) + h/2
    elem['paths'] = [_np.transpose(_np.vstack((x, y)))]
    elem['anchors'] = {'W': [h/2, -w/2], 'E': [h/2, w/2], 'S': [h, 0], 'N': [0, 0]}
    elem['drop'] = [h, 0]
    return elem


def decision(w=4, h=2, responses=None):
    ''' Create decision block (diamond)
        
        Parameters
        ----------
        w: float
            Width of diamond
        h: float
            Height of diamond
        responses: dict
            Dictionary of responses to label at each point of diamond.
            Keys are 'N', 'S', 'E', 'W'. Example: {'E': 'Yes', 'W': 'No'}
        
        Anchors: N, S, E, W
    '''
    elem = {'name': 'DECISION', 'extend': False, 'lblloc': 'center', 'lblofst': 0, 'theta': -90}
    elem['paths'] = [[[0, 0], [h/2, w/2], [h, 0], [h/2, -w/2], [0, 0]]]
    elem['anchors'] = {'W': [h/2, -w/2], 'E': [h/2, w/2], 'S': [h, 0], 'N': [0, 0]}
    elem['drop'] = [h, 0]
    if responses:
        labels = []
        for loc, val in responses.items():
            lblofst = .13
            pos = {'N': [0, lblofst],
                   'S': [h, lblofst],
                   'E': [h/2, w/2+lblofst],
                   'W': [h/2, -w/2-lblofst]}.get(loc)
            align = {'N': ('left', 'bottom'),
                     'S': ('left', 'top'),
                     'E': ('left', 'bottom'),
                     'W': ('right', 'bottom'),
                    }.get(loc)
            labels.append({'label': val, 'pos': pos, 'align': align, 'rotation': 90})
        elem['labels'] = labels
    return elem


def connect(r=0.75):
    ''' Connector (circle) 
    
        Parameters
        ----------
        r: float
            Radius of connector circle
    '''
    elem = {'name': 'CONNECT', 'extend': False, 'lblloc': 'center', 'lblofst': 0, 'theta':-90}
    elem['anchors'] = {'W': [r, -r], 'E': [r, r], 'S': [2*r, 0], 'N': [0, 0]}
    elem['move_cur'] = False
    elem['shapes'] = [{'shape': 'circle',
                       'center': [r, 0],
                       'radius': r}]
    return elem
