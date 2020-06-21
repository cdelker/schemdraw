.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


.. _placement:


Adding circuit elements
=======================

There are two general categories of circuit elements. Two-terminal elements, such as Resistors and Capacitors, are subclasses of :py:class:`schemdraw.elements.Element2Term` and have additional positioning arguments for automatically extending the leads of the two terminals to fit the desired length.
The standard :py:class:`schemdraw.elements.Element` class applies to all elements regardless of the number of terminals, but the leads will not extend. These include, for example, transistors, opamps, and grounds.

Placement
---------

The position of each element can be specified in a number of ways.
If no position is given, the next element will start at the current drawing position, typically where the previous element ends, and in the same drawing direction, as seen below where no position or direction parameters are provided.

.. jupyter-execute::

    d = schemdraw.Drawing()
    d.add(elm.Capacitor())
    d.add(elm.Resistor())
    d.add(elm.Diode())
    d.draw()  

If a direction parameter is provided, the element is rotated in that direction, and future elements take the same direction:

.. jupyter-execute::

    d = schemdraw.Drawing()
    d.add(elm.Capacitor())
    d.add(elm.Resistor('up'))
    d.add(elm.Diode())
    d.draw()  

The `theta` parameter can be used to specify any rotation angle in degrees.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Resistor(theta=20, label='R1'))
    d.add(elm.Resistor(label='R2'))  # Takes position and direction from R1

.. jupyter-execute::
    :hide-code:

    d.draw()


Using anchors
^^^^^^^^^^^^^

The (x, y) position can also be specified using the `at` keyword.
Rather than using exact numerical coordinates, the `at` keyword will usually be set to an "anchor" of another element.

An anchor is simply a predefined position within an element.
Two-terminal elements have anchors named `start`, `center`, and `end`.
Three-terminal elements have other named anchors, for example an Opamp has `in1`, `in2`, and `out` anchors.

Once an element is added to the drawing, it contains attributes defining the coordinates of all the element's anchors.
For example, to draw an opamp and place a resistor on the output, store the return from `add` to a variable. Then set the `at` parameter of the new element as the `out` attribute of the existing element. The current Drawing position is ignored, and reset to the endpoint of the resistor.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    opamp = d.add(elm.Opamp)
    d.add(elm.Resistor('right', at=opamp.out))

.. jupyter-execute::
    :hide-code:

    d.draw()

Additionally, a new element can be placed with its anchor set to the current Drawing position using the `anchor` keyword. Here, an Opamp is placed at the end of a resistor, connected to its `in1` anchor (the inverting input).

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Resistor(label='R1'))
    d.add(elm.Opamp(anchor='in1'))
    
.. jupyter-execute::
    :hide-code:

    d.draw()

Compared to anchoring the opamp at `in2` (the noninverting input):

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Resistor(label='R2'))
    d.add(elm.Opamp(anchor='in2'))
    
.. jupyter-execute::
    :hide-code:

    d.draw()



Placing 2-Terminal Elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Two-terminal elements hae some other placement options because their length can grow to fit a predetermined space.
The `l` parameter sets an exact length for an element.

.. jupyter-execute::

    d = schemdraw.Drawing()
    d.add(elm.Dot())
    d.add(elm.Resistor())
    d.add(elm.Dot())
    d.add(elm.Diode(l=6))
    d.add(elm.Dot())
    d.draw()

The inner zig-zag portion of a resistor has length of 1 unit, while the default lead extensions are 1 unit on each side,
making the default total resistor length 3 units.
This default size can be changed using the `unit` parameter to the :py:class:`schemdraw.Drawing` class.

The `to` parameter will set an exact endpoint for a 2-terminal element.
Notice the Diode is longer than the standard element length in order to fill the diagonal distance.

.. jupyter-execute::

    d = schemdraw.Drawing()
    R = d.add(elm.Resistor())
    C = d.add(elm.Capacitor('up'))
    Q = d.add(elm.Diode(to=R.start))
    d.draw()

The `tox` and `toy` parameters are useful for placing 2-terminal elements to "close the loop", without requiring an exact length.
Here, the Line element does not need to specify an exact length to fill the space and connect back with the Source.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    C = d.add(elm.Capacitor)
    d.add(elm.Diode)
    d.add(elm.Line('down'))

    # Now we want to close the loop, but can use `tox` 
    # to avoid having to know exactly how far to go.
    # Note we passed the [x, y] position of capacitor C,
    # but only the x value will be used.
    d.add(elm.Line('left', tox=C.start))
    
    d.add(elm.Source('up'))

.. jupyter-execute::
    :hide-code:

    d.draw()


Finally, exact endpoints can also be specified using the `endpts` parameter.


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R = d.add(elm.Resistor())
    Q = d.add(elm.Diode('down', l=6))
    d.add(elm.Line('left', tox=R.start))
    d.add(elm.Capacitor('up', toy=R.start))
    d.add(elm.SourceV(endpts=[Q.end, R.start]))
    
.. jupyter-execute::
    :hide-code:

    d.draw()


Orientation
^^^^^^^^^^^

The `flip` and `reverse` keywords are useful for changing direction of directional elements such as Diodes, but they do not affect the 
`d` or `theta` parameters.


.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Zener(label='Normal'))
    d.add(elm.Zener(label='Flip', flip=True))
    d.add(elm.Zener(label='Reverse', reverse=True))

.. jupyter-execute::
    :hide-code:

    d.draw()


Drawing State
^^^^^^^^^^^^^

