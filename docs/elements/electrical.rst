.. _electrical:

Basic Elements
==============

See :ref:`elecelements` for complete class definitions for these elements.

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    from functools import partial
    import schemdraw
    from schemdraw import elements as elm
    from schemdraw.elements import *

    def drawElements(elmlist, cols=3, dx=8, dy=2, lblofst=None, lblloc='rgt'):
        d = schemdraw.Drawing(fontsize=12)
        for i, e in enumerate(elmlist):
            y = i//cols*-dy
            x = (i%cols) * dx

            if isinstance(e, str):
                name = e
                e = getattr(elm, e)
            else:
                name = type(e()).__name__
            if hasattr(e, 'keywords'):  # partials have keywords attribute
                args = ', '.join(['{}={}'.format(k, v) for k, v in e.keywords.items()])
                name = '{}({})'.format(name, args)
            newelm = e().right().at((x, y)).label(name, loc=lblloc, halign='left', valign='center', ofst=lblofst)
            if len(newelm.anchors) > 0:
                for aname, apos in newelm.anchors.items():
                    if aname not in ['center', 'start', 'end', 'istart', 'iend',
                                     'isource', 'idrain', 'iemitter', 'icollector', 'xy']:
                        newelm.label(aname, loc=aname, color='blue', fontsize=10)
            d += newelm
        return d


Two-terminal
------------

Two-terminal devices subclass :py:class:`schemdraw.elements.Element2Term`, and have leads that will be extended to make the element the desired length depending on the arguments.
All two-terminal elements define `start`, `end`, and `center` anchors for placing, and a few define other anchors as shown in blue in the tables below.
Some elements have optional parameters, shown in parenthesis in the table below.


.. _styledelements:

Styled Elements
^^^^^^^^^^^^^^^

These elements change based on IEEE/U.S. vs IEC/European style configured by :py:meth:`schemdraw.elements.style`.
Selectable elements, such as `Resistor`, point to either `ResistorIEEE` or `ResistorIEC`, for example.

IEEE Style
**********

IEEE style, common in the U.S., is the default, or it can be configured using

.. code-block:: python

    elm.style(elm.STYLE_IEEE)


.. jupyter-execute::
    :hide-code:

    elm.style(elm.STYLE_IEEE)
    elmlist = ['Resistor', 'ResistorVar', 'ResistorVar', 'Potentiometer', 'Photoresistor', 'Fuse']
    drawElements(elmlist, cols=2)


IEC/European Style
******************

IEC style can be enabled using

.. code-block:: python

    elm.style(elm.STYLE_IEC)

.. jupyter-execute::
    :hide-code:

    elm.style(elm.STYLE_IEC)
    elmlist = ['Resistor', 'ResistorVar', 'ResistorVar', 'Potentiometer', 'Photoresistor', 'Fuse']
    drawElements(elmlist, cols=2)


Resistors
^^^^^^^^^

Both styles of resistors are always available using these classes.

.. jupyter-execute::
    :hide-code:

    elmlist = [ResistorIEEE, ResistorIEC, ResistorVarIEEE, ResistorVarIEC, Rshunt, PotentiometerIEEE,
               PotentiometerIEC, FuseUS, FuseIEEE, FuseIEC]
    drawElements(elmlist, cols=2)



Capacitors and Inductors
^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:

    elmlist = [Capacitor, partial(Capacitor, polar=True),
               Capacitor2, partial(Capacitor2, polar=True),
               CapacitorVar, CapacitorTrim, Inductor, Inductor2,
               partial(Inductor2, loops=2)]
    drawElements(elmlist, cols=2)


Diodes
^^^^^^

.. jupyter-execute::
    :hide-code:
    
    elmlist = [Diode,
               partial(Diode, fill=True), Schottky, DiodeTunnel, DiodeShockley,
               Zener, Varactor, LED, LED2, Photodiode, Diac, Triac, SCR]
    drawElements(elmlist, cols=2)

Pathological
^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:

    elmlist = [Nullator, Norator, CurrentMirror, VoltageMirror]
    drawElements(elmlist, cols=2)

Miscellaneous
^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:
    
    elmlist = [Breaker, Crystal, CPE, Josephson, partial(Josephson, box=True), Motor, Lamp, Lamp2, Neon, Thermistor, Memristor, Memristor2, Jack, Plug, Terminal]
    drawElements(elmlist, cols=2)


Sources and Meters
^^^^^^^^^^^^^^^^^^
    
