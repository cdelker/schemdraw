Digital Logic
=============

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import logic


Logic gates can be drawn by importing the :py:mod:`schemdraw.logic.logic` module:

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
            
            d += getattr(logic, e)().right().at((x,y)).label(e, loc='right', ofst=.2, halign='left', valign='center')
        return d

    elms = ['And', 'Nand', 'Or', 'Nor', 'Xor', 'Xnor',
            'Buf', 'Not', 'NotNot', 'Tgate', 'Tristate',
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


Logic Parser
------------

Logic trees can also be created from a string logic expression such as "(a and b) or c" using using :py:func:`schemdraw.parsing.logic_parser.logicparse`.
The logic parser requires the `pyparsing <https://pyparsing-docs.readthedocs.io/en/latest/>`_ module.

Examples:

.. jupyter-execute::

    from schemdraw.parsing import logicparse
    logicparse('not ((w and x) or (y and z))', outlabel=r'$\overline{Q}$')
    
.. jupyter-execute::

    logicparse('((a xor b) and (b or c) and (d or e)) or ((w and x) or (y and z))')


Logicparse understands spelled-out logic functions "and", "or", "nand", "nor", "xor", "xnor", "not", but also common symbols such as "+", "&", "⊕" representing "or", "and", and "xor".

.. jupyter-execute::

    logicparse('¬ (a ∨ b) & (c ⊻ d)')  # Using symbols
  

Use the `gateH` and `gateW` parameters to adjust how gates line up:

.. jupyter-execute::

    logicparse('(not a) and b or c', gateH=.5)


Truth Tables
------------

Simple tables can be drawn using the :py:class:`schemdraw.logic.table.Table` class. This class is included in the logic module as its primary purpose was for drawing logical truth tables.

The tables are defined using typical Markdown syntax. The `colfmt` parameter works like the LaTeX tabular environment parameter for defining lines to draw between table columns: "cc|c" draws three centered columns, with a vertical line before the last column.
Each column must be specified with a 'c', 'r', or 'l' for center, right, or left justification
Two pipes (`||`), or a double pipe character (`ǁ`) draw a double bar between columns.
Row lines are added to the table string itself, with either `---` or `===` in the row.

.. jupyter-execute::

    table = '''
     A | B | C
    ---|---|---
     0 | 0 | 0
     0 | 1 | 0
     1 | 0 | 0
     1 | 1 | 1
    '''    
    logic.Table(table, colfmt='cc||c')


Karnaugh Maps
-------------

Karnaugh Maps, or K-Maps, are useful for simplifying a logical truth table into the smallest number of gates. Schemdraw can draw K-Maps, with 2, 3, or 4 input variables, using the :py:class:`schemdraw.logic.kmap.Kmap` class.

.. jupyter-execute::

    logic.Kmap(names='ABCD')

The `names` parameter must be a string with 2, 3, or 4 characters, each defining the name of one input variable.
The `truthtable` parameter contains a list of tuples defining the logic values to display in the map. The first `len(names)` elements are 0's and 1's defining the position of the cell, and the last element is the string to display in that cell.
The `default` parameter is a string to show in each cell of the K-Map when that cell is undefined in the `truthtable`.

For example, this 2x2 K-Map has a '1' in the 01 position, and 0's elsewhere:

.. jupyter-execute::

    logic.Kmap(names='AB', truthtable=[('01', '1')])

K-Maps are typically used by grouping sets of 1's together. These groupings can be drawn using the `groups` parameter. The keys of the `groups` dictionary define which cells to group together, and the values of the dictionary define style parameters for the circle around the group.
Each key must be a string of length `len(names)`, with either a `0`, `1`, or `.` in each position. As an example, with `names='ABCD'`, a group key of `"1..."` will place a circle around all cells where A=1. Or `".00."` draws a circle around all cells where B and C are both 0. Groups will automatically "wrap" around the edges.
Parameters of the style dictionary include `color`, `fill`, `lw`, and `ls`.

.. jupyter-execute::

    logic.Kmap(names='ABCD',
               truthtable=[('1100', '1'),
                           ('1101', '1'),
                           ('1111', '1'),
                           ('1110', '1'),
                           ('0101', '1'),
                           ('0111', 'X'),
                           ('1101', '1'),
                           ('1111', '1'),
                           ('0000', '1'),
                           ('1000', '1')],
               groups={'11..': {'color': 'red', 'fill': '#ff000033'},
                       '.1.1': {'color': 'blue', 'fill': '#0000ff33'},
                       '.000': {'color': 'green', 'fill': '#00ff0033'}})

.. note::

    `Kmap` and `Table` are both Elements, meaning they may be added to a
    schemdraw `Drawing` with other schematic components.
    To save a standalone `Kmap` or `Table` to an image file, first add it to a drawing, and
    save the drawing:

        .. code-block:: python

            with schemdraw.Drawing(file='truthtable.svg'):
                logic.Table(table, colfmt='cc||c')
