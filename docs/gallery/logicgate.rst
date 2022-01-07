Digital Logic
-------------  

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import logic


Logic gate definitions are in the :py:mod:`schemdraw.logic.logic` module. Here it was imported with

.. code-block:: python

    from schemdraw import logic


Half Adder
^^^^^^^^^^

Notice the half and full adders set the drawing unit to 0.5 so the lines aren't quite as long and look better with logic gates.

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(unit=0.5)
        d += (S := logic.Xor().label('S', 'right'))
        d += logic.Line().left(d.unit*2).at(S.in1).idot().label('A', 'left')
        d += (B := logic.Line().left().at(S.in2).dot())
        d += logic.Line().left().label('B', 'left')
        d += logic.Line().down(d.unit*3).at(S.in1)
        d += (C := logic.And().right().anchor('in1').label('C', 'right'))
        d += logic.Wire('|-').at(B.end).to(C.in2)


Full Adder
^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(unit=0.5)
        d += (X1 := logic.Xor())
        d += (A := logic.Line().left(d.unit*2).at(X1.in1).idot().label('A', 'left'))
        d += (B := logic.Line().left().at(X1.in2).dot())
        d += logic.Line().left().label('B', 'left')

        d += logic.Line().right().at(X1.out).idot()
        d += (X2 := logic.Xor().anchor('in1'))
        d += (C := logic.Line().down(d.unit*2).at(X2.in2))
        d.push()
        d += logic.Dot().at(C.center)
        d += logic.Line().tox(A.end).label('C$_{in}$', 'left')
        d.pop()

        d += (A1 := logic.And().right().anchor('in1'))
        d += logic.Wire('-|').at(A1.in2).to(X1.out)
        d.move_from(A1.in2, dy=-d.unit*2)
        d += (A2 := logic.And().right().anchor('in1'))
        d += logic.Wire('-|').at(A2.in1).to(A.start)
        d += logic.Wire('-|').at(A2.in2).to(B.end)
        d.move_from(A1.out, dy=-(A1.out.y-A2.out.y)/2)
        d += (O1 := logic.Or().right().label('C$_{out}$', 'right'))
        d += logic.Line().at(A1.out).toy(O1.in1)
        d += logic.Line().at(A2.out).toy(O1.in2)
        d += logic.Line().at(X2.out).tox(O1.out).label('S', 'right')


J-K Flip Flop
^^^^^^^^^^^^^

Note the use of the LaTeX command **overline{Q}** in the label to draw a bar over the inverting output label.

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        # Two front gates (SR latch)
        d += (G1 := logic.Nand(leadout=.75).anchor('in1'))
        d += logic.Line().length(d.unit/2).label('Q', 'right')
        d.move_from(G1.in1, dy=-2.5)
        d += (G2 := logic.Nand(leadout=.75).anchor('in1'))
        d += logic.Line().length(d.unit/2).label('$\overline{Q}$', 'right')
        d += logic.Wire('N', k=.5).at(G2.in1).to(G1.out).dot()
        d += logic.Wire('N', k=.5).at(G1.in2).to(G2.out).dot()

        # Two back gates
        d += logic.Line().left(d.unit/6).at(G1.in1)
        d += (J := logic.Nand(inputs=3).anchor('out').right())
        d += logic.Wire('n', k=.5).at(J.in1).to(G2.out, dx=1).dot()
        d += logic.Line().left(d.unit/4).at(J.in2).label('J', 'left')
        d += logic.Line().left(d.unit/6).at(G2.in2)
        d += (K := logic.Nand(inputs=3).right().anchor('out'))
        d += logic.Wire('n', k=-.5).at(K.in3).to(G1.out, dx=.5).dot()
        d += logic.Line().left(d.unit/4).at(K.in2).label('K', 'left')
        d += (C := logic.Line().at(J.in3).toy(K.in1))
        d += logic.Dot().at(C.center)
        d += logic.Line().left(d.unit/4).label('CLK', 'left')


S-R Latch (Gates)
^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        d += (g1 := logic.Nor())
        d.move_from(g1.in1, dy=-2.5)
        d += (g2 := logic.Nor().anchor('in1'))
        d += (g1out := logic.Line().right(.25).at(g1.out))
        d += logic.Wire('N', k=.5).at(g2.in1).to(g1out.end).dot()
        d += (g2out := logic.Line().right(.25).at(g2.out))
        d += logic.Wire('N', k=.5).at(g1.in2).to(g2out.end).dot()
        d += logic.Line().at(g1.in1).left(.5).label('R', 'left')
        d += logic.Line().at(g2.in2).left(.5).label('S', 'left')
        d += logic.Line().at(g1.out).right(.75).label('Q', 'right')
        d += logic.Line().at(g2.out).right(.75).label('$\overline{Q}$', 'right')
