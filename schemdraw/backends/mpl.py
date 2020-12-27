''' Matplotlib drawing backend for schemdraw '''

from typing import Sequence
from io import BytesIO
import math

import matplotlib  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
from matplotlib.patches import Arc  # type: ignore

from .. import util
from ..types import Capstyle, Joinstyle, Linestyle, BBox

inline = 'inline' in matplotlib.get_backend()


class Figure(object):
    ''' Schemdraw figure on Matplotlib figure

        Parameters
        ----------
        bbox : schemdraw.segments.BBox
            Coordinate bounding box for drawing, used to
            override Matplotlib's autoscale
        inches_per_unit : float
            Scale for the drawing
        showframe : bool
            Show Matplotlib axis frame
        ax : Matplotlib axis
            Existing axis to draw on
    '''
    def __init__(self, **kwargs):
        if kwargs.get('ax'):
            self.ax = kwargs.get('ax')
            self.fig = self.ax.figure
            self.userfig = True
        else:
            if inline:
                self.fig = plt.Figure()
            else:
                self.fig = plt.figure()
            self.fig.subplots_adjust(
                left=0.05,
                bottom=0.05,
                right=0.95,
                top=0.90)
            self.ax = self.fig.add_subplot()
            self.userfig = False
        self.ax.autoscale_view(True)  # This autoscales all the shapes too
        self.showframe = kwargs.get('showframe', False)
        self.bbox = kwargs.get('bbox', None)
        self.inches_per_unit = kwargs.get('inches_per_unit', .5)

    def set_bbox(self, bbox: BBox):
        ''' Set bounding box, to override Matplotlib's autoscale '''
        self.bbox = bbox

    def show(self) -> None:
        ''' Display figure in interactive window '''
        if not inline:
            self.getfig()
            plt.show()
        plt.close()

    def plot(self, x: float, y: float, color: str='black', ls: Linestyle='-', lw: float=2, fill: str=None,
             capstyle: Capstyle='round', joinstyle: Joinstyle='round',  zorder: int=2) -> None:
        ''' Plot a path '''
        self.ax.plot(x, y, zorder=zorder, color=color, ls=ls, lw=lw,
                     solid_capstyle=capstyle, solid_joinstyle=joinstyle)
        if fill:
            self.ax.fill(x, y, color=fill, zorder=zorder)

    def text(self, s: str, x, y, color='black', fontsize=14, fontfamily='sans-serif',
             rotation=0, halign='center', valign='center', rotation_mode='anchor',
             zorder=3) -> None:
        ''' Add text to the figure '''
        self.ax.text(x, y, s, transform=self.ax.transData, color=color,
                     fontsize=fontsize, fontfamily=fontfamily,
                     rotation=rotation, rotation_mode=rotation_mode,
                     horizontalalignment=halign, verticalalignment=valign,
                     zorder=zorder)

    def poly(self, verts: Sequence[Sequence[float]], closed: bool=True, color: str='black', fill: str=None, lw: float=2, ls: Linestyle='-',
             capstyle: Capstyle='round', joinstyle: Joinstyle='round', zorder: int=1) -> None:
        ''' Draw a polynomial '''
        p = plt.Polygon(verts, closed=closed, ec=color,
                        fc=fill, fill=fill is not None,
                        lw=lw, ls=ls, capstyle=capstyle,
                        joinstyle=joinstyle, zorder=zorder)
        self.ax.add_patch(p)

    def circle(self, center: Sequence[float], radius: float, color: str='black', fill: str=None,
               lw: float=2, ls: Linestyle='-', zorder: int=1) -> None:
        ''' Draw a circle '''
        circ = plt.Circle(xy=center, radius=radius, ec=color, fc=fill,
                          fill=fill is not None, lw=lw, ls=ls, zorder=zorder)
        self.ax.add_patch(circ)

    def arrow(self, x: float, y: float, dx: float, dy: float, headwidth: float=.2, headlength: float=.2,
              color: str='black', lw: float=2, zorder: int=1) -> None:
        ''' Draw an arrow '''

        self.ax.arrow(x, y, dx, dy, head_width=headwidth, head_length=headlength,
                      length_includes_head=True, color=color, lw=lw, zorder=zorder)

    def arc(self, center: Sequence[float], width: float, height: float, theta1: float=0, theta2: float=90, angle: float=0,
            color: str='black', lw: float=2, ls: Linestyle='-', zorder: int=1, arrow: bool=None) -> None:
        ''' Draw an arc or ellipse, with optional arrowhead '''

        arc = Arc(center, width=width, height=height, theta1=theta1,
                  theta2=theta2, angle=angle, color=color,
                  lw=lw, ls=ls, zorder=zorder)
        self.ax.add_patch(arc)

        if arrow is not None:
            x, y = math.cos(math.radians(theta2)), math.sin(math.radians(theta2))
            th2 = math.degrees(math.atan2((width/height)*y, x))
            x, y = math.cos(math.radians(theta1)), math.sin(math.radians(theta1))
            th1 = math.degrees(math.atan2((width/height)*y, x))
            if arrow == 'ccw':
                dx = math.cos(math.radians(th2+90)) / 100
                dy = math.sin(math.radians(theta2+90)) / 100
                s = util.Point((center[0] + width/2*math.cos(math.radians(th2)),
                     center[1] + height/2*math.sin(math.radians(th2))))
            else:
                dx = -math.cos(math.radians(th1+90)) / 100
                dy = -math.sin(math.radians(th1+90)) / 100

                s = util.Point((center[0] + width/2*math.cos(math.radians(th1)),
                     center[1] + height/2*math.sin(math.radians(th1))))

            s = util.rotate(s, angle, center)
            darrow = util.rotate((dx, dy), angle)

            self.ax.arrow(s[0], s[1], darrow[0], darrow[1], head_width=.15,
                          head_length=.25, color=color, zorder=zorder)

    def save(self, fname: str, transparent: bool=True, dpi: float=72) -> None:
        ''' Save the figure to a file '''
        fig = self.getfig()
        fig.savefig(fname, bbox_inches='tight', transparent=transparent, dpi=dpi,
                    bbox_extra_artists=self.ax.get_default_bbox_extra_artists())

    def getfig(self):
        ''' Get the Matplotlib figure '''
        if not self.userfig:
            if self.bbox is None:
                # Use MPL's bbox, which sometimes clips things like arrowheads
                x1, x2 = self.ax.get_xlim()
                y1, y2 = self.ax.get_ylim()
            else:
                x1, y1, x2, y2 = self.bbox
            x1 -= .1  # Add a bit to account for line widths getting cut off
            x2 += .1
            y1 -= .1
            y2 += .1
            self.ax.set_xlim(x1, x2)
            self.ax.set_ylim(y1, y2)
            w = x2-x1
            h = y2-y1

            if not self.showframe:
                self.ax.axes.get_xaxis().set_visible(False)
                self.ax.axes.get_yaxis().set_visible(False)
                self.ax.set_frame_on(False)
            self.ax.get_figure().set_size_inches(self.inches_per_unit*w,
                                                 self.inches_per_unit*h)
        return self.fig

    def getimage(self, ext='svg'):
        ''' Get the image as SVG or PNG bytes array '''
        fig = self.getfig()
        output = BytesIO()
        fig.savefig(output, format=ext, bbox_inches='tight')
        return output.getvalue()

    def _repr_png_(self):
        ''' PNG representation for Jupyter '''
        return self.getimage('png')

    def _repr_svg_(self):
        ''' SVG representation for Jupyter '''
        return self.getimage('svg').decode()
