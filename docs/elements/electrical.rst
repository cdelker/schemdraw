.. _electrical:

Basic Elements
==============

See :ref:`elecelements` for complete class definitions for these elements.

.. jupyter-execute::
    :hide-code:

    from functools import partial
    import schemdraw
    from schemdraw import elements as elm
    schemdraw.use('svg')


Two-terminal
------------

Two-terminal devices subclass :py:class:`schemdraw.elements.Element2Term`, and have leads that will be extended to make the element the desired length depending on the arguments.
All two-terminal elements define `start`, `end`, and `center` anchors for placing, and a few define other anchors as shown in blue in the tables below.
Some elements have optional parameters, shown in parenthesis in the table below.


.. _styledelements:

Resistors
^^^^^^^^^

Resistors elements change style based on IEEE/U.S. vs IEC/European style configured by :py:meth:`schemdraw.elements.style`.
Selectable elements, such as `Resistor`, point to either `ResistorIEEE` or `ResistorIEC`, for example.


IEEE Style
**********

IEEE style, common in the U.S., is the default, or it can be configured using

.. jupyter-execute::
    :hide-output:

    elm.style(elm.STYLE_IEEE)


.. element_list::

    Resistor()
    ResistorVar()
    Potentiometer()
    Photoresistor()
    Fuse()


IEC/European Style
******************

IEC style can be enabled using

.. jupyter-execute::
    :hide-output:

    elm.style(elm.STYLE_IEC)


.. element_list::

    Resistor()
    ResistorVar()
    Potentiometer()
    Photoresistor()
    Fuse()


All Resistors
*************

Either IEEE or IEC styles are always available with these Elements.

.. element_list::

    ResistorIEEE()
    ResistorIEC()
    ResistorVarIEEE()
    ResistorVarIEC()
    PotentiometerIEEE()
    PotentiometerIEC()
    PhotoresistorIEEE()
    PhotoresistorIEC()
    FuseUS()
    FuseIEEE()
    FuseIEC()
    Rshunt()


Capacitors and Inductors
^^^^^^^^^^^^^^^^^^^^^^^^

.. element_list::

    Capacitor()
    Capacitor(polar=True)
    Capacitor2()
    Capacitor2(polar=True)
    CapacitorVar()
    CapacitorTrim()
    Inductor()
    Inductor2()
    Inductor2(loops=2)


Diodes
^^^^^^

All diodes may be filled by passing `fill=True`.

.. element_list::

    Diode()
    Diode(fill=True)
    Schottky()
    DiodeTunnel()
    DiodeShockley()
    Zener()
    DiodeTVS()
    Varactor()
    LED()
    LED2()
    LED(fill='red')
    Photodiode()
    Diac()
    Triac()
    SCR()


Pathological
^^^^^^^^^^^^^

.. element_list::
    :ncols: 2

    Nullator()
    Norator()
    CurrentMirror()
    VoltageMirror()


Miscellaneous
^^^^^^^^^^^^^

.. element_list::

    Breaker()
    Crystal()
    CPE()
    Josephson()
    Josephson(box=True)
    Motor()
    Lamp()
    Lamp2()
    Neon()
    Thermistor()
    Memristor()
    Memristor2()
    Jack()
    Plug()
    Terminal()
    SparkGap()


Sources and Meters
^^^^^^^^^^^^^^^^^^

.. element_list::

    Source()
    SourceV()
    SourceI()
    SourceSin()
    SourcePulse()
    SourceSquare()
    SourceTriangle()
    SourceRamp()
    SourceControlled()
    SourceControlledI()
    SourceControlledV()
    BatteryCell()
    Battery()
    MeterV()
    MeterA()
    MeterI()
    MeterOhm()
    Solar()


Switches
^^^^^^^^

.. element_list::

    Button()
    Button(nc=True)
    Button(contacts=False)
    Switch()
    Switch(nc=True)
    Switch(action='open')
    Switch(action='close')
    Switch(contacts=False)
    Switch(contacts=False, nc=True)
    SwitchReed()


Lines and Arrows
^^^^^^^^^^^^^^^^

.. element_list::

    Line()
    Arrow()
    Arrow(double=True)
    DataBusLine()

Also see :ref:`connecting`.


Single-Terminal
---------------

Single terminal elements are drawn about a single point, and do not move the current drawing position.

Power and Ground
^^^^^^^^^^^^^^^^

