Logic Gates
===========

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import logic


Logic gates can be drawn by importing the :py:mod:`logic` module:

.. code-block:: python

    from schemdraw import logic


Logic gates are shown below. Gates define anchors for `out` and `in1`, `in2`, etc.
`Buf`, `Not`, and `NotNot`, and their Schmitt-trigger counterparts, are two-terminal elements that extend leads.


.. jupyter-execute::
    :hide-code:

    def drawElements(elmlist, cols=3, dx=8, dy=2):
        d = schemdraw.Drawing(fontsize=12)
        for i, e in enumerate(elmlist):
            y = i//cols*-dy
            x = (i%cols) * dx

            eplaced = d.add(getattr(logic, e), d='right', xy=[x, y])
            eplaced.add_label(e, loc='rgt', ofst=.2, align=('left', 'center'))
        return d

    elms = ['And', 'Nand', 'Or', 'Nor', 'Xor', 'Xnor',
            'Buf', 'Not', 'NotNot', 'Tgate',
            'Schmitt', 'SchmittNot', 'SchmittAnd', 'SchmittNand']
    drawElements(elms, dx=6)



Gates with more than 2 inputs can be created using the `inputs` parameter. With more than 3 inputs, the back of the gate will extend up and down.

.. jupyter-execute::

    logic.Nand(inputs=3)


.. jupyter-execute::

    logic.Nor(inputs=4)
    

Finally, any input can be pre-inverted (active low) using the `inputnots` keyword with a list of input numbers, starting at 1 to match the anchor names, on which to add an invert bubble.


.. jupyter-execute::

    logic.Nand(inputs=3, inputnots=[1])