.. jupyter-execute::
    :hide-code:
    
    elmlist = [Source, SourceV, SourceI, SourceSin, SourcePulse,
               SourceSquare, SourceTriangle,
               SourceRamp, SourceControlled,
               SourceControlledV, SourceControlledI, BatteryCell,
               Battery, MeterV, MeterA, MeterI, MeterOhm,
               Solar]
    drawElements(elmlist, cols=2)


Switches
^^^^^^^^

.. jupyter-execute::
    :hide-code:
    
    elmlist = [Button, partial(Button, nc=True),
               Switch, partial(Switch, action='open'),
               partial(Switch, action='close'),
               SwitchReed]
    drawElements(elmlist, cols=2)


Lines and Arrows
^^^^^^^^^^^^^^^^
    
.. jupyter-execute::
    :hide-code:
    
    elmlist = [Line, Arrow, partial(Arrow, double=True), DataBusLine]
    drawElements(elmlist, cols=2)


Single-Terminal
---------------

Single terminal elements are drawn about a single point, and do not move the current drawing position.

Power and Ground
^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:
    
    # One-terminal, don't move position
    elmlist = [Ground, GroundSignal, GroundChassis,
               Vss, Vdd]
    drawElements(elmlist, dx=4, cols=3)


Antennas
^^^^^^^^

.. jupyter-execute::
    :hide-code:
    
    elmlist = [Antenna, AntennaLoop, AntennaLoop2]
    drawElements(elmlist, dx=4, cols=3)


Connection Dots
^^^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:
    
    # One-terminal, don't move position
    elmlist = [Dot, partial(Dot, open=True), DotDotDot,
               Arrowhead, NoConnect]
    drawElements(elmlist, dx=4, cols=3)



Switches
--------

The standard toggle switch is listed with other two-terminal elements above.
Other switch configurations are shown here.

Single-pole double-throw
^^^^^^^^^^^^^^^^^^^^^^^^

Two options for SPDT switches can be also be drawn with arrows by
adding `action='open'` or `action='close'` parameters.

.. jupyter-execute::
    :hide-code:

    elmlist = [SwitchSpdt, SwitchSpdt2,
              partial(SwitchSpdt, action='open'), partial(SwitchSpdt2, action='open'),
              partial(SwitchSpdt, action='close'), partial(SwitchSpdt2, action='close')]
    drawElements(elmlist, cols=2, dx=9, dy=3, lblofst=(.5, 0))


Double-pole
^^^^^^^^^^^

DPST and DPDT switches have a `link` parameter for disabling the dotted line
lnking the poles.

.. jupyter-execute::
    :hide-code:

    elmlist = [SwitchDpst, SwitchDpdt,
               partial(SwitchDpst, link=False),
               partial(SwitchDpdt, link=False)]
    drawElements(elmlist, cols=2, dx=8, dy=4, lblofst=(.7, 0))


Rotary Switch
^^^^^^^^^^^^^

The rotary switch :py:class:`schemdraw.elements.switches.SwitchRotary` takes several parameters, with `n` being the number of contacts and other parameters defining the contact placement.

.. jupyter-execute::
    :hide-code:
    
    (SwitchRotary(n=6).label('SwitchRotary(n=6)', ofst=(0,0.5))
                      .label('P', loc='P', halign='right', color='blue', fontsize=9, ofst=(-.2, 0))
                      .label('T1', loc='T1', color='blue', fontsize=9, ofst=(0, -.2))
                      .label('T2', loc='T2', color='blue', fontsize=9, ofst=(0, -.5))
                      .label('T3', loc='T3', color='blue', fontsize=9, ofst=(.2, 0))
                      .label('T4', loc='T4', color='blue', fontsize=9, ofst=(.2, 0))
                      .label('T5', loc='T5', color='blue', fontsize=9, ofst=(0, .2))
                      .label('T6', loc='T6', color='blue', fontsize=9, ofst=(0, .2))
    )


DIP Switch
^^^^^^^^^^

