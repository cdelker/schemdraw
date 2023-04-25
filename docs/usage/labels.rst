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
    :hide-code:
    
    d = schemdraw.Drawing()

.. jupyter-execute::

    d += elm.Resistor().label('1MΩ')
    d += elm.Capacitor().label('1μF')
    d += elm.Capacitor().label(r'$v = \frac{1}{C} \int i dt$')
    d += elm.Resistor().at((0, -2)).label('$R_0$')
    d += elm.Capacitor().label('$x^2$')

.. jupyter-execute::
    :hide-code:

    d.draw()

Location
********

The label location is specified with the `loc` parameter to the `label` method.
It can be `left`, `right`, `top`, `bottom`, or the name of a defined anchor within the element.
These directions do not depend on rotation. A label with `loc='left'` is always on the leftmost terminal of the element.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += (elm.Resistor()
            .label('Label')  # 'top' is default
            .label('Bottom', loc='bottom')
            .label('Right', loc='right')
            .label('Left', loc='left'))

.. jupyter-execute::
    :hide-code:

    d.draw()

Labels may also be placed near an element anchor by giving the anchor name as the `loc` parameter.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += (elm.BjtNpn()
            .label('b', loc='base')
            .label('c', loc='collector')
            .label('e', loc='emitter'))

.. jupyter-execute::
    :hide-code:

    d.draw()

The :py:meth:`schemdraw.elements.Element.label` method also takes parameters that control the label's rotation, offset, font, alignment, and color.
Label text stays horizontal by default, but may be rotated to the same angle as the element using `rotate=True`, or any angle `X` in degrees with `rotate=X`.
Offsets apply vertically if a float value is given, or in both x and y if a tuple is given.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Resistor().label('no offset')
    d += elm.Resistor().label('offset', ofst=1)
    d += elm.Resistor().label('offset (x, y)', ofst=(-.6, .2))
    d += elm.Resistor().theta(-45).label('no rotate')
    d += elm.Resistor().theta(-45).label('rotate', rotate=True)
    d += elm.Resistor().theta(45).label('90°', rotate=90)

.. jupyter-execute::
    :hide-code:

    d.draw()


Labels may also be added anywhere using the :py:class:`schemdraw.elements.lines.Label` element. The element itself draws nothing, but labels can be added to it:

.. code-block:: python

    elm.Label().label('Hello')


Voltage Labels
**************

A label may also be a list/tuple of strings, which will be evenly-spaced along the length of the element.
This allows for labeling positive and negative along with a component name, for example:

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Resistor().label(('–','$V_1$','+'))  # Note: using endash U+2013 character

.. jupyter-execute::
    :hide-code:

    d.draw()
    
Use the `Gap` element to label voltage across a terminal:

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Line().dot(open=True)
    d += elm.Gap().label(('–','$V_o$','+'))
    d += elm.Line().idot(open=True)

.. jupyter-execute::
    :hide-code:

    d.draw()


Current Arrow Labels
********************

Current Arrow
^^^^^^^^^^^^^

To label the current through an element, the :py:class:`schemdraw.elements.lines.CurrentLabel` element can be added.
The `at` method of this element can take an Element instance to label, and the
arrow will be placed over the center of that Element.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::

    d += (R1 := elm.Resistor())
    d += elm.CurrentLabel().at(R1).label('10 mA')

.. jupyter-execute::
    :hide-code:

    d.draw()


Inline Current Arrow
^^^^^^^^^^^^^^^^^^^^

Alternatively, current labels can be drawn inline as arrowheads on the leads of 2-terminal elements using :py:class:`schemdraw.elements.lines.CurrentLabelInline`. Parameters `direction` and `start` control whether the arrow
is shown pointing into or out of the element, and which end to place the arrowhead on.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += (R1 := elm.Resistor())
    d += elm.CurrentLabelInline(direction='in').at(R1).label('10 mA')

.. jupyter-execute::
    :hide-code:

    d.draw()


Loop Current
^^^^^^^^^^^^

Loop currents can be added using :py:class:`schemdraw.elements.lines.LoopCurrent`, given a list of 4 existing elements surrounding the loop.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += (R1 := elm.Resistor())
    d += (C1 := elm.Capacitor().down())
    d += (D1 := elm.Diode().fill(True).left())
    d += (L1 := elm.Inductor().up())
    d += elm.LoopCurrent([R1, C1, D1, L1], direction='cw').label('$I_1$')

.. jupyter-execute::
    :hide-code:

    d.draw()

Alternatively, loop current arrows can be added anywhere with any size using :py:class:`schemdraw.elements.lines.LoopArrow`.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()
    
.. jupyter-execute::
    :hide-output:
    
    d += (a:=elm.Line().dot())
    d += elm.LoopArrow(width=.75, height=.75).at(a.end)

.. jupyter-execute::
    :hide-code:

    d.draw()


Impedance Arrow Label
^^^^^^^^^^^^^^^^^^^^^

A right-angle arrow label, often used to indicate impedance looking into a node, is added using :py:class:`schemdraw.elements.lines.ZLabel`.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += (R:=elm.RBox().right())
    d += elm.ZLabel().at(R).label('$Z_{in}$')

.. jupyter-execute::
    :hide-code:

    d.draw()



Annotations
***********

To make text and arrow annotations to a schematic, the :py:class:`schemdraw.elements.lines.Annotate` element draws a curvy arrow with label placed at it's end. It is based on the :py:class:`schemdraw.elements.lines.Arc3` element.

The :py:class:`schemdraw.elements.lines.Encircle` and :py:class:`schemdraw.elements.lines.EncircleBox` elements draw an ellipse, or rounded rectangle, surrounding a list of elements.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing(unit=2)
    d += (R1 := elm.Resistor().down().label('R1'))
    d += (c := elm.Line().right().length(1))
    d += (R2 := elm.Resistor().up().label('R2', loc='bottom'))
    d += elm.Line().left().length(1)
    d += elm.Line().down().at(c.center).length(.75).idot()
    d += (R3 := elm.Resistor().down().label('R3'))
    d += (R4 := elm.Resistor().down().label('R4'))

.. jupyter-execute::

    d += (parallel := elm.Encircle([R1, R2], padx=.8).linestyle('--').linewidth(1).color('red'))
    d += (series := elm.Encircle([R3, R4], padx=.8).linestyle('--').linewidth(1).color('blue'))

    d += elm.Annotate().at(parallel.NNE).delta(dx=1, dy=1).label('Parallel').color('red')
    d += elm.Annotate(th1=0).at(series.ENE).delta(dx=1.5, dy=1).label('Series').color('blue')

.. jupyter-execute::
    :hide-code:

    d.draw()