from .logic import And, Or, Buf, Not, NotNot
from ..elements import Arrow, Arrowhead, Dot, Line


from . import legacy
import warnings

def __getattr__(name):
    e = getattr(legacy, name)
    warnings.warn('Dictionary-based elements are deprecated. Update to class-based elements or import from schemdraw.logic.legacy.', DeprecationWarning)
    return e