.. element_list::

    Ground()
    GroundSignal()
    GroundChassis()
    Vss()
    Vdd()


Antennas
^^^^^^^^

.. element_list::

    Antenna()
    AntennaLoop()
    AntennaLoop2()


Connection Dots
^^^^^^^^^^^^^^^

.. element_list::

    Dot()
    Dot(open=True)
    DotDotDot()
    Arrowhead()
    NoConnect()


Switches
--------

The standard toggle switch is listed with other two-terminal elements above.
Other switch configurations are shown here.

Single-pole double-throw
^^^^^^^^^^^^^^^^^^^^^^^^

Two options for SPDT switches can be also be drawn with arrows by
adding `action='open'` or `action='close'` parameters.

.. element_list::
    :ncols: 2

    SwitchSpdt()
    SwitchSpdt2()
    SwitchSpdt(action='open')
    SwitchSpdt2(action='open')
    SwitchSpdt(action='close')
    SwitchSpdt2(action='close')


Double-pole
^^^^^^^^^^^

DPST and DPDT switches have a `link` parameter for disabling the dotted line
lnking the poles.

.. element_list::
    :ncols: 2

    SwitchDpst()
    SwitchDpdt()
    SwitchDpst(link=False)
    SwitchDpdt(link=False)


Rotary Switch
^^^^^^^^^^^^^

The rotary switch :py:class:`schemdraw.elements.switches.SwitchRotary` takes several
parameters, with `n` being the number of contacts and other parameters defining the contact placement.

.. element_list::
    :ncols: 2

    SwitchRotary(n=6)


DIP Switch
^^^^^^^^^^

A set of switches in a dual-inline package, where can show each switch flipped up or down.
See :py:class:`schemdraw.elements.switches.SwitchDIP` for options.

.. element_list::
    :ncols: 2

    SwitchDIP()
    SwitchDIP(pattern=[0, 0, 1])


Audio Elements
--------------

Speakers, Microphones, Jacks

.. element_list::
    :ncols: 2

    Speaker()
    Mic()
    AudioJack()
    AudioJack(ring=True)
    AudioJack(switch=True)
    AudioJack(switch=True, ring=True, ringswitch=True)

    
Labels
------

The `Label` element can be used to add a label anywhere.
The `Gap` is like an "invisible" element, useful for marking the voltage between output terminals.

.. element_list::
    :ncols: 2

    Gap(label=['+', 'Gap', '-'])
    Label(label='Hello')
    Tag(label='Tag')


Operational Amplifiers
----------------------

The :py:class:`schemdraw.elements.opamp.Opamp` element defines several anchors for various inputs, including voltage supplies and offset nulls. Optional leads can be added using the `leads` parameter, with anchors exteded to the ends of the leads.

.. grid:: 3
    :gutter: 0

    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        Opamp

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing(fontsize=10):
                op = elm.Opamp()
                elm.Dot().at(op.in1).color('blue').label('in1', loc='left', valign='center')
                elm.Dot().at(op.in2).color('blue').label('in2', loc='left', valign='center')
                elm.Dot().at(op.out).color('blue').label('out', loc='right', valign='center')
                elm.Dot().at(op.vd).color('blue').label('vd', loc='top')
                elm.Dot().at(op.vs).color('blue').label('vs', loc='bottom')
                elm.Dot().at(op.n1).color('blue').label('n1', loc='bottom')
                elm.Dot().at(op.n2).color('blue').label('n2', loc='top')
                elm.Dot().at(op.n2a).color('blue').label('n2a', loc='top')
                elm.Dot().at(op.n1a).color('blue').label('n1a', loc='bottom')

    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        Opamp(sign=False)

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing(fontsize=10):
                op2 = elm.Opamp(sign=False).at([5, 0]).right()
                elm.Dot().at(op2.in1).color('blue').label('in1', loc='left', valign='center')
                elm.Dot().at(op2.in2).color('blue').label('in2', loc='left', valign='center')
                elm.Dot().at(op2.out).color('blue').label('out', loc='right', valign='center')
                elm.Dot().at(op2.vd).color('blue').label('vd', loc='top')
                elm.Dot().at(op2.vs).color('blue').label('vs', loc='bottom')
                elm.Dot().at(op2.n1).color('blue').label('n1', loc='bottom')
                elm.Dot().at(op2.n2).color('blue').label('n2', loc='top')
                elm.Dot().at(op2.n2a).color('blue').label('n2a', loc='top')
                elm.Dot().at(op2.n1a).color('blue').label('n1a', loc='bottom')

    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        Opamp(leads=True)

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing(fontsize=10):
                op = (elm.Opamp(leads=True).at([10, 0]).right()
                        .label('in1', loc='in1', halign='right', color='blue')
                        .label('in2', loc='in2', halign='right', color='blue')
                        .label('out', loc='out', halign='left', color='blue'))
                elm.Dot().at(op.in1).color('blue')
                elm.Dot().at(op.in2).color('blue')
                elm.Dot().at(op.out).color('blue')


