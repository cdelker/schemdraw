.. _electrical:

Basic Circuit Elements
======================

These elements are defined in the `schemdraw.elements` module.

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    from functools import partial
    import schemdraw
    from schemdraw import elements as elm
    from schemdraw.elements import *
    
    def drawElements(elmlist, cols=3, dx=8, dy=2, lblofst=None):
        d = schemdraw.Drawing(fontsize=12)
        for i, e in enumerate(elmlist):
            y = i//cols*-dy
            x = (i%cols) * dx

            name = type(e()).__name__
            if hasattr(e, 'keywords'):  # partials have keywords attribute
                args = ', '.join(['{}={}'.format(k, v) for k, v in e.keywords.items()])
                name = '{}({})'.format(name, args)
            eplaced = d.add(e, d='right', xy=[x, y])
            eplaced.add_label(name, loc='rgt', align=('left', 'center'), ofst=lblofst)
            anchors = eplaced.absanchors.copy()
            anchors.pop('start', None)
            anchors.pop('end', None)
            anchors.pop('center', None)
            anchors.pop('xy', None)

            if len(anchors) > 0:
                for aname, apos in anchors.items():
                    eplaced.add_label(aname, loc=aname, color='blue', fontsize=10)
        return d


2-terminal Elements
-------------------

Two-terminal devices subclass :py:class:`schemdraw.elements.Element2Term`, and have leads that will be extended to make the element the desired length depending on the arguments.
All two-terminal elements define `start`, `end`, and `center` anchors for placing, and a few define other anchors as shown in blue in the table below.
Some elements have optional parameters, shown in parenthesis in the table below.


.. jupyter-execute::
    :hide-code:

    elmlist = [Resistor, RBox, ResistorVar, RBoxVar, Potentiometer, PotBox, Photoresistor,
               PhotoresistorBox, Thermistor,
               Capacitor, partial(Capacitor, polar=True),
               Capacitor2, partial(Capacitor2, polar=True),
               CapacitorVar, Inductor, Inductor2, partial(Inductor2, loops=2), Diode,
               partial(Diode, fill=True), Schottky, DiodeTunnel, DiodeShockley,
               Zener, LED, LED2, Photodiode, Diac, Triac, SCR, Fuse,
               Crystal, Memristor, Memristor2, Josephson,
               Source, SourceV, SourceI, SourceSin, SourcePulse, SourceSquare, SourceTriangle,
               SourceRamp, SourceControlled,
               SourceControlledV, SourceControlledI, BatteryCell,
               Battery, MeterV, MeterA, MeterI, MeterOhm, Lamp, Motor,
               Solar, Neon,
               Button, partial(Button, nc=True),
               Switch, partial(Switch, action='open'), partial(Switch, action='close'),
               Line, Arrow, partial(Arrow, double=True), LineDot, partial(LineDot, double=True)]
    drawElements(elmlist, cols=2)


Single-Terminal Elements
------------------------

Single terminal elements are drawn about a single point, and do not move the current drawing position.

.. jupyter-execute::
    :hide-code:
    
    # One-terminal, don't move position
    elmlist = [Ground, GroundSignal, GroundChassis,
               Dot, partial(Dot, open=True), DotDotDot,
               Vss, Vdd, Arrowhead]
    drawElements(elmlist, dx=4)


.. jupyter-execute::
    :hide-code:
    
    elmlist = [Antenna, AntennaLoop, AntennaLoop2]
    drawElements(elmlist, dx=4)

Switches
--------

The standard toggle switch is listed with other two-terminal elements above.
Single-pole, double-throw switches are shown here, with anchors `a`, `b`, and `c`,
and the `action` parameter to add an open or closing arrow.

.. jupyter-execute::
    :hide-code:

    elmlist = [SwitchSpdt, partial(SwitchSpdt, action='open'), partial(SwitchSpdt, action='close'),
               SwitchSpdt2, partial(SwitchSpdt2, action='open'), partial(SwitchSpdt2, action='close'),
               SwitchDpst, SwitchDpdt]
    drawElements(elmlist, cols=2, dx=8, dy=3)


Audio Elements
--------------

Speakers and Microphones

.. jupyter-execute::
    :hide-code:
    
    elmlist = [Speaker, Mic]
    drawElements(elmlist, cols=2, dy=5, dx=5, lblofst=[.5, 0])
    
    
.. jupyter-execute::
    :hide-code:
    
    elmlist = [AudioJack, partial(AudioJack, ring=True),
               partial(AudioJack, switch=True),
               partial(AudioJack, switch=True, ring=True, ringswitch=True)]
    drawElements(elmlist, cols=1, dy=5, lblofst=[1.5, 0])

    
Labels
------

The `Label` element can be used to add a label anywhere.
The `Gap` is like an "invisible" element, useful for marking the voltage between output terminals.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=12)
    d.add(elm.Line, d='right', l=1)
    d.add(elm.Dot, open=True)
    d.add(elm.Gap, d='down', label=['+','Gap','–'])
    d.add(elm.Dot, open=True)
    d.add(elm.Line, d='left', l=1)
    d.add(elm.Label, xy=[3.5,-.5], label='Label')
    d.add(elm.Tag('r', at=[3, -2], label='Tag'))
    d.draw()
    
    
    
Operational Amplifiers
----------------------

