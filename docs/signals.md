<link rel="stylesheet" href="css/codehilite.css">

## Signal Processing Elements

Signal processing elements are defined in `SchemDraw.dsp`. Import them with:

    :::python
    from SchemDraw import dsp

Because each element may have multiple connections in and out, these elements
do not automatically extend "leads", so they must be manually connected with
LINE elements. The square elements define anchors 'N', 'S', 'E', and 'W' for
the four directions. Circle-based elements also includ 'NE', 'NW', 'SE', and 'SW'
anchors. Other elements, such as AMP, define 'in' and 'out' anchors when appropriate.

The ARROWHEAD element is useful to show signal flow.

![Signal Processing Components](img/dsp.svg)


Labels are placed in the center of the element. The generic BOX and CIRCLE element can
be used with a label to define other operations. For example, an integrator
may be created using 

    :::python
    d.add(dsp.BOX, label='$\int$')


------------------------------------------------------
[Return to SchemDraw documentation index](index.html)