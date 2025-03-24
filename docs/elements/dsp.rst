Signal Processing
=================

.. jupyter-execute::
    :hide-code:

    import schemdraw
    from schemdraw import dsp
    schemdraw.use('svg')

Signal processing elements can be drawn by importing the :py:mod:`schemdraw.dsp.dsp` module:

.. code-block:: python

    from schemdraw import dsp

Because each element may have multiple connections in and out, these elements
are not 2-terminal elements that extend "leads", so they must be manually connected with
`Line` or `Arrow` elements. The square elements define anchors 'N', 'S', 'E', and 'W' for
the four directions. Circle-based elements also includ 'NE', 'NW', 'SE', and 'SW'
anchors.
Directional elements, such as `Amp`, `Adc`, and `Dac` define anchors `input` and `out`.


.. element_list::
    :module: dsp
    :nolabel:

    Square()
    Circle()
    Sum()
    SumSigma()
    Mixer()
    Speaker()
    Amp()
    OscillatorBox()
    Oscillator()
    Filter()
    Filter(response='lp')
    Filter(response='bp')
    Filter(response='hp')
    Adc()
    Dac()
    Demod()
    Circulator()
    Isolator()
    VGA()



Labels are placed in the center of the element. The generic `Square` and `Circle` elements can be used with a label to define other operations. For example, an integrator
may be created using:

.. jupyter-execute::

    dsp.Square().label(r'$\int$')
