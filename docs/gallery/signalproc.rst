Signal Processing
-----------------

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import dsp


Signal processing elements are in the :py:mod:`schemdraw.dsp` module.

.. code-block:: python

    from schemdraw import dsp


Various Networks
^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    d.add(dsp.Line(l=d.unit/3, label='in'))
    inpt = d.add(dsp.Dot)
    d.add(dsp.Arrow(l=d.unit/3))
    delay = d.add(dsp.Box(w=2, h=2, label='Delay\nT', anchor='W'))
    d.add(dsp.Arrow('right', l=d.unit/2, xy=delay.E))
    sm = d.add(dsp.SumSigma)
    d.add(dsp.Arrow(xy=sm.E, l=d.unit/2))
    intg = d.add(dsp.Box(w=2, h=2, label='$\int$', anchor='W'))
    d.add(dsp.Line('r', xy=intg.E, l=d.unit/2))
    d.add(dsp.Arrowhead(label='out'))
    d.add(dsp.Line('down', xy=inpt.center, l=d.unit/2))
    d.add(dsp.Line('right', tox=sm.S))
    d.add(dsp.Line('up', toy=sm.S))
    d.add(dsp.Arrowhead(botlabel='+'))
    d.draw()


.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(fontsize=14)
    d.add(dsp.Line(l=d.unit/2, label='F(s)'))
    d.push()
    d.add(dsp.Dot)
    d.add(dsp.Line('up', l=d.unit/2))
    d.add(dsp.Arrow('right', l=d.unit/2))
    h1 = d.add(dsp.Box(w=2, h=2, label='$H_1(s)$', anchor='W'))
    d.pop()
    d.add(dsp.Line('down', l=d.unit/2))
    d.add(dsp.Arrow('right', l=d.unit/2))
    h2 = d.add(dsp.Box(w=2, h=2, label='$H_2(s)$', anchor='W'))
    sm = d.add(dsp.SumSigma('right', xy=[h1.E[0] + d.unit/2, 0], anchor='center'))
    d.add(dsp.Line('right', xy=h1.E, tox=sm.N))
    d.add(dsp.Arrow('down', toy=sm.N))
    d.add(dsp.Line('right', xy=h2.E, tox=sm.S))
    d.add(dsp.Arrow('up', toy=sm.S))
    d.add(dsp.Line('right', xy=sm.E, l=d.unit/3))
    d.add(dsp.Arrowhead(label='Y(s)'))
    d.draw()


Superheterodyne Receiver
^^^^^^^^^^^^^^^^^^^^^^^^

`Source <https://www.electronicdesign.com/adc/high-speed-rf-sampling-adc-boosts-bandwidth-dynamic-range>`_.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(fontsize=12)
    d.add(dsp.Antenna)
    d.add(dsp.Line('right', l=d.unit/4))
    filt1 = d.add(dsp.Filter(response='bp', botlabel='RF filter\n#1', anchor='W', lblofst=.2, fill='thistle'))
    d.add(dsp.Line(xy=filt1.E, l=d.unit/4))
    d.add(dsp.Amp(label='LNA', fill='lightblue'))
    d.add(dsp.Line(l=d.unit/4))
    filt2 = d.add(dsp.Filter(response='bp', botlabel='RF filter\n#2', anchor='W', lblofst=.2, fill='thistle'))
    d.add(dsp.Line('right', xy=filt2.E, l=d.unit/3))
    mix = d.add(dsp.Mixer(label='Mixer', fill='navajowhite'))
    d.add(dsp.Line('down', xy=mix.S, l=d.unit/3))
    d.add(dsp.Oscillator('right', rgtlabel='Local\nOscillator', lblofst=.2, anchor='N', fill='navajowhite'))
    d.add(dsp.Line('right', xy=mix.E, l=d.unit/3))
    filtIF = d.add(dsp.Filter(response='bp', anchor='W', botlabel='IF filter', lblofst=.2, fill='thistle'))
    d.add(dsp.Line('right', xy=filtIF.E, l=d.unit/4))
    d.add(dsp.Amp(label='IF\namplifier', fill='lightblue'))
    d.add(dsp.Line(l=d.unit/4))
    demod = d.add(dsp.Demod(anchor='W', botlabel='Demodulator', lblofst=.2, fill='navajowhite'))
    d.add(dsp.Arrow('right', xy=demod.E, l=d.unit/3))
    d.draw()