The :py:class:`schemdraw.Drawing` maintains a drawing state that includes the current x, y position and drawing direction.
A LIFO stack of drawing states can be used, via the :py:meth:`schemdraw.Drawing.push` and :py:meth:`schemdraw.Drawing.pop` method,
for times when it's useful to save the drawing state and come back to it later.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Inductor)
    d.add(elm.Dot)
    d.push()  # Save this drawing position/direction for later
    
    d.add(elm.Capacitor(d='down'))
    d.pop()   # Return to the pushed position/direction
    d.add(elm.Diode)

.. jupyter-execute::
    :hide-code:

    d.draw()



Labels
------

Labels are added to elements using other keyword arguments to the :py:class:`schemdraw.elements.Element` class.
Each label is a string, but LaTeX math is rendered when enclosed in $..$.

- **label**: add a label in the default location for this element
- **toplabel**: add a label above the top of the element
- **botlabel**: add a label below the bottom of the element
- **rgtlabel**: add a label to the right of the element
- **lftlabel**: add a label to the left of the element

These directions do not depend on rotation. A `lftlabel` is always on the left side of the element.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Resistor(label='Label', botlabel='Bottom', rgtlabel='Right', lftlabel='Left'))

.. jupyter-execute::
    :hide-code:

    d.draw()

Alternatively, a label may be a list of strings, which will be evenly-spaced along the length of the element.
This allows for labeling positive and negative anlong with a component name, for example:

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Resistor(label=['–','$R_1$','+']))  # Note: using endash U+2013 character

.. jupyter-execute::
    :hide-code:

    d.draw()
    
See the :py:class:`schemdraw.elements.Element` definition for parameters that control label offest, locaiton, rotation and size.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Resistor(label='no offset'))
    d.add(elm.Resistor(label='offset', lblofst=1))
    d.add(elm.Resistor(theta=-45, label='no rotate'))
    d.add(elm.Resistor(theta=-45, label='rotate', lblrotate=True))

.. jupyter-execute::
    :hide-code:

    d.draw()


For more control over label behavior, use the :py:meth:`schemdraw.elements.Element.add_label` method.
Using this method, labels can be added at arbitrary positions with any alignment.


Current Labels
^^^^^^^^^^^^^^

To label the current through an element, the `CurrentLabel` element is defined.
Typically, it is easier to add this element alongside an existing element using the :py:meth:`schemdraw.Drawing.labelI` method.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R1 = d.add(elm.Resistor)
    d.labelI(R1, '10 mA')

.. jupyter-execute::
    :hide-code:

    d.add(elm.GAP_LABEL, d='up', l=.5)  # To bump the margins...
    d.draw()


Alternatively, current labels can be drawn inline as arrowheads on the leads of 2-terminal elements using :py:meth:`schemdraw.Drawing.labelI_inline`.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R1 = d.add(elm.Resistor)
    d.labelI_inline(R1, '$i_1$', d='in')

.. jupyter-execute::
    :hide-code:

    d.draw()


Loop currents can be added using :py:meth:`schemdraw.Drawing.loopI()`.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R1 = d.add(elm.Resistor)
    C1 = d.add(elm.Capacitor('down'))
    D1 = d.add(elm.Diode('left', fill=True))
    L1 = d.add(elm.Inductor('up'))
    d.loopI([R1, C1, D1, L1], d='cw', label='$I_1$')

.. jupyter-execute::
    :hide-code:

    d.draw()




Styling
-------

Styling parameters include `color`, `fill`, `lw` (linewidth), `ls` (linestyle), `fontsize` and `font`. If a style parameter is not provided when creating an Element, its value is obtained from the element class definition or from the drawing defaults, in that order.

.. jupyter-execute::
    :hide-output:
    
    d = schemdraw.Drawing(color='blue', fill='lightgray')  # All elements are blue with lightgray fill unless specified otherwise
    d.add(elm.Diode())
    d.add(elm.Diode(fill='red'))   # Fill overrides drawing value here
    d.add(elm.Resistor(fill='purple'))  # Fill has no effect on this non-closed element
    d.add(elm.RBox(color='orange', ls='--'))
    d.add(elm.Resistor(lw=5))

.. jupyter-execute::
    :hide-code:

    d.draw()
    
    
Walrus Mode
-----------

Python 3.8's new walrus operator (`:=`) allows for adding elements and referencing them directly to the Drawing initialization.
The global position of an element is not calculated until the element is actually added to the drawing, however, so setting an `at`
position based on another element's anchor attribute won't work. However, the `at` parameter also accepts a tuple of (Element, anchorname)
to allow filling in the position when the element is ready to be drawn.

This mode allows creating an entire schematic in a single call to Drawing.

.. jupyter-execute::

    # R1 can't set at=Q1.base, because base position is not defined until Drawing is created
    schemdraw.Drawing(
        Q1 := elm.BjtNpn(label='$Q_1$'), 
        elm.Resistor('left', at=(Q1, 'base'), label='$R_1$', lftlabel='$V_{in}$'),
        elm.Resistor('up', at=(Q1, 'collector'), label='$R_2$', rgtlabel='$V_{cc}$'),
        elm.Ground(at=(Q1, 'emitter'))
        )
        

Legacy Mode
-----------

Before version 0.7, schemdraw defined elements using dictionaries. In 0.7 elements were upgraded to classes, but a translation lookup still exists so that most old-style schematics are still supported.

.. jupyter-execute::

    d = schemdraw.Drawing()
    d.add(elm.RES, d='right', label='1$\Omega$')
    d.add(elm.CAP, d='down', label='10$\mu$F')
    d.add(elm.LINE, d='left')
    d.add(elm.SOURCE_SIN, d='up', label='10V')
    d.draw()
