.. _images:

Image-based Elements
====================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    schemdraw.use('svg')


Elements can be made from image files, including PNG and SVG images, using :py:class:`schemdraw.elements.ElementImage`.
A common use case is to subclass `ElementImage` and provide the image file and anchor positions in the subclass's init method.
For example, an Arduino Board element may be created from an image:

.. jupyter-execute::

    class ArduinoUno(elm.ElementImage):
        ''' Arduino Element '''
        def __init__(self):
            # Dimensions based on image size to make it about the right
            # size relative to other components
            width = 10.3
            height = width/1.397
            pinspacing = .35   # Spacing between header pins

            super().__init__('ArduinoUNO.png', width=width, height=height, xy=(-.75, 0))

            # Only defining the top header pins as anchors for now
            top = height * .956
            arefx = 3.4
            for i, pinname in enumerate(['aref', 'gnd', 'pin13', 'pin12', 'pin11',
                                        'pin10', 'pin9', 'pin8']):
                self.anchors[pinname] = (arefx + i*pinspacing, top)


The Arduino element is used like any other element:

.. jupyter-execute::

    with schemdraw.Drawing() as d:
        d.config(color='#dd2222', unit=2)
        arduino = ArduinoUno()
        elm.Dot().at(arduino.gnd)
        elm.Resistor().up().scale(.7)
        elm.Line().right().tox(arduino.pin8)
        elm.LED().down().reverse().toy(arduino.pin8).scale(.7)
        elm.Dot().at(arduino.pin8)    


`Arduino Image Source <https://commons.wikimedia.org/wiki/File:ArduinoUNO.png>`_ , CC-BY-SA-3.0.


See :ref:`pictorial` for using Image Elements with other graphical schematic components.