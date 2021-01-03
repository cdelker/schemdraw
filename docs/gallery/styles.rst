Styles
------

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm


Circuit elements can be styled using Matplotlib colors, line-styles, and line widths.

Resistor circle
^^^^^^^^^^^^^^^

Uses named colors in a loop.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    for i, color in enumerate(['red', 'orange', 'yellow', 'yellowgreen', 'green', 'blue', 'indigo', 'violet']):
        d += elm.Resistor().theta(45*i+20).color(color).label('R{}'.format(i))
    d.draw()


Hand-drawn
^^^^^^^^^^

And for a change of pace, activate Matplotlib's XKCD mode for "hand-drawn" look!

.. jupyter-execute::
    :code-below:

    import matplotlib.pyplot as plt
    plt.xkcd()

    d = schemdraw.Drawing(inches_per_unit=.5)
    d += (op := elm.Opamp())
    d += elm.Line().left().at(op.in2).length(d.unit/4)
    d += elm.Line().down().length(d.unit/5)
    d += elm.Ground()
    d += elm.Line().left().at(op.in1).length(d.unit/6)
    d += elm.Dot()
    d.push()
    d += (Rin := elm.Resistor().left().at((op.in1[0]-d.unit/5, op.in1[1]))
          .label('$R_{in}$', 'bottom')
          .label('$v_{in}$', 'left'))
    d.pop()
    d += elm.Line().up().length(d.unit/2)
    d += (Rf := elm.Resistor().right().length(d.unit).label('$R_f$'))
    d += elm.Line().down().toy(op.out)
    d += elm.Dot()
    d += elm.Line().left().tox(op.out)
    d += elm.Line().right().length(d.unit/4).label('$v_{o}$', 'right')
    d.draw()
