.. _electrical:

Basic Circuit Elements
======================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import SchemDraw
    from SchemDraw import elements as e
    def drawElements(elm_list, n=5, dx=1, dy=2, ofst=.8, fname=None, **kwargs):
        x, y = 0, 0
        d = SchemDraw.Drawing(fontsize=12)
        for elm in elm_list:
            A = d.add(elm, xy=[(d.unit+1)*x+1,y], label=elm['name'], **kwargs)
            x = x + dx
            if x >= n:
                x=0
                y=y-dy
        d.draw()


These elements are defined in the `SchemDraw.elements` module.

2-terminal Elements
-------------------

Basic Elements
^^^^^^^^^^^^^^

Basic elements define a `start` and `end` anchor for placing.
Depending on the arguments to the `add` method, the leads may be extended
to make the element the desired length.

.. jupyter-execute::
    :hide-code:

    elms = [
        e.RES, e.RES_VAR, e.RBOX, e.CAP, e.CAP2, e.CAP_P, e.CAP2_P, e.CAP_VAR,
        e.INDUCTOR, e.INDUCTOR2, e.DIODE, e.DIODE_F, e.SCHOTTKY,
        e.SCHOTTKY_F, e.DIODE_TUNNEL, e.DIODE_TUNNEL_F, e.ZENER, e.ZENER_F,
        e.LED, e.LED2, e.PHOTODIODE, e.DIAC, e.DIAC_F, e.TRIAC, e.TRIAC_F,
        e.SCR, e.SCR_F, e.FUSE, e.XTAL, e.MEMRISTOR, e.MEMRISTOR2, e.JJ]
    drawElements(elms, n=4, dy=2.25, lblofst=.8, lblloc='center')


Sources and Meters
^^^^^^^^^^^^^^^^^^


.. jupyter-execute::
    :hide-code:

    sources = [e.SOURCE, e.SOURCE_V, e.SOURCE_I, e.SOURCE_SIN, e.SOURCE_CONT,
               e.SOURCE_CONT_I, e.SOURCE_CONT_V, e.BAT_CELL, e.BATTERY, e.LAMP,
               e.METER_V, e.METER_I, e.METER_OHM]
    drawElements(sources, n=4, dy=2.25, d='right', lblofst=.2)



Switches
^^^^^^^^

.. jupyter-execute::
    :hide-code:

    switches =[e.SWITCH_SPST, e.SWITCH_SPST_OPEN, e.SWITCH_SPST_CLOSE,
               e.SWITCH_SPDT, e.SWITCH_SPDT_OPEN, e.SWITCH_SPDT_CLOSE,
               e.SWITCH_SPDT2, e.SWITCH_SPDT2_OPEN, e.SWITCH_SPDT2_CLOSE,
               e.BUTTON, e.BUTTON_NC]
    drawElements(switches, n=4, dx=1.4, dy=2.5)#, lblofst=.8)


Labels
^^^^^^

The LABEL element can be used to add a label anywhere.
The GAP_LABEL is like an "invisible" element, useful for marking the voltage between output terminals.

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing(fontsize=12)
    d.add(e.LINE, d='right', l=1)
    d.add(e.LABEL, xy=[3,-.5], label='LABEL')
    d.add(e.DOT_OPEN)
    d.add(e.GAP_LABEL, d='down', label=['+','GAP_LABEL','$-$'])  # Use math mode to make it a minus, not a hyphen.
    d.add(e.DOT_OPEN)
    d.add(e.LINE, d='left', l=1)
    d.draw()

Other
^^^^^

.. jupyter-execute::
    :hide-code:

    other =[e.SPEAKER]
    drawElements(other, n=3, lblloc='center', lblofst=1.1)


Lines, Dots, Arrows
-------------------

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing(fontsize=12)
    d.add(e.LINE, l=4, label='LINE')
    d.add(e.DOT, label='DOT')
    d.add(e.LINE, l=2)
    d.add(e.DOT_OPEN, label='DOT_OPEN')
    d.add(e.LINE, l=3)
    d.add(e.ARROWHEAD, label='ARROWHEAD')
    d.draw()


1-terminal elements
-------------------

One-terminal elements do not move the current drawing position, and ignore any `add` parameters
that specify an endpoint.

.. jupyter-execute::
    :hide-code:

    grounds = [e.GND, e.GND_SIG, e.GND_CHASSIS, e.VSS, e.VDD, e.ANT]
    drawElements(grounds, n=3, dy=3)


3-terminal Elements
-------------------

Three terminal elements define anchor names so that any of the three terminals can
be placed at the desired drawing position.

Potentiometer is defined with one additional anchor for the 'tap':

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing(fontsize=12)
    P = d.add(e.POT, botlabel='POT')
    d.add(e.LINE, xy=P.tap, d='up', l=.5)
    P.add_label('tap')
    d.draw()


