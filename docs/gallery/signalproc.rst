Signal Processing
-----------------

.. jupyter-execute::
    :hide-code:

    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import dsp


Signal processing elements are in the :py:mod:`schemdraw.dsp.dsp` module.

.. code-block:: python

    from schemdraw import dsp


Various Networks
^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        dsp.Line().length(d.unit/3).label('in')
        inpt = dsp.Dot()
        dsp.Arrow().length(d.unit/3)
        delay = dsp.Box(w=2, h=2).anchor('W').label('Delay\nT')
        dsp.Arrow().right(d.unit/2).at(delay.E)
        sm = dsp.SumSigma()
        dsp.Arrow().at(sm.E).length(d.unit/2)
        intg = dsp.Box(w=2, h=2).anchor('W').label(r'$\int$')
        dsp.Arrow().right(d.unit/2).at(intg.E).label('out', loc='right')
        dsp.Line().down(d.unit/2).at(inpt.center)
        dsp.Line().tox(sm.S)
        dsp.Arrow().toy(sm.S).label('+', loc='bot')


.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d.config(fontsize=14)
        dsp.Line().length(d.unit/2).label('F(s)').dot()
        d.push()
        dsp.Line().up(d.unit/2)
        dsp.Arrow().right(d.unit/2)
        h1 = dsp.Box(w=2, h=2).anchor('W').label('$H_1(s)$')
        d.pop()
        dsp.Line().down(d.unit/2)
        dsp.Arrow().right(d.unit/2)
        h2 = dsp.Box(w=2, h=2).anchor('W').label('$H_2(s)$')
        sm = dsp.SumSigma().right().at((h1.E[0] + d.unit/2, 0)).anchor('center')
        dsp.Line().at(h1.E).tox(sm.N)
        dsp.Arrow().toy(sm.N)
        dsp.Line().at(h2.E).tox(sm.S)
        dsp.Arrow().toy(sm.S)
        dsp.Arrow().right(d.unit/3).at(sm.E).label('Y(s)', 'right')


Superheterodyne Receiver
^^^^^^^^^^^^^^^^^^^^^^^^

`Source <https://www.electronicdesign.com/adc/high-speed-rf-sampling-adc-boosts-bandwidth-dynamic-range>`_.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(fontsize=12)
        dsp.Antenna()
        dsp.Line().right(d.unit/4)
        dsp.Filter(response='bp').fill('thistle').anchor('W').label('RF filter\n#1', 'bottom', ofst=.2)
        dsp.Line().length(d.unit/4)
        dsp.Amp().fill('lightblue').label('LNA')
        dsp.Line().length(d.unit/4)
        dsp.Filter(response='bp').anchor('W').fill('thistle').label('RF filter\n#2', 'bottom', ofst=.2)
        dsp.Line().length(d.unit/3)
        mix = dsp.Mixer().fill('navajowhite').label('Mixer')
        dsp.Line().at(mix.S).down(d.unit/3)
        dsp.Oscillator().right().anchor('N').fill('navajowhite').label('Local\nOscillator', 'right', ofst=.2)
        dsp.Line().at(mix.E).right(d.unit/3)
        dsp.Filter(response='bp').anchor('W').fill('thistle').label('IF filter', 'bottom', ofst=.2)
        dsp.Line().right(d.unit/4)
        dsp.Amp().fill('lightblue').label('IF\namplifier')
        dsp.Line().length(d.unit/4)
        dsp.Demod().anchor('W').fill('navajowhite').label('Demodulator', 'bottom', ofst=.2)
        dsp.Arrow().right(d.unit/3)


Direct Conversion Receiver
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        dsp.Antenna()
        dsp.Arrow().right(d.unit/2).label('$f_{RF}$', 'bot')
        dsp.Amp().label('LNA')
        dsp.Line().right(d.unit/5).dot()
        d.push()
        dsp.Line().length(d.unit/4)
        mix1 = dsp.Mixer().label('Mixer', ofst=0)
        dsp.Arrow().length(d.unit/2)
        lpf1 = dsp.Filter(response='lp').label('LPF', 'bot', ofst=.2)
        dsp.Line().length(d.unit/6)
        adc1 = dsp.Adc().label('ADC')
        dsp.Arrow().length(d.unit/3)
        dsp1 = dsp.Ic(pins=[dsp.IcPin(side='L'), dsp.IcPin(side='L'), dsp.IcPin(side='R')],
                      size=(2.75, 5), leadlen=0).anchor('inL2').label('DSP')
        dsp.Arrow().at(dsp1.inR1).length(d.unit/3)
        d.pop()

        dsp.Line().toy(dsp1.inL1)
        dsp.Arrow().tox(mix1.W)
        mix2 = dsp.Mixer().label('Mixer', ofst=0)
        dsp.Arrow().tox(lpf1.W)
        dsp.Filter(response='lp').label('LPF', 'bot', ofst=.2)
        dsp.Line().tox(adc1.W)
        dsp.Adc().label('ADC')
        dsp.Arrow().to(dsp1.inL1)

        dsp.Arrow().down(d.unit/6).reverse().at(mix1.S)
        dsp.Line().left(d.unit*1.25)
        dsp.Line().down(d.unit*.75)
        flo = dsp.Dot().label('$f_{LO}$', 'left')
        d.push()
        dsp.Line().down(d.unit/5)
        dsp.Oscillator().right().anchor('N').label('LO', 'left', ofst=.15)
        d.pop()
        dsp.Arrow().down(d.unit/4).reverse().at(mix2.S)
        b1 = dsp.Square().right().label('90°').anchor('N')
        dsp.Arrow().left(d.unit/4).reverse().at(b1.W)
        dsp.Line().toy(flo.center)
        dsp.Line().tox(flo.center)


Digital Filter
^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(unit=1, fontsize=14)
        dsp.Line().length(d.unit*2).label('x[n]', 'left').dot()

        d.push()
        dsp.Line().right()
        dsp.Amp().label('$b_0$', 'bottom')
        dsp.Arrow()
        s0 = dsp.Sum().anchor('W')
        d.pop()

        dsp.Arrow().down()
        z1 = dsp.Square(label='$z^{-1}$')
        dsp.Line().length(d.unit/2).dot()

        d.push()
        dsp.Line().right()
        dsp.Amp().label('$b_1$', 'bottom')
        dsp.Arrow()
        s1 = dsp.Sum().anchor('W')
        d.pop()

        dsp.Arrow().down(d.unit*.75)
        dsp.Square().label('$z^{-1}$')
        dsp.Line().length(d.unit*.75)
        dsp.Line().right()
        dsp.Amp().label('$b_2$', 'bottom')
        dsp.Arrow()
        s2 = dsp.Sum().anchor('W')

        dsp.Arrow().at(s2.N).toy(s1.S)
        dsp.Arrow().at(s1.N).toy(s0.S)

        dsp.Line().right(d.unit*2.75).at(s0.E).dot()
        dsp.Arrow().right().label('y[n]', 'right').hold()
        dsp.Arrow().down()
        dsp.Square().label('$z^{-1}$')
        dsp.Line().length(d.unit/2).dot()
        d.push()
        dsp.Line().left()
        a1 = dsp.Amp().label('$-a_1$', 'bottom')
        dsp.Arrow().at(a1.out).tox(s1.E)
        d.pop()

        dsp.Arrow().down(d.unit*.75)
        dsp.Square().label('$z^{-1}$')
        dsp.Line().length(d.unit*.75)
        dsp.Line().left()
        a2 = dsp.Amp().label('$-a_2$', 'bottom')
        dsp.Arrow().at(a2.out).tox(s2.E)
