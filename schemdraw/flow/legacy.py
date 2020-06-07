''' DEPRECATED element definitions, based on dictionaries instead of classes, translated
    into their newer class counterparts.
'''

from functools import partial

from .. import flow

def start(w, h):
    return partial(flow.Start, w=w, h=h)

def connect(w, h):
    return partial(flow.Connect, w=w, h=h)

def decision(w, h, **kwargs):
    return partial(flow.Decision, w=w, h=h, **kwargs)

def sub(w, h, s=.3):
    return partial(flow.Subroutine, w=w, h=h, s=s)

def data(w, h, s=.5):
    return partial(flow.Data, w=w, h=h, s=s)

def box(w, h):
    return partial(flow.Box, w=w, h=h)

ARROWHEAD = flow.Arrowhead
ARROW = flow.Arrow
DOT = flow.Dot
LINE = flow.Line
