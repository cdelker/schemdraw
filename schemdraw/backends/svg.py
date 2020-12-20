''' SVG drawing backend for schemdraw '''

import os
import sys
import subprocess
import tempfile
import math

from ..util import Point
from . import svgtext


def isnotebook():
    ''' Determine whether code is running in Jupyter/interactive mode '''
    try:
        shell = get_ipython().__class__.__name__
        return shell == 'ZMQInteractiveShell'
    except NameError:
        return False


inline = isnotebook()


def getstyle(color=None, ls=None, lw=None, capstyle=None, joinstyle=None, fill=None):
    ''' Get style for svg element. Leave empty if property matches default '''
    # Note: styles are added to every SVG element, rather than in a global <style>
    # tag, since multiple images in one HTML page may share <styles>.
    s = ''
    if color:
        s += f'stroke:{color};'
    s += f'fill:{str(fill).lower()};'
    if lw:
        s += f'stroke-width:{lw};'
    dash = {'--': '7.4,3.2',
            'dashed': '7.4,3.2',
            ':': '2,3.3',
            'dotted': '2,3.3',
            '-.': '12.8,3.2,2,3.2',
            'dashdot': '12.8,3.2,2,3.2',
            }.get(ls, None)
    if dash is not None:
        s += f'stroke-dasharray:{dash};'
    if capstyle:
        s += f'stroke-linecap:{capstyle};'
    if joinstyle:
        s += f'stroke-linejoin:{joinstyle};'

    if s:
        s = f'style="{s}"'
    return s


