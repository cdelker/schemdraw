
# SchemDraw

SchemDraw is a python package for producing high-quality electrical circuit schematic diagrams. Typical usage:

        import SchemDraw as schem
        import SchemDraw.elements as e
        d = schem.Drawing()
        d.add( e.RES, label='100K$\Omega$' )
        d.add( e.CAP, d='down', botlabel='0.1$\mu$F' )
        d.draw()
        d.save( 'testschematic.png' )

![](img/testschematic.png)

Using an IPython Notebook in inline mode is recommended for the easy creation of these diagrams. Note that the images in this document were saved in PNG format for web compatibility. Better quality will be achieved using a vector format such as eps or svg.


## Installation

SchemDraw can be run under Python 2 or Python 3, and requires the numpy and matplotlib packages.

SchemDraw can be installed from pip using

        pip install SchemDraw

or directly by downloading the package and running

        python setup.py install


## Basic Usage

SchemDraw works on the principle of creating a drawing object, and then adding elements to it. Common elements are defined in SchemDraw.elements, and additional elements can easily be created (see [Defining New Elements]).

Start by setting up a new drawing:

        import SchemDraw as schem
        import SchemDraw.elements as e
        d = schem.Drawing()

Then use the add() method to add elements:

        d.add( e.RES, label='100$\Omega$' )
        d.add( e.CAP, label='0.1$\mu$F' )

And finish by calling draw(), and save() for a image file:

        d.draw()
        d.save( 'testschematic.pdf' )


### Element properties

The add() method takes a number of arguments to define the element position. The first argument is the element definition dictionary.

#### Position and direction

The position of each element can be specified in a number of ways. If no position is given, it will start at the current drawing position, typically where the previous element ends, and in the current drawing direction.

Otherwise, position can be specified using some combination of the keyword arguments:

        xy     : [x,y] starting coordiante.
                 Element drawn in current direction and default length.
        endpts : [[x1,y1], [x2,y2]] start and end coordinates
        to     : [x,y] end coordinate
        tox    : x-value of end coordinate (y-value same as start)
        toy    : y-value of end coordinate (x-value same as start)
        l      : total length of element
        zoom   : zoom/magnification for element (default=1)
        anchor : 'xy' argument refers to this position within the element.
                 For example, an opamp can be anchored to 'in1', 'in2', or 'out'

'to', 'tox', 'toy', 'l' can be used with 'xy' to define start and end points.

If only a starting coordinate is given, the direction defaults to the last element's direction unless specified by either:

        d       : direction ['up','down','left','right']
        theta   : angle (in degrees) to draw the element. Overrides 'd'.


#### Anchoring

Some elements define extra anchors. These are positions that can be used to position this element, or other elements connecting to it. For example, an opamp defines three anchor points: in1, in2, and out.

![](img/opamp.png)

When placing the opamp, it can then be located with respect to the correct terminal. The following will place an opamp with in2 connected to the endpoint of the resistor:

        d.add( e.RES, label='Rin' )
        op = d.add( e.OPAMP, anchor='in2' )

Then, to place a resistor on the output

        d.add( e.RES, xy=op.out, label='Ro' )

![](img/opamp_anchor.png)

All elements have at least three anchors: 'start', 'end', and 'center'.


#### Element orientation

An element can be reversed (for example a diode), or flipped vertically using the arguments:

        flip    : flip the element vertically (when theta=0)
        reverse : reverse a directional element (e.g. diode)


#### Labels

A label string can be added to the element using the 'label' argument (default position) or with 'toplabel', 'botlabel', 'lftlabel', or 'rgtlabel'. Labels can be added in multiple positions, for example labeling a component name with toplabel='R1' and value botlabel='100'. For math symbols, enclose the string in $$ to enable latex-style math mode, e.g.

        label='$R_1 = 100 \Omega$'.

        label, toplabel, botlabel, lftlabel, rgtlabel:
            Add a string label to the element.
        lblofst : offset between text label and element

A label can also be defined as a list of strings. In this case, the strings will be evenly spaced along the length of the element. This is useful for labeling polarities, for example label=['+','$v_o$','-'].

Labels can also be added to an element after it is added to the drawing using the element's add_label() method. This allows arbitrary positions and infinite number of labels.

        D1 = d.add(e.DIODE, label='D1' )
        D1.add_label( '1N4001', loc='bot' )
        D1.add_label( 'a', loc='lft' )
        D1.add_label( 'b', loc='rgt' )

![](img/label_positions.png)

