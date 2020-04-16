.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import SchemDraw
    from SchemDraw import elements as elm

.. _placement:


Adding circuit elements
=======================

All SchemDraw schematics are contained within a :py:class:`SchemDraw.Drawing` object:

.. class:: SchemDraw.Drawing(**kwargs)

    Set up a new circuit drawing
    
    :param kwargs: arguments for customizing the drawing (see `Styling`_).


The first step of any schematic is to create a drawing:

.. code-block:: python

    d = SchemDraw.Drawing()

Circuit elements, such as resistors and capacitors, are added to the Drawing using 
the :py:meth:`SchemDraw.Drawing.add` method, which takes
a dictionary defining the element as a parameter, and other keyword arguments that
define the element's position and other properties.
The element definition will usually be something defined in :py:mod:`SchemDraw.elements`, but can be your onw dictionary defining how to draw the element.
For a description of what goes in to an element definition, see :ref:`customelements`.

.. function:: SchemDraw.Drawing.add(elm_def, **kwargs)

    Add an element to the drawing
    
    :param elm_def: element definition
    :type elm_def: dict
    :param kwargs: keyword arguments to define placement, styling, labels, etc. (see below)
    :returns: an Element instance
    :rtype: SchemDraw.Element

This method returns a :py:class:`SchemDraw.Element` object. Typically, you shouldn't need
to instantiate this object yourself; it is done using the `add` method, which will
automatically place a new `Element` into the `Drawing` and shift it to the desired position.


Placement
---------

The position of each element can be specified in a number of ways.
If no position is given, it will start at the current drawing position, typically where the previous element ends, and in the current drawing direction.
Otherwise, position can be specified using some combination of the keyword arguments to the :py:func:`SchemDraw.Drawing.add` method.

The following :py:func:`SchemDraw.Drawing.add` keyword arguments can be used to define the starting position and ending position of the element:

- **xy** (float array [x, y]): Specifies the starting coordinate of the element. Defaults to the current drawing position (endpoint of the last drawn element.)
- **d** (string) ['up', 'down', 'left', 'right']: Direction to draw the element
- **theta** (float): Angle in degrees to draw the element, overrides `d`.
- **l** (float): Specify the total length of the element in Drawing units
- **anchor** (float array [x, y]): Name of the "pin" in the element to place at `xy` in the Drawing. Typically used for elements with more than two terminals. For example, an OPAMP element has `in1`, `in2`, and `out` anchors.
- **zoom** (float): Zoom factor to enlarge or shrink the element

When no placement parameters are given, the element is placed at the endpoint of the last element added, and in the same direction.

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.RES, theta=20, label='R1')
    d.add(elm.RES, label='R2')  # Takes position and direction from R1

.. jupyter-execute::
    :hide-code:

    d.draw()


Using anchors
^^^^^^^^^^^^^

An anchor is a predefined position within an element.
Two-terminal elements have anchors named `start` and `end`.
Three-terminal elements have other anchors, for example an OPAMP has `in1`, `in2`, and `out` anchors.
There are two ways to use anchors when placing elements.
Using the `anchor` keyword when adding an element will align the element's anchor position with the drawing position.
Here, an opamp is placed at the end of the resistor, connected to its `in1` anchor (the inverting input).

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.RES, label='Resistor')
    d.add(elm.OPAMP, anchor='in1')
    
.. jupyter-execute::
    :hide-code:

    d.draw()

Compared to anchoring the opamp at `in2` (the noninverting input):

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.RES, label='Resistor')
    d.add(elm.OPAMP, anchor='in2')
    
.. jupyter-execute::
    :hide-code:

    d.draw()


Elements can also be placed starting at the anchor point of another existing element.
The :py:class:`SchemDraw.Element` object returned from the `add` function contains attributes defining the x, y coordinates of the element's anchors.
For example, to draw an opamp and place a resistor on the output, store the return from `add`. Then set the `xy` parameter of the new element as the `out` attribute of the existing element:

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    opamp = d.add(elm.OPAMP)
    d.add(elm.RES, xy=opamp.out, d='right')

.. jupyter-execute::
    :hide-code:

    d.draw()


Placing around existing elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Other placement arguments can be used; these override the `d` or `theta` parameters, and are useful to make new elements line up with existing ones.

