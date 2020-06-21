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
        d.add(elm.Resistor(label='R{}'.format(i), theta=45*i+20, color=color))
    d.draw()


Hand-drawn
^^^^^^^^^^

And for a change of pace, activate Matplotlib's XKCD mode for "hand-drawn" look!

.. jupyter-execute::
    :code-below:

    import matplotlib.pyplot as plt
    plt.xkcd()

    d = schemdraw.Drawing(inches_per_unit=.5)
    op = d.add(elm.Opamp)
    d.add(elm.Line('left', xy=op.in2, l=d.unit/4))
    d.add(elm.Line('down', l=d.unit/5))
    d.add(elm.Ground)
    d.add(elm.Line('left', xy=op.in1, l=d.unit/6))
    d.add(elm.Dot)
    d.push()
    Rin = d.add(elm.Resistor('left', xy=op.in1-[d.unit/5,0], botlabel='$R_{in}$', lftlabel='$v_{in}$'))
    d.pop()
    d.add(elm.Line('up', l=d.unit/2))
    Rf = d.add(elm.Resistor('right', l=d.unit*1, label='$R_f$'))
    d.add(elm.Line('down', toy=op.out))
    d.add(elm.Dot)
    d.add(elm.Line('left', tox=op.out))
    d.add(elm.Line('right', l=d.unit/4, rgtlabel='$v_{o}$'))
    d.draw()