BJT and FET transistors also define three anchors:

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing(fontsize=12)
    bjt = d.add(e.BJT_NPN, xy=[0, 0], anchor='base')
    d.add(e.LINE, xy=bjt.base, d='left', l=.3, lblofst=.2, lftlabel='base')
    bjt.add_label('emitter', loc='center', ofst=[.3,-1.3])
    bjt.add_label('collector', loc='center', ofst=[.3,1.0])

    fet = d.add(e.NFET, xy=[4, 0], anchor='gate')
    d.add(e.LINE, xy=fet.gate, d='right', l=0, lblofst=.2, lftlabel='gate')
    fet.add_label('source', loc='center', ofst=[-.5,-1.3])
    fet.add_label('drain', loc='center', ofst=[-.5,1.0])
    d.draw()

Names of the different transistor elements are shown below:

.. jupyter-execute::
    :hide-code:

    bjt = [e.BJT,e.BJT_NPN,e.BJT_PNP,e.BJT_NPN_C,e.BJT_PNP_C,e.BJT_PNP_2C]
    drawElements(bjt, n=3, dy=2.5, lblloc='top')

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing(fontsize=12)
    d.add(e.NFET, label='NFET', lblloc='top')
    d.add(e.PFET, label='PFET', lblloc='top', xy=[3,0] )
    d.add(e.NFET4, label='NFET4', lblloc='top', xy=[6,0])
    d.add(e.PFET4, label='PFET4', lblloc='top', xy=[9,0])
    d.add(e.JFET_N, label='JFET_N', lblloc='top', xy=[0,-3])
    d.add(e.JFET_P, label='JFET_N', lblloc='top', xy=[3,-3])
    d.add(e.JFET_N_C, label='JFET_N_C', lblloc='top', xy=[6,-3])
    d.add(e.JFET_P_C, label='JFET_N_C', lblloc='top', xy=[9,-3])
    d.draw()

An opamp defines three anchors, in1, in2, and out.

.. jupyter-execute::
    :hide-code:
    
    d = SchemDraw.Drawing(fontsize=12)
    op = d.add( e.OPAMP, label='OPAMP' )
    d.add(e.LINE, xy=op.in1, d='left', l=.5, lftlabel='in1')
    d.add(e.LINE, xy=op.in2, d='left', l=.5, lftlabel='in2')
    d.add(e.LINE, xy=op.out, d='right', l=.5, rgtlabel='out')
    d.add(e.GAP_LABEL )
    op2 = d.add(e.OPAMP_NOSIGN, label='OPAMP_NOSIGN' )
    d.add(e.LINE, xy=op2.in1, d='left', l=.5, lftlabel='in1')
    d.add(e.LINE, xy=op2.in2, d='left', l=.5, lftlabel='in2')
    d.add(e.LINE, xy=op2.out, d='right', l=.5, rgtlabel='out')
    d.draw()


Transformers
------------

Transformer elements can be generated using the :py:func:`SchemDraw.elements.transformer` function.

.. function:: SchemDraw.elements.transformer(t1=4, t2=4, core=True, ltaps=None, rtaps=None, loop=False)

   Generate an element definition for a transformer

   :param t1: turns on left side
   :type t1: int
   :param t2: turns on right side
   :type t2: int
   :param core: show the transformer core
   :type core: bool
   :param ltaps: anchor definitions for left side. Each key/value pair defines the name/turn number
   :type ltaps: dict
   :param rtaps: anchor definitions for right side.
   :type rtaps: dict
   :param loop: Use spiral/cycloid (loopy) style
   :type loop: bool
   :returns: element definition dictionary
   :rtype: dict


Two transformers with cycloid=False (left) cycloid=True (right) shown below. Anchor names are `p1` and `p2` for the primary (left) side,
and `s1` and `s2` for the secondary (right) side.

.. jupyter-execute::
    :hide-code:

    d = SchemDraw.Drawing()
    x = d.add(e.transformer(6,3, core=True, loop=False))
    d.add(e.LINE, xy=x.s1, l=d.unit/4)
    d.add(e.LINE, xy=x.s2, l=d.unit/4)
    d.add(e.LINE, xy=x.p1, l=d.unit/4, d='left')
    d.add(e.LINE, xy=x.p2, l=d.unit/4, d='left')

    x2 = d.add(e.transformer(6,3, core=False, loop=True), d='right', xy=(4,0))
    d.add(e.LINE, xy=x2.s1, l=d.unit/4, d='right')
    d.add(e.LINE, xy=x2.s2, l=d.unit/4, d='right')
    d.add(e.LINE, xy=x2.p1, l=d.unit/4, d='left')
    d.add(e.LINE, xy=x2.p2, l=d.unit/4, d='left')
    d.draw()

Example usage with taps:

