Digital Logic
-------------  

.. jupyter-execute::
    :hide-code:

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
        S = logic.Xor().label('S', 'right')
        logic.Line().left(d.unit*2).at(S.in1).idot().label('A', 'left')
        B = logic.Line().left().at(S.in2).dot()
        logic.Line().left().label('B', 'left')
        logic.Line().down(d.unit*3).at(S.in1)
        C = logic.And().right().anchor('in1').label('C', 'right')
        logic.Wire('|-').at(B.end).to(C.in2)


Full Adder
^^^^^^^^^^

.. jupyter-execute::
    :code-below:

    with schemdraw.Drawing() as d:
        d.config(unit=0.5)
        X1 = logic.Xor()
        A = logic.Line().left(d.unit*2).at(X1.in1).idot().label('A', 'left')
        B = logic.Line().left().at(X1.in2).dot()
        logic.Line().left().label('B', 'left')

        logic.Line().right().at(X1.out).idot()
        X2 = logic.Xor().anchor('in1')
        C = logic.Line().down(d.unit*2).at(X2.in2)
        d.push()
        logic.Dot().at(C.center)
        logic.Line().tox(A.end).label('C$_{in}$', 'left')
        d.pop()

        A1 = logic.And().right().anchor('in1')
        logic.Wire('-|').at(A1.in2).to(X1.out)
        d.move_from(A1.in2, dy=-d.unit*2)
        A2 = logic.And().right().anchor('in1')
        logic.Wire('-|').at(A2.in1).to(A.start)
        logic.Wire('-|').at(A2.in2).to(B.end)
        d.move_from(A1.out, dy=-(A1.out.y-A2.out.y)/2)
        O1 = logic.Or().right().label('C$_{out}$', 'right')
        logic.Line().at(A1.out).toy(O1.in1)
        logic.Line().at(A2.out).toy(O1.in2)
        logic.Line().at(X2.out).tox(O1.out).label('S', 'right')


J-K Flip Flop
^^^^^^^^^^^^^

Note the use of the LaTeX command **overline{Q}** in the label to draw a bar over the inverting output label.

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        # Two front gates (SR latch)
        G1 = logic.Nand(leadout=.75).anchor('in1')
        logic.Line().length(d.unit/2).label('Q', 'right')
        d.move_from(G1.in1, dy=-2.5)
        G2 = logic.Nand(leadout=.75).anchor('in1')
        logic.Line().length(d.unit/2).label(r'$\overline{Q}$', 'right')
        logic.Wire('N', k=.5).at(G2.in1).to(G1.out).dot()
        logic.Wire('N', k=.5).at(G1.in2).to(G2.out).dot()

        # Two back gates
        logic.Line().left(d.unit/6).at(G1.in1)
        J = logic.Nand(inputs=3).anchor('out').right()
        logic.Wire('n', k=.5).at(J.in1).to(G2.out, dx=1).dot()
        logic.Line().left(d.unit/4).at(J.in2).label('J', 'left')
        logic.Line().left(d.unit/6).at(G2.in2)
        K = logic.Nand(inputs=3).right().anchor('out')
        logic.Wire('n', k=-.5).at(K.in3).to(G1.out, dx=.5).dot()
        logic.Line().left(d.unit/4).at(K.in2).label('K', 'left')
        C = logic.Line().at(J.in3).toy(K.in1)
        logic.Dot().at(C.center)
        logic.Line().left(d.unit/4).label('CLK', 'left')


S-R Latch (Gates)
^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    with schemdraw.Drawing() as d:
        g1 = logic.Nor()
        d.move_from(g1.in1, dy=-2.5)
        g2 = logic.Nor().anchor('in1')
        g1out = logic.Line().right(.25).at(g1.out)
        logic.Wire('N', k=.5).at(g2.in1).to(g1out.end).dot()
        g2out = logic.Line().right(.25).at(g2.out)
        logic.Wire('N', k=.5).at(g1.in2).to(g2out.end).dot()
        logic.Line().at(g1.in1).left(.5).label('R', 'left')
        logic.Line().at(g2.in2).left(.5).label('S', 'left')
        logic.Line().at(g1.out).right(.75).label('Q', 'right')
        logic.Line().at(g2.out).right(.75).label(r'$\overline{Q}$', 'right')
