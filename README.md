# schemdraw

[![PyPI version](https://img.shields.io/pypi/v/schemdraw.svg)](https://pypi.org/project/schemdraw/)
[![Python versions](https://img.shields.io/pypi/pyversions/schemdraw.svg)](https://pypi.org/project/schemdraw/)
[![Documentation Status](https://readthedocs.org/projects/schemdraw/badge/?version=stable)](https://schemdraw.readthedocs.io/en/stable/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Schemdraw is a Python package for producing high-quality electrical circuit schematic diagrams. Circuit elements are added one at a time, similar to how you might draw them by hand, using Python methods to set placement and orientation.

## Features

- **Electrical elements** -- resistors, capacitors, inductors, diodes, transistors, op-amps, sources, transformers, vacuum tubes, and more
- **Integrated circuits** -- configurable IC packages with arbitrary pin count and labeling
- **Logic gates** -- AND, OR, NOT, XOR, flip-flops, and multiplexers
- **Timing diagrams** -- digital waveforms with clock, data, and edge annotations
- **Signal processing** -- DSP blocks, filters, mixers, and amplifiers
- **Flowcharts** -- decision, process, and data blocks with automatic connectors
- **Pictorial elements** -- breadboard-style and Fritzing-compatible components
- **Multiple backends** -- Matplotlib (PNG, PDF, EPS) and native SVG output
- **Jupyter integration** -- renders inline in notebooks with no extra configuration
- **LaTeX-style math** -- label elements with superscripts, subscripts, and Greek symbols
- **Type hints** -- full type annotation support (`py.typed`)

## Installation

Install from PyPI:

```bash
pip install schemdraw
```

Optional dependencies for additional features:

```bash
# Matplotlib backend (PNG, PDF, EPS export)
pip install schemdraw[matplotlib]

# Math rendering in native SVG backend
pip install schemdraw[svgmath]
```

## Quick start

```python
import schemdraw
import schemdraw.elements as elm

with schemdraw.Drawing() as d:
    elm.Resistor().label('100K\u03A9')
    elm.Capacitor().down().label('0.1\u00B5F', loc='bottom')
    elm.Line().left()
    elm.Ground()
    elm.SourceV().up().label('10V')
```

Elements are placed in a chain: each new element starts where the previous one ended. Use `.up()`, `.down()`, `.left()`, `.right()` to set direction. Use `.at()` and `.anchor()` for precise positioning.

For more examples, see the [Gallery](https://schemdraw.readthedocs.io/en/stable/gallery/index.html).

## Documentation

Full documentation is available at [schemdraw.readthedocs.io](https://schemdraw.readthedocs.io):

- [Getting Started](https://schemdraw.readthedocs.io/en/stable/usage/start.html) -- installation and first circuit
- [Placement & Positioning](https://schemdraw.readthedocs.io/en/stable/usage/placement.html) -- how elements connect
- [Element Reference](https://schemdraw.readthedocs.io/en/stable/elements/electrical.html) -- all available components
- [Gallery](https://schemdraw.readthedocs.io/en/stable/gallery/index.html) -- example circuits and diagrams

## Contributing

Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on reporting issues, submitting pull requests, and setting up a development environment.

## License

Schemdraw is licensed under the [MIT License](LICENSE.txt).
