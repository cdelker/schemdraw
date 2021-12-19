.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


.. _placement:


Usage
=====

There are two general categories of circuit elements. Two-terminal elements, such as Resistors and Capacitors, are subclasses of :py:class:`schemdraw.elements.Element2Term` and have additional positioning methods that automatically extending the leads of the two terminals to fit a desired length.
The standard :py:class:`schemdraw.elements.Element` class applies to all elements regardless of the number of terminals, but the leads will not extend. These include, for example, Transistors, Opamps, and Grounds.

Placement
---------

The position of each element can be specified in a number of ways.
If no position is given, the next element will start at the current drawing position, typically where the previous element ends, and in the same drawing direction, as seen below where no position or direction parameters are provided.

.. jupyter-execute::

    d = schemdraw.Drawing()
    d += elm.Capacitor()
    d += elm.Resistor()
    d += elm.Diode()
    d.draw()  

Remember that `+=` is equivalent to calling `d.add()`.
If a direction method is added to an element, the element is rotated in that direction, and future elements take the same direction:

.. jupyter-execute::

    d = schemdraw.Drawing()
    d += elm.Capacitor()
    d += elm.Resistor().up()
    d += elm.Diode()
    d.draw()  

The `theta` method can be used to specify any rotation angle in degrees.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Resistor().theta(20).label('R1')
    d += elm.Resistor().label('R2')  # Takes position and direction from R1

.. jupyter-execute::
    :hide-code:

    d.draw()


Using anchors
^^^^^^^^^^^^^

The (x, y) position of an element can also be specified using its `at` method.
Rather than using exact numerical coordinates, the `at` parameter will usually be set to an "anchor" of another element.

An anchor is simply a predefined position within an element.
Two-terminal elements have anchors named `start`, `center`, and `end`.
Three-terminal elements have other named anchors, for example an Opamp has `in1`, `in2`, and `out` anchors.
Each element's docstring lists the available anchors.

Once an element is added to the drawing, all its anchor positions will be added as attributes to the element object.
For example, to draw an opamp and place a resistor on the output, store the Opamp instance to a variable. Then call the `at` method of the new element passing the `out` attribute of the Opamp. The current Drawing position is ignored, and is reset to the endpoint of the resistor.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    opamp = d.add(elm.Opamp())
    d.add(elm.Resistor().right().at(opamp.out))

.. jupyter-execute::
    :hide-code:

    d.draw()

Python's walrus operator provides a convenient shorthand notation for adding an element using `+=` and storing it at the same time.
The above code can be written equivalently as:

.. code-block:: python

    d += (opamp := elm.Opamp())
    d += elm.Resistor().right().at(opamp.out)


Additionally, a new element can be placed with its anchor set to the current Drawing position using the `anchor` method. Here, an Opamp is placed at the end of a resistor, connected to the opamp's `in1` anchor (the inverting input).


.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Resistor().label('R1')
    d += elm.Opamp().anchor('in1')
    
.. jupyter-execute::
    :hide-code:

    d.draw()

Compared to anchoring the opamp at `in2` (the noninverting input):

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Resistor().label('R2')
    d += elm.Opamp().anchor('in2')
    
.. jupyter-execute::
    :hide-code:

    d.draw()



Placing 2-Terminal Elements
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Two-terminal elements hae some other placement options because their length can grow to fit a predetermined space.
The `length` method sets an exact length for an element.

.. jupyter-execute::

    d = schemdraw.Drawing()
    d += elm.Dot()
    d += elm.Resistor()
    d += elm.Dot()
    d += elm.Diode().length(6)
    d += elm.Dot()
    d.draw()

The inner zig-zag portion of a resistor has length of 1 unit, while the default lead extensions are 1 unit on each side,
making the default total resistor length 3 units.
This default size can be changed using the `unit` parameter to the :py:class:`schemdraw.Drawing` class.

The `to` method will set an exact endpoint for a 2-terminal element.
The starting point is still the ending location of the previous element.
Notice the Diode is longer than the standard element length in order to fill the diagonal distance.

