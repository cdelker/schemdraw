<link rel="stylesheet" href="css/codehilite.css">

## Flowcharts with SchemDraw

SchemDraw provides basic flowcharting abilities. Flowchart blocks are SchemDraw
elements that can be created using the functions in the `SchemDraw.flow` module.
These functions define the width and height of the flowchart block. They must
be manually sized to fit the label text.

![Flowchart Functions](img/flowcharts.svg)

All flowchart symbols have four anchors named 'N', 'S', 'E', and 'W' for the
four directions. The `blackbox` function can be used with the flowchart elements
to create blocks with multiple inputs/outputs per side.

### Connecting blocks

Flowchart elements do not have "leads" like electrical elements, so they 
must be connected with LINE elements. The ARROWHEAD element can be used to
show flow direction.


### Decisions

To label the decision branches, the `SchemDraw.flow.decision` function takes the
`responses` parameter, a dictionary of responses for each direction. For example:

    :::python
    decision = flow.decision(responses={'W': 'Yes', 'E': 'No', 'S': 'Maybe'})

![Flowchart decisions](img/flowdecision.svg)


### Example

For a simple example, we re-create an [XKCD flowchart](https://xkcd.com/1195/) consisting
of a single decision block:

    :::python 
    d = SchemDraw.Drawing()
    d.add(flow.start(2, 1.5), label='START')
    d.add(flow.LINE, d='down', l=d.unit/3)
    d.add(flow.ARROWHEAD)
    d.add(flow.decision(5.5, 4, responses={'S': 'YES'}), label='Hey, wait,\nthis flowchart\nis a trap!')
    d.add(flow.LINE, d='down', l=d.unit/4)
    d.add(flow.LINE, d='right', l=d.unit*1.1)
    d.add(flow.LINE, d='up', toy=h.E)
    d.add(flow.LINE, d='left', tox=h.E)
    d.add(flow.ARROWHEAD)
    d.draw()

![Flowchart Example, XKCD-1195](img/xkcd1195.svg)


------------------------------------------------------
[Return to SchemDraw documentation index](index.html)