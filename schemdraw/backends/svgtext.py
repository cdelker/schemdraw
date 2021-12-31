''' Convert strings into SVG <text> elements, including some basic
    Latex-like math markup and formatting.

    The math only covers the most common cases in encountered
    electrical schematics:
        - Superscripts
        - Subscripts
        - Overline
        - Greek symbols

    This module also approximates the size of text to get bounding boxes
    and rotation centers.
'''

from __future__ import annotations

from xml.etree import ElementTree as ET
import string
import re

from ..util import Point, rotate
from ..types import Halign, Valign, RotationMode


# Conversion from Latex codes to unicode characters.
# Note: keys must include escaping \ for use in regex.
textable = {
    r'\\Gamma': 'Γ',
    r'\\Delta': 'Δ',
    r'\\Theta': 'Θ',
    r'\\Lambda': 'Λ',
    r'\\Xi': 'Ξ',
    r'\\Pi': 'Π',
    r'\\Sigma': 'Σ',
    r'\\Upsilon': 'Υ',
    r'\\Phi': 'Φ',
    r'\\Psi': 'Ψ',
    r'\\Omega': 'Ω',
    r'\\alpha': 'α',
    r'\\beta': 'β',
    r'\\gamma': 'γ',
    r'\\delta': 'δ',
    r'\\epsilon': 'ϵ',
    r'\\varepsilon': 'ε',
    r'\\zeta': 'ζ',
    r'\\eta': 'η',
    r'\\theta': 'θ',
    r'\\vartheta': 'ϑ',
    r'\\iota': 'ι',
    r'\\kappa': 'κ',
    r'\\lambda': 'λ',
    r'\\mu': 'μ', # \u03BC - "Greek small letter mu" (not \uB5 micro sign)
    r'\\nu': 'ν',
    r'\\xi': 'ξ',
    r'\\omicron': 'ο',
    r'\\pi': 'π',
    r'\\varpi': 'ϖ',
    r'\\rho': 'ρ',
    r'\\sigma': 'σ',
    r'\\tau': 'τ',
    r'\\upsilon': 'υ',
    r'\\phi': 'ϕ',
    r'\\varphi': 'φ',
    r'\\chi': 'χ',
    r'\\psi': 'ψ',
    r'\\omega': 'ω',
    r'\\pm': '±',
    r'\\mp': '∓',
    r'\\times': '×',
    r'\\div': '÷',
    r'\\neq': '≠',
    r'\\leq': '≤',
    r'\\geq': '≥',
    r'\\ll': '≪',
    r'\\gg': '≫',
    r'\\subset': '⊂',
    r'\\subseteq': '⊆',
    r'\\sum': '∑',
    r'\\prod': '∏',
    r'\\coprod': '∐',
    r'\\int': '∫',
    r'\\iint': '∬',
    r'\\iiint': '∭',
    r'\\oint': '∮',
    r'\\infty': '∞',
    r'\\nabla': '∇',
    r'\\Re': 'ℜ',
    r'\\Im': 'ℑ',
    r'\\angle': '∠',
    r'\\measuredangle': '∡',
    r'\\mho': '℧',
    r'\\partial': '∂',
    r'\\mathring{A}': 'Å',
    r'\\hbar': 'ℏ',
    r'\^{\\circ}': '°',
    r'\^\{0\}': '⁰',
    r'\^\{1\}': '¹',
    r'\^\{2\}': '²',
    r'\^\{3\}': '³',
    r'\^\{4\}': '⁴',
    r'\^\{5\}': '⁵',
    r'\^\{6\}': '⁶',
    r'\^\{7\}': '⁷',
    r'\^\{8\}': '⁸',
    r'\^\{9\}': '⁹',
    r'_\{0\}': '₀',
    r'_\{1\}': '₁',
    r'_\{2\}': '₂',
    r'_\{3\}': '₃',
    r'_\{4\}': '₄',
    r'_\{5\}': '₅',
    r'_\{6\}': '₆',
    r'_\{7\}': '₇',
    r'_\{8\}': '₈',
    r'_\{9\}': '₉',
    r'\^0': '⁰',
    r'\^1': '¹',
    r'\^2': '²',
    r'\^3': '³',
    r'\^4': '⁴',
    r'\^5': '⁵',
    r'\^6': '⁶',
    r'\^7': '⁷',
    r'\^8': '⁸',
    r'\^9': '⁹',
    r'_0': '₀',
    r'_1': '₁',
    r'_2': '₂',
    r'_3': '₃',
    r'_4': '₄',
    r'_5': '₅',
    r'_6': '₆',
    r'_7': '₇',
    r'_8': '₈',
    r'_9': '₉'}

# Numbers have unique unicode sub/superscripts.
# Some letters do, but unfortunately not all
numsubscripts = {
    '0': '₀',
    '1': '₁',
    '2': '₂',
    '3': '₃',
    '4': '₄',
    '5': '₅',
    '6': '₆',
    '7': '₇',
    '8': '₈',
    '9': '₉'}