.. jupyter-execute::

    d = schemdraw.Drawing()
    R = d.add(elm.Resistor())
    C = d.add(elm.Capacitor().up())
    Q = d.add(elm.Diode().to(R.start))
    d.draw()

The `tox` and `toy` methods are useful for placing 2-terminal elements to "close the loop", without requiring an exact length.
Here, the Line element does not need to specify an exact length to fill the space and connect back with the Source.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    C = d.add(elm.Capacitor())
    d.add(elm.Diode())
    d.add(elm.Line().down())

    # Now we want to close the loop, but can use `tox` 
    # to avoid having to know exactly how far to go.
    # Note we passed the [x, y] position of capacitor C,
    # but only the x value will be used.
    d.add(elm.Line().left().tox(C.start))
    
    d.add(elm.Source().up())

.. jupyter-execute::
    :hide-code:

    d.draw()


Finally, exact endpoints can also be specified using the `endpoints` method.


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R = d.add(elm.Resistor())
    Q = d.add(elm.Diode().down().length(6))
    d.add(elm.Line().left().tox(R.start))
    d.add(elm.Capacitor().up().toy(R.start))
    d.add(elm.SourceV().endpoints(Q.end, R.start))
    
.. jupyter-execute::
    :hide-code:

    d.draw()


Orientation
^^^^^^^^^^^

The `flip` and `reverse` methods are useful for changing orientation of directional elements such as Diodes,
but they do not affect the drawing direction.


.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Zener().label('Normal')
    d += elm.Zener().flip().label('Flip')
    d += elm.Zener().reverse().label('Reverse')

.. jupyter-execute::
    :hide-code:

    d.draw()


Drawing State
^^^^^^^^^^^^^

The :py:class:`schemdraw.Drawing` maintains a drawing state that includes the current x, y position, stored in the `Drawing.here` attribute as a (x, y) tuple, and drawing direction stored in the `Drawing.theta` attribute.
A LIFO stack of drawing states can be used, via the :py:meth:`schemdraw.Drawing.push` and :py:meth:`schemdraw.Drawing.pop` method,
for times when it's useful to save the drawing state and come back to it later.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::

    d += elm.Inductor()
    d += elm.Dot()
    print('d.here:', d.here)
    d.push()  # Save this drawing position/direction for later

    d += elm.Capacitor().down()  # Go off in another direction temporarily
    print('d.here:', d.here)

    d.pop()   # Return to the pushed position/direction
    print('d.here:', d.here)
    d += elm.Diode()
    d.draw()

Changing the drawing position can be accomplished by calling :py:meth:`schemdraw.Drawing.move`.


Labels
------

Labels are added to elements using the :py:meth:`schemdraw.elements.Element.label` method.
Some unicode utf-8 characters are allowed, such as :code:`'1μF'` and :code:`'1MΩ'` if the character is included in your font set.
Alternatively, full LaTeX math expressions can be rendered when enclosed in `$..$`, such as :code:`r'$\tau = \frac{1}{RC}$'`
For a description of supported math expressions, in the Matplotlib backend see `Matplotlib Mathtext <https://matplotlib.org/3.3.0/tutorials/text/mathtext.html/>`_, and the SVG backend refer to the `Ziamath <https://ziamath.readthedocs.io>`_ package.

Subscripts and superscripts are also added using LaTeX math mode, for example:

.. code-block:: python

    .label('$V_0$')  # subscript 0
    .label('$x^2$')  # superscript 2


The label location is specified with the `loc` parameter to the `label` method.
It can be `left`, `right`, `up`, `down`, or the name of a defined anchor within the element.
These directions do not depend on rotation. A label with `loc='left'` is always on the left side of the element.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.Resistor()
          .label('Label')
          .label('Bottom', loc='bottom')
          .label('Right', loc='right')
          .label('Left', loc='left'))

.. jupyter-execute::
    :hide-code:

    d.draw()

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d.add(elm.BjtNpn()
          .label('b', loc='base')
          .label('c', loc='collector')
          .label('e', loc='emitter'))

.. jupyter-execute::
    :hide-code:

    d.draw()


