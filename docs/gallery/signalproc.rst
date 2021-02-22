Signal Processing
-----------------

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
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
    
    d = schemdraw.Drawing()
    d += dsp.Line().length(d.unit/3).label('in')
    d += (inpt := dsp.Dot())
    d += dsp.Arrow().length(d.unit/3)
    d += (delay := dsp.Box(w=2, h=2).anchor('W').label('Delay\nT'))
    d += dsp.Arrow().right().length(d.unit/2).at(delay.E)
    d += (sm := dsp.SumSigma())
    d += dsp.Arrow().at(sm.E).length(d.unit/2)
    d += (intg := dsp.Box(w=2, h=2).anchor('W').label('$\int$'))
    d += dsp.Arrow().right().at(intg.E).length(d.unit/2).label('out', loc='right')
    d += dsp.Line().down().at(inpt.center).length(d.unit/2)
    d += dsp.Line().right().tox(sm.S)
    d += dsp.Arrow().up().toy(sm.S).label('+', loc='bot')
    d.draw()


.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(fontsize=14)
    d += dsp.Line().length(d.unit/2).label('F(s)')
    d.push()
    d += dsp.Dot()
    d += dsp.Line().up().length(d.unit/2)
    d += dsp.Arrow().right().length(d.unit/2)
    d += (h1 := dsp.Box(w=2, h=2).anchor('W').label('$H_1(s)$'))
    d.pop()
    d += dsp.Line().down().length(d.unit/2)
    d += dsp.Arrow().right().length(d.unit/2)
    d += (h2 := dsp.Box(w=2, h=2).anchor('W').label('$H_2(s)$'))
    d += (sm := dsp.SumSigma().right().at((h1.E[0] + d.unit/2, 0)).anchor('center'))
    d += dsp.Line().right().at(h1.E).tox(sm.N)
    d += dsp.Arrow().down().toy(sm.N)
    d += dsp.Line().right().at(h2.E).tox(sm.S)
    d += dsp.Arrow().up().toy(sm.S)
    d += dsp.Arrow().right().at(sm.E).length(d.unit/3).label('Y(s)', 'right')
    d.draw()


Superheterodyne Receiver
^^^^^^^^^^^^^^^^^^^^^^^^

`Source <https://www.electronicdesign.com/adc/high-speed-rf-sampling-adc-boosts-bandwidth-dynamic-range>`_.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(fontsize=12)
    d += dsp.Antenna()
    d += dsp.Line().right().length(d.unit/4)
    d += (filt1 := dsp.Filter(response='bp').fill('thistle').anchor('W').label('RF filter\n#1', 'bottom', ofst=.2))
    d += dsp.Line().at(filt1.E).length(d.unit/4)
    d += dsp.Amp().fill('lightblue').label('LNA')
    d += dsp.Line().length(d.unit/4)
    d += (filt2 := dsp.Filter(response='bp').anchor('W').fill('thistle').label('RF filter\n#2', 'bottom', ofst=.2))
    d += dsp.Line().right().at(filt2.E).length(d.unit/3)
    d += (mix := dsp.Mixer().fill('navajowhite').label('Mixer'))
    d += dsp.Line().down().at(mix.S).length(d.unit/3)
    d += dsp.Oscillator().right().anchor('N').fill('navajowhite').label('Local\nOscillator', 'right', ofst=.2)
    d += dsp.Line().right().at(mix.E).length(d.unit/3)
    d += (filtIF := dsp.Filter(response='bp').anchor('W').fill('thistle').label('IF filter', 'bottom', ofst=.2))
    d += dsp.Line().right().at(filtIF.E).length(d.unit/4)
    d += dsp.Amp().fill('lightblue').label('IF\namplifier')
    d += dsp.Line().length(d.unit/4)
    d += (demod := dsp.Demod().anchor('W').fill('navajowhite').label('Demodulator', 'bottom', ofst=.2))
    d += dsp.Arrow().right().at(demod.E).length(d.unit/3)
    d.draw()


