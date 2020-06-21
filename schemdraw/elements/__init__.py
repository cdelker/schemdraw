from .elements import Element, ElementDrawing, Element2Term
from .twoterm import Resistor, RBox, ResistorVar, Thermistor, Photoresistor, PhotoresistorBox, Capacitor, Capacitor2, CapacitorVar, CapacitorTrim, Diode, Schottky, DiodeTunnel, DiodeShockley, Zener, LED, LED2, Photodiode, Potentiometer, Diac, Triac, SCR, Memristor, Memristor2, Josephson, Fuse, Inductor, Inductor2, Crystal, Breaker, PotBox, RBoxVar
from .oneterm import Ground, GroundSignal, GroundChassis, Antenna, AntennaLoop, AntennaLoop2, Vss, Vdd
from .opamp import Opamp
from .sources import Source, SourceV, SourceI, SourceSin, SourcePulse, SourceSquare, SourceTriangle, SourceRamp, SourceControlled, SourceControlledV, SourceControlledI, BatteryCell, Battery, MeterV, MeterI, MeterA, MeterOhm, Lamp, Solar, Neon
from .switches import Switch, SwitchSpdt, SwitchSpdt2, SwitchDpst, SwitchDpdt, Button
from .transistors import NFet, PFet, JFet, JFetN, JFetP, Bjt, BjtNpn, BjtPnp, BjtPnp2c
from .misc import Speaker, Mic, Motor, AudioJack
from .xform import Transformer
from .cables import Coax, Triax
from .intcircuits import IcPin, Ic, Multiplexer
from .lines import Line, Dot, Arrowhead, Arrow, LineDot, DotDotDot, Gap, Label, Tag, CurrentLabel, CurrentLabelInline, LoopCurrent, Rect
from .connectors import OrthoLines, RightLines, Header, Jumper, BusConnect, BusLine, DB25, DB9, CoaxConnect
from .compound import ElementCompound, Optocoupler, Relay


from . import legacy
import warnings

def __getattr__(name):
    e = getattr(legacy, name, None)
    if e is None:
        raise AttributeError('Element `{}` not found.'.format(name))
    warnings.warn('Dictionary-based elements are deprecated. Update to class-based elements or import from schemdraw.elements.legacy.', DeprecationWarning)
    return e