Alternatively, a label may be a list/tuple of strings, which will be evenly-spaced along the length of the element.
This allows for labeling positive and negative along with a component name, for example:

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Resistor().label(('–','$R_1$','+'))  # Note: using endash U+2013 character

.. jupyter-execute::
    :hide-code:

    d.draw()
    
The :py:meth:`schemdraw.elements.Element.label` method also takes parameters that control the label's rotation, offset, and color.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    d += elm.Resistor().label('no offset')
    d += elm.Resistor().label('offset', ofst=1)
    d += elm.Resistor().theta(-45).label('no rotate')
    d += elm.Resistor().theta(-45).label('rotate', rotate=True)
    d += elm.Resistor().theta(45).label('90°', rotate=90)

.. jupyter-execute::
    :hide-code:

    d.draw()


Current Arrow Labels
^^^^^^^^^^^^^^^^^^^^

To label the current through an element, the :py:class:`schemdraw.elements.lines.CurrentLabel` element can be added.
The `at` method of this element can take an Element instance to label, and the
arrow will be placed over the center of that Element.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::

    R1 = d.add(elm.Resistor())
    d.add(elm.CurrentLabel().at(R1).label('10 mA'))
    d.draw()


Alternatively, current labels can be drawn inline as arrowheads on the leads of 2-terminal elements using :py:class:`schemdraw.elements.lines.CurrentLabelInline`. Parameters `direction` and `start` control whether the arrow
is shown pointing into or out of the element, and which end to place the arrowhead on.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R1 = d.add(elm.Resistor())
    d.add(elm.CurrentLabelInline(direction='in').at(R1).label('10 mA'))

.. jupyter-execute::
    :hide-code:

    d.draw()


Loop currents can be added using :py:class:`schemdraw.elements.lines.LoopCurrent`, given
 a list of 4 existing elements surrounding the loop.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:

    R1 = d.add(elm.Resistor())
    C1 = d.add(elm.Capacitor().down())
    D1 = d.add(elm.Diode().fill(True).left())
    L1 = d.add(elm.Inductor().up())
    d.add(elm.LoopCurrent([R1, C1, D1, L1], direction='cw').label('$I_1$'))

.. jupyter-execute::
    :hide-code:

    d.draw()

Alternatively, loop current arrows can be added anywhere with any size using :py:class:`schemdraw.elements.lines.LoopArrow`.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()
    
.. jupyter-execute::
    :hide-output:
    
    d = schemdraw.Drawing()
    d += (a:=elm.LineDot())
    d += elm.LoopArrow(width=.75, height=.75).at(a.end)

.. jupyter-execute::

    d.draw()




Styling
-------

Element styling methods include `color`, `fill`, `linewidth`, and `linestyle`. If a style method is not called when creating an Element, its value is obtained from from the drawing defaults.

.. jupyter-execute::
    :hide-output:
    
    # All elements are blue with lightgray fill unless specified otherwise    
    d = schemdraw.Drawing(color='blue', fill='lightgray')

    d += elm.Diode()
    d += elm.Diode().fill('red')        # Fill overrides drawing color here
    d += elm.Resistor().fill('purple')  # Fill has no effect on non-closed elements
    d += elm.RBox().linestyle('--').color('orange')
    d += elm.Resistor().linewidth(5)

.. jupyter-execute::
    :hide-code:

    d.draw()


U.S. versus European Style
^^^^^^^^^^^^^^^^^^^^^^^^^^

By default, a `Resistor` and related elements (variable resistor, photo resistor, etc.) appear in IEEE/U.S. style. To configure
IEC/European style, use the :py:meth:`schemdraw.elements.style` method with either `elm.STYLE_IEC` or `elm.STYLE_IEEE` parameter.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()

.. jupyter-execute::

    elm.style(elm.STYLE_IEC)
    d += elm.Resistor()
    d.draw()
    

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()

.. jupyter-execute::

    elm.style(elm.STYLE_IEEE)
    d += elm.Resistor()
    d.draw()


Global styles
^^^^^^^^^^^^^

