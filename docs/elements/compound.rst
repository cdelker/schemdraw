Compound Elements
=================

Several compound elements defined based on other basic elements.

.. jupyter-execute::
    :hide-code:
    
    import schemdraw
    from schemdraw import elements as elm
    schemdraw.use('svg')


Optocoupler
-----------

:py:class:`schemdraw.elements.compound.Optocoupler` can be drawn with or without a base contact.


.. element_list::
    :ncols: 2

    Optocoupler()
    Optocoupler(base=True)



Relay
-----

:py:class:`schemdraw.elements.compound.Relay` can be drawn with different options for switches and inductor solenoids.

.. element_list::
    :ncols: 2

    Relay()
    Relay(switch='spdt')
    Relay(swithc='dpst')
    Relay(switch='dpdt')


Wheatstone
----------

:py:class:`schemdraw.elements.compound.Wheatstone` can be drawn with or without the output voltage taps.
The `labels` argument specifies a list of labels for each resistor.

.. element_list::
    :ncols: 2

    Wheatstone()
    Wheatstone(vout=True)


Rectifier
----------

:py:class:`schemdraw.elements.compound.Rectifier` draws four diodes at 45 degree angles.
The `labels` argument specifies a list of labels for each diode.

.. element_list::
    :ncols: 2

    Rectifier()

