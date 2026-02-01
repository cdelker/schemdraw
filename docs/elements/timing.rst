Timing Diagrams
===============

.. jupyter-execute::
    :hide-code:

    import schemdraw
    from schemdraw import logic
    schemdraw.use('svg')


Digital timing diagrams may be drawn using the :py:class:`schemdraw.logic.timing.TimingDiagram` Element in the :py:mod:`schemdraw.logic` module.
Bit Field diagrams may be drawn using :py:class:`schemdraw.logic.bitfield.BitField`.

Timing diagrams and bit fields are set up using the WaveJSON syntax used by the `WaveDrom <https://wavedrom.com/>`_ JavaScript application.

Timing Diagrams
---------------

.. code-block:: python

    from schemdraw import logic


.. jupyter-execute::

    logic.TimingDiagram(
        {'signal': [
            {'name': 'A', 'wave': '0..1..01.'},
            {'name': 'B', 'wave': '101..0...'}]})

The input is a dictionary containing a `signal`, which is a list of each wave to show in the diagram. Each signal is a dictionary which must contain a `name` and `wave`.
An empty dictionary leaves a blank row in the diagram.

Every character in the `wave` specifies the state of the wave for one period. A dot `.` means the previous state is repeated.
Wave characters 'n' and 'p' specify clock signals, and 'N', and 'P' draw clocks with arrows.
'1' and '0' are used to define high and low signals. '2' draws a data block, and '3' through '9' draw data filled with a color. 'x' draws a don't-care or undefined data state.

Data blocks can be labeled by adding a 'data' item to the wave's dictionary.

This example shows the different wave sections:

.. jupyter-execute::

    logic.TimingDiagram(
        {'signal': [
            {'name': 'clock n', 'wave': 'n......'},
            {'name': 'clock p', 'wave': 'p......'},
            {'name': 'clock N', 'wave': 'N......'},
            {'name': 'clock P', 'wave': 'P......'},
            {},
            {'name': '1s and 0s', 'wave': '0.1.01.'},
            {'name': 'data', 'wave': '2..=.2.'},  # '=' is the same as '2'
            {'name': 'data named', 'wave': '3.4.6..', 'data': ['A', 'B', 'C']},
            {'name': 'dont care', 'wave': 'xx..x..'},
            {},
            {'name': 'high z', 'wave': 'z.10.z.'},
            {'name': 'pull up/down', 'wave': '0u..d.1'},
        ]})


Putting them together in a more realistic example:

.. jupyter-execute::

    logic.TimingDiagram(
        {'signal': [
            {'name': 'clk', 'wave': 'P......'},
            {'name': 'bus', 'wave': 'x.==.=x', 'data': ['head', 'body', 'tail']},
            {'name': 'wire', 'wave': '0.1..0.'}]})


The `config` key, containing a dictionary with `hscale`, may be used to change the width of one period in the diagram:

.. jupyter-execute::
    :emphasize-lines: 6

    logic.TimingDiagram(
        {'signal': [
            {'name': 'clk', 'wave': 'P......'},
            {'name': 'bus', 'wave': 'x.==.=x', 'data': ['head', 'body', 'tail']},
            {'name': 'wire', 'wave': '0.1..0.'}],
         'config': {'hscale': 2}})


Signals may also be nested into different groups:

.. jupyter-execute::

    logic.TimingDiagram(
        {'signal': ['Group', 
          ['Set 1',
            {'name': 'A', 'wave': '0..1..01.'},
            {'name': 'B', 'wave': '101..0...'}],
          ['Set 2',
            {'name': 'C', 'wave': '0..1..01.'},
            {'name': 'D', 'wave': '101..0...'}]
                   ]})


Using the `node` key in a waveform, plus the `edge` key in the top-level dictionary, provides a way to show transitions between different edges.

.. jupyter-execute::
    :emphasize-lines: 5

    logic.TimingDiagram(
        {'signal': [
            {'name': 'A', 'wave': '0..1..01.', 'node': '...a.....'},
            {'name': 'B', 'wave': '101..0...', 'node': '.....b...'}],
         'edge': ['a~>b']
        })


Each string in the edge list must start and end with a node name (single character). The characters between them define the type of connecting line: '-' for straight line, '~' for curve, '-\|' for orthogonal lines, and \< or \> to include arrowheads.
For example, 'a-~>b' draws a curved line with arrowhead between nodes a and b.


