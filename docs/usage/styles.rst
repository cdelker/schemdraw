.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


.. _styles:


Styling
-------

Style options, such as color, line thickness, and fonts, may be set at the global level (all Schemdraw Drawings), at the Drawing level, or on individual Elements.

Individual Elements
*******************

Element styling methods include `color`, `fill`, `linewidth`, and `linestyle`.
If a style method is not called when creating an Element, its value is obtained from from the drawing or global defaults.

Color and fill parameters accept any named `SVG color <https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg>`_ or a hex color string such as '#6A5ACD'. Linestyle parameters may be '-', '--', ':', or '-.'.

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

The `label` method also accepts color, font, and fontsize parameters, allowing labels with different style as their elements.


Drawing style
*************

Styles may be applied to an entire drawing using the :py:meth:`schemdraw.Drawing.config` method.
These parameters include color, linewidth, font, fontsize, linestyle, fill, and background color.
Additionally, the `config` method allows specification of the default 2-Terminal element length.


Global style
************

Styles may be applied to every new drawing created by Schemdraw (during the Python session) using :py:meth:`schemdraw.config`, using the same arguments as the Drawing config method.

.. jupyter-execute::
    :emphasize-lines: 1

    schemdraw.config(lw=1, font='serif')
    with schemdraw.Drawing() as d:
        d += elm.Resistor().label('100KΩ')
        d += elm.Capacitor().down().label('0.1μF', loc='bottom')
        d += elm.Line().left()
        d += elm.Ground()
        d += elm.SourceV().up().label('10V')

.. jupyter-execute::
    :hide-code:
    
    schemdraw.config()


Global Element Configuration
****************************

The :py:meth:`schemdraw.elements.Element.style` can be used to configure styles on individual element classes that apply to all Drawings.
It may be used, for example, to fill all Diode elements by default, without requiring the `fill()` method on every Diode instance.

Its argument is a dictionary of {name: Element} class pairs.
Combined with `functools.partial <https://docs.python.org/3/library/functools.html#functools.partial>`_ from the standard library, parameters to elements can be set globally.
For example, the following code fills all Diode elements:

.. jupyter-execute::
    :emphasize-lines: 3

    from functools import partial

    elm.style({'Diode': partial(elm.Diode, fill=True)})

    with schemdraw.Drawing() as d:
        d += elm.Diode()
        d += elm.Diode()

Be careful, though, because the `style` method can overwrite existing elements in the namespace.


U.S. versus European Style
**************************

The main use of :py:meth:`schemdraw.elements.Element.style` is to reconfigure elements in IEEE/U.S. style or IEC/European style.
The `schemdraw.elements.STYLE_IEC` and `schemdraw.elements.STYLE_IEEE` are dictionaries for use in the `style` method to change configuration of various elements that use different standard symbols (resistor, variable resistor, photo resistor, etc.)

To configure IEC/European style, use the `style` method with the `elm.STYLE_IEC` dictionary.

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()

.. jupyter-execute::
    :emphasize-lines: 1

    elm.style(elm.STYLE_IEC)
    d += elm.Resistor()

.. jupyter-execute::
    :hide-code:

    d.draw()
    

.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()

.. jupyter-execute::
    :emphasize-lines: 1

    elm.style(elm.STYLE_IEEE)
    d += elm.Resistor()

.. jupyter-execute::
    :hide-code:

    d.draw()

To see all the elements that change between IEEE and IEC, see :ref:`styledelements`.


Themes
******

Schemdraw also supports themeing, to enable dark mode, for example.
The defined themes match those in the `Jupyter Themes <https://github.com/dunovank/jupyter-themes>`_ package:

    * default (black on white)
    * dark (white on black)
    * solarizedd
    * solarizedl
    * onedork
    * oceans16
    * monokai
    * gruvboxl
    * gruvboxd
    * grade3
    * chesterish

They are enabled using :py:meth:`schemdraw.theme`:

.. jupyter-execute::
    :emphasize-lines: 1

    schemdraw.theme('monokai')
    with schemdraw.Drawing() as d:
        d += elm.Resistor().label('100KΩ')
        d += elm.Capacitor().down().label('0.1μF', loc='bottom')
        d += elm.Line().left()
        d += elm.Ground()
        d += elm.SourceV().up().label('10V')

.. jupyter-execute::
    :hide-code:

    schemdraw.theme('default')
