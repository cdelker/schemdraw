''' Matplotlib drawing backend for schemdraw '''

from __future__ import annotations
from typing import Optional, Sequence, BinaryIO
from io import BytesIO
import math

import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from matplotlib import font_manager, transforms
from matplotlib.patches import Arc, Rectangle, PathPatch, Path # type: ignore

from .. import util
from ..types import Capstyle, Joinstyle, Linestyle, BBox, XY

inline = 'inline' in matplotlib.get_backend()


def fix_capstyle(capstyle):
    ''' Matplotlib uses 'projecting' rather than 'square' for some reason '''
    if capstyle == 'square':
        return 'projecting'
    return capstyle


class Figure:
    ''' Schemdraw figure on Matplotlib figure

        Args:
            bbox: Coordinate bounding box for drawing, used to
                override Matplotlib's autoscale
            inches_per_unit: Scale for the drawing
            showbbox: Draw bounding box and margin box
            ax: Existing Matplotlib axis to draw on
    '''
    def __init__(self, **kwargs):
        self.showbbox = kwargs.get('showbbox', False)
        self.bbox = kwargs.get('bbox', None)
        self.inches_per_unit = kwargs.get('inches_per_unit', .5)
        if kwargs.get('ax'):
            self.ax = kwargs.get('ax')
            self.fig = self.ax.figure
            self.userfig = True
        else:
            # a Figure (big F) is not part of the pyplot interface
            # so won't be shown double in Jupyter/inline interfaces.
            # But a figure (small f) is required to show the image in
            # MPL's popup GUI.
            if inline:
                self.fig = plt.Figure()
            else:
                self.fig = plt.figure()
            self.fig.subplots_adjust(
                left=0.0,
                bottom=0.0,
                right=1.,
                top=1.)
            self.ax = self.fig.add_subplot()
            self.userfig = False
            self.ax.set_aspect('equal')
            self.ax.axes.get_xaxis().set_visible(False)
            self.ax.axes.get_yaxis().set_visible(False)
            self.ax.set_frame_on(False)

        # whitespace around contents
        self.margin = kwargs.get('margin', .1) + .03  # Plus half a line width for linecaps

    def set_bbox(self, bbox: BBox):
        ''' Set bounding box, to override Matplotlib's autoscale '''
        self.bbox = bbox

    def show(self) -> None:
        ''' Display figure in interactive window. Does nothing
            when running inline (ie Jupyter) which shows the
            figure using _repr_ methods.
        '''
        if not inline:
            self.getfig()
            self.fig.show()
            plt.show()   # To start the MPL event loop

    def bgcolor(self, color: str) -> None:
        ''' Set background color of drawing '''
        self.fig.set_facecolor(color)

    def addclip(self, patch, clip):
        ''' Set clipping region for the patch '''
        if clip:
            cliprect = Rectangle((clip.xmin, clip.ymax),
                                 abs(clip.xmax-clip.xmin), abs(clip.ymax-clip.ymin),
                                 transform=self.ax.transData)
            patch.set_clip_path(cliprect)

    def plot(self, x: float, y: float, color: str = 'black', ls: Linestyle = '-',
             lw: float = 2, fill: Optional[str] = None, capstyle: Capstyle = 'round',
             joinstyle: Joinstyle = 'round', clip: Optional[BBox] = None, zorder: int = 2) -> None:
        ''' Plot a path '''
        p, = self.ax.plot(x, y, zorder=zorder, color=color, ls=ls, lw=lw,
                          solid_capstyle=fix_capstyle(capstyle),
                          solid_joinstyle=joinstyle)
        self.addclip(p, clip)
        if fill:
            p, = self.ax.fill(x, y, color=fill, zorder=zorder-1)
            self.addclip(p, clip)

    def text(self, s: str, x: float, y: float, color: str = 'black',
             fontsize: float = 14, fontfamily: str = 'sans-serif',
             mathfont: Optional[str] = None, rotation: float = 0,
             halign: str = 'center', valign: str = 'center',
             rotation_mode: str = 'anchor', clip: Optional[BBox] = None, zorder=3) -> None:
        ''' Add text to the figure '''
        valign = 'baseline' if valign == 'base' else valign
        if fontfamily.endswith('.ttf') or fontfamily.endswith('otf'):
            if fontfamily not in [f.fname for f in font_manager.fontManager.ttflist]:
                font_manager.fontManager.addfont(fontfamily)
            idx = [f.fname for f in font_manager.fontManager.ttflist].index(fontfamily)
            fontfamily = font_manager.fontManager.ttflist[idx].name

        t = self.ax.text(x, y, s, transform=self.ax.transData, color=color,
                         fontsize=fontsize, fontfamily=fontfamily,
                         math_fontfamily=mathfont, linespacing=1,
                         rotation=rotation, rotation_mode=rotation_mode,
                         horizontalalignment=halign, verticalalignment=valign,
                         zorder=zorder, clip_on=False)
        self.addclip(t, clip)

    def poly(self, verts: Sequence[XY], closed: bool = True,
             color: str = 'black', fill: Optional[str] = None, lw: float = 2, ls: Linestyle = '-', hatch: bool = False,
             capstyle: Capstyle = 'round', joinstyle: Joinstyle = 'round', clip: Optional[BBox] = None, zorder: int = 1) -> None:
        ''' Draw a polynomial '''
        h = '///////' if hatch else None
        p = plt.Polygon(verts, closed=closed, ec=color,
                        fc=fill, fill=fill is not None,
                        lw=lw, ls=ls, hatch=h, capstyle=fix_capstyle(capstyle),
                        joinstyle=joinstyle, zorder=zorder)
        self.ax.add_patch(p)
        self.addclip(p, clip)

    def circle(self, center: XY, radius: float, color: str = 'black', fill: Optional[str] = None,
               lw: float = 2, ls: Linestyle = '-', clip: Optional[BBox] = None, zorder: int = 1) -> None:
        ''' Draw a circle '''
        circ = plt.Circle(xy=center, radius=radius, ec=color, fc=fill,
                          fill=fill is not None, lw=lw, ls=ls, zorder=zorder)
        self.ax.add_patch(circ)
        self.addclip(circ, clip)

    def arrow(self, xy: XY, theta: float,
              arrowwidth: float = .15, arrowlength: float = .25,
              color: str = 'black', lw: float = 2, clip: Optional[BBox] = None, zorder: int = 1) -> None:
        ''' Draw an arrowhead '''
        # Easier to skip Matplotlib's arrow or annotate methods and just draw a line
        # and a polygon.
        dx = arrowlength/2 * math.cos(math.radians(theta))
        dy = arrowlength/2 * math.sin(math.radians(theta))
        x, y = xy
        head = util.Point((x, y))
        tail = util.Point((x-dx, y-dy))
        fullen = math.sqrt(dx**2 + dy**2)

        # Endpoints of the arrow fins
        fin1 = util.Point((fullen - arrowlength, arrowwidth/2)).rotate(theta) + tail
        fin2 = util.Point((fullen - arrowlength, -arrowwidth/2)).rotate(theta) + tail

        p = plt.Polygon((fin1, head, fin2), closed=True, ec='none',
                        fc=color, fill=color is not None,
                        lw=lw, zorder=zorder)
        self.ax.add_patch(p)
        self.addclip(p, clip)

    def bezier(self, p: Sequence[util.Point], color: str = 'black',
               lw: float = 2, ls: Linestyle = '-', capstyle: Capstyle = 'round', zorder: int = 1,
               arrow: Optional[str] = None, arrowlength: float = 0.25, arrowwidth: float = 0.15,
               clip: Optional[BBox] = None) -> None:
        ''' Draw a cubic or quadratic bezier '''
        # Keep original points for arrow head
        # and adjust points for line so they don't extrude from arrows.
        lpoints = [p0 for p0 in p]
        if arrow is not None:
            if '<' in arrow:
                th1 = math.atan2(p[0].y - p[1].y, p[0].x - p[1].x)
                lpoints[0] = util.Point((p[0].x - math.cos(th1) * arrowlength/2,
                                         p[0].y - math.sin(th1) * arrowlength/2))
            if '>' in arrow:
                th2 = math.atan2(p[-1].y - p[-2].y, p[-1].x - p[-2].x)
                lpoints[-1] = util.Point((p[-1].x - math.cos(th2) * arrowlength/2,
                                          p[-1].y - math.sin(th2) * arrowlength/2))

        if len(p) == 4:
            codes = [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
        else:
            codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3]
        curve = PathPatch(Path(lpoints, codes),
                          fc='none', ec=color, ls=ls, lw=lw,
                          capstyle=fix_capstyle(capstyle),
                          transform=self.ax.transData)
        self.ax.add_patch(curve)
        self.addclip(curve, clip)

        if arrow is not None:
            if '<' in arrow:
                delta = p[0] - p[1]
                theta = math.degrees(math.atan2(delta.y, delta.x))
                self.arrow(p[0], theta, arrowlength=arrowlength,
                           arrowwidth=arrowwidth, color=color, zorder=zorder)
            elif arrow.startswith('o'):
                self.circle(p[0], radius=arrowwidth/2, color=color, fill=color, lw=0,
                            clip=clip, zorder=zorder)

            if '>' in arrow:
                delta = p[-1] - p[-2]
                theta = math.degrees(math.atan2(delta.y, delta.x))
                self.arrow(p[-1], theta, arrowlength=arrowlength,
                           arrowwidth=arrowwidth, color=color, zorder=zorder)
            elif arrow.endswith('o'):
                self.circle(p[-1], radius=arrowwidth/2, color=color, fill=color, lw=0,
                            clip=clip, zorder=zorder)

    def path(self, path: Sequence[XY | str],
            color: str = 'black', lw: float = 2, ls: Linestyle = '-',
            fill: Optional[str] = None,
            capstyle: Capstyle = 'round',
            joinstyle: Joinstyle = 'round', 
            zorder: int = 1,
            clip: Optional[BBox] = None,
            ) -> None:
        CODES = {
            'M': [Path.MOVETO],
            'C': [Path.CURVE4, Path.CURVE4, Path.CURVE4], 
            'Q': [Path.CURVE3, Path.CURVE3],
            'L': [Path.LINETO],
            'Z': [Path.CLOSEPOLY]}

        points = [p for p in path if not isinstance(p, str)]
        strcodes =  [p for p in path if isinstance(p, str)]
        codes: list[int] = []
        for s in strcodes:
            codes.extend(CODES.get(s, [Path.MOVETO]))  # type: ignore

        if strcodes[-1] == 'Z':
            points.append((0, 0))  # Ingored point, but required by MPL

        curve = PathPatch(Path(points, codes),
                          fc='none' if fill is None else fill,
                          ec=color, ls=ls, lw=lw,
                          fill=(fill is not None),
                          capstyle=fix_capstyle(capstyle),
                          joinstyle=joinstyle,
                          zorder=zorder,
                          transform=self.ax.transData)
        self.ax.add_patch(curve)
        self.addclip(curve, clip)

    def arc(self, center: XY, width: float, height: float,
            theta1: float = 0, theta2: float = 90, angle: float = 0,
            color: str = 'black', lw: float = 2, ls: Linestyle = '-',
            fill: Optional[str] = None,
            zorder: int = 1, clip: Optional[BBox] = None, arrow: Optional[str] = None) -> None:
        ''' Draw an arc or ellipse, with optional arrowhead '''

        if fill is None:
            arc = Arc(center, width=width, height=height, theta1=theta1,
                    theta2=theta2, angle=angle, color=color,
                    lw=lw, ls=ls, zorder=zorder)
            self.ax.add_patch(arc)
            self.addclip(arc, clip)
        else:
            # Matplotlib doesn't support filled arcs, so make one using Polygon
            while theta1 > theta2:
                theta1 -= 360

            theta = util.linspace(math.radians(theta2), math.radians(theta1), 50)
            points = [(width/2*math.cos(th) + center[0], 
                       height/2*math.sin(th) + center[1]) for th in theta]
            poly = plt.Polygon(points, closed=False,
                              ec=color,
                              fc=fill, fill=fill is not None,
                              lw=lw, ls=ls, zorder=zorder)

            if angle:
                tr = transforms.Affine2D().translate(-center[0], -center[1]).rotate_deg(angle).translate(center[0], center[1])
                poly.set_transform(tr+self.ax.transData)

            self.ax.add_patch(poly)
            self.addclip(poly, clip)

        if arrow is not None:
            x, y = math.cos(math.radians(theta2)), math.sin(math.radians(theta2))
            th2 = math.degrees(math.atan2((width/height)*y, x))
            x, y = math.cos(math.radians(theta1)), math.sin(math.radians(theta1))
            th1 = math.degrees(math.atan2((width/height)*y, x))
            if arrow in ['ccw', 'both'] or '>' in arrow:
                dx = math.cos(math.radians(th2+90)) / 100
                dy = math.sin(math.radians(theta2+90)) / 100
                s = util.Point((center[0] + width/2*math.cos(math.radians(th2)),
                                center[1] + height/2*math.sin(math.radians(th2))))
            elif arrow in ['cw', 'both'] or '<' in arrow:
                dx = -math.cos(math.radians(th1+90)) / 100
                dy = -math.sin(math.radians(th1+90)) / 100

                s = util.Point((center[0] + width/2*math.cos(math.radians(th1)),
                                center[1] + height/2*math.sin(math.radians(th1))))

            s = util.rotate(s, angle, center)
            darrow = util.rotate((dx, dy), angle)

            a = self.ax.arrow(s[0], s[1], darrow[0], darrow[1], head_width=.15,
                              head_length=.25, color=color, zorder=zorder)
            self.addclip(a, clip)

    def image(self, image: str | BinaryIO, xy: XY, width: float, height: float,
              rotate: float = 0, zorder: int = 1, imgfmt: Optional[str] = None):
        ''' Add an image to the figure
        
            Args:
                image: File name or open file pointer
                xy: Position for the image
                width: Image width in data coordinates
                height: Image height in data coordinates
                rotate: Image rotation in degrees
                zorder: Z-Order for image
                imgfmt: file format of image. Required if image is
                    open file pointer.
        '''
        try:
            if image.endswith('svg'):  # type: ignore
                raise ValueError('SVG images not supported in matplotlib backend')
        except AttributeError:
            pass

        try:
            imdat = plt.imread(image)
        except SyntaxError as ex:
            raise ValueError('SVG images not supported in matplotlib backend') from ex

        tr = transforms.Affine2D().rotate_deg(rotate).translate(xy[0], xy[1])
        im = self.ax.imshow(imdat, extent=(0, width, 0, height), zorder=zorder)
        im.set_transform(tr+self.ax.transData)

    def save(self, fname: str, transparent: bool = True, dpi: float = 72) -> None:
        ''' Save the figure to a file '''
        fig = self.getfig()
        fig.subplots_adjust(0, 0, 1, 1)
        fig.savefig(fname,
                    bbox_inches='tight',
                    transparent=transparent, dpi=dpi,
                    bbox_extra_artists=self.ax.get_default_bbox_extra_artists(),
                    pad_inches=0)

    def getfig(self):
        ''' Get the Matplotlib figure '''
        if self.showbbox:
            self.plot((self.bbox.xmin, self.bbox.xmin, self.bbox.xmax, self.bbox.xmax, self.bbox.xmin),
                      (self.bbox.ymin, self.bbox.ymax, self.bbox.ymax, self.bbox.ymin, self.bbox.ymin),
                      color='red', lw=.5)
            self.plot((self.bbox.xmin-self.margin, self.bbox.xmin-self.margin, self.bbox.xmax+self.margin, self.bbox.xmax+self.margin, self.bbox.xmin-self.margin),
                      (self.bbox.ymin-self.margin, self.bbox.ymax+self.margin, self.bbox.ymax+self.margin, self.bbox.ymin-self.margin, self.bbox.ymin-self.margin),
                      color='black', lw=.5)

        if not self.userfig:
            x1, x2 = self.bbox.xmin - self.margin, self.bbox.xmax + self.margin
            y1, y2 = self.bbox.ymin - self.margin, self.bbox.ymax + self.margin
            self.ax.set_xlim(x1, x2)
            self.ax.set_ylim(y1, y2)
            w = x2-x1
            h = y2-y1
            self.ax.axes.get_xaxis().set_visible(False)
            self.ax.axes.get_yaxis().set_visible(False)
            self.ax.set_frame_on(False)
            try:
                self.ax.get_figure().set_size_inches(self.inches_per_unit*w,
                                                     self.inches_per_unit*h)
            except ValueError:
                pass  # infinite size (no elements yet)
        return self.fig

    def getimage(self, ext='svg'):
        ''' Get the image as SVG or PNG bytes array '''
        fig = self.getfig()
        output = BytesIO()
        fig.savefig(output, format=ext,
                    bbox_inches='tight',
                    bbox_extra_artists=self.ax.get_default_bbox_extra_artists(),
                    pad_inches=0)

        return output.getvalue()

    def clear(self) -> None:
        ''' Remove everything '''
        self.ax.clear()

    def __repr__(self):
        if plt.isinteractive():
            self.show()
        return super().__repr__()

    def _repr_png_(self):
        ''' PNG representation for Jupyter '''
        return self.getimage('png')

    def _repr_svg_(self):
        ''' SVG representation for Jupyter '''
        return self.getimage('svg').decode()
