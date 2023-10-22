.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


.. _labels:

Labels
------

Labels are added to elements using the :py:meth:`schemdraw.elements.Element.label` method.
Some unicode utf-8 characters are allowed, such as :code:`'1μF'` and :code:`'1MΩ'` if the character is included in your font set.
Alternatively, full LaTeX math expressions can be rendered when enclosed in `$..$`
For a description of supported math expressions, in the Matplotlib backend see `Matplotlib Mathtext <https://matplotlib.org/stable/tutorials/text/mathtext.html>`_, and the SVG backend refer to the `Ziamath <https://ziamath.readthedocs.io>`_ package.
Subscripts and superscripts are also added using LaTeX math mode, enclosed in `$..$`:

.. jupyter-execute::
    
    with schemdraw.Drawing():
        elm.Resistor().label('1MΩ')
        elm.Capacitor().label('1μF')
        elm.Capacitor().label(r'$v = \frac{1}{C} \int i dt$')
        elm.Resistor().at((0, -2)).label('$R_0$')
        elm.Capacitor().label('$x^2$')

Location
********

The label location is specified with the `loc` parameter to the `label` method.
It can be `left`, `right`, `top`, `bottom`, or the name of a defined anchor within the element.
These directions do not depend on rotation. A label with `loc='left'` is always on the leftmost terminal of the element.

.. jupyter-execute::

    with schemdraw.Drawing():
        (elm.Resistor()
            .label('Label')  # 'top' is default
            .label('Bottom', loc='bottom')
            .label('Right', loc='right')
            .label('Left', loc='left'))

Labels may also be placed near an element anchor by giving the anchor name as the `loc` parameter.

.. jupyter-execute::

    with schemdraw.Drawing():
        (elm.BjtNpn()
            .label('b', loc='base')
            .label('c', loc='collector')
            .label('e', loc='emitter'))

The :py:meth:`schemdraw.elements.Element.label` method also takes parameters that control the label's rotation, offset, font, alignment, and color.
Label text stays horizontal by default, but may be rotated to the same angle as the element using `rotate=True`, or any angle `X` in degrees with `rotate=X`.
Offsets apply vertically if a float value is given, or in both x and y if a tuple is given.

.. jupyter-execute::

    with schemdraw.Drawing():
        elm.Resistor().label('no offset')
        elm.Resistor().label('offset', ofst=1)
        elm.Resistor().label('offset (x, y)', ofst=(-.6, .2))
        elm.Resistor().theta(-45).label('no rotate')
        elm.Resistor().theta(-45).label('rotate', rotate=True)
        elm.Resistor().theta(45).label('90°', rotate=90)


Labels may also be added anywhere using the :py:class:`schemdraw.elements.lines.Label` element. The element itself draws nothing, but labels can be added to it:

.. code-block:: python

    elm.Label().label('Hello')


Voltage Labels
**************

A label may also be a list/tuple of strings, which will be evenly-spaced along the length of the element.
This allows for labeling positive and negative along with a component name, for example:

.. jupyter-execute::

    elm.Resistor().label(('–','$V_1$','+'))  # Note: using endash U+2013 character

    
Use the `Gap` element to label voltage across a terminal:

.. jupyter-execute::

    with schemdraw.Drawing():
        elm.Line().dot(open=True)
        elm.Gap().label(('–','$V_o$','+'))
        elm.Line().idot(open=True)


Current Arrow Labels
********************

Current Arrow
^^^^^^^^^^^^^

To label the current through an element, the :py:class:`schemdraw.elements.lines.CurrentLabel` element can be added.
The `at` method of this element can take an Element instance to label, and the
arrow will be placed over the center of that Element.

.. jupyter-execute::

    with schemdraw.Drawing():
        R1 = elm.Resistor()
        elm.CurrentLabel().at(R1).label('10 mA')

For transistors, the label will follow sensible bias currents by default.

