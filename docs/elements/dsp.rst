Signal Processing
=================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import SchemDraw
    from SchemDraw import dsp

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

Signal processing elements can be drawn by importing the :py:mod:`dsp` module:

.. code-block:: python

    from SchemDraw import dsp

Because each element may have multiple connections in and out, these elements
do not automatically extend "leads", so they must be manually connected with
LINE elements. The square elements define anchors 'N', 'S', 'E', and 'W' for
the four directions. Circle-based elements also includ 'NE', 'NW', 'SE', and 'SW'
anchors. Other elements, such as AMP, define 'in' and 'out' anchors when appropriate.

The ARROWHEAD basic circuit element is useful to show signal flow.

.. jupyter-execute::
    :hide-code:

    elms = [dsp.BOX, dsp.CIRCLE, dsp.SUM, dsp.SUMSIGMA, dsp.MIX, dsp.SPEAKER1,
            dsp.AMP, dsp.OSCBOX, dsp.OSC, dsp.FILT, dsp.FILT_LP, dsp.FILT_BP,
            dsp.FILT_HP, dsp.ADC, dsp.DAC, dsp.DEMOD]
    drawElements(elms, n=4, lblofst=.8, lblloc='center')

Labels are placed in the center of the element. The generic BOX and CIRCLE element can
be used with a label to define other operations. For example, an integrator
may be created using:

.. jupyter-execute::
    :hide-code:
    
    d = SchemDraw.Drawing()

.. jupyter-execute::

    d.add(dsp.BOX, label='$\int$');

.. jupyter-execute::
    :hide-code:
    
    d.draw()
