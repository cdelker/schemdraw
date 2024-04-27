''' Load Fritzing part files as Schemdraw elements

    See https://github.com/fritzing/fritzing-app/wiki/2.1-Part-file-format

    Only extracts the breadboard view (schematic, PCB, and icon are not used)
'''
from __future__ import annotations
from typing import Optional
import re
import warnings
import zipfile
from io import BytesIO
from collections import namedtuple
from xml.etree import ElementTree as ET

from ..util import Point
from ..backends import matrix
from ..elements import ElementImage
from .pictorial import parse_size_to_units


FritzingInfo = namedtuple('FritzingInfo', 'author version title url label date description')


def find_transforms(element, tree):
    '''' Find all 'transform' tags in tree leading up to element '''
    parents = {c: p for p in tree.iter() for c in p}
    xforms = []
    def _find(elm):
        if (xf := elm.get('transform')):
            xforms.append(xf)
        p = parents.get(elm)
        if p is not None:
            _find(p)
    _find(element)
    return xforms


def extract(elm: ET.Element, tag: str) -> Optional[str]:
    ''' Extract the tag's text from the element, returning None if tag 
        doesn't exist
    '''
    item = elm.find(tag)
    return item.text if item is not None else None


def fritz_parts(fname: str) -> list[str | None]:
    ''' List titles of all Fritzing parts in the file '''
    zip = zipfile.ZipFile(fname)
    parts = [f.filename for f in zip.infolist() if f.filename.endswith('.fzp')]
    names = []
    for part in parts:    
        module = ET.fromstring(zip.read(part))
        title = module.find('title')
        if title is not None:
            names.append(title.text)
    return names


