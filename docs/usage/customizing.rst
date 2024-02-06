Customizing Elements
====================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import logic
    from schemdraw.segments import *


Grouping Elements
-----------------

If a set of circuit elements are to be reused multiple times, they can be grouped into a single element.
Create and populate a drawing, but set `show=False`.
Instead, use the Drawing to create a new :py:class:`schemdraw.elements.ElementDrawing`, which converts the drawing into an element instance
to add to other drawings.
    
.. jupyter-execute::
    :emphasize-lines: 8-10

    with schemdraw.Drawing(show=False) as d1:
        d1 += elm.Resistor()
        d1.push()
        d1 += elm.Capacitor().down()
        d1 += elm.Line().left()
        d1.pop()

    with schemdraw.Drawing() as d2:  # Add a second drawing
        for i in range(3):
            d2 += elm.ElementDrawing(d1)   # Add the first drawing to it 3 times
    
    
.. _customelements:

Defining custom elements
------------------------

All elements are subclasses of :py:class:`schemdraw.elements.Element` or :py:class:`schemdraw.elements.Element2Term`.
For elements consisting of several other already-defined elements (like a relay), :py:class:`schemdraw.elements.compound.ElementCompound` can be used for easy combining of multiple elements.
Subclasses only need to define the `__init__` method in order to add lines, shapes, and text to the new element, all of which are defined using :py:class:`schemdraw.segments.Segment` classes. New Segments should be appended to the `Element.segments` attribute list.

Coordinates are all defined in element cooridnates, where the element begins
at (0, 0) and is drawn from left to right.
The drawing engine will rotate and translate the element to its final position, and for two-terminal
elements deriving from Element2Term, will add lead extensions to the correct length depending
on the element's placement parameters.
Therefore elements deriving from Element2Term should not define the lead extensions
(e.g. a Resistor only defines the zig-zag portion).
A standard resistor is 1 drawing unit long, and with default lead extension will become 3 units long.

Segments include :py:class:`schemdraw.segments.Segment`, :py:class:`schemdraw.segments.SegmentPoly`,
:py:class:`schemdraw.segments.SegmentCircle`, :py:class:`schemdraw.segments.SegmentArc`, :py:class:`schemdraw.segments.SegmentText`, and :py:class:`schemdraw.segments.SegmentBezier`.

As an example, here's the definition of our favorite element, the resistor:

.. code-block:: python

    class Resistor(Element2Term):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.segments.append(Segment([(0, 0),
                                          (0.5*reswidth, resheight),
                                          (1.5*reswidth, -resheight),
                                          (2.5*reswidth, resheight),
                                          (3.5*reswidth, -resheight),
                                          (4.5*reswidth, resheight),
                                          (5.5*reswidth, -resheight),
                                          (6*reswidth, 0)]))

The resistor is made of one path.
`reswidth` and `resheight` are constants that define the height and width of the resistor zigzag (and are referenced by several other elements too).
Browse the source code in the `Schemdraw.elements` submodule to see the definitions of the other built-in elements.

In addition to the list of Segments, any named anchors and other parameters should be specified.
Anchors should be added to the `Element.anchors` dictionary as {name: (x, y)} key/value pairs.

Parameters and Defaults
^^^^^^^^^^^^^^^^^^^^^^^

`Element` subclasses may have an `_element_defaults` class attribute dictionary to specify default parameters used for
drawing the element.
This dictionary will be ChainMapped with the `_element_defaults` from all its parent classes into the `Element.defaults`
dictionary the user may change to modify default behaviors.

To access any of these parameters when defining the element, use the `self.params` dictionary, which ensures the correct parameter,
whether a default value, a default from a parent class, or a parameter overriden by the user, is obtained.
Any non-`None` named arguments provided to the Element will be inserted into `self.params` automatically
(by the `Element.__new__` method).

Parameters that need to be set dynamically during instantiation should be set in the `self.elmparams` dictionary, so they may
still be overriden by the user.

For example, consider the `Dot` element:

.. code-block::

    class Dot(Element):
        ''' Connection Dot

            Keyword Args:
                radius: Radius of dot [default: 0.075]
                open: Draw as an open circle [default: False]
        '''
        _element_defaults = {
            'radius': 0.075,
            'open': False}
        def __init__(self,
                    radius: Optional[float] = None,
                    open: Optional[bool] = None,
                    **kwargs):
            super().__init__(**kwargs)
            fill = 'bg' if self.params['open'] else True
            self.elmparams['fill'] = fill
            self.segments.append(SegmentCircle((0, 0), self.params['radius']))
            self.anchors['center'] = (0, 0)

It contains two default parameters, `radius`, and `open`.
The user may override these for every new Dot by setting `Dot.defaults['radius'] = value`.
Or to override the defaults for a single instance of Dot, provide the parameter at instantiation:
`Dot(radius=value)`.

Inside the `Dot.__init__` method, the `fill` parameter is determined based on the value of
the `open` parameter, read from `self.params['open']`. The Dot is filled when the dot is not open,
but filled with background color ('bg') when the dot is open. Because the fill value was added to
`self.elmparams`, the user may sitll specify their own fill color using `Dot(fill=color)`.

