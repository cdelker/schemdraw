.. _gallerytiming:

Timing Diagrams
---------------

.. jupyter-execute::
    :hide-code:

    import schemdraw
    from schemdraw import elements as elm
    from schemdraw import logic


Timing diagrams, based on `WaveDrom <https://wavedrom.com/>`_, are drawn using the :py:class:`schemdraw.logic.timing.TimingDiagram` class.

.. code-block:: python

    from schemdraw import logic



SRAM read/write cycle
^^^^^^^^^^^^^^^^^^^^^

The SRAM examples make use of Schemdraw's extended 'edge' notation for labeling
timings just above and below the wave.

.. jupyter-execute::
    :code-below:
    
    logic.TimingDiagram(
        {'signal': [
            {'name': 'Address',     'wave': 'x4......x.', 'data': ['Valid address']},
            {'name': 'Chip Select', 'wave': '1.0.....1.'},
            {'name': 'Out Enable',  'wave': '1.0.....1.'},
            {'name': 'Data Out',    'wave': 'z...x6...z', 'data': ['Valid data']},
        ],
         'edge': ['[0^:1.2]+[0^:8] $t_{WC}$',
                  '[0v:1]+[0v:5] $t_{AQ}$',
                  '[1:2]+[1:5] $t_{EQ}$',
                  '[2:2]+[2:5] $t_{GQ}$',
                  '[0^:5]-[3v:5]{lightgray,:}',
                 ]
        }, ygap=.5, grid=False)


.. jupyter-execute::
    :code-below:
    
    logic.TimingDiagram(
        {'signal': [
            {'name': 'Address',      'wave': 'x4......x.', 'data': ['Valid address']},
            {'name': 'Chip Select',  'wave': '1.0......1'},
            {'name': 'Write Enable', 'wave': '1..0...1..'},
            {'name': 'Data In',      'wave': 'x...5....x', 'data': ['Valid data']},
        ],
         'edge': ['[0^:1]+[0^:8] $t_{WC}$',
                  '[2:1]+[2:3] $t_{SA}$',
                  '[3^:4]+[3^:7] $t_{WD}$',
                  '[3^:7]+[3^:9] $t_{HD}$',
                  '[0^:1]-[2:1]{lightgray,:}'],
        }, ygap=.4, grid=False)



J-K Flip Flop
^^^^^^^^^^^^^

Timing diagram for a J-K flip flop taken from `here <https://commons.wikimedia.org/wiki/File:JK_timing_diagram.svg>`_.
Notice the use of the `async` dictionary parameter on the J and K signals, and the color parameters for the output signals.

.. jupyter-execute::
    :code-below:

    logic.TimingDiagram(
        {'signal': [
            {'name': 'clk', 'wave': 'P......'},
            {'name': 'J', 'wave': '0101', 'async': [0, .8, 1.3, 3.7, 7]},
            {'name': 'K', 'wave': '010101', 'async': [0, 1.2, 2.3, 2.8, 3.2, 3.7, 7]},
            {'name': 'Q', 'wave': '010.101', 'color': 'red', 'lw': 1.5},
            {'name': r'$\overline{Q}$', 'wave': '101.010', 'color': 'blue', 'lw': 1.5}],
        'config': {'hscale': 1.5}}, risetime=.05)


Tutorial Examples
^^^^^^^^^^^^^^^^^

These examples were copied from `WaveDrom Tutorial <https://wavedrom.com/tutorial.html>`_.
They use the `from_json` class method so the examples can be pasted directly as a string. Otherwise, the setup must be converted to a proper Python dictionary.

.. jupyter-execute::
    :code-below:
    
    logic.TimingDiagram.from_json('''{ signal: [{ name: "Alfa", wave: "01.zx=ud.23.456789" }] }''')
    
    
.. jupyter-execute::
    :code-below:
    
    logic.TimingDiagram.from_json('''{ signal: [
      { name: "clk",         wave: "p.....|..." },
      { name: "Data",        wave: "x.345x|=.x", data: ["head", "body", "tail", "data"] },
      { name: "Request",     wave: "0.1..0|1.0" },
      {},
      { name: "Acknowledge", wave: "1.....|01." }
      ]}''')