Direct Conversion Receiver
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    d.add(dsp.Antenna)
    d.add(dsp.Arrow('right', l=d.unit/2, botlabel='$f_{RF}$'))
    d.add(dsp.Amp(label='LNA'))
    d.add(dsp.Line('right', l=d.unit/5))
    d.add(dsp.Dot)
    d.push()
    d.add(dsp.Line(l=d.unit/4))
    mix1 = d.add(dsp.Mixer(label='Mixer', lblofst=0))
    d.add(dsp.Arrow(l=d.unit/2))
    lpf1 = d.add(dsp.Filter(response='lp', botlabel='LPF', lblofst=.2))
    d.add(dsp.Line(l=d.unit/6))
    adc1 = d.add(dsp.Adc(label='ADC'))
    d.add(dsp.Arrow(l=d.unit/3))
    dsp1 = d.add(dsp.Ic(pins=[dsp.IcPin(side='L'), dsp.IcPin(side='L'), dsp.IcPin(side='R')],
                        size=(2.75, 5), leadlen=0, anchor='inL2', label='DSP'))
    d.add(dsp.Arrow(xy=dsp1.inR1, l=d.unit/3))
    d.pop()

    d.add(dsp.Line('down', toy=dsp1.inL1))
    d.add(dsp.Arrow('right', tox=mix1.W))
    mix2 = d.add(dsp.Mixer(label='Mixer', lblofst=0))
    d.add(dsp.Arrow(tox=lpf1.W))
    d.add(dsp.Filter(response='lp', botlabel='LPF', lblofst=.2))
    d.add(dsp.Line(tox=adc1.W))
    d.add(dsp.Adc(label='ADC'))
    d.add(dsp.Arrow(to=dsp1.inL1))

    d.add(dsp.Arrowhead(xy=mix1.S, d='up'))
    d.add(dsp.Line('down', xy=mix1.S, l=d.unit/6))
    d.add(dsp.Line('left', l=d.unit*1.25))
    d.add(dsp.Line('down', l=d.unit*.75))
    flo = d.add(dsp.Dot(lftlabel='$f_{LO}$'))
    d.push()
    d.add(dsp.Line('down', l=d.unit/5))
    d.add(dsp.Oscillator('right', rgtlabel='LO', anchor='N', lblofst=.15))
    d.pop()
    d.add(dsp.Arrowhead('up', xy=mix2.S))
    d.add(dsp.Line('down', xy=mix2.S, l=d.unit/4))
    b1 = d.add(dsp.Square('right', label='90°', anchor='N'))
    d.add(dsp.Arrowhead('right', xy=b1.W))
    d.add(dsp.Line('left', xy=b1.W, l=d.unit/4))
    d.add(dsp.Line('up', toy=flo.center))
    d.add(dsp.Line('left', tox=flo.center))
    d.draw()


Digital Filter
^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=1, fontsize=14)
    d.add(dsp.Line(lftlabel='x[n]', l=d.unit*2))
    d.add(dsp.Dot)

    d.push()
    d.add(dsp.Line('right'))
    d.add(dsp.Amp(botlabel='$b_0$'))
    d.add(dsp.ARROW)
    s0 = d.add(dsp.Sum(anchor='W'))
    d.pop()

    d.add(dsp.Arrow('down'))
    z1 = d.add(dsp.Square(label='$z^{-1}$'))
    d.add(dsp.Line(l=d.unit/2))
    d.add(dsp.DOT)

    d.push()
    d.add(dsp.Line('right'))
    d.add(dsp.Amp(botlabel='$b_1$'))
    d.add(dsp.Arrow)
    s1 = d.add(dsp.Sum(anchor='W'))
    d.pop()

    d.add(dsp.Arrow('down', l=d.unit*.75))
    d.add(dsp.Square(label='$z^{-1}$'))
    d.add(dsp.Line(l=d.unit*.75))
    d.add(dsp.Line('right'))
    d.add(dsp.Amp(botlabel='$b_2$'))
    d.add(dsp.Arrow)
    s2 = d.add(dsp.Sum(anchor='W'))

    d.add(dsp.Arrow('up', xy=s2.N, toy=s1.S))
    d.add(dsp.Arrow('up', xy=s1.N, toy=s0.S))

    d.add(dsp.LineDot('right', xy=s0.E, l=d.unit*2.75))
    d.push()
    d.add(dsp.Arrow('right', rgtlabel='y[n]'))
    d.pop()
    d.add(dsp.Arrow('down'))
    d.add(dsp.Square(label='$z^{-1}$'))
    d.add(dsp.Line(l=d.unit/2))
    d.add(dsp.Dot)
    d.push()
    d.add(dsp.Line('left'))
    a1 = d.add(dsp.Amp(botlabel='$-a_1$'))
    d.add(dsp.Arrow(xy=a1.out, tox=s1.E))
    d.pop()

    d.add(dsp.Arrow('down', l=d.unit*.75))
    d.add(dsp.Square(label='$z^{-1}$'))
    d.add(dsp.Line(l=d.unit*.75))
    d.add(dsp.Line('left'))
    a1 = d.add(dsp.Amp(botlabel='$-a_2$'))
    d.add(dsp.Arrow(xy=a1.out, tox=s2.E))
    d.draw()
