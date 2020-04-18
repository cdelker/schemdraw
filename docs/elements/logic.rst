Logic Gates
===========

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import SchemDraw
    from SchemDraw import logic

    def drawElements(elm_list, n=5, dx=1, dy=2, ofst=.8, fname=None, **kwargs):
        x, y = 0, 0
        d = SchemDraw.Drawing(fontsize=12)
        for element in elm_list:
            A = d.add(element, xy=[(d.unit+1)*x+1,y], label=element['name'], **kwargs)
            x = x + dx
            if x >= n:
                x=0
                y=y-dy
        d.draw()


Logic gates can be drawn by importing the :py:mod:`logic` module:

.. code-block:: python

    from SchemDraw import logic

Typical AND, OR, NAND, NOR, XOR, XNOR, and NOT gates with 2, 3, or 4 inputs are predefined.
Anchors are defined as 'in1', 'in2', etc. for each input, and 'out' for the output.

.. jupyter-execute::
    :hide-code:

    gates = [logic.AND2, logic.NAND2, logic.OR2, logic.NOR2, logic.XOR2, logic.XNOR2,
             logic.AND3, logic.NAND3, logic.OR3, logic.NOR3, logic.XOR3, logic.XNOR3,
             logic.OR4, logic.NOR4, logic.XOR4, logic.XNOR4,             
             logic.BUF, logic.NOT, logic.NOTNOT]
    drawElements(gates, n=5, dy=2.5, lblloc='center', lblofst=.8)


Two functions are available to generate gates with higher number of inputs, including invert-bubbles on the inputs.
The :py:func:`andgate` and :py:func:`orgate` method:

.. function:: SchemDraw.logic.andgate(inputs=2, nand=False, inputnots=[])
   
   :param inputs: number of inputs
   :type inputs: int
   :param nand: add invert bubble on the output, making a NAND gate
   :type nand: bool
   :param inputnots: Input numbers (starting with 1) that have invert bubble
   :type inputnots: list
   :rtype: dict
   :returns: element definition dictionary

.. function:: SchemDraw.logic.orgate(inputs=2, nor=False, xor=False, inputnots=[])
   
   :param inputs: number of inputs
   :type inputs: int
   :param nor: add invert bubble on the output, making a NOR gate
   :type nor: bool
   :param xor: draw as exclusive-or gate
   :type xor: bool
   :param inputnots: Input numbers (starting with 1) that have invert bubble
   :type inputnots: list
   :rtype: dict
   :returns: element definition dictionary

As an example, the following line generates a 3-input NAND gate with one input pre-inverted.

.. jupyter-execute::
    
    gate = logic.andgate(inputs=3, nand=True, inputnots=[1])

.. jupyter-execute::
    :hide-code:
    
    d = SchemDraw.Drawing()
    d.add(gate)
    d.draw()