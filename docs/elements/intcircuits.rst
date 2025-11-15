
.. jupyter-execute::
    :hide-code:

    import schemdraw
    from schemdraw import elements as elm
    schemdraw.use('svg')


.. _integratedcircuit:

Integrated Circuits
-------------------

The :py:class:`schemdraw.elements.intcircuits.Ic` class is used to make integrated circuits, multiplexers, and other black box elements. The :py:class:`schemdraw.elements.intcircuits.IcPin` class is used to define each input/output pin before adding it to the Ic.

All pins will be given an anchor name of `inXY` where X is the side (L, R, T, B), and Y is the pin number along that side.
Pins also define anchors based on the `name` parameter.
If the `anchorname` parameter is provided for the pin, this name will be used, so that the pin `name` can be any string even if it cannot be used as a Python variable name.

Here, a J-K flip flop, as part of an HC7476 integrated circuit, is drawn with input names and pin numbers.

.. jupyter-execute::

    JK = elm.Ic(pins=[elm.IcPin(name='>', pin='1', side='left'),
                      elm.IcPin(name='K', pin='16', side='left'),
                      elm.IcPin(name='J', pin='4', side='left'),
                      elm.IcPin(name=r'$\overline{Q}$', pin='14', side='right', anchorname='QBAR'),
                      elm.IcPin(name='Q', pin='15', side='right')],
                edgepadW = .5,  # Make it a bit wider
                pinspacing=1).label('HC7476', 'bottom', fontsize=12)
    display(JK)


Notice the use of `$\overline{Q}$` to acheive the label on the inverting output.
The anchor positions can be accessed using attributes, such as `JK.Q` for the
non-inverting output. However, inverting output is named `$\overline{Q}`, which is
not accessible using the typical dot notation. It could be accessed using 
`getattr(JK, r'$\overline{Q}$')`, but to avoid this an alternative anchorname of `QBAR`
was defined.


Multiplexers
^^^^^^^^^^^^

Multiplexers and demultiplexers are drawn with the :py:class:`schemdraw.elements.intcircuits.Multiplexer` class which wraps the Ic class.


.. jupyter-execute::

    elm.Multiplexer(
        pins=[elm.IcPin(name='C', side='L'),
              elm.IcPin(name='B', side='L'),
              elm.IcPin(name='A', side='L'),
              elm.IcPin(name='Q', side='R'),
              elm.IcPin(name='T', side='B', invert=True)],
        edgepadH=-.5)
        
See the :ref:`gallery` for more examples.


Seven-Segment Display
^^^^^^^^^^^^^^^^^^^^^

A seven-segment display, in :py:class:`schemdraw.elements.intcircuits.SevenSegment`, provides a single digit
with several options including decimal point and common anode or common cathode mode. The :py:meth:`schemdraw.elements.intcircuits.sevensegdigit` method generates a list of Segment objects that can be used to add
a digit to another element, for example to make a multi-digit display.

.. jupyter-execute::
    :hide-code:

    elm.SevenSegment()


DIP Integrated Circuits
^^^^^^^^^^^^^^^^^^^^^^^

Integrated circuits can be drawn in dual-inline package style with :py:class:`schemdraw.elements.intcircuits.IcDIP`.
Anchors allow connecting elements externally to show the IC in a circuit, or interanally to show the internal
configuration of the IC (see :ref:`dip741`.)

.. jupyter-execute::
    :hide-code:
    
    elm.IcDIP()


Predefined ICs
^^^^^^^^^^^^^^

A few common integrated circuits are predefined as shown below.

.. grid:: 2

    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        VoltageRegulator

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing():
                j = elm.VoltageRegulator()


    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        DFlipFlop

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing():
                d = elm.DFlipFlop()
                d.label('D', loc='D', fontsize=10, color='blue')
                d.label('Q', loc='Q', fontsize=10, color='blue')
                d.label('Qbar', loc='Qbar', fontsize=10, color='blue')
                d.label('CLK', loc='CLK', fontsize=10, color='blue')


    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        JKFlipFlop

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing():
                j = elm.JKFlipFlop()
                j.label('J', loc='J', fontsize=10, color='blue')
                j.label('K', loc='K', fontsize=10, color='blue')
                j.label('Q', loc='Q', fontsize=10, color='blue')
                j.label('Qbar', loc='Qbar', fontsize=10, color='blue')
                j.label('CLK', loc='CLK', fontsize=10, color='blue')


    .. grid-item-card::
        :class-body: sd-text-nowrap sd-fs-6

        Ic555

        .. jupyter-execute::
            :hide-code:

            with schemdraw.Drawing():
                d = elm.Ic555()
                d.label('RST', loc='RST', fontsize=10, color='blue')
                d.label('DIS', loc='DIS', fontsize=10, color='blue')
                d.label('Vcc', loc='Vcc', fontsize=10, color='blue')
                d.label('THR', loc='THR', fontsize=10, color='blue')
                d.label('TRG', loc='TRG', fontsize=10, color='blue')
                d.label('CTL', loc='CTL', fontsize=10, color='blue')
                d.label('OUT', loc='OUT', fontsize=10, color='blue')
                d.label('GND', loc='GND', fontsize=10, color='blue')
