''' Matplotlib drawing backend for schemdraw '''

from io import StringIO, BytesIO
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

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
    '''
    def __init__(self, **kwargs):
        self.fig = plt.figure()
        self.fig.subplots_adjust(
            left=0.05,
            bottom=0.05,
            right=0.95,
            top=0.90)
        self.ax = self.fig.add_subplot()
        self.ax.autoscale_view(True)  # This autoscales all the shapes too
        self.showframe = kwargs.get('showframe', False)
        self.bbox = kwargs.get('bbox', None)
        self.inches_per_unit = kwargs.get('inches_per_unit', .5)

    def set_bbox(self, bbox):
        ''' Set bounding box, to override Matplotlib's autoscale '''
        self.bbox = bbox
        
    def show(self):
        ''' Display figure in interactive window '''
        if not inline:
            self.getfig()
            plt.show()
        plt.close()

    def plot(self, x, y, color='black', ls='-', lw=2, fill=None,
             capstyle='round', joinstyle='round',  zorder=2):
        ''' Plot a path '''
        self.ax.plot(x, y, zorder=zorder, color=color, ls=ls, lw=lw,
                     solid_capstyle=capstyle, solid_joinstyle=joinstyle)
        if fill:
            self.ax.fill(x, y, color=fill, zorder=zorder)

    def text(self, s, x, y, color='black', fontsize=14, fontfamily='sans-serif',
             rotation=0, halign='center', valign='center', rotation_mode='anchor',
             zorder=3):
        ''' Add text to the figure '''
        self.ax.text(x, y, s, transform=self.ax.transData, color=color,
                     fontsize=fontsize, fontfamily=fontfamily,
                     rotation=rotation, rotation_mode=rotation_mode,
                     horizontalalignment=halign, verticalalignment=valign,
                     zorder=zorder)

    def poly(self, verts, closed=True, color='black', fill=None, lw=2, ls='-',
             capstyle='round', joinstyle='round', zorder=1):
        ''' Draw a polynomial '''
        p = plt.Polygon(verts, closed=closed, ec=color,
                        fc=fill, fill=fill is not None,
                        lw=lw, ls=ls, capstyle=capstyle,
                        joinstyle=joinstyle, zorder=zorder)
        self.ax.add_patch(p)

    def circle(self, center, radius, color='black', fill=None,
               lw=2, ls='-', zorder=1):
        ''' Draw a circle '''
        circ = plt.Circle(xy=center, radius=radius, ec=color, fc=fill,
                          fill=fill is not None, lw=lw, ls=ls, zorder=zorder)
        self.ax.add_patch(circ)

    def arrow(self, x, y, dx, dy, headwidth=.2, headlength=.2,
              color='black', lw=2, zorder=1):
        ''' Draw an arrow '''

        self.ax.arrow(x, y, dx, dy, head_width=headwidth, head_length=headlength,
                      length_includes_head=True, color=color, lw=lw, zorder=zorder)

    def arc(self, center, width, height, theta1=0, theta2=90, angle=0,
            color='black', lw=2, ls='-', zorder=1, arrow=None):
        ''' Draw an arc or ellipse, with optional arrowhead '''

        arc = Arc(center, width=width, height=height, theta1=theta1,
                  theta2=theta2, angle=angle, color=color,
                  lw=lw, ls=ls, zorder=zorder)
        self.ax.add_patch(arc)

        if arrow is not None:
            x, y = np.cos(np.deg2rad(theta2)), np.sin(np.deg2rad(theta2))
            th2 = np.rad2deg(np.arctan2((width/height)*y, x))
            x, y = np.cos(np.deg2rad(theta1)), np.sin(np.deg2rad(theta1))
            th1 = np.rad2deg(np.arctan2((width/height)*y, x))
            if arrow == 'ccw':
                dx = np.cos(np.deg2rad(th2+90)) / 100
                dy = np.sin(np.deg2rad(theta2+90)) / 100
                s = [center[0] + width/2*np.cos(np.deg2rad(th2)),
                     center[1] + height/2*np.sin(np.deg2rad(th2))]
            else:
                dx = -np.cos(np.deg2rad(th1+90)) / 100
                dy = - np.sin(np.deg2rad(th1+90)) / 100

                s = [center[0] + width/2*np.cos(np.deg2rad(th1)),
                     center[1] + height/2*np.sin(np.deg2rad(th1))]

            # Rotate the arrow head
            co = np.cos(np.radians(angle))
            so = np.sin(np.radians(angle))
            m = np.array([[co, so], [-so, co]])
            s = np.dot(s-center, m)+center
            darrow = np.dot([dx, dy], m)

            self.ax.arrow(s[0], s[1], darrow[0], darrow[1], head_width=.15,
                          head_length=.25, color=color, zorder=zorder)

    def save(self, fname, transparent=True, dpi=72):
        ''' Save the figure to a file '''
        fig = self.getfig()
        fig.savefig(fname, bbox_inches='tight', transparent=transparent, dpi=dpi,
                    bbox_extra_artists=self.ax.get_default_bbox_extra_artists())

    def getfig(self):
        ''' Get the Matplotlib figure '''
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
        ''' Get the image as SVG or PNG '''
        fig = self.getfig()
        if ext == 'svg':
            output = StringIO()
            fig.savefig(output, format='svg', bbox_inches='tight')
        else:
            output = BytesIO()
            fig.savefig(output, format=ext, bbox_inches='tight')

        return output.getvalue()

    def _repr_png_(self):
        ''' PNG representation for Jupyter '''
        return self.getimage('png')

    def _repr_svg_(self):
        ''' SVG representation for Jupyter '''
        return self.getimage('svg')
