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

.. class:: schemdraw.elements.compound.Optocoupler(**kwargs)

    An optocoupler/optoisolator element
    
    :param box: Draw a box around the optocoupler
    :type box: bool
    :param boxfill: Color to fill the box
    :type boxfill: string
    :param boxpad: Padding between phototransistor and box
    :type boxpad: float
    :param base: Add a base contact to the phototransistor
    :type base: bool


.. jupyter-execute::
    :hide-code:
    
    drawElements([elm.Optocoupler, partial(elm.Optocoupler, base=True)])


Relay
-----

.. class:: schemdraw.elements.compound.Relay(**kwargs)

    A relay with inductor and switch
    
    :param unit: Unit length of the inductor
    :type unit: float
    :param cylcoid: Use cycloid style inductor
    :type cycloid: bool
    :param switch: Switch style; 'spst', 'spdt', 'dpst', or 'dpdt'
    :type switch: bool
    :param swreverse: Reverse the switch direction
    :type swreverse: bool
    :param swflip: Flip the switch
    :type swflip: bool
    :param core: Show inductor core bar
    :type core: bool
    :param link: Show dotted line linking inductor and switch
    :type link: bool
    :param box: Draw a box around the relay
    :type box: bool
    :param boxfill: Color to fill the box
    :type boxfill: string
    :param boxpad: Spacing between components and box
    :type boxpad: float

.. jupyter-execute::
    :hide-code:
    
    drawElements([elm.Relay, 
                  partial(elm.Relay, switch='spdt'),
                  partial(elm.Relay, switch='dpst'),
                  partial(elm.Relay, switch='dpdt')],
                  cols=2, dy=3)
