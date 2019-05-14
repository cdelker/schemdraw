#!/bin/bash
# Build HTML files from markdown. Requires python-markdown and pygments.

python -m markdown -x codehilite index.md > index.html
python -m markdown -x codehilite usage.md > usage.html
python -m markdown -x codehilite gallery.md > gallery.html
python -m markdown -x codehilite elements.md > elements.html
python -m markdown -x codehilite examples.md > examples.html
python -m markdown -x codehilite flowcharts.md > flowcharts.html
python -m markdown -x codehilite logic.md > logic.html
python -m markdown -x codehilite signals.md > signals.html