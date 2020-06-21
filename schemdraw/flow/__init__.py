from .flow import Box, Subroutine, Data, Start, Decision, Connect
from ..elements import Arrow, Arrowhead, Line, Dot


from . import legacy
import warnings

def __getattr__(name):
    e = getattr(legacy, name, None)
    if e is None:
        raise AttributeError('Element `{}` not found.'.format(name))
    warnings.warn('Dictionary-based elements are deprecated. Update to class-based elements or import from schemdraw.flow.legacy.', DeprecationWarning)
    return e