numsuperscripts = {
    '0': '⁰',
    '1': '¹',
    '2': '²',
    '3': '³',
    '4': '⁴',
    '5': '⁵',
    '6': '⁶',
    '7': '⁷',
    '8': '⁸',
    '9': '⁹'}


def replacelatex(text: str) -> str:
    ''' Replace latex math codes with unicode equivalents '''
    for k, v in textable.items():
        text = re.sub(k, v, text)
    return text


def mathtextsvg(text: str) -> ET.Element:
    ''' Convert any math string delimited by $..$ into a <tspan> element
        that can be used in <text>

        Args:
            text: The text to convert
    '''
    text = text.replace('>', '%gt;').replace('<', '$lt;')
    tokens = re.split(r'(\$.*?\$)', text)
    svgtext = ''
    for t in tokens:
        if not (t.startswith('$') and t.endswith('$')):
            svgtext += t
            continue

        t = t[1:-1]
        t = replacelatex(t)

        # Find superscripts within {}
        sups = re.split(r'(\^\{.*?\})', t)
        for sup in sups:
            if sup.startswith('^'):
                chrs = sup[2:-1]
                if chrs.isnumeric():
                    chrs = ''.join([numsuperscripts[c] for c in chrs])
                    t = t.replace(sup, chrs)
                else:
                    t = t.replace(sup, f'<tspan baseline-shift="super" font-size="smaller">{chrs}</tspan>')
        # Find superscripts single char
        sups = re.split(r'(\^.)', t)
        for sup in sups:
            if sup.startswith('^'):
                t = t.replace(sup, f'<tspan baseline-shift="super" font-size="smaller">{sup[1]}</tspan>')

        # Find subscripts within {}
        sups = re.split(r'(\_\{.*?\})', t)
        for sup in sups:
            if sup.startswith('_'):
                chrs = sup[2:-1]
                if chrs.isnumeric():
                    chrs = ''.join([numsubscripts[c] for c in chrs])
                    t = t.replace(sup, chrs)
                else:
                    t = t.replace(sup, f'<tspan baseline-shift="sub" font-size="smaller">{chrs}</tspan>')
        # Find subscripts single char
        sups = re.split(r'(\_.)', t)
        for sup in sups:
            if sup.startswith('_'):
                t = t.replace(sup, fr'<tspan baseline-shift="sub" font-size="smaller">{sup[1]}</tspan>')

        # \sqrt
        sups = re.split(r'(\\sqrt{.*})', t)
        for sup in sups:
            if sup.startswith(r'\sqrt{'):
                t = t.replace(sup, fr'√\overline{{{sup[6:-1]}}}')

        # \overline
        sups = re.split(r'(\\overline{.*})', t)
        for sup in sups:
            if sup.startswith(r'\overline{'):
                t = t.replace(sup, f'<tspan text-decoration="overline">{sup[10:-1]}</tspan>')
        svgtext += t
        
    svgtext = '<tspan>' + svgtext + '</tspan>'
    return ET.fromstring(svgtext)


def string_width(st: str, fontsize: float=12, font: str='Arial') -> float:
    ''' Estimate string width based on individual characters

        Args:
            st: string to estimate
            fontsize: font size
            font: font family

        Returns:
            Estimated width of string
    '''
    # adapted from https://stackoverflow.com/a/16008023/13826284
    # The only alternative is to draw the string to an actual canvas

    size = 0  # in milinches
    if 'times' in font.lower() or ('serif' in font.lower() and 'sans' not in font.lower()):
        # Estimates based on Times Roman
        for s in st:
            if s in 'lij:.,;t': size += 47
            elif s in '|': size += 37
            elif s in '![]fI/\\': size += 55
            elif s in '`-(){}r': size += 60
            elif s in 'sJ°': size += 68
            elif s in '"zcae?1': size += 74
            elif s in '*^kvxyμbdhnopqug#$_α' + string.digits: size += 85
            elif s in '#$+<>=~FSP': size += 95
            elif s in 'ELZT': size += 105
            elif s in 'BRC': size += 112
            elif s in 'DAwHUKVXYNQGO': size += 122
            elif s in '&mΩ': size += 130
            elif s in '%': size += 140
            elif s in 'MW@∠': size += 155
            else: size += 60

    else:  # Arial, or other sans fonts
        for s in st:
            if s in 'lij|\' ': size += 37
            elif s in '![]fI.,:;/\\t': size += 50
            elif s in '`-(){}r"': size += 60
            elif s in '*^zcsJkvxyμ°': size += 85
            elif s in 'aebdhnopqug#$L+<>=?_~FZTα' + string.digits: size += 95
            elif s in 'BSPEAKVXY&UwNRCHD': size += 112
            elif s in 'QGOMm%@Ω': size += 140
            elif s in 'W∠': size += 155
            else: size += 75
    return size * 72 / 1000.0 * (fontsize/12)  # to points