.. jupyter-execute::

    with schemdraw.Drawing():
        Q1 = elm.AnalogNFet()
        elm.CurrentLabel().at(Q1).label('10 µA')

        Q2 = elm.AnalogNFet().at([4,0]).flip().reverse()
        elm.CurrentLabel().at(Q2).label('10 µA')


Inline Current Arrow
^^^^^^^^^^^^^^^^^^^^

Alternatively, current labels can be drawn inline as arrowheads on the leads of 2-terminal elements using :py:class:`schemdraw.elements.lines.CurrentLabelInline`. Parameters `direction` and `start` control whether the arrow
is shown pointing into or out of the element, and which end to place the arrowhead on.

.. jupyter-execute::

    with schemdraw.Drawing():
        R1 = elm.Resistor()
        elm.CurrentLabelInline(direction='in').at(R1).label('10 mA')


Loop Current
^^^^^^^^^^^^

Loop currents can be added using :py:class:`schemdraw.elements.lines.LoopCurrent`, given a list of 4 existing elements surrounding the loop.

.. jupyter-execute::

    with schemdraw.Drawing():
        R1 = elm.Resistor()
        C1 = elm.Capacitor().down()
        D1 = elm.Diode().fill(True).left()
        L1 = elm.Inductor().up()
        elm.LoopCurrent([R1, C1, D1, L1], direction='cw').label('$I_1$')

Alternatively, loop current arrows can be added anywhere with any size using :py:class:`schemdraw.elements.lines.LoopArrow`.

.. jupyter-execute::
    
    with schemdraw.Drawing():
        a = elm.Line().dot()
        elm.LoopArrow(width=.75, height=.75).at(a.end)


Impedance Arrow Label
^^^^^^^^^^^^^^^^^^^^^

A right-angle arrow label, often used to indicate impedance looking into a node, is added using :py:class:`schemdraw.elements.lines.ZLabel`.

.. jupyter-execute::

    with schemdraw.Drawing():
        R = elm.RBox().right()
        elm.ZLabel().at(R).label('$Z_{in}$')


Annotations
***********

To make text and arrow annotations to a schematic, the :py:class:`schemdraw.elements.lines.Annotate` element draws a curvy arrow with label placed at it's end. It is based on the :py:class:`schemdraw.elements.lines.Arc3` element.

The :py:class:`schemdraw.elements.lines.Encircle` and :py:class:`schemdraw.elements.lines.EncircleBox` elements draw an ellipse, or rounded rectangle, surrounding a list of elements.

.. jupyter-input::

    parallel = elm.Encircle([R1, R2], padx=.8).linestyle('--').linewidth(1).color('red')
    series = elm.Encircle([R3, R4], padx=.8).linestyle('--').linewidth(1).color('blue')

    elm.Annotate().at(parallel.NNE).delta(dx=1, dy=1).label('Parallel').color('red')
    elm.Annotate(th1=0).at(series.ENE).delta(dx=1.5, dy=1).label('Series').color('blue')


.. jupyter-execute::
    :hide-code:

    with schemdraw.Drawing(unit=2):
        R1 = elm.Resistor().down().label('R1')
        c = elm.Line().right().length(1)
        R2 = elm.Resistor().up().label('R2', loc='bottom')
        elm.Line().left().length(1)
        elm.Line().down().at(c.center).length(.75).idot()
        R3 = elm.Resistor().down().label('R3')
        R4 = elm.Resistor().down().label('R4')
        parallel = elm.Encircle([R1, R2], padx=.8).linestyle('--').linewidth(1).color('red')
        series = elm.Encircle([R3, R4], padx=.8).linestyle('--').linewidth(1).color('blue')

        elm.Annotate().at(parallel.NNE).delta(dx=1, dy=1).label('Parallel').color('red')
        elm.Annotate(th1=0).at(series.ENE).delta(dx=1.5, dy=1).label('Series').color('blue')

