Logic Gates
-----------    

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import logic


Logic gate definitions are in the :py:mod:`schemdraw.logic` module. Here it was imported with

.. code-block:: python

    from schemdraw import logic


Half Adder
^^^^^^^^^^

Notice the half and full adders set the drawing unit to 0.5 so the lines aren't quite as long and look better with logic gates.

.. jupyter-execute::
    :code-below:

    d = schemdraw.Drawing(unit=.5)
    S = d.add(logic.Xor(rgtlabel='$S$'))
    A = d.add(logic.Dot(xy=S.in1))
    d.add(logic.Line('left', l=d.unit*2, lftlabel='$A$'))
    d.add(logic.Line('left', xy=S.in2))
    B = d.add(logic.Dot)
    d.add(logic.Line('left', lftlabel='$B$'))

    d.add(logic.Line('down', xy=A.start, l=d.unit*3))
    C = d.add(logic.And('right', anchor='in1', rgtlabel='$C$'))
    d.add(logic.Line('down', xy=B.start, toy=C.in2))
    d.add(logic.Line(to=C.in2))
    d.draw()


Full Adder
^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing(unit=.5)
    X1 = d.add(logic.Xor)
    d.add(logic.Dot)
    A = d.add(logic.Dot(xy=X1.in1))
    Ain = d.add(logic.Line('left', l=d.unit*2, lftlabel='$A$'))
    d.add(logic.Line('left', xy=X1.in2))
    B = d.add(logic.Dot)
    d.add(logic.Line('left', lftlabel='$B$'))

    d.add(logic.Line('right', xy=X1.out, l=d.unit))
    X2 = d.add(logic.Xor(anchor='in1'))
    C = d.add(logic.Line('down', xy=X2.in2, l=d.unit*2))
    d.push()
    d.add(logic.Dot(xy=C.center))
    d.add(logic.Line('left', tox=Ain.end, lftlabel='$C_{in}$'))
    d.pop()

    A1 = d.add(logic.And('right', anchor='in1'))
    d.add(logic.Line('left', xy=A1.in2, tox=X1.out))
    d.add(logic.Line('up', toy=X1.out))
    A2 = d.add(logic.And('right', anchor='in1', xy=[A1.in1[0],A1.in2[1]-d.unit*2]))
    d.add(logic.Line('left', xy=A2.in1, tox=A.start))
    d.add(logic.Line('up', toy=A.start))
    d.add(logic.Line('left', xy=A2.in2, tox=B.start))
    d.add(logic.Line('up', toy=B.start))

    O1 = d.add(logic.Or('right', xy=[A1.out[0],(A1.out[1]+A2.out[1])/2], rgtlabel='$C_{out}$'))
    d.add(logic.Line('down', xy=A1.out, toy=O1.in1))
    d.add(logic.Line('up', xy=A2.out, toy=O1.in2))
    d.add(logic.Line('right', xy=X2.out, tox=O1.out, rgtlabel='$S$'))
    d.draw()


J-K Flip Flop
^^^^^^^^^^^^^

Note the use of the LaTeX command **overline{Q}** in the label to draw a bar over the inverting output label.

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    # Two front gates (SR latch)
    G1 = d.add(logic.Nand(anchor='in1'))
    d.add(logic.Line(l=d.unit/6))
    Q1 = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/6))
    Q2 = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/3, rgtlabel='$Q$'))
    G2 = d.add(logic.Nand(anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5]))
    d.add(logic.Line(l=d.unit/6))
    Qb = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/3))
    Qb2 = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/6, rgtlabel='$\overline{Q}$'))
    S1 = d.add(logic.Line(xy=G2.in1, d='up', l=d.unit/6))
    d.add(logic.Line('down', xy=Q1.start, l=d.unit/6))
    d.add(logic.Line(to=S1.end))
    R1 = d.add(logic.Line('down', xy=G1.in2, l=d.unit/6))
    d.add(logic.Line('up', xy=Qb.start, l=d.unit/6))
    d.add(logic.Line(to=R1.end))

    # Two back gates
    d.add(logic.Line('left', xy=G1.in1, l=d.unit/6))
    J = d.add(logic.Nand(inputs=3, anchor='out', reverse=True))
    d.add(logic.Line('up', xy=J.in3, l=d.unit/6))
    d.add(logic.Line('right', tox=Qb2.start))
    d.add(logic.Line('down', toy=Qb2.start))
    d.add(logic.Line('left', xy=J.in2, l=d.unit/4, lftlabel='$J$'))
    d.add(logic.Line('left', xy=G2.in2, l=d.unit/6))
    K = d.add(logic.Nand(inputs=3, anchor='out', reverse=True))
    d.add(logic.Line('down', xy=K.in1, l=d.unit/6))
    d.add(logic.Line('right', tox=Q2.start))
    d.add(logic.Line('up', toy=Q2.start))
    d.add(logic.Line('left', xy=K.in2, l=d.unit/4, lftlabel='$K$'))
    C = d.add(logic.Line('down', xy=J.in1, toy=K.in3))
    d.add(logic.Dot(xy=C.center))
    d.add(logic.Line('left', xy=C.center, l=d.unit/4, lftlabel='$CLK$'))
    d.draw()



S-R Latch (Gates)
^^^^^^^^^^^^^^^^^

.. jupyter-execute::
    :code-below:
    
    d = schemdraw.Drawing()
    d.add(logic.Line(l=d.unit/4, lftlabel='$R$'))
    G1 = d.add(logic.Nor(anchor='in1'))
    d.add(logic.Line(l=d.unit/4))
    Q = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/4, rgtlabel='$Q$'))

    G2 = d.add(logic.Nor(anchor='in1', xy=[G1.in1[0],G1.in1[1]-2.5]))
    d.add(logic.Line(l=d.unit/4))
    Qb = d.add(logic.Dot)
    d.add(logic.Line(l=d.unit/4, rgtlabel='$\overline{Q}$'))
    S1 = d.add(logic.Line('up', xy=G2.in1, l=d.unit/6))
    d.add(logic.Line('down', xy=Q.start, l=d.unit/6))
    d.add(logic.Line(to=S1.end))
    R1 = d.add(logic.Line('down', xy=G1.in2, l=d.unit/6))
    d.add(logic.Line('up', xy=Qb.start, l=d.unit/6))
    d.add(logic.Line(to=R1.end))
    d.add(logic.Line('left', xy=G2.in2, l=d.unit/4, lftlabel='$S$'))
    d.draw()
