.. _electrical:

Basic Circuit Elements
======================

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
            eplaced = d.add(e().right().at([x, y])
                            .label(name, loc=lblloc, halign='left', valign='center', ofst=lblofst))
            anchors = eplaced.absanchors.copy()
            anchors.pop('start', None)
            anchors.pop('end', None)
            anchors.pop('center', None)
            anchors.pop('xy', None)

            if len(anchors) > 0:
                for aname, apos in anchors.items():
                    eplaced.add_label(aname, loc=aname, color='blue', fontsize=10)
        return d


Two-terminal Elements
---------------------

Two-terminal devices subclass :py:class:`schemdraw.elements.Element2Term`, and have leads that will be extended to make the element the desired length depending on the arguments.
All two-terminal elements define `start`, `end`, and `center` anchors for placing, and a few define other anchors as shown in blue in the tables below.
Some elements have optional parameters, shown in parenthesis in the table below.


Styled Elements
^^^^^^^^^^^^^^^

These elements change based on U.S. vs European/IEC style configured by :py:meth:`schemdraw.elements.style`.
Selectable elements, such as `Resistor`, point to either `ResistorUS` or `ResistorIEC`, for example.

U.S Style
*********

U.S. style is the default, or it can be configured using

.. code-block:: python

    elm.style(elm.STYLE_US)


.. jupyter-execute::
    :hide-code:

    elm.style(elm.STYLE_US)
    elmlist = ['Resistor', 'ResistorVar', 'ResistorVar', 'Potentiometer', 'Photoresistor', 'Fuse']
    drawElements(elmlist, cols=2)


European/IEC Style
******************

European style can be enabled using

.. code-block:: python

    elm.style(elm.STYLE_IEC)

.. jupyter-execute::
    :hide-code:

    elm.style(elm.STYLE_IEC)
    elmlist = ['Resistor', 'ResistorVar', 'ResistorVar', 'Potentiometer', 'Photoresistor', 'Fuse']
    drawElements(elmlist, cols=2)


Resistors
^^^^^^^^^

Both U.S. and European styles of resistors are always available using these classes.

.. jupyter-execute::
    :hide-code:

    elmlist = [ResistorUS, ResistorIEC, ResistorVarUS, ResistorVarIEC, PotentiometerUS,
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


Miscmiscellaneous
^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:
    
    elmlist = [Fuse, partial(Fuse, dots=False), Breaker, Crystal, CPE, Josephson, Motor, Lamp, Neon, Thermistor, Memristor, Memristor2]
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
    
    elmlist = [Line, Arrow, partial(Arrow, double=True), LineDot,
               partial(LineDot, double=True)]
    drawElements(elmlist, cols=2)


Single-Terminal Elements
------------------------

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
               Arrowhead]
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

The :py:class:`schemdraw.elements.opamp.Opamp` element defines several anchors for various inputs, including voltage supplies and offset nulls.


.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=12)
    op = d.add(elm.Opamp, label='Opamp', lblofst=.6)
    d.add(elm.LINE, xy=op.in1, d='left', l=.5, lftlabel='in1', color='blue')
    d.add(elm.LINE, xy=op.in2, d='left', l=.5, lftlabel='in2', color='blue')
    d.add(elm.LINE, xy=op.out, d='right', l=.5, rgtlabel='out', color='blue')
    d.add(elm.LINE, xy=op.vd, d='up', l=.25, rgtlabel='vd', color='blue')
    d.add(elm.LINE, xy=op.vs, d='down', l=.25, lftlabel='vs', color='blue')
    d.add(elm.LINE, xy=op.n2, d='up', l=.25, rgtlabel='n2', color='blue')
    d.add(elm.LINE, xy=op.n1, d='down', l=.25, lftlabel='n1', color='blue')
    d.add(elm.LINE, xy=op.n2a, d='up', l=.22, rgtlabel='n2a', lblofst=0, color='blue')
    d.add(elm.LINE, xy=op.n1a, d='down', l=.22, lftlabel='n1a', lblofst=0, color='blue')    

    op2 = d.add(elm.Opamp, sign=False, xy=[5, 0], d='right', label='Opamp(sign=False)', lblofst=.6)
    d.add(elm.LINE, xy=op2.in1, d='left', l=.5, lftlabel='in1', color='blue')
    d.add(elm.LINE, xy=op2.in2, d='left', l=.5, lftlabel='in2', color='blue')
    d.add(elm.LINE, xy=op2.out, d='right', l=.5, rgtlabel='out', color='blue')
    d.add(elm.LINE, xy=op2.vd, d='up', l=.25, rgtlabel='vd', color='blue')
    d.add(elm.LINE, xy=op2.vs, d='down', l=.25, lftlabel='vs', color='blue')
    d.add(elm.LINE, xy=op2.n2, d='up', l=.25, rgtlabel='n2', color='blue')
    d.add(elm.LINE, xy=op2.n1, d='down', l=.25, lftlabel='n1', color='blue')
    d.add(elm.LINE, xy=op2.n2a, d='up', l=.22, rgtlabel='n2a', lblofst=0, color='blue')
    d.add(elm.LINE, xy=op2.n1a, d='down', l=.22, lftlabel='n1a', lblofst=0, color='blue')
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

    elmlist = [NFet, partial(NFet, bulk=True), partial(PFet, bulk=True),
               JFet, JFetN, JFetP, partial(JFetN, circle=True), partial(JFetP, circle=True)]
    drawElements(elmlist, dx=6.5, dy=3, lblofst=[0, -.8])



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


Anchors, including a custom tap on the right side:

.. jupyter-execute::

    x = d.add(elm.Transformer(t1=4, t2=8)#, rtaps={'B':3}))
              .tap(name='B', pos=3, side='secondary'))
    d.add(elm.Line().at(x.s1).length(d.unit/4).label('s1', 'rgt').color('blue'))
    d.add(elm.Line().at(x.s2).length(d.unit/4).label('s2', 'rgt').color('blue'))
    d.add(elm.Line().at(x.p1).length(d.unit/4).left().label('p1', 'lft').color('blue'))
    d.add(elm.Line().at(x.p2).length(d.unit/4).left().label('p2', 'lft').color('blue'))
    d.add(elm.Line().at(x.B).length(d.unit/4).right().label('B', 'rgt').color('blue'))
    d.draw()
