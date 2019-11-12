<link rel="stylesheet" href="css/codehilite.css">

## SchemDraw

SchemDraw is a python package for producing high-quality electrical circuit schematic diagrams. Typical usage:

    :::python
    import SchemDraw
    import SchemDraw.elements as e
    d = SchemDraw.Drawing()
    V1 = d.add(e.SOURCE_V, label='10V')
    d.add(e.RES, d='right', label='100K$\Omega$')
    d.add(e.CAP, d='down', botlabel='0.1$\mu$F')
    d.add(e.LINE, to=V1.start)
    d.add(e.GND)
    d.draw()
    d.save('testschematic.eps')

![](img/testschematic.svg)


### Gallery

A [gallery of circuits](gallery.html) is here, in addition to the examples on the following pages.


### Usage in Jupyter Notebook

Using a Jupyter Notebook in inline mode is recommended for the easy creation of these diagrams. 
Images will look best when saved in a vector format, such as svg, eps, or pdf.
Place this code at the very beginning of the notebook, *before* importing SchemDraw:

    :::python
    %matplotlib inline
    %config InlineBackend.figure_format = 'svg'


### Installation

SchemDraw can be run under Python 2 or Python 3, and requires the numpy and matplotlib packages.

SchemDraw can be installed from pip using

    :::bash
    pip install SchemDraw
    
SchemDraw can also be installed from conda using

    :::bash
    conda install -c jangenoe SchemDraw

or directly by downloading the package and running

    :::bash
    python setup.py install


### Usage

See the [usage page](usage.html).


### Examples

[Some additional examples, with source code.](examples.html)

-----------------------------------------------------------

### Schematic Components

Schematic elements are defined in several modules categorized by functional type:

[Basic Electrical Elements](elements.html)

[Logic Gates](logic.html)

[Flowcharting Symbols](flowcharts.html)

[Signal Processing](signals.html)


-----------------------------------------------------------

### Links

Source code git repository and issue tracker: [https://bitbucket.org/cdelker/schemdraw](https://bitbucket.org/cdelker/schemdraw)

This documentation available online: [https://cdelker.bitbucket.io/SchemDraw/](https://cdelker.bitbucket.io/SchemDraw/)