Next, a `SegmentCircle` is added with radius taken from `self.params['radius']`, so that the
default radius will be used unless overridden. Finally, an anchor named `center` is defined at the center of the dot.

When drawn, the parameters for the element are obtained from a ChainMap of the parameters in this order of preference:

1) Setter methods like `.fill()` or `.color()` called after the element is instantiated
2) Named arguments provided to Element instantiation
3) Defaults set by the user in Element.defaults (inheriting from parent classes)
4) Parameters defined in the Element attribute `self.elmparams`
5) Parameters defined by Drawing.config
6) Parameters defined by Schemdraw.config


Flux Capacitor Example
^^^^^^^^^^^^^^^^^^^^^^

For an example, let's make a flux capacitor circuit element.

Since everyone knows a flux-capacitor has three branches, we should subclass the standard :py:class:`schemdraw.elements.Element` class instead of :py:class:`schemdraw.elements.Element2Term`.
Start by importing the Segments and define the class name and `__init__` function:

.. code-block:: python

    from schemdraw.segments import *

    class FluxCapacitor(Element):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

The `d` and `kwargs` are passed to `super` to initialize the Element.

We want a dot in the center of our flux capacitor, so start by adding a `SegmentCircle`. The `fclen` and `radius` variables could be set as arguments to the __init__ and/or added to `_element_defaults` for the user to adjust, if desired, but here they are defined as constants in the __init__.

.. code-block:: python

            fclen = 0.5
            radius = 0.075
            self.segments.append(SegmentCircle((0, 0), radius))

Next, add the paths as Segment instances, which are drawn as lines. The flux capacitor will have three paths, all extending from the center dot:

.. code-block:: python

            self.segments.append(Segment([(0, 0), (0, -fclen*1.41)]))
            self.segments.append(Segment([(0, 0), (fclen, fclen)]))
            self.segments.append(Segment([(0, 0), (-fclen, fclen)]))
        
        
And at the end of each path is an open circle. Append three more `SegmentCircle` instances.
By specifying `fill=None` the SegmentCircle will always remain unfilled regardless of any `fill` arguments provided to `Drawing` or `FluxCapacitor`.

.. code-block:: python

            self.segments.append(SegmentCircle((0, -fclen*1.41), 0.2, fill=None))
            self.segments.append(SegmentCircle((fclen, fclen), 0.2, fill=None))
            self.segments.append(SegmentCircle((-fclen, fclen), 0.2, fill=None))
    

Finally, we need to define anchor points so that other elements can be connected to the right places.
Here, they're called `p1`, `p2`, and `p3` for lack of better names (what do you call the inputs to a flux capacitor?)
Add these to the `self.anchors` dictionary.

.. code-block:: python

            self.anchors['p1'] = (-fclen, fclen)
            self.anchors['p2'] = (fclen, fclen)
            self.anchors['p3'] = (0, -fclen*1.41)

Here's the Flux Capacitor class all in one:

.. jupyter-execute::

    class FluxCapacitor(elm.Element):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            radius = 0.075
            fclen = 0.5
            self.segments.append(SegmentCircle((0, 0), radius))
            self.segments.append(Segment([(0, 0), (0, -fclen*1.41)]))
            self.segments.append(Segment([(0, 0), (fclen, fclen)]))
            self.segments.append(Segment([(0, 0), (-fclen, fclen)]))
            self.segments.append(SegmentCircle((0, -fclen*1.41), 0.2, fill=None))
            self.segments.append(SegmentCircle((fclen, fclen), 0.2, fill=None))
            self.segments.append(SegmentCircle((-fclen, fclen), 0.2, fill=None))
            self.anchors['p1'] = (-fclen, fclen)
            self.anchors['p2'] = (fclen, fclen)
            self.anchors['p3'] = (0, -fclen*1.41)


Try it out:

.. jupyter-execute::

    FluxCapacitor()


Segment objects
---------------

After an element is added to a drawing, the :py:class:`schemdraw.segments.Segment` objects defining it are accessible in the `segments` attribute list of the Element.
For even more control over customizing individual pieces of an element, the parameters of a Segment can be changed.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()
    
.. jupyter-execute::

    d += (n := logic.Nand())
    n.segments[1].color = 'red'
    n.segments[1].zorder = 5  # Put the bubble on top

.. jupyter-execute::
    :hide-code:

    d.draw()


Matplotlib axis
---------------

When using the Matplotlib backend (the default), a final customization option is to use the Matplotlib figure and add to it.
A :py:class:`schemdraw.Figure` is returned from the `draw` method, which contains `fig` and `ax` attributes holding the Matplotlib figure.

.. jupyter-execute::
    :emphasize-lines: 4-5

    schemdraw.use('matplotlib')
    d = schemdraw.Drawing()
    d.add(elm.Resistor())
    schemfig = d.draw()
    schemfig.ax.axvline(.5, color='purple', ls='--')
    schemfig.ax.axvline(2.5, color='orange', ls='-', lw=3);
    display(schemfig)
    