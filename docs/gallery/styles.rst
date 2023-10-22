Styles
------

.. jupyter-execute::
    :hide-code:

    import schemdraw
    from schemdraw import elements as elm


Circuit elements can be styled using Matplotlib colors, line-styles, and line widths.

Resistor circle
^^^^^^^^^^^^^^^

Uses named colors in a loop.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        for i, color in enumerate(['red', 'orange', 'yellow', 'yellowgreen', 'green', 'blue', 'indigo', 'violet']):
            elm.Resistor().theta(45*i+20).color(color).label('R{}'.format(i))


Hand-drawn
^^^^^^^^^^

And for a change of pace, activate Matplotlib's XKCD mode for "hand-drawn" look!

.. jupyter-execute::
    :code-below:

    import matplotlib.pyplot as plt
    plt.xkcd()

    with schemdraw.Drawing() as d:
        op = elm.Opamp(leads=True)
        elm.Line().down().at(op.in2).length(d.unit/4)
        elm.Ground(lead=False)
        Rin = elm.Resistor().at(op.in1).left().idot().label('$R_{in}$', loc='bot').label('$v_{in}$', loc='left')
        elm.Line().up().at(op.in1).length(d.unit/2)
        elm.Resistor().tox(op.out).label('$R_f$')
        elm.Line().toy(op.out).dot()
        elm.Line().right().at(op.out).length(d.unit/4).label('$v_{o}$', loc='right')