''' DEPRECATED element definitions, based on dictionaries instead
    of classes, translated into their newer class counterparts.
'''

from functools import partial

from .. import elements as elm

RES = elm.Resistor
RES_VAR = elm.ResistorVar
RBOX = elm.ResistorIEC
POT = elm.Potentiometer
CAP = elm.Capacitor
CAP_P = partial(elm.Capacitor, polar=True)
CAP2 = elm.Capacitor2
CAP2_P = partial(elm.Capacitor2, polar=True)
CAP_VAR = elm.CapacitorVar
INDUCTOR = elm.Inductor
INDUCTOR2 = elm.Inductor2
SOURCE = elm.Source
SOURCE_V = elm.SourceV
SOURCE_I = elm.SourceI
SOURCE_SIN = elm.SourceSin
SOURCE_CONT = elm.SourceControlled
SOURCE_CONT_I = elm.SourceControlledI
SOURCE_CONT_V = elm.SourceControlledV
BATT_CELL = elm.BatteryCell
BATTERY = elm.Battery
METER_V = elm.MeterV
METER_I = elm.MeterI
METER_OHM = elm.MeterOhm
XTAL = elm.Crystal
DIODE = elm.Diode
DIODE_F = partial(elm.Diode, fill=True)
SCHOTTKY = elm.Schottky
SCHOTTKY_F = partial(elm.Schottky, fill=True)
DIODE_TUNNEL = elm.DiodeTunnel
DIODE_TUNNEL_F = partial(elm.DiodeTunnel, fill=True)
ZENER = elm.Zener
ZENER_F = partial(elm.Zener, fill=True)
LED = elm.LED  # Same name!
LED2 = elm.LED2
PHOTODIODE = elm.Photodiode
DIAC = elm.Diac
DIAC_F = partial(elm.Diac, fill=True)
TRIAC = elm.Triac
TRIAC_F = partial(elm.Triac, fill=True)
SCR = elm.SCR
SCR_F = partial(elm.SCR, fill=True)
MEMRISTOR = elm.Memristor
MEMRISTOR2 = elm.Memristor2
JJ = elm.Josephson
FUSE = elm.Fuse
DOT_OPEN = partial(elm.Dot, fill='white')
DOT = elm.Dot
ARROWHEAD = elm.Arrowhead
LINE = elm.Line
ARROW = elm.Arrow
ARROW_DOUBLE = partial(elm.Arrow, double=True)
ARROWLINE = elm.CurrentLabel
ARROW_I = elm.CurrentLabel
LINEDOT = elm.LineDot
LINE_DOT = elm.LineDot
LINE_DOT_DOUBLE = partial(elm.LineDot, double=True)
LINE_DOT_OPEN = partial(elm.LineDot, fill='white')
LINE_DOT_OPEN_DOUBLE = partial(elm.LineDot, fill='white', double=True)
ELLIPSIS = elm.DotDotDot
GAP_LABEL = elm.Gap
GAP = elm.Gap
LABEL = elm.Label
GND = elm.Ground
GND_SIG = elm.GroundSignal
GND_CHASSIS = elm.GroundChassis
ANT = elm.Antenna
VSS = elm.Vss
VDD = elm.Vdd
coax = COAX = elm.Coax
triax = TRIAX = elm.Triax
OPAMP_NOSIGN = partial(elm.Opamp, sign=False)
OPAMP = elm.Opamp
NFET = elm.NFet
NFET4 = partial(elm.NFet, bulk=True)
PFET = elm.PFet
PFET4 = partial(elm.PFet, bulk=True)
JFET_N = elm.JFetN
JFET_N_C = partial(elm.JFetN, circle=True)
JFET_P = elm.JFetP
JFET_P_C = partial(elm.JFetP, circle=True)
BJT = elm.Bjt
BJT_NPN = elm.BjtNpn
BJT_NPN_C = partial(elm.BjtNpn, circle=True)
BJT_PNP = elm.BjtPnp
BJT_PNP_C = partial(elm.BjtPnp, circle=True)
BJT_PNP_2C = elm.BjtPnp2c
SWITCH_SPST = elm.Switch
SWITCH_SPST_OPEN = partial(elm.Switch, action='open')
SWITCH_SPST_CLOSE = partial(elm.Switch, action='close')
SWITCH_SPDT = elm.SwitchSpdt
SWITCH_SPDT_OPEN = partial(elm.SwitchSpdt, action='open')
SWITCH_SPDT_CLOSE = partial(elm.SwitchSpdt, action='close')
SWITCH_SPDT2 = elm.SwitchSpdt
SWITCH_SPDT2_OPEN = partial(elm.SwitchSpdt2, action='open')
SWITCH_SPDT2_CLOSE = partial(elm.SwitchSpdt2, action='close')
BUTTON = elm.Button
BUTTON_NC = partial(elm.Button, nc=True)
SPEAKER = elm.Speaker
MIC = elm.Mic
LAMP = elm.Lamp
MOTOR = elm.Motor
transformer = elm.Transformer


