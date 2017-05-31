#!/bin/bash
# Build HTML files from markdown. Requires python-markdown and pygments.

python -m markdown -x codehilite index.md > index.html
python -m markdown -x codehilite gallery.md > gallery.html
