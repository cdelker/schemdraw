from .elements import Element, ElementDrawing, Element2Term
from .container import Container
from .twoterm import (Resistor, ResistorIEEE, ResistorIEC, ResistorVar, ResistorVarIEEE,
                      ResistorVarIEC, Thermistor, Photoresistor, PhotoresistorIEEE, PhotoresistorIEC,
                      Rshunt, Capacitor, Capacitor2, CapacitorVar, CapacitorTrim, Diode, Schottky, DiodeTunnel,
                      DiodeShockley, Zener, Varactor, LED, LED2, Photodiode, Potentiometer, PotentiometerIEEE,
                      PotentiometerIEC, Diac, Triac, SCR, Memristor, Memristor2, Josephson, Fuse, FuseUS, FuseIEEE,
                      FuseIEC, Inductor, Inductor2, Crystal, Breaker, CPE, SparkGap, RBox, RBoxVar,
                      PotBox, PhotoresistorBox, Nullator, Norator, CurrentMirror, VoltageMirror)
from .oneterm import Ground, GroundSignal, GroundChassis, Antenna, AntennaLoop, AntennaLoop2, Vss, Vdd, NoConnect
from .opamp import Opamp
from .sources import (Source, SourceV, SourceI, SourceSin, SourcePulse, SourceSquare, SourceTriangle, SourceRamp,
                      SourceControlled, SourceControlledV, SourceControlledI, BatteryCell, Battery, MeterV, MeterI,
                      MeterA, MeterOhm, Lamp, Lamp2, Solar, Neon)
from .switches import (Switch, SwitchSpdt, SwitchSpdt2, SwitchDpst, SwitchDpdt, Button, SwitchReed,
                       SwitchRotary, SwitchDIP)
from .transistors import (NFet, PFet, AnalogNFet, AnalogPFet, AnalogBiasedFet,
                          JFet, JFetN, JFetP, Bjt, BjtNpn, BjtPnp, BjtPnp2c, Bjt2, BjtNpn2, BjtPnp2,
                          BjtPnp2c2, NFet2, PFet2, JFet2, JFetN2, JFetP2, NMos, PMos, NMos2, PMos2)
from .misc import Speaker, Mic, Motor, AudioJack
from .xform import Transformer
from .cables import Coax, Triax
from .intcircuits import (IcPin, Ic, Multiplexer, IcDIP, VoltageRegulator, DFlipFlop, JKFlipFlop, Ic555,
                          SevenSegment, sevensegdigit)
from .lines import (Line, DataBusLine, Dot, Arrowhead, Arrow, DotDotDot, Wire, Gap, Label, Tag, CurrentLabel,
                    CurrentLabelInline, ZLabel, LoopCurrent, LoopArrow, Rect, Arc2, Arc3, ArcZ, ArcN, ArcLoop,
                    Annotate, Encircle, EncircleBox)
from .connectors import OrthoLines, RightLines, Header, Jumper, BusConnect, BusLine, DB25, DB9, CoaxConnect, Plug, Jack, Terminal
from .compound import ElementCompound, Optocoupler, Relay, Rectifier, Wheatstone
from .twoports import (ElementTwoport, TwoPort, VoltageTransactor, TransimpedanceTransactor, CurrentTransactor,
                       TransadmittanceTransactor, Nullor, VMCMPair)
from .outlets import (OutletA, OutletB, OutletC, OutletD, OutletE, OutletF, OutletG, OutletH, OutletI, OutletJ,
                      OutletK, OutletL)
from .image import ElementImage


