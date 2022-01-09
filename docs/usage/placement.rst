.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


.. _placement:

Placing Elements
================

Elements are added to a Drawing using the `add` method or `+=` shortcut.
The Drawing maintains a current position and direction, such that the default placement of the next element
will start at the end of the previous element, going in the same direction.

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d += elm.Capacitor()
        d += elm.Resistor()
        d += elm.Diode()

If a direction method (`up`, `down`, `left`, `right`) is added to an element, the element is rotated in that direction, and future elements take the same direction:

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d += elm.Capacitor()
        d += elm.Resistor().up()
        d += elm.Diode()

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


Anchors
-------

All elements have a set of predefined "anchor" positions within the element.
For example, a bipolar transistor has `base`, `emitter`, and `collector` anchors.
All two-terminal elements have anchors named `start`, `center`, and `end`.
The docstring for each element lists the available anchors.
Once an element is added to the drawing, all its anchor positions will be added as attributes to the element object, so the base position of transistor assigned to variable `Q` may be accessed via `Q.base`.

Rather than working in absolute (x, y) coordinates, anchors can be used to set the position of new elements.
Using the `at` method, one element can be placed starting on the anchor of another element.

For example, to draw an opamp and place a resistor on the output, store the Opamp instance to a variable. Then call the `at` method of the new element passing the `Opamp.out` anchor. After the resistor is drawn, the current drawing position is moved to the endpoint of the resistor.

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


The second purpose for anchors is aligning new elements with respect to existing elements.

Suppose a resistor has just been placed, and now an Opamp should be connected to the resistor.
The `anchor` method tells the Drawing which input on the Opamp should align with resistor.
Here, an Opamp is placed at the end of a resistor, connected to the opamp's `in1` anchor (the inverting input).

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


Dimensions
----------

The inner zig-zag portion of a resistor has length of 1 unit, while the default lead extensions are 1 unit on each side,
making the default total resistor length 3 units.
Placement methods such as `at` and `to` accept a tuple of (x, y) position in these units.


.. jupyter-execute::
    :hide-code:

    with schemdraw.Drawing() as d:
        d += elm.Resistor()
        d += elm.Line(arrow='|-|').at((1, .7)).to((2, .7)).label('1.0').color('royalblue')
        d += elm.Line(arrow='|-|').at((0, -.7)).to((3, -.7)).label('Drawing.unit', 'bottom').color('royalblue')

This default 2-terminal length can be changed using the `unit` parameter to the :py:meth:`schemdraw.Drawing.config` method:

.. code-block:: python

    with schemdraw.Drawing() as d:
        d.config(unit=2)
        ...

.. jupyter-execute::
    :hide-code:
    
    with schemdraw.Drawing() as d:
        d.config(unit=2)
        d += elm.Resistor()
        d += elm.Line(arrow='|-|').at((.5, .7)).to((1.5, .7)).label('1.0').color('royalblue')
        d += elm.Line(arrow='|-|').at((0, -.7)).to((2, -.7)).label('Drawing.unit', 'bottom').color('royalblue')


Two-Terminal Elements
---------------------

In Schemdraw, a "Two-Terminal Element" is any element that can grow to fill a given length (this includes elements such as the Potentiometer, even though it electrically has three terminals).
All two-terminal elements subclass :py:class:`schemdraw.elements.Element2Term`.
They have some additional methods for setting placement and length.

The `length` method sets an exact length for a two-terminal element. Alternatively, the `up`, `down`, `left`, and `right` methods on two-terminal elements take a length parameter.

.. jupyter-execute::
    :emphasize-lines: 5

    with schemdraw.Drawing() as d:
        d += elm.Dot()
        d += elm.Resistor()
        d += elm.Dot()
        d += elm.Diode().length(6)
        d += elm.Dot()

The `to` method will set an exact endpoint for a 2-terminal element.
The starting point is still the ending location of the previous element.
Notice the Diode is stretched longer than the standard element length in order to fill the diagonal distance.

.. jupyter-execute::
    :emphasize-lines: 4

    with schemdraw.Drawing() as d:
        R = d.add(elm.Resistor())
        C = d.add(elm.Capacitor().up())
        Q = d.add(elm.Diode().to(R.start))

The `tox` and `toy` methods are useful for placing 2-terminal elements to "close the loop", without requiring an exact length. 
They extend the element horizontally or vertically to the x- or y- coordinate of the anchor given as the argument. 
These methods automatically change the drawing direction.
Here, the Line element does not need to specify an exact length to fill the space and connect back with the Source.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:
    :emphasize-lines: 9

    d += (C := elm.Capacitor())
    d += elm.Diode()
    d += elm.Line().down()

    # Now we want to close the loop, but can use `tox` 
    # to avoid having to know exactly how far to go.
    # The Line will extend horizontally to the same x-position
    # as the Capacitor's `start` anchor.
    d += elm.Line().tox(C.start)

    # Now close the loop by relying on the fact that all
    # two-terminal elements (including Source and Line)
    # are the same length by default
    d += elm.Source().up()

.. jupyter-execute::
    :hide-code:

    d.draw()


Finally, exact endpoints can also be specified using the `endpoints` method.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()

.. jupyter-execute::
    :hide-output:
    :emphasize-lines: 5

    d += (R := elm.Resistor())
    d += (Q := elm.Diode().down(6))
    d += elm.Line().tox(R.start)
    d += elm.Capacitor().toy(R.start)
    d += elm.SourceV().endpoints(Q.end, R.start)

.. jupyter-execute::
    :hide-code:

    d.draw()


Orientation
-----------

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
-------------

