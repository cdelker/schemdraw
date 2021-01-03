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
            eplaced = d.add(e, d='right', xy=[x, y])
            eplaced.add_label(name, loc='rgt', align=('left', 'center'))
            anchors = eplaced.absanchors.copy()
            anchors.pop('start', None)
            anchors.pop('end', None)
            anchors.pop('center', None)
            anchors.pop('xy', None)

            if len(anchors) > 0:
                for aname, apos in anchors.items():
                    eplaced.add_label(aname, loc=aname, color='blue', fontsize=10)
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
