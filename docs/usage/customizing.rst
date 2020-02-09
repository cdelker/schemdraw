Customizing Elements
====================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import SchemDraw
    from SchemDraw import elements as elm
    from SchemDraw import logic


Reusing groups of elements
--------------------------

If a set of circuit elements are to be reused multiple times, they can be grouped into a single element.
Create and populate a drawing, but don't call `draw` on it.
Instead, use :py:func:`group_elements`, then add the result as an element to another drawing

.. function:: SchemDraw.group_elements(drawing, anchors=None)

    Create a new element definition based on all the elements in the drawing.
    
    :param drawing: SchemDraw.Drawing with elements to group
    :param anchors: dictionary of anchor names: locations within the group
    
.. jupyter-execute::

    d1 = SchemDraw.Drawing()
    d1.add(elm.RES)
    d1.push()
    d1.add(elm.CAP, d='down')
    d1.add(elm.LINE, d='left')
    d1.pop()
    RC = SchemDraw.group_elements(d1)   # Create the group to reuse

    d2 = SchemDraw.Drawing()   # Add the group to another drawing several times
    for i in range(3):
        d2.add(RC)
    d2.draw()
    
    
.. _customelements:

Defining custom elements
------------------------

New elements can be defined by creating a dictionary describing how the element should be drawn.
An element is made up of paths and/or shapes.
A path is simply a list of xy coordinates (drawn using Matplotlib's `plot` function).
A shape can be a circle, polygon, arrow, or arc (a Matplotlib patch).

Coordinates are all defined in element cooridnates, where the element begins
at [0, 0] and is drawn from left to right. The drawing engine will then rotate
and translate the element to its final position. A standard resistor is
1 drawing unit long, and with default lead extension will become 3 units long.

Possible dictionary keys:

- **name**:  A name string for the element. Currently only used for documentation and testing.
- **paths**: A list of each path line in the element. For example, a capacitor has two paths, one for each capacitor "plate". On 2-terminal elements, the leads will be automatically extended away from the first and last points of the first path, and don't need to be included in the path.
- **base**:  Dictionary defining a base element. For example, the variable resistor has a base of resistor, then adds an additional path.
- **shapes**: A list of shape dictionaries. See below for options.
- **theta**: Default angle (in degrees) for the element. Overrides the current drawing angle.
- **anchors**: A dictionary defining named positions within the element. For example, the NFET element has a 'source', 'gate', and 'drain' anchor. Each anchor will become an attribute of the element class which can then be used for connecting other elements.
- **extend** (bool) Extend the leads to fill the full element length.
- **move_cur**: (bool) Move the drawing cursor location after drawing.
- **color**: A matplotlib-compatible color for the element. Examples include 'red', 'blue', '#34ac92'
- **drop**: Final location to leave drawing cursor.
- **lblloc**: ['top', 'bot', 'lft', 'rgt'] default location for text label. Defaults to 'top'.
- **lblofst**: Default distance between element and text label.
- **labels**: List of (label, pos) tuples defining text labels to always draw in the element.
- **ls**: [':', '--', '-'] linestyle (same as matplotlib). Only applies to paths.

In the `shapes` list, each shape is defined by a dictionary. All shape dictionaries contain

- **shape**: key can be [ 'circle', 'poly', 'arc', 'arrow' ]
- **zorder**: drawing order within the element

The remaining keys depend on the type of shape as follows.

Circle:

- **center**: [x, y] center coordinate
- **radius**: radius of circle
- **fill**: (bool) fill the circle
- **fillcolor**: color for fill

Poly:

- **xy**: List of xy coordinates defining polygon
- **closed**: (bool) Close the polygon
- **fill**: (bool) fill the polygon
- **fillcolor**: color for fill

Arc:

- **center**: Center coordinate of arc
- **width**, **height'** width and height of arc
- **theta1**: Starting angle (degrees)
- **theta2**: Ending angle (degrees)
- **angle**: Rotation angle of entire arc
- **arrow**: ['cw', 'ccw'] Add an arrowhead, clockwise or counterclockwise

Arrow:

- **start**: [x, y] start of arrow
- **end**: [x, y] end of arrow
- **headwidth**: width of arrowhead
- **headlength**: length of arrowhead

Here's the definition of our favorite element, the resistor:

.. code-block:: python

    RES = {
        'name': 'RES',
        'paths': [
                  [[0, 0], [0.5*_rw, _rh], [1.5*_rw, -_rh], [2.5*_rw, _rh], [3.5*_rw, -_rh], [4.5*_rw, _rh], [5.5*_rw, -_rh], [6*_rw, 0]]
                 ]
          }

The resistor is made of just one path.
`_rw` and `_rh` are constants that define the height and width of the resistor.
Browse the source code in elements.py to see the definitions of the other built-in elements.


Flux Capacitor Example
^^^^^^^^^^^^^^^^^^^^^^

For an example, let's make a flux capacitor circuit element.
Here, we'll start by defining the `fclen` variable as the length of one leg so we can change it easily.
Remember a resistor is 1 unit long.

.. code-block:: python

    fclen = 0.5
    
The custom element is a dictionary of parameters.
We want a dot in the center of our flux capacitor, so use the `base` key to start with the already defined `DOT` element.

.. code-block:: python

    FLUX_CAP = {
        'base': elm.DOT,

Next, add the paths, which are drawn as lines. The flux capacitor will have three paths, all extending from the center dot:

.. code-block:: python

    'paths': [[[0, 0], [0, -fclen*1.41]],  # Leg going down
              [[0, 0], [fclen, fclen]],    # Leg going up/right
              [[0, 0], [-fclen, fclen]]],  # Leg going up/left

And at the end of each path is an open circle. These are added to the dictionary using the `shapes` key as a list of shape dictionaries.

.. code-block:: python

    'shapes': [{'shape': 'circle', 'center': [0, -fclen*1.41], 'radius': .2, 'fill': False},
               {'shape': 'circle', 'center': [fclen, fclen], 'radius': .2, 'fill': False},
               {'shape': 'circle', 'center': [-fclen, fclen], 'radius': .2, 'fill': False}],
    
Finally, we need to define anchor points so that other elements can be connected to the right places.
Here, they're called `p1`, `p2`, and `p3` for lack of better names (what do you call the inputs to a flux capacitor?)

.. code-block:: python

    'anchors': {'p1': [-fclen, fclen], 'p2': [fclen, fclen], 'p3': [0, -fclen]}
    
Here's the element dictionary all in one:

.. jupyter-execute::

    fclen = 0.5
    FLUX_CAP = {
        'base': elm.DOT,
        'paths': [[[0, 0], [0, -fclen*1.41]],  # Leg going down
                  [[0, 0], [fclen, fclen]],    # Leg going up/right
                  [[0, 0], [-fclen, fclen]]],  # Leg going up/left
        'shapes': [{'shape': 'circle', 'center': [0, -fclen*1.41], 'radius': .2, 'fill': False},
                   {'shape': 'circle', 'center': [fclen, fclen], 'radius': .2, 'fill': False},
                   {'shape': 'circle', 'center': [-fclen, fclen], 'radius': .2, 'fill': False}],
        'anchors': {'p1': [-fclen, fclen], 'p2': [fclen, fclen], 'p3': [0, -fclen]}
        }


Test it out by adding the new custom element to a drawing:

.. jupyter-execute::

    d = SchemDraw.Drawing()
    fc = d.add(FLUX_CAP)
    d.draw()



Segment objects
---------------

Each path and shape in the element definition is translated into drawing coordinates and becomes a :py:class:`SchemDraw.Segment` object
contained in `segments` list attribute of the :py:class:`SchemDraw.Element` instance.
For even more control over individual pieces of an element, the parameters of a Segment can be changed.

.. jupyter-execute::
    :hide-code:
    
    d = SchemDraw.Drawing()
    
.. jupyter-execute::

    n = d.add(logic.NAND2)
    n.segments[-1].color = 'red'
    n.segments[-1].zorder = 5  # Put the bubble on top
    d.draw()


Matplotlib axis
---------------

As a final customization option, remember that SchemDraw draws everything on a Matplotlib axis.
This axis can be obtained using `plt.gca()` and used for whatever purpose.

.. jupyter-execute::

    import matplotlib.pyplot as plt
    d = SchemDraw.Drawing()
    d.add(elm.RES)
    d.draw()
    ax = plt.gca()
    ax.axvline(.5, color='purple', ls='--')
    ax.axvline(2.5, color='orange', ls='-', lw=3);

    