.. jupyter-execute::

    d = SchemDraw.Drawing()
    xf = d.add( e.transformer(t1=4, t2=8, rtaps={'B':3}, loop=False ) )
    d.add(e.LINE, xy=xf.s1, l=d.unit/4, rgtlabel='s1')
    d.add(e.LINE, xy=xf.s2, l=d.unit/4, rgtlabel='s2')
    d.add(e.LINE, xy=xf.p1, l=d.unit/4, d='left', lftlabel='p1')
    d.add(e.LINE, xy=xf.p2, l=d.unit/4, d='left', lftlabel='p2')
    d.add(e.LINE, xy=xf.B, l=d.unit/2, d='right', rgtlabel='B')
    d.draw()


Blackboxes and ICs
------------------

Elements drawn as boxes, such as integrated circuits, can be generated using the :py:func:`SchemDraw.elements.blackbox` function.
An arbitrary number of inputs/outputs can be drawn to each side of the box.
The inputs can be evenly spaced (default) or arbitrarily placed anywhere along each edge.

.. function:: SchemDraw.elements.blackbox(w, h, linputs=None, rinputs=None, tinputs=None, binputs=None, \
    mainlabel='', leadlen=0.5, lblsize=16, lblofst=.15, plblofst=.1, plblsize=12, hslant=None, vslant=None)

   :param w: width of blackbox rectangle
   :param h: height of blackbox rectangle
   :param mainlabel: main box label
   :param leadlen: length of lead exetensions from each pin
   :param lblsize: font size for labels (inside the box)
   :param lblofst: label offset
   :param plblsize: font size for pin labels (outside the box)
   :param plblofst: pin label offset
   :param hslant: angle (degrees) to slant horizontal sides (e.g. for multiplexers)
   :param vslant: angle (degrees) to slant vertical sides
   :param linputs: pin definition dictionary for left side of box
   :type linputs: dict
   :param rinputs: pin definition dictionary for right side of box
   :type rinputs: dict
   :param tinputs: pin definition dictionary for top side of box
   :type tinputs: dict
   :param binputs: pin definition dictionary for bottom side of box
   :type binputs: dict
   :returns: element definition dictionary
   :rtype: dict

Each pin definition dictionary may contain the following keys:

- **labels**: list of string labels for each input. drawn inside the box. default is blank. label of '>' will be converted to a clock input.
- **plabels**: list of pin label strings. drawn outside the box. Default is blank.
- **spacing**: distance between pins. Defaults to evenly spaced pins along side.
- **loc**: list of pin locations (0 to 1), along side. Defaults to evenly spaced pins. Overrides spacing argument.
- **leads**: True/False, draw leads coming out of box. Default=True.
- **lblofst**: float offset for labels. Default=.15
- **plblofst**: float offset for pin labels. Default=.1
- **lblsize**: font size for labels. Default=16
- **plblsize**: font size for pin labels. Default=12


Anchors to each input will be automatically generated using the 'labels' keyword of the pin definition dictionary 
for each side of the box if provided.
Duplicate input names will be appended with a number. If not provided, the anchors will be named 'inL1', 'inL2'...
for the left side, for the right side 'inR1', inR2', etc.

Here, a J-K flip flop, as part of an HC7476 integrated circuit, is drawn with input names and pin numbers.

.. jupyter-execute::
    :hide-code:
    
    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    linputs = {'labels':['>', 'K', 'J'], 'plabels':['1', '16', '4']}
    rinputs = {'labels':['$\overline{Q}$', 'Q'], 'plabels':['14', '15']}
    JK = e.blackbox(3, 6, linputs=linputs, rinputs=rinputs, mainlabel='7476')
    d.add(JK)

.. jupyter-execute::
    :hide-code:
    
    d.draw()





Multiplexers
^^^^^^^^^^^^

Multiplexers and demultiplexers may be drawn using the :py:func:`SchemDraw.elements.mux` function which wraps the :py:func:`SchemDraw.elements.blackbox` function.

.. function:: SchemDraw.elements.mux(inputs=None, outputs=None, ctrls=None, topctrls=None, \
                                     demux=False, h=None, w=None, pinspacing=1, ctrlspacing=.6,  \
                                     slope=25, **kwargs)
   
   :param inputs: names of input pins
   :type inputs: list
   :param outputs: names of output pins
   :type outputs: list
   :param ctrls: names of control signals on bottom of mux
   :type ctrls: list
   :param topctrls: names of control signals on top of mux
   :type topctrls: list
   :param demux: draw as demultiplexer
   :type demux: bool
   :param h: height of mux
   :param w: width of mux
   :param pinspacing: distance between pins on input and output sides
   :param ctrlspacing: distance between pins on top and bottom sides
   :param slope: angle (degrees) o slope top and bottom
   :param kwargs: passed to blackbox function

.. jupyter-execute::
    :hide-code:
    
    d = SchemDraw.Drawing()

.. jupyter-execute::
    :hide-output:

    m1 = e.mux(inputs=['A','B','C','D'], outputs=['X'], ctrls=['0','1'])
    d.add(m1)

.. jupyter-execute::
    :hide-code:
    
    d.draw()

