# Contributing to schemdraw

Thank you for your interest in contributing to schemdraw! Contributions of all kinds are welcome: bug reports, feature requests, documentation improvements, new elements, and code fixes.

## Reporting bugs

Report bugs and feature requests on the [Issue Tracker](https://github.com/cdelker/schemdraw/issues). When reporting a bug, please include:

- A minimal code example that reproduces the issue
- The schemdraw version (`schemdraw.__version__`)
- Your Python version and operating system
- The full traceback if an exception occurred
- Expected vs. actual behavior

## Development setup

1. Fork the repository and clone your fork:

```bash
git clone https://github.com/YOUR_USERNAME/schemdraw.git
cd schemdraw
```

2. Create a virtual environment and install in development mode:

```bash
python -m venv .venv
source .venv/bin/activate    # Linux/macOS
# .venv\Scripts\activate     # Windows

pip install -e .
pip install -e ".[matplotlib,svgmath]"
```

3. Install testing and documentation dependencies:

```bash
pip install pytest nbval ipykernel
python -m ipykernel install --user --name python3 --display-name "Python 3 (ipykernel)"
```

## Running tests

The test suite uses Jupyter notebooks validated through `nbval`, plus standalone Python test scripts:

```bash
# Run the full test suite
python -m pytest --nbval-lax test/ -q

# Run a specific test notebook
python -m pytest --nbval-lax test/test_elements.ipynb

# Run a standalone test script
python test/test_svgtext.py
```

All tests must pass before submitting a pull request.

## Code style

- Maximum line length: **120 characters** (configured in `.flake8`)
- Follow [PEP 8](https://peps.python.org/pep-0008/) conventions
- Use type annotations where practical (the package ships with `py.typed`)
- Allowed short variable names: `i, j, k, x, y, dx, dy, lw, ls, at, xy, ax` (configured in `.pylintrc`)

## Submitting a pull request

1. Create a feature branch from `master`:

```bash
git checkout -b fix/short-description master
```

2. Make your changes. For bug fixes, include a test that fails without the fix.

3. Run the full test suite and confirm zero failures:

```bash
pip install .
python -m pytest --nbval-lax test/ -q
```

4. Commit with a clear message describing what changed and why:

```bash
git commit -m "Fix short description of the change"
```

5. Push and open a pull request against `master`.

### What to include in a pull request

- **Bug fixes**: a test that reproduces the bug, plus the fix.
- **New elements**: add the element to the appropriate `schemdraw/elements/` module, include it in the relevant test notebook (e.g., `test/test_elements.ipynb`), and add documentation in `docs/elements/`.
- **Documentation changes**: if you modify behavior, update the corresponding `.rst` file in `docs/`.

## Adding a new element

1. Identify the appropriate module in `schemdraw/elements/` (e.g., `twoterm.py` for two-terminal components, `opamp.py` for op-amps).
2. Define the element class, inheriting from `Element`, `Element2Term`, or another base class.
3. Define the element geometry using segments (`Segment`, `SegmentCircle`, `SegmentArc`, etc.).
4. Define anchors for connection points.
5. Add the element to the module's `__all__` list if applicable.
6. Add an entry in the test notebooks and in `docs/elements/`.

See existing elements for reference -- start with a simple one like `Resistor` in `twoterm.py`.

## Building the documentation

The documentation is built with [Sphinx](https://www.sphinx-doc.org/) and hosted on [Read the Docs](https://schemdraw.readthedocs.io/en/stable/):

```bash
pip install -r docs/requirements.txt
cd docs
make html
```

The generated HTML will be in `docs/_build/html/`.

## Questions?

If you have questions about contributing, open an issue on the [Issue Tracker](https://github.com/cdelker/schemdraw/issues) -- we are happy to help.