A set of switches in a dual-inline package, where can show each switch flipped up or down.
See :py:class:`schemdraw.elements.switches.SwitchDIP` for options.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()
    d += (elm.SwitchDIP().label('SwitchDIP', 'right')
         .label('a1', color='blue', loc='a1', valign='top', fontsize=11)
         .label('a2', color='blue', loc='a2', valign='top', fontsize=11)
         .label('a3', color='blue', loc='a3', valign='top', fontsize=11)
         .label('b1', color='blue', loc='b1', valign='bottom', fontsize=11)
         .label('b2', color='blue', loc='b2', valign='bottom', fontsize=11)
         .label('b3', color='blue', loc='b3', valign='bottom', fontsize=11))
    d += (elm.SwitchDIP(pattern=(0, 0, 1)).label('SwitchDIP(pattern=(0, 0, 1))', 'right')
         .label('a1', color='blue', loc='a1', valign='top', fontsize=11)
         .label('a2', color='blue', loc='a2', valign='top', fontsize=11)
         .label('a3', color='blue', loc='a3', valign='top', fontsize=11)
         .label('b1', color='blue', loc='b1', valign='bottom', fontsize=11)
         .label('b2', color='blue', loc='b2', valign='bottom', fontsize=11)
         .label('b3', color='blue', loc='b3', valign='bottom', fontsize=11).at((5, 0)))
    d.draw()




Audio Elements
--------------

Speakers, Microphones, Jacks

.. jupyter-execute::
    :hide-code:
    
    elmlist = [Speaker, Mic]
    drawElements(elmlist, cols=2, dy=5, dx=5, lblofst=[.7, 0])
    
    
.. jupyter-execute::
    :hide-code:
    
    elmlist = [AudioJack, partial(AudioJack, ring=True),
               partial(AudioJack, switch=True),
               partial(AudioJack, switch=True, ring=True, ringswitch=True)]
    drawElements(elmlist, cols=1, dy=3, lblofst=[1.7, 0])

    
Labels
------

The `Label` element can be used to add a label anywhere.
The `Gap` is like an "invisible" element, useful for marking the voltage between output terminals.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=12)
    d += elm.Line().right().length(1)
    d += elm.Dot(open=True)
    d += elm.Gap().down().label(['+','Gap','–'])
    d += elm.Dot(open=True)
    d += elm.Line().left().length(1)
    d += elm.Label(label='Label').at([3.5, -.5])
    d += elm.Tag().right().at([5, -.5]).label('Tag')
    d.draw()


Operational Amplifiers
----------------------

The :py:class:`schemdraw.elements.opamp.Opamp` element defines several anchors for various inputs, including voltage supplies and offset nulls. Optional leads can be added using the `leads` parameter, with anchors exteded to the ends of the leads.


.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=12)
    d += (op := elm.Opamp().label('Opamp', ofst=.6))
    d += elm.Dot().at(op.in1).color('blue').label('in1', loc='left', valign='center')
    d += elm.Dot().at(op.in2).color('blue').label('in2', loc='left', valign='center')
    d += elm.Dot().at(op.out).color('blue').label('out', loc='right', valign='center')
    d += elm.Dot().at(op.vd).color('blue').label('vd', loc='top')
    d += elm.Dot().at(op.vs).color('blue').label('vs', loc='bottom')
    d += elm.Dot().at(op.n1).color('blue').label('n1', loc='bottom')
    d += elm.Dot().at(op.n2).color('blue').label('n2', loc='top')
    d += elm.Dot().at(op.n2a).color('blue').label('n2a', loc='top')
    d += elm.Dot().at(op.n1a).color('blue').label('n1a', loc='bottom')

    d += (op2 := elm.Opamp(sign=False).at([5, 0]).right().label('Opamp(sign=False)', ofst=.6))
    d += elm.Dot().at(op2.in1).color('blue').label('in1', loc='left', valign='center')
    d += elm.Dot().at(op2.in2).color('blue').label('in2', loc='left', valign='center')
    d += elm.Dot().at(op2.out).color('blue').label('out', loc='right', valign='center')
    d += elm.Dot().at(op2.vd).color('blue').label('vd', loc='top')
    d += elm.Dot().at(op2.vs).color('blue').label('vs', loc='bottom')
    d += elm.Dot().at(op2.n1).color('blue').label('n1', loc='bottom')
    d += elm.Dot().at(op2.n2).color('blue').label('n2', loc='top')
    d += elm.Dot().at(op2.n2a).color('blue').label('n2a', loc='top')
    d += elm.Dot().at(op2.n1a).color('blue').label('n1a', loc='bottom')

    d += (op:=elm.Opamp(leads=True).at([10, 0]).right().label('Opamp(leads=True)', ofst=.6)
            .label('in1', loc='in1', halign='right', color='blue')
            .label('in2', loc='in2', halign='right', color='blue')
            .label('out', loc='out', halign='left', color='blue'))
    d += elm.Dot().at(op.in1).color('blue')
    d += elm.Dot().at(op.in2).color('blue')
    d += elm.Dot().at(op.out).color('blue')
    d.draw()