class FritzingPart(ElementImage):
    ''' Load a Fritzing Part File as a Schemdraw Element

        Anchors will be extracted from the Part definition file.
        Note some anchors are not valid Python identifiers and
        therefore must be accessed through the Element.absanchors
        dictionary rather than an attribute of the element instance.

        Args:
            fname: Filename of fritzing .fzpz archive
            partname: Name of part within the file. Use `listparts` to
                show all names. If not provided, first part is drawn.
            partidx: Index of part within the file. If not provided,
                first part is drawn. Overrides `partname`.
            scale: Scale factor
    '''
    def __init__(self, fname: str,
                 partname: Optional[str] = None,
                 partidx: Optional[int] = None,
                 scale: float = 1.0):
        self.fname = fname
        self.zip = zipfile.ZipFile(self.fname)
        parts = [f.filename for f in self.zip.infolist() if f.filename.endswith('.fzp')]

        if partidx is not None:
            part = parts[partidx]
        elif partname is not None:
            part = parts[fritz_parts(fname).index(partname)]
        else:
            part = parts[0]

        self.module = ET.fromstring(self.zip.read(part))
        self.info = FritzingInfo(
            author=extract(self.module, 'author'),
            version=extract(self.module, 'version'),
            title=extract(self.module, 'title'),
            url=extract(self.module, 'url'),
            label=extract(self.module, 'label'),
            date=extract(self.module, 'date'),
            description=extract(self.module, 'description'),
        )

        views = self.module.find('views')
        if views is None:
            raise ValueError('Part has no views')

        breadboard = views.find('breadboardView')
        if breadboard is None:
            raise ValueError('Part has no breadboardView')

        layers = breadboard.find('layers')
        if layers is None:
            raise ValueError('Part breadboardView has no layers')

        svgfile = layers.get('image', '')
        image = self.zip.read('svg.' + svgfile.replace('/', '.'))
        imagebuf = BytesIO(image)
        self.imagexml = ET.fromstring(image)

        width = self.imagexml.get('width', '0')
        height = self.imagexml.get('height', '0')
        self.width_units = parse_size_to_units(width) * scale
        self.height_units = parse_size_to_units(height) * scale

        if self.width_units == 0 or self.height_units == 0:
            warnings.warn('Part has 0 width or height')

        viewbox = self.imagexml.get('viewBox')
        if viewbox:
            _, _, vieww, viewh = viewbox.split()
            self.vieww = float(vieww)
            self.viewh = float(viewh)
            self._scale = self.width_units / self.vieww
        else:
            # Some examples don't have a viewBox, assume same as width/height
            try:
                width_f = float(width)
            except ValueError:
                width_f = float(width[:-2])
            self._scale = self.width_units / width_f

        super().__init__(image=imagebuf, imgfmt='svg', width=self.width_units, height=self.height_units)
        self._findanchors()

    def _anchor_position(self, name: str, anchorelm: ET.Element) -> tuple[Optional[float], Optional[float]]:
        ''' Extract position of the anchor element from its SVG tag '''
        matrices: list[matrix.Matrix3x3] = []
        anchorx: Optional[float] = None
        anchory: Optional[float] = None

        # Anchor is SVG tag, pick out the exact point
        if anchorelm.tag.endswith('circle') or anchorelm.tag.endswith('ellipse'):
            anchorx = float(anchorelm.get('cx', '0'))
            anchory = float(anchorelm.get('cy', '0'))
        elif anchorelm.tag.endswith('rect'):
            rectwidth = float(anchorelm.get('width', '0'))
            rectheight = float(anchorelm.get('height', '0'))
            anchorx = float(anchorelm.get('x', '0')) + rectwidth/2
            anchory = float(anchorelm.get('y', '0')) + rectheight/2
        elif anchorelm.tag.endswith('polygon'):
            pointlist = anchorelm.get('points', '')
            pointstrs = re.split(',| ', pointlist)
            points = [float(p) for p in pointstrs if p]
            xpoints = points[::2]
            ypoints = points[1::2]
            anchorx = (max(xpoints) + min(xpoints)) / 2
            anchory = (max(ypoints) + min(ypoints)) / 2
        elif anchorelm.tag.endswith('path'):
            path = anchorelm.get('d', '')
            path = path.replace('-', ' -')  # Some negative numbers don't have space before
            pointstrs = re.split(',| |M|L|H|V|Q|C|A|Z|m|l|h|v|q|c|a|z', path)
            # First item in list is 'M' directive, or similar
            # Let anchor just be the first point in the path.
            # Could be that center of path was intended, but that will get weird
            # with Bezier control points, etc.
            # NOTE: relative (lowercase m) moves won't work correctly
            pointstrs = [p for p in pointstrs if p]
            anchorx = float(pointstrs[0])
            anchory = float(pointstrs[1])
        elif anchorelm.tag.endswith('g'):
            # Set anchor based on first element within the group
            if len(anchorelm) > 0:
                return self._anchor_position(name, anchorelm[0])
            else:
                warnings.warn(f'Connector {name} is empty')
                return None, None
        else:
            warnings.warn(f'Connector {name} unimplemented connector tag: {anchorelm.tag}')
            return None, None

        # Pick out SVG transforms leading up to the anchor element
        xforms = find_transforms(anchorelm, self.imagexml)
        for xf in xforms:
            for xfmode, value in re.findall(r'(.*?)\((.*?)\)', xf):
                xfmode = xfmode.strip()
                valuestrs = re.split(',| ', value)
                values = [float(v) for v in valuestrs if v]

                if xfmode == 'translate':
                    m = matrix.matrix_translate(*values)
                elif xfmode == 'rotate':
                    m = matrix.matrix_rotate(*values)
                elif xfmode == 'scale':
                    m = matrix.matrix_scale(*values)
                elif xfmode == 'skewX':
                    m = matrix.matrix_skewx(values[0])
                elif xfmode == 'skewY':
                    m = matrix.matrix_skewy(values[0])
                elif xfmode == 'matrix':
                    m = matrix.matrix(*values)
                else:
                    raise NotImplementedError(f'Transform {xfmode} not implemented')
                matrices.append(m)

        # Apply the transformation matrices and scale to drawing units
        anchorx, anchory = matrix.transform_all(Point((anchorx, anchory)), matrices)
        anchorx = anchorx * self._scale
        anchory = self.height_units - anchory * self._scale
        return anchorx, anchory

    def _findanchors(self):
        ''' Find anchor positions '''
        for connector in self.module.find('connectors'):
            name = connector.get('name')
            breadboard = connector.find('views').find('breadboardView')
            svgid = breadboard.find('p').get('svgId')

            anchorelm = self.imagexml.findall(f".//*[@id='{svgid}']")
            if len(anchorelm) == 0:
                anchorelm = self.imagexml.findall(f".//*[@id='{svgid}pin']")

            if len(anchorelm) == 0:
                return

            anchorelm = anchorelm[0]
            anchorx, anchory = self._anchor_position(name, anchorelm)

            if anchorx is not None and anchory is not None:
                self.anchors[name] = Point((anchorx, anchory))