__all__ = [
    "Element", "ElementDrawing", "ElementImage", "Element2Term", "Container",
    "Resistor", "ResistorIEEE", "ResistorIEC", "ResistorVar", "ResistorVarIEEE", "ResistorVarIEC", "Rshunt",
    "Thermistor", "Photoresistor", "PhotoresistorIEEE", "PhotoresistorIEC", "Capacitor", "Capacitor2",
    "CapacitorVar", "CapacitorTrim", "Diode", "Schottky", "DiodeTunnel", "DiodeShockley", "Zener", "Varactor",
    "LED", "LED2", "Photodiode", "Potentiometer", "PotentiometerIEEE", "PotentiometerIEC", "Diac", "Triac", "SCR",
    "Memristor", "Memristor2", "Josephson", "Fuse", "FuseUS", "FuseIEEE", "FuseIEC", "Inductor", "Inductor2",
    "Crystal", "Breaker", "ResistorVarIEC", "CPE", "SparkGap", "RBox", "RBoxVar", "PotBox", "PhotoresistorBox",
    "Nullator", "Norator", "CurrentMirror", "VoltageMirror",
    "Ground", "GroundSignal", "GroundChassis", "Antenna", "AntennaLoop", "AntennaLoop2", "Vss", "Vdd", "NoConnect",
    "Opamp", "Source", "SourceV", "SourceI", "SourceSin", "SourcePulse", "SourceSquare", "SourceTriangle",
    "SourceRamp", "SourceControlled", "SourceControlledV", "SourceControlledI", "BatteryCell", "Battery", "MeterV",
    "MeterI", "MeterA", "MeterOhm", "Lamp", "Lamp2", "Solar", "Neon", "Switch", "SwitchSpdt", "SwitchSpdt2", "SwitchDpst",
    "SwitchDpdt", "Button", "SwitchReed", "SwitchRotary", "SwitchDIP", "NFet", "PFet", "AnalogNFet", "AnalogPFet",
    "AnalogBiasedFet", "JFet", "JFetN", "JFetP",
    "Bjt", "BjtNpn", "BjtPnp", "BjtPnp2c", "Bjt2", "BjtNpn2", "BjtPnp2", "BjtPnp2c2", "NFet2", "PFet2", "JFet2",
    "JFetN2", "JFetP2", "NMos", "PMos", "NMos2", "PMos2",
    "Speaker", "Mic", "Motor", "AudioJack", "Transformer", "Coax", "Triax",
    "IcPin", "Ic", "Multiplexer", "IcDIP", "VoltageRegulator", "DFlipFlop", "JKFlipFlop", "Ic555", "SevenSegment",
    "sevensegdigit", "Line", "DataBusLine", "Dot", "Annotate", "ZLabel", "Arrowhead", "Arrow", "DotDotDot", "Wire",
    "Gap", "Label", "Tag", "CurrentLabel", "CurrentLabelInline", "LoopCurrent", "LoopArrow", "Rect",
    "Arc2", "Arc3", "ArcZ", "ArcN", "ArcLoop", "Encircle", "EncircleBox", "OrthoLines", "RightLines", "Header",
    "Jumper", "BusConnect", "BusLine", "DB25", "DB9", "CoaxConnect", "Plug", "Jack", "Terminal", "ElementCompound", "Optocoupler",
    "Relay", "Rectifier", "Wheatstone", "ElementTwoport", "TwoPort", "VoltageTransactor", "TransimpedanceTransactor",
    "CurrentTransactor", "TransadmittanceTransactor", "Nullor", "VMCMPair", "OutletA", "OutletB", "OutletC", "OutletD",
    "OutletE", "OutletF", "OutletG", "OutletH", "OutletI", "OutletJ", "OutletK", "OutletL"]


STYLE_IEEE = {'Resistor': ResistorIEEE,
              'ResistorVar': ResistorVarIEEE,
              'Potentiometer': PotentiometerIEEE,
              'Photoresistor': PhotoresistorIEEE,
              'Fuse': FuseUS}
STYLE_IEC = {'Resistor': ResistorIEC,
             'ResistorVar': ResistorVarIEC,
             'Potentiometer': PotentiometerIEC,
             'Photoresistor': PhotoresistorIEC,
             'Fuse': FuseIEC}


def style(style):
    ''' Set global element style

        Args:
            style: dictionary of elementname: Element
            to change the element module namespace.
            Use `elements.STYLE_IEEE` or `elements.STYLE_IEC`
            to define U.S./IEEE or European/IEC element styles.
    '''
    for name, element in style.items():
        globals()[name] = element
