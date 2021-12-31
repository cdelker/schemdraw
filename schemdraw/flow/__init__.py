from .flow import Box, RoundBox, Subroutine, Data, Start, Ellipse, Decision, Connect, Process, RoundProcess
from .flow import Terminal, Circle, State, StateEnd
from ..elements import Arrow, Arrowhead, Line, Dot, Wire, Arc2, Arc3, ArcZ, ArcN, ArcLoop


from . import legacy
import warnings

def __getattr__(name):
    e = getattr(legacy, name, None)
    if e is None:
        raise AttributeError('Element `{}` not found.'.format(name))
    warnings.warn('Dictionary-based elements are deprecated. Update to class-based elements or import from schemdraw.flow.legacy.', DeprecationWarning)
    return e