Using JSON
----------

Because the examples from WaveDrom use JavaScript and JSON, they sometimes cannot be directly pasted into Python as dictionaries.
The :py:meth:`schemdraw.logic.timing.TimingDiagram.from_json` method allows input of the WaveJSON as a string pasted directly from the Javascript/JSON examples without modification.

Notice lack of quoting on the dictionary keys, requiring the `from_json` method to parse the string.

.. jupyter-execute::

    logic.TimingDiagram.from_json('''{ signal: [
      { name: "clk",  wave: "P......" },
      { name: "bus",  wave: "x.==.=x", data: ["head", "body", "tail", "data"] },
      { name: "wire", wave: "0.1..0." }
    ]}''')



Schemdraw's Customizations
--------------------------

Schemdraw extends the WaveJSON spcification with a few additional options. 

Style Parameters
****************

Each wave dictionary accpets a `color` and `lw` parameter.
The rise/fall time for transitions can be set using the `risetime` parameter to TimingDiagram. Other colors and font sizes may be speficied using keyword arguments to :py:class:`schemdraw.logic.timing.TimingDiagram`.

Asynchronous Signals
********************

WaveDrom does not have a means for defining asynchronous signals - all waves must transition on period boundaries. Schemdraw adds asyncrhonous signals using the `async` parameter, as a list of period multiples for each transition in the wave. Note the beginning and end time of the wave must also be specified, so the length of the `async` list must be one more than the length of `wave`.

.. jupyter-execute::
    :emphasize-lines: 4

    logic.TimingDiagram(
        {'signal': [
            {'name': 'clk', 'wave': 'n......'},
            {'name': 'B', 'wave': '010', 'async': [0, 1.6, 4.25, 7]}]},
        risetime=.03)


Variable Voltage Levels
***********************

Another Schemdraw extension adds adjustable voltage levels within a signal using the `level` parameter.
The value can take 10 different values, specified as digits in the `level` string, where a `1` corresponds to 10%, `2` to 20%, etc., with `0` meaning 100% of the normal high voltage level.
As with the `wave` parameter, a period is used to repeat the previous level value.

Here, the first pulse is 100%, the second at 50%, and the third at 20%.

.. jupyter-execute::
    :emphasize-lines: 4

    logic.TimingDiagram(
        {'signal': [
            {'wave':  '0.1..0.1.0.1.',
             'level': '0......5...2.',
            }],
        })


Extended Edge Notation
**********************

Additional "edge" string notations are allowed for more complex labeling of edge timings, including asynchronous start and end times and labels just above or below a wave.

Each edge string using this syntax takes the form

.. code-block:: python

    '[WaveNum:Period]<->[WaveNum:Period]{color,ls} Label'

Everything after the first space will be drawn as the label in the center of the line.
The values in square brackets designate the start and end position of the line.
`WaveNum` is the integer row number (starting at 0) of the wave, and `Period` is the possibly fractional number of periods in time for the node. `WaveNum` may be appended by a `^` or `v` to designate notations just above, or just below, the wave, respectively.

Between the two square-bracket expressions is the standard line/arrow type designator. In optional curly braces, the line color and linestyle may be entered.

Some examples are shown here:

.. jupyter-execute::
    :emphasize-lines: 5-7

    logic.TimingDiagram(
        {'signal': [
            {'name': 'A', 'wave': 'x3...x'},
            {'name': 'B', 'wave': 'x6.6.x'}],
         'edge': ['[0^:1]+[0^:5] $t_1$',
                  '[1^:1]<->[1^:3] $t_o$',
                  '[0^:3]-[1v:3]{gray,:}',
                 ]},
        ygap=.5, grid=False)


When placing edge labels above or below the wave, it can be useful to add the `ygap` parameter to TimingDiagram to increase the spacing between waves. 


See the :ref:`gallerytiming` Gallery for more examples.


.. note::

    `TimingDiagram` is an `Element`, meaning it may be added to a
    schemdraw `Drawing` with other schematic components.
    To save a standalone `TimingDiagram` to an image file, first add it to a drawing, and
    save the drawing:

        .. code-block:: python

            with schemdraw.Drawing(file='timing.svg'):
                logic.TimingDiagram(
                    {'signal': [
                        {'name': 'A', 'wave': '0..1..01.'},
                        {'name': 'B', 'wave': '101..0...'}]})

Bit Field Diagrams
------------------

