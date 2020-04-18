''' Signal Processing Elements. These do not have "leads" like
electrical elements to accomodate connections from any direction.
'''

import numpy as _np

from .elements import ARROWHEAD, ANT, LINE, DOT, ic, multiplexer
from .flow import box as makebox


BOX = {  # Base box element. Label will be centered in the box
    'name': 'BOX',
    'paths': [[[0, 0], [0, .5], [1, .5], [1, -.5], [0, -0.5], [0, 0]]],
    'extend': False,
    'lblloc': 'center',
    'lblofst': 0,
    'anchors': {'N': [0.5, 0.5], 'S': [0.5, -0.5], 'E': [1, 0], 'W': [0, 0]},
    'drop': [1, 0]
    }


_rad = 0.5
_k = .5*_np.sqrt(2)/2
CIRCLE = {  # Base circle element, label will be centered in the circle
    'name': 'CIRCLE',
    'shapes': [{'shape': 'circle', 'center': [_rad, 0], 'radius': _rad}],
    'lblloc': 'center',
    'lblofst': 0,
    'extend': False,
    'drop': [_rad*2, 0],
    'anchors': {'W': [0, 0], 'E': [_rad*2, 0], 'N': [_rad, _rad], 'S': [_rad, -_rad],
                'NW': [_rad-_k, _k], 'SW': [_rad-_k, -_k], 'SE': [_rad+_k, -_k], 'NE': [_rad+_k, _k],
                'center': [_rad, 0]}
    }

SUM = {
    'name': 'SUM',
    'base': CIRCLE,
    'paths': [[[.5, .2], [.5, -.2]],
              [[.3, 0], [.7, 0]]]
    }

SUMSIGMA = {
    'name': 'SUMSIGMA',
    'base': CIRCLE,
    'labels': [{'label': '$\Sigma$', 'pos':[0.45, 0], 'align':('center', 'center')}]
    }

MIX = {
    'name': 'MIX',
    'base': CIRCLE,
    'paths': [[[_rad+_k, _k], [_rad-_k, -_k]],
              [[_rad+_k, -_k], [_rad-_k, _k]]],
    'lblloc': 'top',
    'lblofst': .2
    }

# Speaker with only one terminal
SPEAKER1 = {
    'name': 'SPEAKER1',
    'paths': [[[0, 0], [0, 0.25], [0.25, 0.25], [0.25, -.25], [0, -.25], [0, 0]],
              [[0.25, 0.25], [0.5, 0.5], [0.5, -0.5], [0.25, -0.25], [.25, .25]]],
    'extend': False,
    }

_amph = 1.
_ampl = .75
AMP = {
    'name': 'AMP',
    'paths': [[[0, 0], [0, -_amph/2], [_ampl, 0], [0, _amph/2], [0, 0]]],
    'extend': False,
    'drop': [_ampl, 0],
    'anchors': {'in': [0, 0], 'out': [_ampl, 0]}
    }

_sinx = _np.linspace(-_np.pi, _np.pi, num=20)
_siny = -_np.sin(_sinx) 
_sinx = _sinx / _np.pi *.3 + .5
_siny = _siny / 10

# Oscillator in a box
OSCBOX = {
    'name': 'OSCBOX',
    'base': BOX,
    'paths': [list(zip(_sinx, _siny))]
    }

# Oscillator in a circle
OSC = {
    'name': 'OSC',
    'base': CIRCLE,
    'paths': [list(zip(_sinx, _siny))]
    }


# Filters -- boxes with sine waves, some crossed out
FILT = {  # Base filter, nothing rejected, "all pass"?
    'name': 'FILT',
    'base': BOX,
    'paths': [list(zip(_sinx, _siny)),
              list(zip(_sinx, _siny+.25)),
              list(zip(_sinx, _siny-.25))]
    }

FILT_BP = {  # Band pass
    'name': 'FILT_BP',
    'base': FILT,
    'paths': [[[.45, .17], [.55, .33]],     # slash through top
              [[.45, -.33], [.55, -.17]]],  # slash through bottom
    }

FILT_LP = {  # Low pass
    'name': 'FILT_LP',
    'base': FILT,
    'paths':[[[.45, .17], [.55, .33]],    # slash through top
             [[.45, -.08], [.55, .08]]],  # slash through middle
    }

FILT_HP = {  # High pass
    'name': 'FILT_HP',
    'base': FILT,
    'paths':[
             [[.45, -.08], [.55, .08]],    # slash through middle
             [[.45, -.33], [.55, -.17]]],  # slash through bottom
    }


# ADC/DACs
ADC = {
    'name': 'ADC',
    'extend': False,
    'paths': [[[0, 0], [.22, .5], [1.4, .5], [1.4, -.5], [.22, -.5], [0, 0]]],
    'anchors': {'in': [0, 0], 'out': [1.4, 0], 'E': [1.4, 0], 'W': [0, 0]},
    'lblloc': 'center',
    'lblofst': 0,
    'drop': [1.4, 0]
    }

DAC = {
    'name': 'DAC',
    'extend': False,
    'paths': [[[0, 0], [0, .5], [1.18, .5], [1.4, 0], [1.18, -.5], [0, -.5], [0, 0]]],
    'anchors': {'in': [0, 0], 'out': [1.4, 0], 'E': [1.4, 0], 'W': [0, 0]},
    'lblloc': 'center',
    'lblofst': 0,
    'drop': [1.4, 0]
    }


# Demodulator, box with diode in it
DEMOD = {
    'name': 'DEMOD',
    'base': BOX,
    'paths': [[[.15, 0], [.85, 0]],
              [[.7, .25], [.7, -.25]]],
    'shapes': [{'shape': 'poly', 'fill': True, 'zorder': 3,
               'xy': [[.7, 0], [.3, .25], [.3, -.25]]}]
    }