The Opamp element defines several anchors for various inputs, including voltage supplies and offset nulls.


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
    d


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
    drawElements(elmlist, dx=6.5, dy=3)


Field-Effect Transistors
^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :hide-code:

    elmlist = [NFet, partial(NFet, bulk=True), partial(PFet, bulk=True),
               JFet, JFetN, JFetP, partial(JFetN, circle=True), partial(JFetP, circle=True)]
    drawElements(elmlist, dx=6.5, dy=3, lblofst=[0, -.8])



Cables
------

Coaxial and Triaxial cables are 2-Terminal elements that can be made with several options and anchors.
Coax parameters include length, radius, and leadlen for setting the distance between leads and the shell.
Triax parameters include length, radiusinner, radiusouter, leadlen, and shieldofststart for offseting the outer shield from the inner guard.


.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(fontsize=10)
    d.add(elm.Coax(label='Coax'))
    d.add(elm.Coax(length=4, radius=.5, label='Coax(length=5, radius=.5)'))
    C = d.add(elm.Coax(at=[0, -3], length=5))
    d.add(elm.Line('down', xy=C.shieldstart, l=.2, lftlabel='shieldstart', color='blue'))
    d.add(elm.Line('down', xy=C.shieldcenter, l=.6, lftlabel='shieldcenter', color='blue'))
    d.add(elm.Line('down', xy=C.shieldend, l=1, lftlabel='shieldend', color='blue'))
    d.add(elm.Line('up', xy=C.shieldstart_top, l=.2, rgtlabel='shieldstart_top', color='blue'))
    d.add(elm.Line('up', xy=C.shieldcenter_top, l=.6, rgtlabel='shieldcenter_top', color='blue'))
    d.add(elm.Line('up', xy=C.shieldend_top, l=1, rgtlabel='shieldend_top', color='blue'))

    d.add(elm.Triax(at=[0, -7], d='right', label='Triax'))
    d.add(elm.Triax(length=4, radiusinner=.5, label='Triax(length=5, radiusinner=.5)'))
    C = d.add(elm.Triax(at=[1, -10], length=5))
    d.add(elm.Line('down', xy=C.shieldstart, l=.2, lftlabel='shieldstart', color='blue'))
    d.add(elm.Line('down', xy=C.shieldcenter, l=.6, lftlabel='shieldcenter', color='blue'))
    d.add(elm.Line('down', xy=C.shieldend, l=1, lftlabel='shieldend', color='blue'))
    d.add(elm.Line('up', xy=C.shieldstart_top, l=.2, rgtlabel='shieldstart_top', color='blue'))
    d.add(elm.Line('up', xy=C.shieldcenter_top, l=.6, rgtlabel='shieldcenter_top', color='blue'))
    d.add(elm.Line('up', xy=C.shieldend_top, l=1, rgtlabel='shieldend_top', color='blue'))
    d.add(elm.Line(theta=45, xy=C.guardend_top, l=1, rgtlabel='guardend_top', color='blue'))
    d.add(elm.Line(theta=-45, xy=C.guardend, l=1, rgtlabel='guardend', color='blue'))
    d.add(elm.Line(theta=135, xy=C.guardstart_top, l=.3, lftlabel='guardstart_top', color='blue'))
    d.add(elm.Line(theta=-145, xy=C.guardstart, l=.5, lftlabel='guardstart', color='blue'))
    d


.. jupyter-execute::
    :hide-code:

    elmlist = [CoaxConnect]
    drawElements(elmlist, dx=1, dy=1, lblofst=[.5, 0])


Transformers
------------

The :py:func:`schemdraw.elements.xform.Transformer` element is used to create various transformers.
Anchors `p1`, `p2`, `s1`, and `s2` are defined for all transformers, with other anchors defined based on the `rtaps` and `ltaps` parameters.


.. class:: schemdraw.elements.xform.Transformer(t1=4, t2=4, core=True, ltaps=None, rtaps=None, loop=False)

   Transformer element

   :param t1: turns on left side
   :type t1: int
   :param t2: turns on right side
   :type t2: int
   :param core: show the transformer core
   :type core: bool
   :param ltaps: anchor definitions for left side. Each key/value pair defines the name/turn number
   :type ltaps: dict
   :param rtaps: anchor definitions for right side.
   :type rtaps: dict
   :param loop: Use spiral/cycloid (loopy) style
   :type loop: bool
   :returns: element definition dictionary
   :rtype: dict


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing(fontsize=12)
    d.add(elm.Transformer(label='Transformer'))
    d.add(elm.Transformer(at=[5, 0], loop=True, label='Transformer(loop=True)'))
    d.here = [0, -4]


Anchors, including a custom tap on the right side:

.. jupyter-execute::

    x = d.add(elm.Transformer(t1=4, t2=8, rtaps={'B':3}))
    d.add(elm.Line, xy=x.s1, l=d.unit/4, rgtlabel='s1', color='blue')
    d.add(elm.Line, xy=x.s2, l=d.unit/4, rgtlabel='s2', color='blue')
    d.add(elm.Line, xy=x.p1, l=d.unit/4, d='left', lftlabel='p1', color='blue')
    d.add(elm.Line, xy=x.p2, l=d.unit/4, d='left', lftlabel='p2', color='blue')
    d.add(elm.Line, xy=x.B, l=d.unit/4, d='right', rgtlabel='B', color='blue')
    display(d)