- **to** (float array [x, y]): Specify the exact end coordinate of the element. Leads will be extended to the required length.
- **tox** (float): Specify only the x-value of the end coordinate. Y-value will remain the same as start (for horizontal elements)
- **toy** (float): Specify only the y-value of the end coordinate. X-value will remain the same as start (for vertical elements)
- **endpts** (float array [[x1, y1], [x2, y2]]): Define both start and end coordinates of the element. Overrides any other positioning arguments.

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    C = d.add(elm.CAP)
    d.add(elm.DIODE)
    d.add(elm.LINE, d='down')

    # Now we want to close the loop, but can use `tox` 
    # to avoid having to know exactly how far to go.
    # Note we passed the [x, y] position of capacitor C,
    # but only the x value will be used.
    d.add(elm.LINE, d='left', tox=C.start)
    
    d.add(elm.SOURCE, d='up')

.. jupyter-execute::
    :hide-code:

    d.draw()

Note that these parameters will have no effect on elements that don't automatically extend leads, such as most three-terminal elements.


Orientation
^^^^^^^^^^^

Two more arguments control the orientation of elements. These do not affect the direction `d` parameter or the
start and end anchors of the element.

- **flip** (bool): Flip the element about its axis, for example to move the LED "light" to the other side.
- **reverse** (bool): Reverse the element direction, for example to swap orientation of a diode.

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.ZENER, label='Normal')
    d.add(elm.ZENER, label='Flip', flip=True)
    d.add(elm.ZENER, label='Reverse', reverse=True)

.. jupyter-execute::
    :hide-code:

    d.draw()


Drawing State
^^^^^^^^^^^^^

The :py:class:`SchemDraw.Drawing` maintains a drawing state that includes the current x, y position and drawing direction.
A LIFO stack of drawing states can be used, via the :py:meth:`SchemDraw.Drawing.push` and :py:meth:`SchemDraw.Drawing.pop` method,
for times when it's useful to save the drawing state and come back to it later.

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.INDUCTOR)
    d.add(elm.DOT)
    d.push()  # Save this drawing position/direction for later
    
    d.add(elm.CAP, d='down')
    d.pop()   # Return to the pushed position/direction
    d.add(elm.DIODE)

.. jupyter-execute::
    :hide-code:

    d.draw()



Labels
------

Labels are added to elements using other keyword arguments to `add`.
Each label is a string, but LaTeX math is rendered when enclosed in $..$.

- **label** (string): add a label in the default location for this element
- **toplabel** (string): add a label above the top of the element
- **botlabel** (string): add a label below the bottom of the element
- **rgtlabel** (string): add a label to the right of the element
- **lftlabel** (string): add a label to the left of the element

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.RES, label='Label', botlabel='Bottom', rgtlabel='Right', lftlabel='Left')

.. jupyter-execute::
    :hide-code:

    d.draw()

Alternatively, a label may be a list of strings, which will be evenly-spaced along the length of the element.
This allows for labeling positive and negative anlong with a component name, for example:

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.RES, label=['$-$','$R_1$','+'])  # Using $-$ to get a proper minus sign rather than a hyphen

.. jupyter-execute::
    :hide-code:

    d.draw()
    
Several other `add` arguments control the behavior of labels:

- **lblofst** (float): offset between the label and element
- **lblsize** (int): font size of label, overriding Drawing.fontsize
- **lblrotate** (bool): Rotate the label text to align with the element, to acheive vertical text for example.
- **lblloc** (string): ['top', 'bottom', 'left', 'right', 'center']. Position for drawing the label specified by 'label' parameter.


.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.RES, label='no offset')
    d.add(elm.RES, label='offset', lblofst=1)
    d.add(elm.RES, theta=-45, label='no rotate')
    d.add(elm.RES, theta=-45, label='rotate', lblrotate=True)

.. jupyter-execute::
    :hide-code:

    d.draw()


For more control over label behavior, use the :py:meth:`SchemDraw.Element.add_label` method.
Labels can be added at arbitrary positions with any alignment.

.. method:: SchemDraw.Element.add_label(label, loc='top', ofst=None, align=None, size=None, rotation=0)

    :param label: label to add
    :type label: string
    :param loc: label position with respect to element: ['top', 'bot', 'lft' 'rgt', 'center'], or name of an anchor defined in this element
    :param ofst: offset between element and label. Can be (x,y) list for 'center' or anchor loc, float otherwise
    :param align: label alignment as tuple of (horizontal, vertical). Horizontal can be ['center', 'left', 'right'], and vertical ['center', 'top', 'bottom']
    :param size: font size for label
    :param rotation: rotation angle, in degrees
    :type rotation: float


