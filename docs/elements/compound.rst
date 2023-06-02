Compound Elements
=================

Several compound elements defined based on other basic elements.

.. jupyter-execute::
    :hide-code:
    
    %config InlineBackend.figure_format = 'svg'
    from functools import partial
    import schemdraw
    from schemdraw import elements as elm

    def drawElements(elmlist, cols=3, dx=8, dy=2):
        d = schemdraw.Drawing(fontsize=12)
        for i, e in enumerate(elmlist):
            y = i//cols*-dy
            x = (i%cols) * dx

            name = type(e()).__name__
            if hasattr(e, 'keywords'):  # partials have keywords attribute
                args = ', '.join(['{}={}'.format(k, v) for k, v in e.keywords.items()])
                name = '{}({})'.format(name, args)
            newelm = e().right().at((x, y)).label(name, loc='rgt', halign='left', valign='center')

            if len(newelm.anchors) > 0:
                for aname, apos in newelm.anchors.items():
                    if aname not in ['start', 'end', 'center', 'xy']:
                        newelm.label(aname, loc=aname, color='blue', fontsize=10)
            d += newelm
        return d
    

Optocoupler
-----------

:py:class:`schemdraw.elements.compound.Optocoupler` can be drawn with or without a base contact.


.. jupyter-execute::
    :hide-code:
    
    drawElements([elm.Optocoupler, partial(elm.Optocoupler, base=True)])


Relay
-----

:py:class:`schemdraw.elements.compound.Relay` can be drawn with different options for switches and inductor solenoids.

.. jupyter-execute::
    :hide-code:
    
    drawElements([elm.Relay, 
                  partial(elm.Relay, switch='spdt'),
                  partial(elm.Relay, switch='dpst'),
                  partial(elm.Relay, switch='dpdt')],
                  cols=2, dy=3)


Wheatstone
----------

:py:class:`schemdraw.elements.compound.Wheatstone` can be drawn with or without the output voltage taps.
The `labels` argument specifies a list of labels for each resistor.


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()
    d += (W:=elm.Wheatstone()
            .label('N', loc='N', color='blue', fontsize=10)
            .label('S', loc='S', color='blue', fontsize=10)
            .label('E', loc='E', color='blue', fontsize=10)
            .label('W', loc='W', color='blue', fontsize=10)
            .label('Wheatstone', loc='S', ofst=(0, -.5)))
    d += (W:=elm.Wheatstone(vout=True).at((7, 0))
            .label('N', loc='N', color='blue', fontsize=10)
            .label('S', loc='S', color='blue', fontsize=10)
            .label('E', loc='E', color='blue', fontsize=10)
            .label('W', loc='W', color='blue', fontsize=10)
            .label('vo1', loc='vo1', color='blue', fontsize=10)
            .label('vo2', loc='vo2', color='blue', fontsize=10)
            .label('Wheatstone(vout=True)', loc='S', ofst=(0, -.5)))
    d.draw()


Rectifier
----------

:py:class:`schemdraw.elements.compound.Rectifier` draws four diodes at 45 degree angles.
The `labels` argument specifies a list of labels for each diode.


.. jupyter-execute::
    :hide-code:
    
    d = schemdraw.Drawing()
    d += (W:=elm.Rectifier()
            .label('N', loc='N', color='blue', fontsize=10)
            .label('S', loc='S', color='blue', fontsize=10)
            .label('E', loc='E', color='blue', fontsize=10)
            .label('W', loc='W', color='blue', fontsize=10)
            .label('Rectifier', loc='S', ofst=(0, -.5)))
    d.draw()