The add_label() method takes the following arguments:

        label: text label to add
        loc: location for the label ['top', 'bot', 'lft', 'rgt'].
        txtofst: unit offset between element bounding box and label.
        align: alignment tuple for (horizontal, vertical):
               (['center', 'left', 'right'], ['center', 'top', 'bottom'])


#### Other

Other element arguments include:

        move_cur : move the cursor after drawing. Default=True.
        color    : matplotlib color. e.g. 'red', '#34a4e6', (.8,0,.8)


### Drawing parameters

When setting up a new schematic drawing, a few parameters are available to set the overall drawing size. Arguments to Drawing() are:

        unit : Full length of a resistor element in matplotlib plot units.
               Inner portion of resistor is length 1. Default=3.
        inches_per_unit : inches per unit to scale drawing. Default=.5
        txtofst  : Default distance from element to text label. Default=0.1.
        fontsize : Default font size. Default=16.
        font     : matplotlib font-family. Default='sans-serif'.


### Drawing state

The drawing state (current position and direction), can be saved and recalled using:

        d.push()   # Save the drawing state
        ... Do some things that change the drawing state
        d.pop()    # Recall the drawing state


### Saving an image

The final image can be saved to a file using d.save(). The filename extension determines the type of file to be saved. Any matplotlib-compatible file format can be used. Saving in a vector-based format, such as eps, pdf, or svg, is recommended for best quality.

        d.save('testimage.eps')


-----------------------------------------------------------

## Elements

A number of common elements are predefined in the SchemDraw.elements module.

### 2-Terminal Elements

![](img/2term.png)

### Sources and meters

![](img/sources.png)

![](img/meters.png)

### Grounds

Grounds don't move the current drawing position.

![](img/grounds.png)

### Switches

![](img/switches.png)

### Potentiometer

Potentiometer is defined with one additional anchor for the 'tap'.

![](img/pot.png)

### Opamp

An opamp defines three anchors, in1, in2, and out.

![](img/opamp.png)

### Transistors

Transistors also define three anchors as shown below.

![](img/bjt_anchors.png)
![](img/fet_anchors.png)

Types of transistors are shown below:

![](img/bjt.png)

### Connecting elements

Elements are connected with lines and dot elements. Dots don't change the current drawing position.

![](img/connectors.png)

### Label element

The LABEL element can be used to add a label to a blank space, such as marking the voltage between output terminals

![](img/label.png)


### Current Arrow

To label the current through an element, the ARROWI element is defined. Typically, it can be added alongside an existing element using the drawing's labelI() method, which takes the arguments:
        elm       : element to add arrow to
        label     : string or list of strings to space along arrow
        arrowofst : distance from element to arrow
        arrowlen  : length of arrow in drawing units
        top       : [True,False] draw on top (or bottom) of element

For example:

        R1 = d.add( e.RES )
        d.labelI( R1, '10mA' )

![](img/labeli.png)


### Loop currents

Loop currents can be added using the drawing's loopI() method:
        elm_list : boundary elements in order of top, right, bot, left
        label    : text label for center of loop
        d        : arrow direction 'cw' or 'ccw'. Default='cw'
        theta1   : start angle of arrow arc (degrees). Default=35
        theta2   : end angle of arrow arc (degrees). Default=-35

For example:

        R1 = d.add( e.RES )
        C1 = d.add( e.CAP, d='down' )
        D1 = d.add( e.DIODE_F, d='left')
        L1 = d.add( e.INDUCTOR, d='up' )
        d.loopI( [R1, C1, D1, L1], d='cw', label='$I_1$' )

![](img/loopi.png)



-----------------------------------------------------------

## Examples

Following are examples of more complicated circuit diagrams. Most are useless circuits made for torturing ECE201 students. Further examples can be found in the docs folder in examples.ipynb.

### Example 1

This example demonstrates use of push() and pop() and using 'tox' and 'toy' keywords.

        d = schem.Drawing(unit=2)  # unit=2 makes elements with shorter than normal leads
        d.push()
        R1 = d.add( e.RES, d='down', label='20$\Omega$')
        V1 = d.add( e.SOURCE_V, d='down', reverse=True, label='120V')
        d.add( e.LINE, d='right', l=3 )
        d.add( e.DOT )
        d.pop()
        d.add( e.LINE, d='right', l=3)
        d.add( e.DOT )
        d.add( e.SOURCE_V, d='down', label='60V', reverse=True )
        d.add( e.RES, label='5$\Omega$')
        d.add( e.DOT )
        d.add( e.LINE, d='right', l=3)
        d.add( e.SOURCE_I, d='up', label='36A' )
        d.add( e.RES, label='10$\Omega$')
        d.add( e.DOT )
        d.add( e.LINE, d='left', l=3, move_cur=False )
        d.add( e.LINE, d='right', l=3)
        d.add( e.DOT )
        R6 = d.add( e.RES, d='down', toy=V1.start, label='6$\Omega$' )
        d.add( e.DOT )
        d.add( e.LINE, d='left', l=3, move_cur=False)
        d.add( e.RES, d='right', xy=R6.start, label='1.6$\Omega$')
        d.add( e.DOT, label='a')
        d.add( e.LINE, d='right', xy=R6.end)
        d.add( e.DOT, label='b')
        d.draw()

