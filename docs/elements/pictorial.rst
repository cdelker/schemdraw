.. _pictorial:

Pictorial Elements
==================

.. jupyter-execute::
    :hide-code:

    %config InlineBackend.figure_format = 'svg'
    import schemdraw
    from schemdraw import elements as elm
    schemdraw.use('svg')

Pictorial Schematics use pictures, rather than symbols, to represent circuit elements.
Schemdraw provides a few common pictorial elements, and more may be added by loading in
:ref:`images`.

All the built-in pictorial elements are drawn below.

.. jupyter-execute::

    from schemdraw import pictorial

    with schemdraw.Drawing():
        bb = pictorial.Breadboard().up()
        pictorial.CapacitorCeramic().at(bb.J1)
        pictorial.CapacitorMylar().at(bb.J4)
        pictorial.CapacitorElectrolytic().at(bb.J7)
        pictorial.TO92().at(bb.J10)
        pictorial.LED().at(bb.J13)
        pictorial.LEDOrange().at(bb.J16)
        pictorial.LEDYellow().at(bb.J19)
        pictorial.LEDGreen().at(bb.J22)
        pictorial.LEDBlue().at(bb.J25)
        pictorial.LEDWhite().at(bb.J28)
        pictorial.Diode().at(bb.F9).to(bb.F14)
        pictorial.Resistor().at(bb.F2).to(bb.F7)
        pictorial.DIP().at(bb.E18).up()


Breadboard
----------

The :py:class:`schemdraw.pictorial.pictorial.Breadboard` element has anchors at each pin location. Anchor names for the center block of pins
use the column letter and row number, such as `A1` for the top left pin.
The power strip columns along each side are `L1_x` for the first column on the left side or `L2_x`, for
the second column on the left side, with `x` designating the row number. Similarly, `R1_x` and `R2_x`
designate anchors on the right power strip columns. Note the "missing" rows in the power strip columns, such as row 6,
are not defined. Some examples are shown below.

.. jupyter-execute::

    with schemdraw.Drawing():
        bb = pictorial.Breadboard()
        elm.Dot(radius=.15).at(bb.A1).color('red')
        elm.Dot(radius=.15).at(bb.H10).color('orange')
        elm.Dot(radius=.15).at(bb.L1_1).color('cyan')
        elm.Dot(radius=.15).at(bb.R2_7).color('magenta')
        elm.Dot(radius=.15).at(bb.L2_13).color('green')


Resistors
---------

Resistors and Diodes inherit from :py:class:`schemdraw.elements.Element2Term`, meaning they may be extended to any length.
Resistors take `value` and `tolerance` arguments used to set the color bands. The colors
will be the closest possible color code using 3 bands to represent the value.

.. jupyter-execute::

    with schemdraw.Drawing():
        pictorial.Resistor(100)
        pictorial.Resistor(220)
        pictorial.Resistor(520)
        pictorial.Resistor(10000)


Dual-inline Packages (DIP)
--------------------------

Integrated circuits in DIP packages may be drawn with the :py:class:`schemdraw.pictorial.pictorial.DIP` element. The
`npins` argument sets the total number of pins and `wide` argument specifies a wide-body (0.6 inch)
versus the narrow-body (0.3 inch) package.

DIPs have anchors `pinX`, where `X` is the pin number.

.. jupyter-execute::

    with schemdraw.Drawing():
        pictorial.DIP()
        pictorial.DIP(npins=14).at((2, 0))
        pictorial.DIP(npins=28, wide=True).at((4, 0))
        

Colors
------

The pictorial elements are drawn using solid shapes. As such, the `.fill()` method must be
used to change their color, while the `.color()` method will set only the color of the outline, if the Element has one.
For example, to create a custom-color LED:

.. jupyter-execute::

    pictorial.LED().fill('purple')


Dimensions
----------

The pictorial elements are designed with spacing so they fit together in a breadboard with 0.1 inch spacing between pins.
Some constants are defined to assist in creating other pictorial elements:
`pictorial.INCH` and `pictorial.MILLIMETER` convert inches and millimeters to schemdraw's drawing units.
`pictorial.PINSPACING` is equal to 0.1 inch, the standard spacing between breadboard and DIP pins.


Example
-------

This example combines an :py:class:`schemdraw.elements.ElementImage` of an Arduino Uno board
with pictorial elements.

.. jupyter-execute::

    class ArduinoUno(elm.ElementImage):
        ''' Arduino Element '''
        def __init__(self):
            width = 10.3  # Set the width to scale properly for 0.1 inch pin spacing on headers
            height = width/1.397  # Based on image dimensions
            super().__init__('ArduinoUNO.png', width=width, height=height, xy=(-.75, 0))

            # Define all the anchors
            top = height * .956
            arefx = 3.4
            pinspace = pictorial.PINSPACING
            for i, pinname in enumerate(['aref', 'gnd_top', 'pin13', 'pin12', 'pin11',
                                        'pin10', 'pin9', 'pin8']):
                self.anchors[pinname] = (arefx + i*pinspace, top)

            bot = .11*pictorial.INCH
            botx = 1.23*pictorial.INCH
            for i, pinname in enumerate(['ioref', 'reset', 'threev3',
                                        'fivev', 'gnd1', 'gnd2', 'vin']):
                self.anchors[pinname] = (botx + i*pinspace, bot)

            botx += i*pinspace + pictorial.PINSPACING*2
            for i, pinname in enumerate(['A0', 'A1', 'A2', 'A3', 'A4', 'A5']):
                self.anchors[pinname] = (botx + i*pinspace, bot)


    with schemdraw.Drawing():
        ard = ArduinoUno()
        bb = pictorial.Breadboard().at((0, 9)).up()
        elm.Wire('n', k=-1).at(ard.gnd2).to(bb.L2_29).linewidth(4)
        elm.Wire().at(ard.pin12).to(bb.A14).color('red').linewidth(4)
        pictorial.LED().at(bb.E14)
        pictorial.Resistor(330).at(bb.D15).to(bb.L2_15)

`Arduino Image Source <https://commons.wikimedia.org/wiki/File:ArduinoUNO.png>`_ , CC-BY-SA-3.0.


Fritzing Part Files
-------------------

Schemdraw can import part files in the `Fritzing <https://fritzing.org/>`_ format and use them in pictorial schematics.
Use :py:class:`schemdraw.pictorial.fritz.FritzingPart` and provide the file name of an `.fzpz` or `.fzbz` part file.
Schemdraw's anchors will be set based on the part "connectors" defined in the part file.
In this example, a part is downloaded from the `Adafruit Fritzing Library <https://github.com/adafruit/Fritzing-Library>`_ and used in a drawing.

.. jupyter-execute::

    from urllib.request import urlretrieve
    part = 'https://github.com/adafruit/Fritzing-Library/raw/master/parts/Adafruit%20OLED%20Monochrome%20128x32%20SPI.fzpz'
    fname, msg = urlretrieve(part)

    with schemdraw.Drawing() as d:
        oled = pictorial.FritzingPart(fname)
        elm.Line().down().at(oled.GND).length(.5)
        elm.Ground()
        elm.Line().down().at(oled.absanchors['3.3V']).color('red').length(1.5).label('3.3V', loc='left')
        elm.Button().at(oled.RESET)
        elm.Ground(lead=False)

Note that occasionally anchor names defined in Fritzing parts are not valid as Python identifiers, such as the `3.3V` anchor above, and therefore cannot be used as attributes of the element instance (`f.3.3V` doesn't work, obviously). In these cases, the anchor must be accessed through the `absanchors` dictionary.