Transistors
-----------

Bipolar Junction Transistors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. element_list::

    Bjt()
    BjtNpn()
    BjtPnp()
    Bjt(circle=True)
    BjtNpn(circle=True)
    BjtPnp(circle=True)
    BjtPnp2c()
    BjtPnp2c(circle=True)
    NpnSchottky()
    PnpSchottky()
    IgbtN()
    IgbtP()
    NpnPhoto()
    PnpPhoto()


Field-Effect Transistors
^^^^^^^^^^^^^^^^^^^^^^^^

.. element_list::
    NFet()
    PFet()
    NFet(bulk=True)
    PFet(bulk=True)
    JFet()
    JFetN()
    JFetP()
    JFetN(circle=True)
    JFetP(circle=True)
    Hemt()
    Hemt(split=False)
    Hemt(arrow=False)
    NMos()
    PMos()
    NMos(diode=True)
    PMos(diode=True)
    NMos(circle=True)
    PMos(circle=True)


.. element_list::
    :ncols: 2

    AnalogNFet()
    AnalogPFet()
    AnalogBiasedFet()
    AnalogNFet(bulk=True)
    AnalogPFet(bulk=True)
    AnalogBiasedFet(bluk=True)
    AnalogBiasedFet(arrow=False)
    AnalogPFet(arrow=False)
    AnalogBiasedFet(arrow=False)
    AnalogNFet(offset_gate=False)
    AnalogPFet(offset_gate=False)
    AnalogBiasedFet(offset_gate=False)


"Two-Terminal" Transistors
^^^^^^^^^^^^^^^^^^^^^^^^^^

Another set of transistor elements subclass :py:class:`schemdraw.elements.Element2Term` so they
have emitter and collector (or source and drain) leads extended to the desired length.
These can be easier to place centered between endpoints, for example.

.. element_list::

    BjtNpn2()
    BjtPnp2()
    BjtPnp2c2()
    NFet2()
    PFet2()
    JFetN2()
    JFetP2()
    NMos2(diode=True)
    PMos2(diode=True)
    NMos2(circle=True)
    PMos2(circle=True)


Two-ports
-----------

Twoport elements share the interface defined by :py:class:`schemdraw.elements.twoports.ElementTwoport`, providing a set of anchors and various styling options. The terminals and box can be enabled or disabled using the `terminals` and `box` arguments. In addition, the `boxfill`, `boxlw`, and `boxls` provide the option to style the outline separately from other elements.

.. element_list::
    :ncols: 2

    TwoPort()
    TwoPort(terminals=False, boxlw=3)


Generic
^^^^^^^

.. element_list::
    :ncols: 2

    TwoPort()
    TwoPort(reverse_output=True)
    TwoPort(arrow=False)
    TwoPort(sign=False)