![](img/ex01.png)


### Capacitor discharging

Shows how to connect to a switch element anchors.

        d = schem.Drawing()
        V1 = d.add( e.SOURCE_V, label='5V' )
        d.add( e.LINE, d='right', l=d.unit*.75 )
        S1 = d.add( e.SWITCH_SPDT2_CLOSE, d='up', anchor='b', rgtlabel='$t=0$' )
        d.add( e.LINE, d='right', xy=S1.c,  l=d.unit*.75 )
        d.add( e.RES, d='down', label='$100\Omega$', botlabel=['+','$v_o$','-'] )
        d.add( e.LINE, to=V1.start )
        d.add( e.CAP, xy=S1.a, d='down', toy=V1.start, label='1$\mu$F' )
        d.add( e.DOT )
        d.draw()

![](img/cap-charge.png)


### Inverting Opamp

Shows how to connect to an opamp

        d = schem.Drawing(inches_per_unit=.5)
        op = d.add( e.OPAMP )
        d.add( e.LINE, d='left', xy=op.in2, l=d.unit/4 )
        d.add( e.LINE, d='down', l=d.unit/5 )
        d.add( e.GND )
        d.add( e.LINE, d='left', xy=op.in1, l=d.unit/6 )
        d.add( e.DOT )
        d.push()
        Rin = d.add( e.RES, d='left', xy=op.in1-[d.unit/5,0], botlabel='$R_{in}$', lftlabel='$v_{in}$' )
        d.pop()
        d.add( e.LINE, d='up', l=d.unit/2 )
        Rf = d.add( e.RES,  d='right', l=d.unit*1, label='$R_f$' )
        d.add( e.LINE, d='down', toy=op.out )
        d.add( e.DOT )
        d.add( e.LINE, d='left', tox=op.out )
        d.add( e.LINE, d='right', l=d.unit/4, rgtlabel='$v_{o}$' )
        d.draw()

![](img/inv_opamp.png)


### Capacitor network

Another good problem to torture ECE201 students. Shows how to place an element using 'endpts' to cross a diagonal.

        d = schem.Drawing()
        A  = d.add( e.DOT, label='a' )
        C1 = d.add( e.CAP, label='8nF' )
        C2 = d.add( e.CAP, label='18nF' )
        C3 = d.add( e.CAP, botlabel='8nF', d='down' )
        C4 = d.add( e.CAP, botlabel='32nF', d='left' )
        C5 = d.add( e.CAP, botlabel='40nF' )
        B  = d.add( e.DOT, label='b' )
        C6 = d.add( e.CAP, label='2.8nF', endpts=[C1.end,C5.start])
        C7 = d.add( e.CAP, endpts=[C2.end,C5.start])
        C7.add_label( '5.6nF', loc='center', ofst=[-.3,-.1], align=('right','bottom') )
        d.draw()

![](img/cap-net.png)


### S-R Latch

Demonstrates using transistors

        d = schem.Drawing()
        Q1 = d.add( e.BJT_NPN_C, reverse=True, lftlabel='Q1' )
        Q2 = d.add( e.BJT_NPN_C, xy=[d.unit*2,0], label='Q2' )
        d.add( e.LINE, xy=Q1.collector, d='up', l=d.unit/2 )

        R1 = d.add( e.RES, d='up', label='R1', move_cur=False )
        d.add( e.DOT, lftlabel='V1' )
        d.add( e.RES, d='right', botlabel='R3', l=d.unit*.75 )
        d.add( e.DOT )
        d.push()
        d.add( e.LINE, d='up', l=d.unit/8 )
        d.add( e.DOT_OPEN, label='Set' )
        d.pop()
        d.add( e.LINE, to=Q2.base )

        d.add( e.LINE, xy=Q2.collector, d='up', l=d.unit/2 )
        d.add( e.DOT, rgtlabel='V2' )
        R2 = d.add( e.RES, d='up', botlabel='R2', move_cur=False )
        d.add( e.RES, d='left', botlabel='R4', l=d.unit*.75 )
        d.add( e.DOT )
        d.push()
        d.add( e.LINE, d='up', l=d.unit/8 )
        d.add( e.DOT_OPEN, label='Reset' )
        d.pop()
        d.add( e.LINE, to=Q1.base )

        d.add( e.LINE, xy=Q1.emitter, d='down', l=d.unit/4 )
        BOT = d.add( e.LINE, d='right', tox=Q2.emitter )
        d.add( e.LINE, to=Q2.emitter )
        d.add( e.DOT, xy=BOT.center )
        d.add( e.GND, xy=BOT.center )

        TOP = d.add( e.LINE, endpts=[R1.end,R2.end])
        d.add( e.DOT, xy=TOP.center )
        d.add( e.LINE, xy=TOP.center, d='up', l=d.unit/8, rgtlabel='Vcc' )
        d.draw()

