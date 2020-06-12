from .elements import Element, ElementDrawing, Element2Term
from .twoterm import Resistor, ResistorBox, ResistorVar, Capacitor, Capacitor2, CapacitorVar, Diode, Schottky, DiodeTunnel, Zener, LED, LED2, Photodiode, Potentiometer, Diac, Triac, SCR, Memristor, Memristor2, Josephson, Fuse, Inductor, Inductor2, Crystal
from .oneterm import Ground, GroundSignal, GroundChassis, Antenna, Vss, Vdd
from .opamp import Opamp
from .sources import Source, SourceV, SourceI, SourceSin, SourceControlled, SourceControlledV, SourceControlledI, BatteryCell, Battery, MeterV, MeterI, MeterA, MeterOhm, Lamp
from .switches import Switch, SwitchSpdt, SwitchSpdt2, SwitchDpst, SwitchDpdt, Button
from .transistors import NFet, PFet, JFet, JFetN, JFetP, Bjt, BjtNpn, BjtPnp, BjtPnp2c
from .misc import Speaker, Mic, Motor
from .xform import Transformer
from .cables import Coax, Triax
from .intcircuits import IcPin, Ic, Multiplexer
from .lines import Line, Dot, Arrowhead, Arrow, LineDot, DotDotDot, Gap, Label, CurrentLabel, CurrentLabelInline, LoopCurrent


from . import legacy
import warnings

def __getattr__(name):
    e = getattr(legacy, name)
    warnings.warn('Dictionary-based elements are deprecated. Update to class-based elements or import from schemdraw.elements.legacy.', DeprecationWarning)
    return e