The style method :py:meth:`schemdraw.elements.style` can also be used to configure
global styles on individual elements. Its argument is a dictionary of {name: Element} class pairs.
Combined with `functools.partial <https://docs.python.org/3/library/functools.html#functools.partial>`_ from the standard library, parameters to elements can be set globally.
For example, the following code fills all Diode elements without adding the `fill()` method or `fill` keyword argument to every diode.

.. jupyter-execute::

    from functools import partial

    elm.style({'Diode': partial(elm.Diode, fill=True)})

    d = schemdraw.Drawing()
    d += elm.Diode()
    d += elm.Diode()
    d.draw()


Be careful, though, because the `style` method can overwrite existing elements in the namespace.

    
Walrus Mode
-----------

Python 3.8's new walrus operator (`:=`) allows for adding elements and assigning them to a variable all in one line.
The global position of an element is not calculated until the element is actually added to the drawing, however, so setting an `at`
position based on another element's anchor attribute won't work. However, the `at` parameter also accepts a tuple of (Element, anchorname)
to allow filling in the position when the element is ready to be drawn.

This mode allows creating an entire schematic in a single call to Drawing.

.. jupyter-execute::

    # R1 can't set .at(Q1.base), because base position is not defined until Drawing is created
    # But it can set .at((Q1, 'base')).
    schemdraw.Drawing(
        Q1 := elm.BjtNpn().label('$Q_1$'), 
        elm.Resistor().left().at((Q1, 'base')).label('$R_1$').label('$V_{in}$', 'left'),
        elm.Resistor().up().at((Q1, 'collector')).label('$R_2$').label('$V_{cc}$', 'right'),
        elm.Ground().at((Q1, 'emitter'))
        )


Keyword Arguments
-----------------

All :py:class:`schemdraw.elements.Element` types take keyword arguments that can also be used to set
element properties, partly for historical reasons but also for easy element setup via dictionary unpacking. 
The keyword arguments are equivalent to calling the Element setup methods.
The keyword arguments are not validated or type checked, so the chained method interface
described above is recommended for configuring elements.


+--------------------+-------------------------------+
| Keyword Argument   | Method Equivalent             |
+====================+===============================+
| `d='up'`           | `.up()`                       |
+--------------------+-------------------------------+
| `d='down'`         | `.down()`                     |
+--------------------+-------------------------------+
| `d='left'`         | `.left()`                     |
+--------------------+-------------------------------+
| `d='right'`        | `.right()`                    |
+--------------------+-------------------------------+
| `theta=X`          | `.theta(X)`                   |
+--------------------+-------------------------------+
| `at=X` or `xy=X`   | `.at(X)`                      |
+--------------------+-------------------------------+
| `flip=True`        | `.flip()`                     |
+--------------------+-------------------------------+
| `reverse=True`     | `.reverse()`                  |
+--------------------+-------------------------------+
| `anchor=X`         | `.anchor(X)`                  | 
+--------------------+-------------------------------+
| `zoom=X`           | `.scale(X)`                   |
+--------------------+-------------------------------+
| `color=X`          | `.color(X)`                   |
+--------------------+-------------------------------+
| `fill=X`           | `.fill(X)`                    |
+--------------------+-------------------------------+
| `ls=X`             | `.linestyle(X)`               |
+--------------------+-------------------------------+
| `lw=X`             | `.linewidth(X)`               |
+--------------------+-------------------------------+
| `zorder=X`         | `.zorder(X)`                  |
+--------------------+-------------------------------+
| `move_cur=False`   | `.hold()`                     |
+--------------------+-------------------------------+
| `label=X`          | `.label(X)`                   |
+--------------------+-------------------------------+
| `botlabel=X`       | `.label(X, loc='bottom')`     |
+--------------------+-------------------------------+
| `lftlabel=X`       | `.label(X, loc='left')`       |
+--------------------+-------------------------------+
| `rgtlabel=X`       | `.label(X, loc='right')`      |
+--------------------+-------------------------------+
| `toplabel=X`       | `.label(X, loc='top')`        |
+--------------------+-------------------------------+
| `lblloc=X`         | `.label(..., loc=X)`          |
+--------------------+-------------------------------+