class Figure(object):
    ''' Schemdraw figure drawn directly to SVG

        Parameters
        ----------
        bbox : schemdraw.segments.BBox
            Coordinate bounding box for drawing
        inches_per_unit : float
            Scale for the drawing
        showframe : bool
            Show frame around entire drawing
    '''
    # Each arrowhead gets its own id in svg <defs>
    # Make at the class level since multiple SVGs on a page
    # will reuse defs from an earlier drawing

    def __init__(self, bbox, **kwargs):
        self.svgelements = []  # List of tuples: (zorder, SVG elements text)
        self.showframe = kwargs.get('showframe', False)
        self.scale = 64.8 * kwargs.get('inches_per_unit', .5)  # Magic scale factor that matches what MPL did
        self.set_bbox(bbox)

    def set_bbox(self, bbox):
        ''' Set the bounding box '''
        self.bbox = bbox
        self.pxwidth = (self.bbox.xmax-self.bbox.xmin) * self.scale
        self.pxheight = (self.bbox.ymax-self.bbox.ymin) * self.scale
        self.pxwidth = max(5, self.pxwidth)
        self.pxheight = max(5, self.pxheight)

    def xform(self, x, y):
        ''' Convert x, y in user coords to svg pixel coords '''
        return x*self.scale, -y*self.scale

    def plot(self, x, y, color='black', ls='-', lw=2, fill='none',
             capstyle='round', joinstyle='round', zorder=2):
        ''' Plot a path '''
        s = '<path d="M {},{} '.format(*self.xform(x[0], y[0]))
        for xx, yy in zip(x[1:], y[1:]):
            if str(xx) == 'nan' or str(yy) == 'nan':
                s += 'M '
                continue
            elif not s.endswith('M '):
                s += 'L '
            xx, yy = self.xform(xx, yy)
            s += '{},{} '.format(xx, yy)

        s = s.strip() + '" '  # End path points
        s += getstyle(color=color, ls=ls, lw=lw, capstyle=capstyle, joinstyle=joinstyle, fill=fill)
        s += ' />'
        self.svgelements.append((zorder, s))

    def text(self, s, x, y, color='black', fontsize=14, fontfamily='sans-serif',
             rotation=0, halign='center', valign='center', rotation_mode='anchor', zorder=3):
        ''' Add text to the figure '''
        x, y = self.xform(x, y)
        texttag = svgtext.text_tosvg(s, x, y, font=fontfamily, size=fontsize,
                                     halign=halign, valign=valign, color=color,
                                     rotation=rotation, rotation_mode=rotation_mode, testmode=False)
        self.svgelements.append((zorder, texttag))

    def poly(self, verts, closed=True, color='black', fill='none', lw=2, ls='-',
             capstyle='round', joinstyle='round', zorder=1):
        ''' Draw a polygon '''
        if not closed:
            x = [v[0] for v in verts]
            y = [v[1] for v in verts]
            self.plot(x, y, color=color, fill=fill, lw=lw, ls=ls,
                      capstyle=capstyle, joinstyle=joinstyle, zorder=zorder)
        else:
            s = '<polygon points="'
            for xx, yy in verts:
                xx, yy = self.xform(xx, yy)
                s += '{},{} '.format(xx, yy)
            s += '" '
            s += getstyle(color=color, ls=ls, lw=lw, capstyle=capstyle, joinstyle=joinstyle, fill=fill)
            s += '/>'
            self.svgelements.append((zorder, s))

    def circle(self, center, radius, color='black', fill='none', lw=2, ls='-', zorder=1):
        ''' Draw a circle '''
        x, y = self.xform(*center)
        radius = radius * self.scale
        s = '<circle cx="{}" cy="{}" r="{}" '.format(x, y, radius)
        s += getstyle(color=color, lw=lw, fill=fill)
        s += '/>'
        self.svgelements.append((zorder, s))

    def arrow(self, x, y, dx, dy, headwidth=.2, headlength=.2,
              color='black', lw=2, zorder=1):
        ''' Draw an arrow '''
        x, y = self.xform(x, y)
        dx, dy = dx*self.scale, dy*self.scale
        headwidth = headwidth*self.scale
        headlength = headlength*self.scale

        # Draw arrow as path
        head = Point((x+dx, y-dy))
        tail = Point((x, y))
        fullen = math.sqrt(dx**2 + dy**2)
        theta = -math.degrees(math.atan2(dy, dx))

        finc = Point((fullen - headlength, 0)).rotate(theta) + tail
        fin1 = Point((fullen - headlength, headwidth/2)).rotate(theta) + tail
        fin2 = Point((fullen - headlength, -headwidth/2)).rotate(theta) + tail

        s = f'<path d="M {head[0]} {head[1]} '
        s += f'L {fin1[0]} {fin1[1]} '
        s += f'L {finc[0]} {finc[1]} '
        s += f'L {tail[0]} {tail[1]} '
        s += f'L {finc[0]} {finc[1]} '
        s += f'L {fin2[0]} {fin2[1]} Z" '
        s += getstyle(color=color, lw=lw, capstyle='miter', joinstyle='miter', fill=color)
        s += ' />'
        self.svgelements.append((zorder, s))
        return

    def arc(self, center, width, height, theta1=0, theta2=90, angle=0,
            color='black', lw=2, ls='-', zorder=1, arrow=None):
        ''' Draw an arc or ellipse, with optional arrowhead '''
        centerx, centery = self.xform(*center)
        width, height = width*self.scale, height*self.scale
        angle = -angle
        theta1 = -theta1
        theta2 = -theta2
        anglerad = math.radians(angle)

        theta1 = math.radians(theta1)
        theta2 = math.radians(theta2)
        t1 = math.atan2(width*math.sin(theta1), height*math.cos(theta1))
        t2 = math.atan2(width*math.sin(theta2), height*math.cos(theta2))
        while t1 < t2:
            t1 += 2*math.pi

        startx = centerx + width/2 * math.cos(t2)*math.cos(anglerad) - height/2 * math.sin(t2)*math.sin(anglerad)
        starty = centery + width/2 * math.cos(t2)*math.sin(anglerad) + height/2 * math.sin(t2)*math.cos(anglerad)
        endx = centerx + width/2 * math.cos(t1)*math.cos(anglerad) - height/2 * math.sin(t1)*math.sin(anglerad)
        endy = centery + width/2 * math.cos(t1)*math.sin(anglerad) + height/2 * math.sin(t1)*math.cos(anglerad)

        startx, starty = round(startx, 2), round(starty, 2)
        endx, endy = round(endx, 2), round(endy, 2)
        dx, dy = endx-startx, endy-starty

        s = ''
        if abs(dx) < .1 and abs(dy) < .1:
            # Full ellipse - can't be drawn with a single <path>
            # because when start/end points are the same it draws a dot.
            s += f'<ellipse cx="{centerx}" cy="{centery}" rx="{width/2}" ry="{height/2}"'
            if angle != 0:
                s += f' transform="rotate({angle} {centerx} {centery})"'
            s += f' stroke="{color}" stroke-width="{lw}" fill="none"/>'
            self.svgelements.append((zorder, s))

        else:
            flags = '1 1' if abs(t2-t1) >= math.pi else '0 1'
            s += f'<path d="M {startx} {starty}'
            s += f' a {width/2} {height/2} {angle} {flags} {dx} {dy}"'
            s += f' stroke="{color}" stroke-width="{lw}" fill="none"'
            s += '/>'
            self.svgelements.append((zorder, s))

        if arrow is not None:
            # Back to user coordinates
            width, height = width/self.scale, height/self.scale
            angle = -angle
            theta1 = -math.degrees(theta1)
            theta2 = -math.degrees(theta2)

            headlength = .25
            headwidth = .15

            x, y = math.cos(math.radians(theta2)), math.sin(math.radians(theta2))
            th2 = math.degrees(math.atan2((width/height)*y, x))
            x, y = math.cos(math.radians(theta1)), math.sin(math.radians(theta1))
            th1 = math.degrees(math.atan2((width/height)*y, x))
            if arrow == 'ccw':
                dx = math.cos(math.radians(th2+90)) * headlength
                dy = math.sin(math.radians(theta2+90)) * headlength
                s = [center[0] + width/2*math.cos(math.radians(th2)),
                     center[1] + height/2*math.sin(math.radians(th2))]
            else:
                dx = -math.cos(math.radians(th1+90)) * headlength
                dy = -math.sin(math.radians(th1+90)) * headlength
                s = [center[0] + width/2*math.cos(math.radians(th1)),
                     center[1] + height/2*math.sin(math.radians(th1))]

            s = Point(s).rotate(angle, center)
            darrow = Point((dx, dy)).rotate(angle)

            self.arrow(s[0], s[1], darrow[0], darrow[1], headwidth=headwidth,
                       headlength=headlength, color=color, lw=1, zorder=zorder)

    def save(self, fname, **kwargs):
        ''' Save the figure to a file '''
        svg = self.getimage().decode()
        with open(fname, 'w') as f:
            f.write(svg)

    def getimage(self, ext='svg'):
        ''' Get the image as SVG or PNG bytes array '''
        pad = 2
        x0 = self.bbox.xmin * self.scale - pad
        y0 = -self.bbox.ymax * self.scale - pad

        s = '<svg height="{}pt" width="{}pt" viewBox="{} {} {} {}">'.format(self.pxheight+2*pad, self.pxwidth+2*pad, x0, y0, self.pxwidth+2*pad, self.pxheight+2*pad)

        if self.showframe:
            s += f'<rect x="{x0}" y="{y0}" width="{self.pxwidth}" height="{self.pxheight}" style="fill:none; stroke-width:1; stroke:black;" />'

        elements = sorted(self.svgelements, key=lambda x: x[0])  # sort by zorder
        elements = [x[1] for x in elements]        
        s += '\n'.join(elements)
        s += '</svg>'
        return s.encode('utf-8')

    def _repr_svg_(self):
        ''' SVG representation for Jupyter '''
        return self.getimage().decode()

    def __repr__(self):
        return self.getimage().decode()

    def show(self):
        ''' Show drawing in default program, if not inline in Jupyter '''
        if not inline:
            handle, path = tempfile.mkstemp(suffix='.svg')
            with os.fdopen(handle, 'w') as f:
                f.write(self.getimage().decode())

            if sys.platform == 'win32':
                os.startfile(path)
            else:
                cmd = 'open' if sys.platform == 'darwin' else 'xdg-open'
                subprocess.call([cmd, path])