def ic(*pins, **kwargs):
    ''' Define an integrated circuit element

        Parameters
        ----------
        *pins: dict
            A dictionary defining each input/output pin.
            Each dictionary may contain the following
            optional keys:

            name: string
                Signal name, labeled inside the IC box.
                If name is '>', a proper clock input triangle
                will be drawn instead of a text label.
            pin: string
                Pin name, labeled outside the IC box
            side: string ['left', 'right', 'top', 'bottom']
                Which side the pin belongs on
            pos: float
                Absolute position as fraction from 0-1 along the
                side. If not provided, pins are evenly spaced along
                the side.
            slot: string
                Position designation for the pin in "X/Y" format
                where X is the pin number and Y the total number
                of pins along the side. Use when missing pins
                are desired with even spacing.
            invert: bool
                Draw an invert bubble outside the pin
            invertradius: float
                Radius of invert bubble
            color: string
                Matplotlib color for label
            rotation: float
                Rotation angle for label (degrees)
            anchorname: string
                Name of anchor at end of pin lead. By default pins
                will have anchors of both the `name` parameter
                and `inXY` where X the side designation
                ['L', 'R', 'T', 'B'] and Y the pin number along
                that side.

        Keyword Arguments
        -----------------
        size: (w, h) tuple
            Size of the IC. If not provided, size is
            automatically determined based on number of
            pins and the pinspacing parameter.
        pinspacing: float
            Smallest distance between pins [1.25]
        edgepadH: float
            Additional distance from edge to first pin on
            vertical sides [.25]
        edgepadW: float
            Additional distance from edge to first pin on
            horizontal sides [.25]
        lblofst: float
            Default offset for (internal) labels [.15]
        plblofst: float
            Default offset for external pin labels [.1]
        leadlen: float
            Length of leads extending from box [.5]
        lblsize: int
            Font size for (internal) labels [14]
        plblsize: int
            Font size for external pin labels [11]
        slant: float
            Degrees to slant top and bottom sides,
            (e.g. for multiplexers) [0]
    '''
    pins = [elm.IcPin(**p) for p in pins]
    return elm.Ic(pins=pins, **kwargs)


def multiplexer(*pins, **kwargs):
    ''' Draw a multiplexer or demultiplexer.

        Parameters
        ----------
        *pins: dict
            List of pin definitions. See IC method.

        Keyword Arguments
        -----------------
        demux: bool
            Draw demultiplexer (opposite slope)
        slant: float
            Angle to slant top/bottom edges
        **kwargs:
            See IC method.
    '''
    slant = kwargs.pop('slant', 25)
    demux = kwargs.pop('demux', False)
    slant = -slant if not demux else slant
    return ic(*pins, slant=slant, **kwargs)
