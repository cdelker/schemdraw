<link rel="stylesheet" href="css/codehilite.css">

## Logic Gates

Logic gates can be drawn by importing the logic module:

    :::python
    from SchemDraw import logic

Typical AND, OR, NAND, NOR, XOR, XNOR, and NOT gates with 2, 3, or 4 inputs are predefined. Anchors are defined as 'in1', 'in2', etc. for each input, and 'out' for the output.

![](img/gates.svg)

Two functions are available to generate more complicated, multi-input gates. The `andgate()` method is defined with parameters:

        inputs    : (int) number of inputs to gate.
        nand      : (bool) invert bubble on output
        inputnots : (list) list of input numbers (starting at 1) with invert bubble

and the `orgate()` method:

        inputs    : (int) number of inputs to gate.
        nor       : (bool) invert bubble on output
        xor       : (bool) exclusive-or
        inputnots : (list) list of input numbers (starting at 1) with invert bubble

As an example, the following line generates a 3-input NAND gate with one input pre-inverted.

    :::python
    logic.andgate(inputs=3, nand=True, inputnots=[1])

![](img/and_inputnot.svg)


------------------------------------------------------
[Return to SchemDraw documentation index](index.html)