Bit Field diagrams may be drawn using :py:class:`schemdraw.logic.bitfield.BitField`.
They work similar to timing diagrams, with a single parameter dictionary defining the element, which may also be supplied in a `from_json` class method.

.. jupyter-execute::

    logic.BitField(
        {'reg': [
            { "name": "IPO",   "bits": 8, "attr": "RO" },
            {                  "bits": 7 },
            { "name": "BRK",   "bits": 5, "attr": "RW", "type": 4 },
            { "name": "CPK",   "bits": 2 },
            { "name": "Clear", "bits": 3 },
            { "bits": 8 }
        ],
        }
    )


The dictionary passed to BitField may have two keys: `reg` and `config`.
The `reg` key is a list of bit groups within the register. Each item in the list may have attributes:

    * name: Text to display within the bit group
    * bits: Number of bits within the group
    * attr: Label to show below the group. May be a string, or integer. If integer, the binary representation is shown. May also be a list of multiple lines.
    * type: 0-9 code to fill the bit group. Or may be any valid color string.

Schemdraw adds these parameters not available in the original WaveDrom:
    * scale: Scale factor for bit width in the group
    * number: Show first and last bit numbers above the group

The `config` dictionary may include these key-value pairs:
    * lanes: Number of lanes
    * hflip: Reverse order of lanes
    * vflip: Reverse order of bits
    * compact: Remove whitespace between lanes
    * bits: Total number of bits to include (padded out if not included in the `reg` list)
    * label: Dictionary of either 'left' or 'right' and text to display left or right of the lanes.

Additional parameters may be passed directly to `BitField`. Values in the config dictionary above take precedence.

    * bitheight: Height of a bit register box in drawing units
    * width: Full width of the register box in drawing units
    * fontsize: Size of all text labels
    * lw: Line width for borders
    * ygap: Distance between lanes. Omit to auto-space based on label heights
    * vflip: Flip order of bits
    * hflip: Flip order of lanes
    * compact: Remove whitespace between lanes


Schemdraw's implementation has these known differences compared to WaveDrom:

    * 'type' parameter, which is used to specify a fill color, can be the 0-9 code as in WaveDrom, or any valid color string
    * hspace defines the full width of the register in pixels, without including any labels
    * vspace defines the full width of a register in pixels, without including any labels or padding
    * margins are ignored (but can be set by adding the BitField to a schemdraw Drawing)

Examples are below, many borrowed from [here](https://observablehq.com/collection/@drom/bitfield).

.. jupyter-execute::

    logic.BitField.from_json(r'''
    {reg:[
        {name: 'OP-IMM-32', bits: 7,  attr: 0b0011011},
        {name: 'rd',     bits: 5,  attr: 0},
        {name: 'func3',  bits: 3,  attr: ['SLLIW', 'SRLIW', 'SRAIW']},
        {bits: 10},
        {name: 'imm?',   bits: 7, attr: [0, 32, 32]}
    ]}
    '''
    )

.. jupyter-execute::

    logic.BitField.from_json(r'''
    {reg: [
    {bits: 8, name: "'S'", type: 4},
    {bits: 8, name: "'1'", type: 4, attr: 'type'},
    {bits: 8, name: "'0'", attr: 'count 0', type: 5},
    {bits: 8, name: "'C'", attr: 'count 1', type: 5},
    {bits: 8, attr: 'addr0', type: 2},
    {bits: 8, attr: 'addr1', type: 2},
    {bits: 8, attr: 'addr2', type: 2},
    {bits: 8, attr: 'addr3', type: 2},
    {bits: 48, name: 'data', type: 6},
    {bits: 16, name: 'checksum', type: 7},
    {bits: 8, name: "'\\r'"},
    {bits: 8, name: "'\\n'"},
    ], config: {hspace: 800, lanes: 3, bits: 144, vflip: true, hflip: true}}
    '''
    )

.. jupyter-execute::

    logic.BitField.from_json('''
    {'reg': [
        {'name': '0x3',   'bits': 7,  attr: 'CMD' },
        {'name': '0x001', 'bits': 1,  attr: 'REC', scale: 3 },
        {'name': 'OP_T',  'bits': 8,  attr: 'OP_T' },
        {'name': '0x0',   'bits': 13, attr: 'ARG_POINTER', scale: .5, number: false },
        {'name': '0x2',   'bits': 3,  attr: 'MODE' },
    ],
    }
    ''')
