Signal Processing
=================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    from functools import partial
    import schemdraw
    from schemdraw import dsp

Signal processing elements can be drawn by importing the :py:mod:`schemdraw.dsp.dsp` module:

.. code-block:: python

    from schemdraw import dsp

Because each element may have multiple connections in and out, these elements
are not 2-terminal elements that extend "leads", so they must be manually connected with
`Line` or `Arrow` elements. The square elements define anchors 'N', 'S', 'E', and 'W' for
the four directions. Circle-based elements also includ 'NE', 'NW', 'SE', and 'SW'
anchors.
Directional elements, such as `Amp`, `Adc`, and `Dac` define anchors `input` and `out`.


.. jupyter-execute::
    :hide-code:

    def drawElements(elmlist, cols=3, dx=8, dy=2):
        d = schemdraw.Drawing(fontsize=12)
        for i, e in enumerate(elmlist):
            y = i//cols*-dy
            x = (i%cols) * dx

            name = type(e()).__name__
            if hasattr(e, 'keywords'):  # partials have keywords attribute
                args = ', '.join(['{}={}'.format(k, v) for k, v in e.keywords.items()])
                name = '{}({})'.format(name, args)
            d += e().right().at((x,y)).label(name, loc='rgt', ofst=.2, halign='left', valign='center')
        return d

    elms = [dsp.Square, dsp.Circle, dsp.Sum, dsp.SumSigma, dsp.Mixer, dsp.Speaker,
            dsp.Amp, dsp.OscillatorBox, dsp.Oscillator, dsp.Filter, 
            partial(dsp.Filter, response='lp'), partial(dsp.Filter, response='bp'),
            partial(dsp.Filter, response='hp'), dsp.Adc, dsp.Dac, dsp.Demod,
            dsp.Circulator, dsp.Isolator, dsp.VGA
            ]
    drawElements(elms, dx=6)


Labels are placed in the center of the element. The generic `Square` and `Circle` elements can be used with a label to define other operations. For example, an integrator
may be created using:

.. jupyter-execute::

    dsp.Square().label(r'$\int$')