Transactors (ideal amplifiers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Like the generic twoport, the transactors provide the option to reverse the direction of the output or current using the `reverse_output` argument.

.. element_list::
    :ncols: 2

    VoltageTransactor()
    TransimpedanceTransactor()
    TransadmittanceTransactor()
    CurrentTransactor()


Pathological
^^^^^^^^^^^^

.. element_list::
    :ncols: 2

    Nullor()
    VMCMPair()


Custom
^^^^^^

The :py:class:`schemdraw.elements.twoports.ElementTwoport` class can be used to define custom twoports by specifying an `input_element` and `output_element`. The `bpadx`, `bpady`, `minw`, `unit`, `width` can be used to tune the horizontal and vertical padding, minimum width of the elements, length of components, and width of the twoport respectively.


.. jupyter-execute::

    elm.ElementTwoport(
        input_element=elm.Inductor2,
        output_element=elm.SwitchReed,
        unit=2.5, width=2.5)

.. jupyter-execute::

    elm.ElementTwoport(
        input_element=elm.Lamp,
        output_element=partial(elm.Photodiode, reverse=True, flip=True),
        width=3)


Cables
------

:py:class:`schemdraw.elements.cables.Coax` and :py:class:`schemdraw.elements.cables.Triax` cables are 2-Terminal elements that can be made with several options and anchors.
Coax parameters include length, radius, and leadlen for setting the distance between leads and the shell.
Triax parameters include length, radiusinner, radiusouter, leadlen, and shieldofststart for offseting the outer shield from the inner guard.


.. grid:: 2
    :gutter: 0

    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        Coax

        .. jupyter-execute::
            :hide-code:

            elm.Coax()

    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        Triax()

        .. jupyter-execute::
            :hide-code:

            elm.Triax()

    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        Coax(length=5, radius=0.5)

        .. jupyter-execute::
            :hide-code:

            elm.Coax(length=5, radius=0.5)


    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        Triax(length=5, radiusinner=0.5)

        .. jupyter-execute::
            :hide-code:

            elm.Triax(length=5, radiusinner=0.5)

    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing(fontsize=10):
                C = elm.Coax().length(5)
                elm.Line().down().at(C.shieldstart).length(.2).label('shieldstart', 'lft', halign='right').color('blue')
                elm.Line().down().at(C.shieldcenter).length(.6).label('shieldcenter', 'lft', halign='right').color('blue')
                elm.Line().down().at(C.shieldend).length(1).label('shieldend', 'lft', halign='center').color('blue')
                elm.Line().up().at(C.shieldstart_top).length(.2).label('shieldstart_top', 'rgt', halign='right').color('blue')
                elm.Line().up().at(C.shieldcenter_top).length(.6).label('shieldcenter_top', 'rgt', halign='right').color('blue')
                elm.Line().up().at(C.shieldend_top).length(1).label('shieldend_top', 'rgt', halign='center').color('blue')


    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing(fontsize=10):
                C = elm.Triax().length(5)
                elm.Line().down().at(C.shieldstart).length(.2).label('shieldstart', 'left', halign='right').color('blue')
                elm.Line().down().at(C.shieldcenter).length(.6).label('shieldcenter', 'left', halign='right').color('blue')
                elm.Line().down().at(C.shieldend).length(1).label('shieldend', 'left', halign='center').color('blue')
                elm.Line().up().at(C.shieldstart_top).length(.2).label('shieldstart_top', 'rgt', halign='right').color('blue')
                elm.Line().up().at(C.shieldcenter_top).length(.6).label('shieldcenter_top', 'rgt', halign='right').color('blue')
                elm.Line().up().at(C.shieldend_top).length(1).label('shieldend_top', 'rgt', halign='center').color('blue')
                elm.Line().theta(45).at(C.guardend_top).length(1).label('guardend_top', 'rgt', halign='left').color('blue')
                elm.Line().theta(-45).at(C.guardend).length(1).label('guardend', 'rgt', halign='left').color('blue')
                elm.Line().theta(135).at(C.guardstart_top).length(.3).label('guardstart_top', 'left', halign='right').color('blue')
                elm.Line().theta(-145).at(C.guardstart).length(.5).label('guardstart', 'left', halign='right').color('blue')

.. element_list::
    :ncols: 2

    CoaxConnect()


Transformers
------------

The :py:class:`schemdraw.elements.xform.Transformer` element is used to create various transformers.
Anchors `p1`, `p2`, `s1`, and `s2` are defined for all transformers.
Other anchors can be created using the `taps` method to add tap locations to
either side.

.. element_list::

    Transformer()
    Transformer(loop=True)
    Transformer(core=False)


Here is a transformers with anchor "B" added using the `tap` method. Note the tap by itself
does not draw anything, but defines a named anchor to connect to.

.. jupyter-execute::

    with schemdraw.Drawing(fontsize=10) as d:
        x = elm.Transformer(t1=4, t2=8).tap(name='B', pos=3, side='secondary')
        elm.Line().at(x.s1).length(d.unit/4).label('s1', 'rgt').color('blue')
        elm.Line().at(x.s2).length(d.unit/4).label('s2', 'rgt').color('blue')
        elm.Line().at(x.p1).length(d.unit/4).left().label('p1', 'lft').color('blue')
        elm.Line().at(x.p2).length(d.unit/4).left().label('p2', 'lft').color('blue')
        elm.Line().at(x.B).length(d.unit/4).right().label('B', 'rgt').color('blue')