![](img/SR-Latch.png)


-----------------------------------------------------------

## Defining New Elements

New elements can be defined by creating a python dictionary describing how the element should be drawn. An element can be made up of paths and/or shapes. A path is simply a list of xy coordinates which will be plotted with matplotlib. A shape is a predefined matplotlib patch, such as a circle (defined by center and radius).

Coordinates are all defined in element cooridnates, where the element begins
at [0,0] and is drawn from left to right. The drawing engine will then rotate
and translate the element to its final position. A standard resistor is
1 drawing unit long, and with default lead extension will become 3 units long.

Possible dictionary keys:

        name:  A name string for the element. Currently only used for testing.
        paths: A list of each path line in the element. For example, a capacitor
               has two paths, one for each capacitor "plate". On 2-terminal
               elements, the leads will be automatically extended away from the
               first and last points of the first path, and don't need to
               be included in the path.
        base:  Dictionary defining a base element. For example, the variable
               resistor has a base of resistor, then adds an additional path.
        shapes: A list of shape dictionaries.
                'shape' key can be [ 'circle', 'poly', 'arc', 'arrow' ]
                Other keys depend on the shape as follows.
                circle:
                    'center': xy center coordinate
                    'radius': radius of circle
                    'fill'  : [True, False] fill the circle
                    'fillcolor' : color for fill
                poly:
                    'xy' : List of xy coordinates defining polygon
                    'closed': [True, False] Close the polygon
                    'fill'  : [True, False] fill the polygon
                    'fillcolor' : color for fill
                arc:
                    'center' : Center coordinate of arc
                    'width', 'height': width and height of arc
                    'theta1' : Starting angle (degrees)
                    'theta2' : Ending angle (degrees)
                    'angle'  : Rotation angle of entire arc
                    'arrow'  : ['cw', 'ccw'] Add an arrowhead, clockwise or counterclockwise
                arrow:
                    'start'  : start of arrow
                    'end'    : end of arrow
                    'headwidth', 'headlength': width and length of arrowhead
        theta: Default angle (in degrees) for the element. Overrides the current
               drawing angle.
        anchors: A dictionary defining named positions within the element. For
                 example, the NFET element has a 'source', 'gate', and 'drain'
                 anchor. Each anchor will become an attribute of the element class
                 which can then be used for connecting other elements.
        extend: [True, False] Extend the leads to fill the full element length.
        move_cur: [True, False] Move the drawing cursor location after drawing.
        color: A matplotlib-compatible color for the element. Examples include
               'red', 'blue', '#34ac92'
        drop: Final location to leave drawing cursor.
        lblloc: ['top', 'bot', 'lft', 'rgt'] default location for text label.
                Defaults to 'top'.
        lblofst: Default distance between element and text label.
        labels: List of (label, pos) tuples defining text labels to always draw
                in the element.


Using the 'base' key, a new element can be defined as an extension of some base element. As an example, let's define a sinusoidal voltage source (the SOURCE_SIN element). It can be based on a SOURCE element, with the addition of a path to draw a sine wave inside the circle. A path can be created using standard numpy processing, so first we'll make a sine wave path. Since the circle is centered at [.5,0], center the sine wave there too:

        sin_y = np.linspace(.25,.75,num=25) - 0.5
        sin_x = .2 * np.sin((sin_y-.25)*np.pi*2/.5) + 0.5
        sin_path = np.transpose(np.vstack((sin_x,sin_y)))

Then define the element dictionary. It's just a SOURCE element with an additional path:

        SOURCE_SIN = {
            'name'  : 'SOURCE_SIN',
            'base'  : SOURCE,
            'paths' : [ sin_path ]
            }