The :py:class:`schemdraw.Drawing` maintains a drawing state that includes the current x, y position, stored in the `Drawing.here` attribute as a (x, y) tuple, and drawing direction stored in the `Drawing.theta` attribute.
A LIFO stack of drawing states can be used, via the :py:meth:`schemdraw.Drawing.push` and :py:meth:`schemdraw.Drawing.pop` method,
for situations when it's useful to save the drawing state and come back to it later.

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()

.. jupyter-execute::
    :emphasize-lines: 4,10

    d += elm.Inductor()
    d += elm.Dot()
    print('d.here:', d.here)
    d.push()  # Save this drawing position/direction for later

    d += elm.Capacitor().down()  # Go off in another direction temporarily
    d += elm.Ground(lead=False)
    print('d.here:', d.here)

    d.pop()   # Return to the pushed position/direction
    print('d.here:', d.here)
    d += elm.Diode()
    d.draw()

Changing the drawing position can be accomplished by calling :py:meth:`schemdraw.Drawing.move` or :py:meth:`schemdraw.Drawing.move_from`.


Drop and Hold Methods
*********************

To place an element without moving the drawing position, use the :py:meth:`schemdraw.elements.Element.hold` method. The element will be placed without changing the drawing state.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()
    
.. jupyter-execute::
    :emphasize-lines: 5

    d += elm.Diode()  # Normal placement: drawing position moves to end of element
    d += elm.Dot().color('red')

    d.here = (0, -1)
    d += elm.Diode().hold()  # Hold method prevents position from changing
    d += elm.Dot().color('blue')

.. jupyter-execute::
    :hide-code:
    
    d.draw()


Three-terminal elements do not necessarily leave the drawing position where desired, so after drawing an element, the current drawing position can be set using the :py:meth:`schemdraw.elements.Element.drop` method to specify an anchor at which to place the cursor.
This reduces the need to assign every element to a variable name.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()
    
.. jupyter-execute::
    :emphasize-lines: 5

    d += elm.BjtNpn()
    d += elm.Resistor().label('R1')
    d.here = (5, 0)

    d += elm.BjtNpn().drop('emitter')
    d += elm.Resistor().label('R2')

.. jupyter-execute::
    :hide-code:
    
    d.draw()


Connecting Elements
-------------------

Typically, the :py:class:`schemdraw.elements.lines.Line` element is used to connect elements together.
More complex line routing requires multiple Line elements.
The :py:class:`schemdraw.elements.lines.Wire` element is used as a shortcut for placing multiple connecting lines at once.
The Wire element connects the start and end points based on its `shape` parameter.
The `k` parameter is used to set the distance before the wire first changes direction.

.. list-table:: Wire Shape Parameters
   :widths: 25 50
   :header-rows: 1

   * - Shape Parameter
     - Description
   * - `-`
     - Direct Line
   * - `-\|`
     - Horizontal then vertical
   * - `\|-`
     - Vertical then horizontal
   * - `n`
     - Vertical-horizontal-vertical (like an n or u)
   * - `c`
     - Horizontal-vertical-horizontal (like a c or ↄ)
   * - `z`
     - Horizontal-diagonal-horizontal
   * - `N`
     - Vertical-diagonal-vertical

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()
    d += (A := elm.Dot().label('A', halign='right', ofst=(-.1, 0)))
    d += (B := elm.Dot().label('B').at((4, 4)))
    d += (C := elm.Dot().label('C', ofst=(-.2, 0)).at((7, 4)))
    d += (D := elm.Dot().label('D', ofst=(-.2, 0)).at((9, 0)))
    d += (E := elm.Dot().label('E', ofst=(-.2, 0)).at((11, 4)))
    d += (F := elm.Dot().label('F', ofst=(-.2, 0)).at((13, 0)))

.. jupyter-execute::

    d += elm.Wire('-', arrow='->').at(A.center).to(B.center).color('deeppink').label('"-"')
    d += elm.Wire('|-', arrow='->').at(A.center).to(B.center).color('mediumblue').label('"|-"')
    d += elm.Wire('-|', arrow='->').at(A.center).to(B.center).color('darkseagreen').label('"-|"')
    d += elm.Wire('c', k=-1, arrow='->').at(C.center).to(D.center).color('darkorange').label('"c"', halign='left')
    d += elm.Wire('n', arrow='->').at(C.center).to(D.center).color('orchid').label('"n"')
    d += elm.Wire('N', arrow='->').at(E.center).to(F.center).color('darkred').label('"N"', 'start', ofst=(-.1, -.75))
    d += elm.Wire('z', k=.5, arrow='->').at(E.center).to(F.center).color('teal').label('"z"', halign='left', ofst=(0, .5))

.. jupyter-execute::
    :hide-code:

    d.draw()

Both `Line` and `Wire` elements take an `arrow` parameter, a string specification of arrowhead types at the start and end of the wire. The arrow string may contain "<", ">", for arrowheads, "\|" for an endcap, and "o" for a dot. Some examples are shown below:

.. jupyter-execute::
    :hide-code:

    d = schemdraw.Drawing()
    
.. jupyter-execute::

    d += elm.Line(arrow='->').label('"->"', 'right')
    d += elm.Line(arrow='<-').at((0, -.75)).label('"<-"', 'right')
    d += elm.Line(arrow='<->').at((0, -1.5)).label('"<->"', 'right')
    d += elm.Line(arrow='|->').at((0, -2.25)).label('"|->"', 'right')
    d += elm.Line(arrow='|-o').at((0, -3.0)).label('"|-o"', 'right')

.. jupyter-execute::
    :hide-code:

    d.draw()    

Because dots are used to show connected wires, all two-terminal elements have `dot` and `idot` methods for quickly adding a dot at the end or beginning of the element, respectively.

.. jupyter-execute::

    elm.Resistor().dot()


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