def text_approx_size(text: str, font: str='Arial', size: float=16) -> tuple[float, float, float]:
    ''' Get approximate width, height and line spacing of multiline text

        Does not account for descent or ascent of text (for example,
        a "g" going below the baseline), or for superscripts/subscripts.

        Args:
            text: The text to approximate
            font: Font family, either Arial or Times
            size: Font point size

        Returns:
            w: Width of text box, in points
            h: Height of text box, in points
            dy: Spacing between lines of text, in points
    '''
    w = 0.
    h = 0.
    lines = text.splitlines()
    dy = size if len(lines) > 1 else size * 0.8
    for line in lines:
        math = ' '.join(mathtextsvg(line).itertext())  # itertext strips all the tags
        w = max(w, string_width(math, fontsize=size, font=font))
        h += dy
    return w, h, dy


def text_tosvg(text: str, x: float, y: float, font: str='Arial', size: float=16, color: str='black',
               halign: Halign='center', valign: Valign='center',
               rotation: float=0, rotation_mode: RotationMode='anchor',
               testmode: bool=False) -> ET.Element:
    ''' Convert text to svg <text> tag.

        Args:
            text: The text to convert
            x: Anchor x position, points
            y: Anchor y position, points
            font: Font family
            size: Font point size
            color: Font color
            halign: Horizontal alignment (left, center, right)
            valign: Vertical alignment (top, center, bottom)
            rotation: Rotation angle, degrees
            rotation_mode: Rotation mode (anchor, default), see
            Matplotlib https://matplotlib.org/3.1.1/gallery/text_labels_and_annotations/demo_text_rotation_mode.html
            testmode: For testing, draw rectable around text bounding box
                and dot at text anchor

        Returns:
            Text formatted in svg <text> element string.
    '''
    w, h, dy = text_approx_size(text, font=font, size=size)

    textelm = ET.Element('text')
    
    for line in text.splitlines():
        tspan = mathtextsvg(line)
        tspan.set('x', str(x))
        tspan.set('dy', str(dy))
        textelm.append(tspan)

    boxx = x
    if halign == 'center':
        boxx -= w/2
    elif halign == 'right':
        boxx -= w

    ytext = y
    if valign == 'center':
        ytext += h/2
    elif valign == 'top':
        ytext += h
    anchor = {'center': 'middle', 'left': 'start', 'right': 'end'}.get(halign, 'start')

    org = Point((x, y))
    p1 = Point((boxx, ytext)).rotate(-rotation, org)
    p2 = Point((boxx, ytext-h)).rotate(-rotation, org)
    p3 = Point((boxx+w, ytext-h)).rotate(-rotation, org)
    p4 = Point((boxx+w, ytext)).rotate(-rotation, org)

    # Bounding box, unshifted for "default" rotation mode
    pxmin = min(p1[0], p2[0], p3[0], p4[0])
    pxmax = max(p1[0], p2[0], p3[0], p4[0])
    pymin = min(p1[1], p2[1], p3[1], p4[1])
    pymax = max(p1[1], p2[1], p3[1], p4[1])

    dx = dy = 0
    if rotation != 0 and rotation_mode == 'default':
        if halign == 'left':
            dx = x-pxmin
        elif halign == 'center':
            dx = x-(pxmax+pxmin)/2
        else:  # right
            dx = x-pxmax
        if valign == 'top':
            dy = y-pymin
        elif valign == 'center':
            dy = y-(pymax+pymin)/2
        else:  # bottom
            dy = y-pymax
        xform = f'translate({dx} {dy}) rotate({-rotation} {x} {y})'
    else:
        xform = f'rotate({-rotation} {x} {y})'

    textelm.set('x', str(x))
    textelm.set('y', str(ytext-h))
    textelm.set('fill', color)
    textelm.set('font-size', str(size))
    textelm.set('font-family', font)
    textelm.set('text-anchor', anchor)
    textelm.set('transform', xform)

    if testmode:
        pxmin += dx   # Final bounding box
        pxmax += dx
        pymin += dy
        pymax += dy

        topelm = ET.Element('g')  # Put everything in a group
        topelm.append(textelm)
        box = ET.SubElement(topelm, 'rect')
        box.set('x', str(boxx))
        box.set('y', str(ytext-h))
        box.set('width', str(w))
        box.set('height', str(h))
        box.set('style', 'stroke:blue;stroke-width:1;fill:none')
        box.set('transform', xform)
        circ = ET.SubElement(topelm, 'circle')
        circ.set('cx', str(x))
        circ.set('cy', str(y))
        circ.set('r', '1.5')
        circ.set('stroke', 'red')
        circ.set('fill', 'red')
        rect = ET.SubElement(topelm, 'rect')
        rect.set('x', str(pxmin))
        rect.set('y', str(pymin))
        rect.set('width', str(pxmax-pxmin))
        rect.set('height', str(pymax-pymin))
        rect.set('style', 'stroke:red;stroke-width:1;fill:none')
        textelm = topelm

    return textelm