Transistors
-----------

Bipolar Junction Transistors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:

    elmlist = [Bjt, BjtNpn, BjtPnp,
               partial(Bjt, circle=True),
               partial(BjtNpn, circle=True), partial(BjtPnp, circle=True),
               BjtPnp2c, partial(BjtPnp2c, circle=True),]
    drawElements(elmlist, dx=6.5, dy=3, lblofst=(0, .2))


Field-Effect Transistors
^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:

    elmlist = [NFet, PFet, partial(NFet, bulk=True), partial(PFet, bulk=True),
               JFet, JFetN, JFetP, partial(JFetN, circle=True), partial(JFetP, circle=True),
               AnalogNFet, AnalogPFet, AnalogBiasedFet, partial(AnalogNFet, bulk=True),
               partial(AnalogPFet, bulk=True), partial(AnalogBiasedFet, bulk=True),
               partial(AnalogNFet, arrow=False), partial(AnalogPFet, arrow=False),
               partial(AnalogBiasedFet, arrow=False), partial(AnalogNFet, offset_gate=False),
               partial(AnalogPFet, offset_gate=False), partial(AnalogBiasedFet, offset_gate=False),]
    drawElements(elmlist, dx=6.5, dy=3, lblofst=[0, -.8])


"Two-Terminal" Transistors
^^^^^^^^^^^^^^^^^^^^^^^^^^

Another set of transistor elements subclass :py:class:`schemdraw.elements.Element2Term` so they
have emitter and collector (or source and drain) leads extended to the desired length.
These can be easier to place centered between endpoints, for example.

.. jupyter-execute::
    :hide-code:

    elmlist = [BjtNpn2, BjtPnp2, BjtPnp2c2, NFet2, PFet2, JFetN2, JFetP2]
    drawElements(elmlist, dx=6.5, dy=3)


Two-ports
-----------

Twoport elements share the interface defined by :py:class:`schemdraw.elements.twoports.ElementTwoport`, providing a set of anchors and various styling options. The terminals and box can be enabled or disabled using the `terminals` and `box` arguments. In addition, the `boxfill`, `boxlw`, and `boxls` provide the option to style the outline separately from other elements.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=12)
    d += (tp := elm.TwoPort().label('TwoPort', ofst=.6)).anchor('center')
    d += elm.Dot().at(tp.in_p).color('blue').label('in_p', loc='left', valign='center')
    d += elm.Dot().at(tp.in_n).color('blue').label('in_n', loc='left', valign='center')
    d += elm.Dot().at(tp.out_p).color('blue').label('out_p', loc='right', valign='center')
    d += elm.Dot().at(tp.out_n).color('blue').label('in_n', loc='right', valign='center')
    d += elm.Dot().at(tp.center).color('blue').label('center', loc='top')

    d += (tp := elm.TwoPort(terminals=False, boxlw=3).label('TwoPort(terminals=False, boxlw=3)', ofst=.6)).anchor('center').at([7,0])

    d.draw()

Generic
^^^^^^^

.. jupyter-execute::
    :hide-code:

    elmlist = [TwoPort, partial(TwoPort, reverse_output=True), partial(TwoPort, arrow=False),
               partial(TwoPort, sign=False)]
    drawElements(elmlist, dy=3, cols=2)


