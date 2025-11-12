Compound Elements
=================

Several compound elements defined based on other basic elements.

.. jupyter-execute::
    :hide-code:
    
    from functools import partial
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


Two-ports
-----------

Twoport elements share the interface defined by :py:class:`schemdraw.elements.twoports.ElementTwoport`, providing a set of anchors and various styling options. The terminals and box can be enabled or disabled using the `terminals` and `box` arguments. In addition, the `boxfill`, `boxlw`, and `boxls` provide the option to style the outline separately from other elements.

.. element_list::
    :ncols: 2

    TwoPort()
    TwoPort(terminals=False, boxlw=3)


Generic
^^^^^^^

.. element_list::
    :ncols: 2

    TwoPort()
    TwoPort(reverse_output=True)
    TwoPort(arrow=False)
    TwoPort(sign=False)


Transactors (ideal amplifiers)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Like the generic twoport, the transactors provide the option to reverse the direction of the output or current using the `reverse_output` argument.

.. element_list::
    :ncols: 2

    VoltageTransactor()
    TransimpedanceTransactor()
    TransadmittanceTransactor()
    CurrentTransactor()


Pathological
^^^^^^^^^^^^

.. element_list::
    :ncols: 2

    Nullor()
    VMCMPair()


Custom
^^^^^^

The :py:class:`schemdraw.elements.twoports.ElementTwoport` class can be used to define custom twoports by specifying an `input_element` and `output_element`. The `bpadx`, `bpady`, `minw`, `unit`, `width` can be used to tune the horizontal and vertical padding, minimum width of the elements, length of components, and width of the twoport respectively.


.. jupyter-execute::

    elm.ElementTwoport(
        input_element=elm.Inductor2,
        output_element=elm.SwitchReed,
        unit=2.5, width=2.5)

.. jupyter-execute::

    elm.ElementTwoport(
        input_element=elm.Lamp,
        output_element=partial(elm.Photodiode, reverse=True, flip=True),
        width=3)