Direct Conversion Receiver
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing()
    d += dsp.Antenna()
    d += dsp.Arrow().right().length(d.unit/2).label('$f_{RF}$', 'bot')
    d += dsp.Amp().label('LNA')
    d += dsp.Line().right().length(d.unit/5)
    d += dsp.Dot()
    d.push()
    d += dsp.Line().length(d.unit/4)
    d += (mix1 := dsp.Mixer().label('Mixer', ofst=0))
    d += dsp.Arrow().length(d.unit/2)
    d += (lpf1 := dsp.Filter(response='lp').label('LPF', 'bot', ofst=.2))
    d += dsp.Line().length(d.unit/6)
    d += (adc1 := dsp.Adc().label('ADC'))
    d += dsp.Arrow().length(d.unit/3)
    d += (dsp1 := dsp.Ic(pins=[dsp.IcPin(side='L'), dsp.IcPin(side='L'), dsp.IcPin(side='R')],
                        size=(2.75, 5), leadlen=0).anchor('inL2').label('DSP'))
    d += dsp.Arrow().at(dsp1.inR1).length(d.unit/3)
    d.pop()

    d += dsp.Line().down().toy(dsp1.inL1)
    d += dsp.Arrow().right().tox(mix1.W)
    d += (mix2 := dsp.Mixer().label('Mixer', ofst=0))
    d += dsp.Arrow().tox(lpf1.W)
    d += dsp.Filter(response='lp').label('LPF', 'bot', ofst=.2)
    d += dsp.Line().tox(adc1.W)
    d += dsp.Adc().label('ADC')
    d += dsp.Arrow().to(dsp1.inL1)

    d += dsp.Arrow().down().reverse().at(mix1.S).length(d.unit/6)
    d += dsp.Line().left().length(d.unit*1.25)
    d += dsp.Line().down().length(d.unit*.75)
    d += (flo := dsp.Dot().label('$f_{LO}$', 'left'))
    d.push()
    d += dsp.Line().down().length(d.unit/5)
    d += dsp.Oscillator().right().anchor('N').label('LO', 'left', ofst=.15)
    d.pop()
    d += dsp.Arrow().down().reverse().at(mix2.S).length(d.unit/4)
    d += (b1 := dsp.Square().right().label('90°').anchor('N'))
    d += dsp.Arrow().left().reverse().at(b1.W).length(d.unit/4)
    d += dsp.Line().up().toy(flo.center)
    d += dsp.Line().left().tox(flo.center)
    d.draw()


Digital Filter
^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=1, fontsize=14)
    d += dsp.LineDot().length(d.unit*2).label('x[n]', 'left')

    d.push()
    d += dsp.Line().right()
    d += dsp.Amp().label('$b_0$', 'bottom')
    d += dsp.Arrow()
    d += (s0 := dsp.Sum().anchor('W'))
    d.pop()

    d += dsp.Arrow().down()
    d += (z1 := dsp.Square(label='$z^{-1}$'))
    d += dsp.LineDot().length(d.unit/2)

    d.push()
    d += dsp.Line().right()
    d += dsp.Amp().label('$b_1$', 'bottom')
    d += dsp.Arrow()
    d += (s1 := dsp.Sum().anchor('W'))
    d.pop()

    d += dsp.Arrow().down().length(d.unit*.75)
    d += dsp.Square().label('$z^{-1}$')
    d += dsp.Line().length(d.unit*.75)
    d += dsp.Line().right()
    d += dsp.Amp().label('$b_2$', 'bottom')
    d += dsp.Arrow()
    d += (s2 := dsp.Sum().anchor('W'))

    d += dsp.Arrow().up().at(s2.N).toy(s1.S)
    d += dsp.Arrow().up().at(s1.N).toy(s0.S)

    d += dsp.LineDot().right().at(s0.E).length(d.unit*2.75)
    d.push()
    d += dsp.Arrow().right().label('y[n]', 'right')
    d.pop()
    d += dsp.Arrow().down()
    d += dsp.Square().label('$z^{-1}$')
    d += dsp.LineDot().length(d.unit/2)
    d.push()
    d += dsp.Line().left()
    d += (a1 := dsp.Amp().label('$-a_1$', 'bottom'))
    d += dsp.Arrow().at(a1.out).tox(s1.E)
    d.pop()

    d += dsp.Arrow().down().length(d.unit*.75)
    d += dsp.Square().label('$z^{-1}$')
    d += dsp.Line().length(d.unit*.75)
    d += dsp.Line().left()
    d += (a2 := dsp.Amp().label('$-a_2$', 'bottom'))
    d += dsp.Arrow().at(a2.out).tox(s2.E)
    d.draw()