Transactors (ideal amplifiers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Like the generic twoport, the transactors provide the option to reverse the direction of the output or current using the `reverse_output` argument.

.. jupyter-execute::
    :hide-code:

    elmlist = [VoltageTransactor, TransimpedanceTransactor,TransadmittanceTransactor, CurrentTransactor]
    drawElements(elmlist, dy=3, cols=2)

Pathological
^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:

    elmlist = [Nullor, VMCMPair]
    drawElements(elmlist, dy=3, cols=2)

Custom
^^^^^^

The :py:class:`schemdraw.elements.twoports.ElementTwoport` class can be used to define custom twoports by specifying an `input_element` and `output_element`. The `bpadx`, `bpady`, `minw`, `unit`, `width` can be used to tune the horizontal and vertical padding, minimum width of the elements, length of components, and width of the twoport respectively.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::

    d += elm.ElementTwoport(input_element=elm.Inductor2,
                            output_element=elm.SwitchReed,
                            unit=2.5, width=2.5).anchor('center')

    d += elm.ElementTwoport(input_element=elm.Lamp,
                            output_element=partial(elm.Photodiode, reverse=True, flip=True),
                            width=3).anchor('center').at([7,0])

.. jupyter-execute::
    :hide-code:

    d.draw()

Cables
------

:py:class:`schemdraw.elements.cables.Coax` and :py:class:`schemdraw.elements.cables.Triax` cables are 2-Terminal elements that can be made with several options and anchors.
Coax parameters include length, radius, and leadlen for setting the distance between leads and the shell.
Triax parameters include length, radiusinner, radiusouter, leadlen, and shieldofststart for offseting the outer shield from the inner guard.


.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=10)
    d += elm.Coax().label('Coax')
    d += elm.Coax(length=4, radius=.5).label('Coax(length=5, radius=.5)')
    d += (C := elm.Coax().at([0, -3]).length(5))
    d += elm.Line().down().at(C.shieldstart).length(.2).label('shieldstart', 'lft', halign='right').color('blue')
    d += elm.Line().down().at(C.shieldcenter).length(.6).label('shieldcenter', 'lft', halign='right').color('blue')
    d += elm.Line().down().at(C.shieldend).length(1).label('shieldend', 'lft', halign='center').color('blue')
    d += elm.Line().up().at(C.shieldstart_top).length(.2).label('shieldstart_top', 'rgt', halign='right').color('blue')
    d += elm.Line().up().at(C.shieldcenter_top).length(.6).label('shieldcenter_top', 'rgt', halign='right').color('blue')
    d += elm.Line().up().at(C.shieldend_top).length(1).label('shieldend_top', 'rgt', halign='center').color('blue')

    d += elm.Triax().at([0, -7]).right().label('Triax')
    d += elm.Triax(length=4, radiusinner=.5).label('Triax(length=5, radiusinner=.5)')
    d += (C := elm.Triax().at([1, -10]).length(5))
    d += elm.Line().down().at(C.shieldstart).length(.2).label('shieldstart', 'left', halign='right').color('blue')
    d += elm.Line().down().at(C.shieldcenter).length(.6).label('shieldcenter', 'left', halign='right').color('blue')
    d += elm.Line().down().at(C.shieldend).length(1).label('shieldend', 'left', halign='center').color('blue')
    d += elm.Line().up().at(C.shieldstart_top).length(.2).label('shieldstart_top', 'rgt', halign='right').color('blue')
    d += elm.Line().up().at(C.shieldcenter_top).length(.6).label('shieldcenter_top', 'rgt', halign='right').color('blue')
    d += elm.Line().up().at(C.shieldend_top).length(1).label('shieldend_top', 'rgt', halign='center').color('blue')
    d += elm.Line().theta(45).at(C.guardend_top).length(1).label('guardend_top', 'rgt', halign='left').color('blue')
    d += elm.Line().theta(-45).at(C.guardend).length(1).label('guardend', 'rgt', halign='left').color('blue')
    d += elm.Line().theta(135).at(C.guardstart_top).length(.3).label('guardstart_top', 'left', halign='right').color('blue')
    d += elm.Line().theta(-145).at(C.guardstart).length(.5).label('guardstart', 'left', halign='right').color('blue')
    d.draw()


.. jupyter-execute::
    :hide-code:

    elmlist = [CoaxConnect]
    drawElements(elmlist, dx=1, dy=1, lblofst=[.5, 0])



Transformers
------------

The :py:class:`schemdraw.elements.xform.Transformer` element is used to create various transformers.
Anchors `p1`, `p2`, `s1`, and `s2` are defined for all transformers.
Other anchors can be created using the `taps` method to add tap locations to
either side.


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12)
    d.add(elm.Transformer().label('Transformer'))
    d.add(elm.Transformer(loop=True).at([5, 0]).label('Transformer(loop=True)'))
    d.here = [0, -4]
    d.draw()


Here is a transformers with anchor "B" added using the `tap` method. Note the tap by itself
does not draw anything, but defines a named anchor to connect to.

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
        x = d.add(elm.Transformer(t1=4, t2=8)
                  .tap(name='B', pos=3, side='secondary'))
        d += elm.Line().at(x.s1).length(d.unit/4).label('s1', 'rgt').color('blue')
        d += elm.Line().at(x.s2).length(d.unit/4).label('s2', 'rgt').color('blue')
        d += elm.Line().at(x.p1).length(d.unit/4).left().label('p1', 'lft').color('blue')
        d += elm.Line().at(x.p2).length(d.unit/4).left().label('p2', 'lft').color('blue')
        d += elm.Line().at(x.B).length(d.unit/4).right().label('B', 'rgt').color('blue')
