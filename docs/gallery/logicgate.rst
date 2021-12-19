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

    d = schemdraw.Drawing(unit=.5)
    d += (S := logic.Xor().label('S', 'right'))
    d += (A := logic.Dot().at(S.in1))
    d += logic.Line().left().length(d.unit*2).label('A', 'left')
    d += logic.Line().left().at(S.in2)
    d += (B := logic.Dot())
    d += logic.Line().left().label('B', 'left')

    d += logic.Line().down().at(A.start).length(d.unit*3)
    d += (C := logic.And().right().anchor('in1').label('C', 'right'))
    d += logic.Line().down().at(B.start).toy(C.in2)
    d += logic.Line().to(C.in2)
    d.draw()


Full Adder
^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(unit=.5)
    d += (X1 := logic.Xor())
    d += logic.Dot()
    d += (A := logic.Dot().at(X1.in1))
    d += (Ain := logic.Line().left().length(d.unit*2).label('A', 'left'))
    d += logic.Line().left().at(X1.in2)
    d += (B := logic.Dot())
    d += logic.Line().left().label('B', 'left')

    d += logic.Line().right().at(X1.out).length(d.unit)
    d += (X2 := logic.Xor().anchor('in1'))
    d += (C := logic.Line().down().at(X2.in2).length(d.unit*2))
    d.push()
    d += logic.Dot().at(C.center)
    d += logic.Line().left().tox(Ain.end).label('C$_{in}$', 'left')
    d.pop()

    d += (A1 := logic.And().right().anchor('in1'))
    d += logic.Line().left().at(A1.in2).tox(X1.out)
    d += logic.Line().up().toy(X1.out)
    d += (A2 := logic.And().right().anchor('in1').at((A1.in1[0],A1.in2[1]-d.unit*2)))
    d += logic.Line().left().at(A2.in1).tox(A.start)
    d += logic.Line().up().toy(A.start)
    d += logic.Line().left().at(A2.in2).tox(B.start)
    d += logic.Line().up().toy(B.start)

    d += (O1 := logic.Or().right().at((A1.out[0],(A1.out[1]+A2.out[1])/2))
                    .label('C$_{out}$', 'right'))
    d += logic.Line().down().at(A1.out).toy(O1.in1)
    d += logic.Line().up().at(A2.out).toy(O1.in2)
    d += logic.Line().right().at(X2.out).tox(O1.out).label('S', 'right')
    d.draw()


J-K Flip Flop
^^^^^^^^^^^^^

Note the use of the LaTeX command **overline{Q}** in the label to draw a bar over the inverting output label.

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    # Two front gates (SR latch)
    d += (G1 := logic.Nand().anchor('in1'))
    d += logic.Line().length(d.unit/6)
    d += (Q1 := logic.Dot())
    d += logic.Line().length(d.unit/6)
    d += (Q2 := logic.Dot())
    d += logic.Line().length(d.unit/3).label('Q', 'right')
    d += (G2 := logic.Nand().anchor('in1').at((G1.in1[0],G1.in1[1]-2.5)))
    d += logic.Line().length(d.unit/6)
    d += (Qb := logic.Dot())
    d += logic.Line().length(d.unit/3)
    d += (Qb2 := logic.Dot())
    d += logic.Line().length(d.unit/6).label('$\overline{Q}$', 'right')
    d += (S1 := logic.Line().up().at(G2.in1).length(d.unit/6))
    d += logic.Line().down().at(Q1.start).length(d.unit/6)
    d += logic.Line().to(S1.end)
    d += (R1 := logic.Line().down().at(G1.in2).length(d.unit/6))
    d += logic.Line().up().at(Qb.start).length(d.unit/6)
    d += logic.Line().to(R1.end)

    # Two back gates
    d += logic.Line().left().at(G1.in1).length(d.unit/6)
    d += (J := logic.Nand(inputs=3).anchor('out').reverse())
    d += logic.Line().up().at(J.in3).length(d.unit/6)
    d += logic.Line().right().tox(Qb2.start)
    d += logic.Line().down().toy(Qb2.start)
    d += logic.Line().left().at(J.in2).length(d.unit/4).label('J', 'left')
    d += logic.Line().left().at(G2.in2).length(d.unit/6)
    d += (K := logic.Nand(inputs=3).reverse().anchor('out'))
    d += logic.Line().down().at(K.in1).length(d.unit/6)
    d += logic.Line().right().tox(Q2.start)
    d += logic.Line().up().toy(Q2.start)
    d += logic.Line().left().at(K.in2).length(d.unit/4).label('K', 'left')
    d += (C := logic.Line().down().at(J.in1).toy(K.in3))
    d += logic.Dot().at(C.center)
    d += logic.Line().left().at(C.center).length(d.unit/4).label('CLK', 'left')
    d.draw()



S-R Latch (Gates)
^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    d += logic.Line().length(d.unit/4).label('R', 'left')
    d += (G1 := logic.Nor().anchor('in1'))
    d += logic.Line().length(d.unit/4)
    d += (Q := logic.Dot())
    d += logic.Line().length(d.unit/4).label('Q', 'right')

    d += (G2 := logic.Nor().at((G1.in1[0],G1.in1[1]-2.5)).anchor('in1'))
    d += logic.Line().length(d.unit/4)
    d += (Qb := logic.Dot())
    d += logic.Line().length(d.unit/4).label('$\overline{Q}$', 'right')
    d += (S1 := logic.Line().up().at(G2.in1).length(d.unit/6))
    d += logic.Line().down().at(Q.start).length(d.unit/6)
    d += logic.Line().to(S1.end)
    d += (R1 := logic.Line().down().at(G1.in2).length(d.unit/6))
    d += logic.Line().up().at(Qb.start).length(d.unit/6)
    d += logic.Line().to(R1.end)
    d += logic.Line().left().at(G2.in2).length(d.unit/4).label('S', 'left')
    d.draw()
