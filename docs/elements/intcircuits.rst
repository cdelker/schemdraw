
.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


.. _integratedcircuit:

Integrated Circuits
===================

The :py:class:`schemdraw.elements.intcircuits.Ic` class is used to make integrated circuits, multiplexers, and other black box elements. The :py:class:`schemdraw.elements.intcircuits.IcPin` class is used to define each input/output pin before adding it to the Ic.

.. class:: schemdraw.elements.intcircuits.IcPin(**kwargs)

    Define a single input/output pin for an integrated circuit
    or black box.
    
    :param name: Input/output name, drawn inside the box. A name of '>' will be drawn as a proper clock input triangle.
    :type name: string
    :param pinname: Pin name (usually a pin number), drawn outside the box
    :type pinname: string
    :param side: Side of box for the pin, 'left', 'right', 'top', 'bottom' (or their first letter abbreviations)
    :type side: string
    :param pos: Pin position as fraction from 0-1 along the side
    :type pos: float
    :param slot: Slot definition of pin location, given in 'X/Y' format. '2/4' is the second pin on a side with 4 pins.
    :type slot: string
    :param invert: Add in invert bubble to the pin
    :type invert: bool
    :param color: Color for the pin and label
    :type color: string or RGB tuple
    :param rotation: Rotation angle (degrees) for label text
    :type rotation: float
    :param anchorname: Named anchor for this pin
    :type anchorname: string
    

.. class:: schemdraw.elements.intcircuits.Ic(**kwargs)

    An integrated circuit or black box element
    
    :param pins: List if IcPin instances defining all the input/outputs
    :type pins: list
    :param pinspacing: Spacing between pins
    :type pinspacing: float
    :param edgepadH: Padding between top/bottom and first pin
    :type edgepadH: float
    :param edgepadW: Padding between left/right and first pin
    :type edgepadW: float
    :param lofst: Offset between edge and label inside the box
    :type lofst: float
    :param lblsize: Font size for labels inside the box
    :type lblsize: float
    :param plblofst: Offset between edge and pin label outside the box
    :type plblofst: float
    :param plblsize: Font size for pin labels outside the box
    :type plblsize: float
    :param slant: Slant angle of top/bottom edges (e.g. for multiplexers)
    :type slant: float

All pins will be given an anchor name of `inXY` where X is the side (L, R, T, B), and Y is the pin number along that side.
Pins also define anchors based on the `name` parameter.
If the `anchorname` parameter is provided for the pin, this name will be used, so that the pin `name` can be any string even if it cannot be used as a Python variable name.

Here, a J-K flip flop, as part of an HC7476 integrated circuit, is drawn with input names and pin numbers.

.. jupyter-execute::

    JK = elm.Ic(pins=[elm.IcPin(name='>', pin='1', side='left'),
                     elm.IcPin(name='K', pin='16', side='left'),
                     elm.IcPin(name='J', pin='4', side='left'),
                     elm.IcPin(name='$\overline{Q}$', pin='14', side='right', anchorname='QBAR'),
                     elm.IcPin(name='Q', pin='15', side='right')],
                edgepadW = .5,  # Make it a bit wider
                botlabel='HC7476',
                lblsize=12,
                pinspacing=1)
    display(JK)


Notice the use of `$\overline{Q}$` to acheive the label on the inverting output.
The anchor positions can be accessed using attributes, such as `JK.Q` for the
non-inverting output. However, inverting output is named `$\overline{Q}`, which is
not accessible using the typical dot notation. It could be accessed using 
`getattr(JK, '$\overline{Q}$')`, but to avoid this an alternative anchorname of `QBAR`
was defined.


Multiplexers
^^^^^^^^^^^^

Multiplexers and demultiplexers are drawn with the :py:class:`schemdraw.elements.intcircuits.Multiplexer` class which wraps the Ic class.


.. class:: schemdraw.elements.intcircuits.Multiplexer(**kwargs)

    Multiplexer or Demultiplexer element
    
    :param slant: Slant angle (degrees) of top and bottom edges
    :type slant: float
    :param demux: Draw as demultiplexer
    :type bool:
    :param kwargs: Passed to Ic class


.. jupyter-execute::

    elm.Multiplexer(
        pins=[elm.IcPin(name='C', side='L'),
              elm.IcPin(name='B', side='L'),
              elm.IcPin(name='A', side='L'),
              elm.IcPin(name='Q', side='R'),
              elm.IcPin(name='T', side='B', invert=True)],
        edgepadH=-.5)
        
See the :ref:`gallery` for more examples.