Current Labels
^^^^^^^^^^^^^^

To label the current through an element, the ARROWI element is defined.
Typically, it can be added alongside an existing element using the :py:meth:`SchemDraw.Drawing.labelI` method:

.. method:: SchemDraw.Drawing.labelI(elm, label='', arrowofst=0.4, arrowlen=2, reverse=False, top=True)

    Add a current arrow along the element
    
    :param elm: SchemDraw.Element to add arrow to
    :param label: string or list of strings to space along arrow
    :param arrowofst: distance between element and arrow
    :param arrowlen: length of arrow in drawing units
    :param reverse: reverse the arrow, opposite to elm.theta
    :type reverse: bool
    :param top: draw the arrow on top of the element
    :type top: bool

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R1 = d.add(elm.RES)
    d.labelI(R1, '10 mA')

.. jupyter-execute::
    :hide-code:

    d.add(elm.GAP_LABEL, d='up', l=.5)  # To bump the margins...
    d.draw()


Alternatively, current labels can be drawn inline as arrowheads on the leads of 2-terminal elements using :py:meth:`SchemDraw.Drawing.labelI_inline`.

.. method:: SchemDraw.Drawing.labelI_inline(elm, label='', botlabel='', d='in', start=True, ofst=0)

        Draw an inline current arrow on the element.
        
        :param elm: SchemDraw.element to add arrow to
        :param label: string label above the arrowhead
        :type label: string
        :param botlabel: string label below the arrowhead
        :type botlabel: string
        :param d: arrowhead direction, either 'in' or 'out'
        :type d: string
        :param start: place arrowhead near start (or end) of element
        :type start: bool
        :param ofst: additional offset along elemnet leads

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R1 = d.add(elm.RES)
    d.labelI_inline(R1, '$i_1$', d='in')

.. jupyter-execute::
    :hide-code:

    d.draw()


Loop currents can be added using :py:meth:`SchemDraw.Drawing.loopI()`.

.. method:: SchemDraw.Drawing.loopI(elm_list, label='', d='cw', theta1=35, theta2=-35, pad=.2)

    Draw an arc to indicate a loop current bordered by elements in list
    
    :param elm_list: boundary elements in order of top, right, bot, left
    :type elm_list: list
    :param label: text label for center of loop
    :param d: arrow direction ['cw', 'ccw']
    :param theta1: start angle of arrow arc (degrees). Default 35.
    :param theta2: end angle of arrow arc (degrees). Default -35.

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R1 = d.add(elm.RES)
    C1 = d.add(elm.CAP, d='down')
    D1 = d.add(elm.DIODE_F, d='left')
    L1 = d.add(elm.INDUCTOR, d='up')
    d.loopI([R1, C1, D1, L1], d='cw', label='$I_1$')

.. jupyter-execute::
    :hide-code:

    d.draw()



Styling
-------

When creating a new drawing, the keyword arguments to :py:class:`SchemDraw.Drawing` are used to set default styles such as colors and fontsize.

- **unit** (float): default length of a 2-terminal element, including leads. The zigzag portion of resistor element is length 1 unit, and by default the total length is 3 units.
- **inches_per_unit** (float): Inches per unit to scale drawing into real dimensions
- **txtofst** (float): default distance from element to text label
- **fontsize** (int): default font size for all labels
- **font** (string): matplotlib font-family name
- **color** (strong): matplotlib color name to apply to all circuit elements
- **lw** (float): default line width
- **ls** (stirng): default line style (matplotlib style name)

The Drawing color, lw, and ls parameters apply to all elements, unless overriden in argumetns to :py:func:`SchemDraw.Drawing.add`.
When adding an element, it's indivudal options are:

- **color** (string): matplotlib color name for the element
- **ls** (string): line style for the element
- **lw** (float): line width for the elemlent
- **fill** (string): fill color name (only used on closed-path elements)
- **zorder** (int): z-order for specifying which elements are drawn first.

.. jupyter-execute::
    :hide-output:
    
    d = SchemDraw.Drawing(color='blue')  # All elements are blue unless specified otherwise
    d.add(elm.DIODE, fill='red')
    d.add(elm.RES, fill='purple')          # Fill has no effect on this non-closed element
    d.add(elm.RBOX, color='orange', ls='--')
    d.add(elm.RES, lw=5)

.. jupyter-execute::
    :hide-code:

    d.draw()


