Timing Diagrams
===============

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import logic


Digital timing diagrams may be drawn using the :py:class:`schemdraw.logic.timing.TimingDiagram` Element in the :py:mod:`schemdraw.logic` module.

Timing diagrams are set up using the WaveJSON syntax used by the `WaveDrom <https://wavedrom.com/>`_ JavaScript application.


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
