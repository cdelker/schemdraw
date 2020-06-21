''' Connectors and bus lines '''

import warnings
import numpy as np

from ..segments import Segment, SegmentText, SegmentCircle, SegmentPoly
from ..elements import Element, Line
from ..adddocs import adddocs


@adddocs(Element)
class OrthoLines(Element):
    ''' Orthogonal connection line
        
        Parameters
        ----------
        at : xy tuple
            Starting position
        to : xy tuple
            Ending position
        n : int
            Number of parallel lines
        dy : float
            Distance between parallel lines
    '''
    def place(self, dwgxy, dwgtheta, **dwgparams):
        self.dwgparams = dwgparams
        if self.cparams is None:
            self.buildparams()

        self.params['theta'] = 0
        xy = np.asarray(self.cparams.get('at', dwgxy))
        to = np.asarray(self.cparams.get('to'))
        n = self.cparams.get('n', 1)
        ndy = self.cparams.get('dy', .6)
        xstart = self.cparams.get('xstart', None)
        dx = to[0] - xy[0]
        dy = to[1] - xy[1]

        if dy == 0:
            for i in range(n):
                y = -i*ndy
                self.segments.append(Segment([[0, y], [dx, y+dy]], theta=0))
        else:
            # x0 is first line to go up
            if xstart is not None:
                x0 = dx*xstart
            elif dx > 0:
                x0 = dx/2 - (ndy*(n-1)/2)
            else:
                x0 = dx/2 + (ndy*(n-1)/2)

            for i in range(n):
                y = -i*ndy
                if dy > 0:
                    x = x0 + ndy*i if dx > 0 else x0 - ndy*i
                else:
                    x = x0 + (n-i)*ndy if dx > 0 else x0 - (n-i)*ndy
                self.segments.append(Segment([[0, y], [x, y], [x, y+dy], [dx, y+dy]], theta=0))
        return super().place(dwgxy, dwgtheta, **dwgparams)


@adddocs(Element)
class RightLines(Element):
    ''' Right-angle line
        
        Parameters
        ----------
        at : xy tuple
            Starting position for horizontal segment of line
        to : xy tuple
            Ending position, vertical segment
        n : int
            Number of parallel lines
        dy : float
            Distance between parallel lines
    '''
    def place(self, dwgxy, dwgtheta, **dwgparams):
        self.dwgparams = dwgparams
        if self.cparams is None:
            self.buildparams()

        self.params['theta'] = 0
        xy = np.asarray(self.cparams.get('at', dwgxy))
        to = np.asarray(self.cparams.get('to'))
        n = self.cparams.get('n', 1)
        ndy = self.cparams.get('dy', .6)
        dx = to[0] - xy[0]
        dy = to[1] - xy[1]
        for i in range(n):
            y = -i*ndy
            if dy > 0:
                x = dx - i*ndy if dx < 0 else dx + i*ndy
            else:
                x = dx + (n-i-1)*ndy if dx > 0 else dx - (n-i-1)*ndy
            self.segments.append(Segment([[0, y], [x, y], [x, dy]], theta=0))
        return super().place(dwgxy, dwgtheta, **dwgparams)


@adddocs(Element)
class Header(Element):
    ''' Header connector element

        Parameters
        ----------
        rows : int
            Number of rows [4]
        cols : int
            Number of columns. Pin numbering requires 1 or 2 columns. [1]
        style : string
            Connector style, 'round', 'square', or 'screw'
        numbering : string
            Pin numbering order. 'lr' for left-to-right numbering,
            'ud' for up-down numbering, or 'ccw' for counter-clockwise
            integrated-circuit style numbering. Pin 1 is always at the
            top-left corner, unless `flip` parameter is also set.
        shownumber : bool
            Draw pin numbers outside the header [False]
        pinsleft : list of string
            List of pin labels for left side
        pinsright : list of string
            List of pin labels for right side
        pinalignleft : string
            Vertical alignment for pins on left side ('center', 'top', 'bottom')
        pinalignright : string
            Vertical alignment for pins on right side ('center', 'top', 'bottom')
        pinfontsizeleft : float
            Font size for pin labels on left
        pinfontsizeright : float
            Font size for pin labels on right
        pinspacing : float
            Distance between pins [0.6]
        edge : float
            Distance between header edge and first pin row/column [0.3]
        pinfill : string
            Color to fill pin circles            
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rows = kwargs.get('rows', 4)
        cols = kwargs.get('cols', 1)
        style = kwargs.get('style', 'round')
        number = kwargs.get('numbering', 'lr')
        shownumber = kwargs.get('shownumber', False)
        pinspacing = kwargs.get('pinspacing', .6)
        lpinlabels = kwargs.get('pinsleft', [])
        rpinlabels = kwargs.get('pinsright', [])
        lpinlabelalign = kwargs.get('pinalignleft', 'bottom')
        rpinlabelalign = kwargs.get('pinalignright', 'bottom')
        pinfontsizeleft = kwargs.get('pinfontsizeleft', 9)
        pinfontsizeright = kwargs.get('pinfontsizeright', 9)
        edge = kwargs.get('edge', .3)
        self.params['theta'] = 0
        pinfill = kwargs.get('pinfill', 'white')
        if cols > 2:
            warnings.warn('Header numbering not supported with cols > 2')
        
        w = (cols-1) * pinspacing + edge*2
        h = (rows-1) * pinspacing + edge*2
        pinrad = .1
        
        self.segments.append(SegmentPoly([[0, 0], [0, h], [w, h], [w, 0]]))
        for row in range(rows):
            for col in range(cols):
                xy = [col*pinspacing+edge, h-row*pinspacing-edge]
                
                if style == 'square':
                    x, y = xy
                    self.segments.append(SegmentPoly([[x-pinrad, y-pinrad], [x+pinrad, y-pinrad],
                                                      [x+pinrad, y+pinrad], [x-pinrad, y+pinrad]],
                                                     fill='white', zorder=4))
                elif style == 'screw':
                    x, y = xy                    
                    self.segments.append(SegmentCircle(xy, pinrad*1.75, fill=pinfill, zorder=4))
                    self.segments.append(Segment([[x+pinrad, y+pinrad], [x-pinrad, y-pinrad]], zorder=5))
                    
                else:  # style == 'round'
                    self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))

                if number == 'lr' or number is True:
                    pnumber = str(row*cols + col + 1)
                elif number == 'ud':
                    pnumber = str(row + col*rows + 1)
                else: # number == 'ccw'
                    pnumber = str(rows*col+(rows-row)) if col%2 else str(row+1)
                self.anchors['p{}'.format(pnumber)] = xy
                
                if shownumber:
                    numxy = [w+.05 if col%2 else -.05, xy[1]]
                    align = ('left' if col%2 else 'right', 'bottom')
                    self.segments.append(SegmentText(numxy, pnumber, fontsize=pinfontsizeleft, align=align))
                
                if lpinlabels and (cols == 1 or not col%2):
                    lblxy = [-.05, xy[1]]
                    self.segments.append(SegmentText(lblxy, lpinlabels[row], fontsize=pinfontsizeleft,
                                                     align=('right', lpinlabelalign)))

                if rpinlabels and (cols == 1 or col%2):
                    lblxy = [w+.05, xy[1]]
                    self.segments.append(SegmentText(lblxy, rpinlabels[row], fontsize=pinfontsizeright,
                                                     align=('left', rpinlabelalign)))
                        
        
class Jumper(Element):
    ''' Jumper for use on a Header element

        Parameters
        ----------
        pinspacing : float
            Spacing between pins
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pinspacing = kwargs.get('pinspacing', .6)
        self.params['theta'] = 0        
        pinrad = .1
        x = pinrad*2.5
        self.segments.append(SegmentPoly([[-x, -x], [pinspacing+x, -x],
                                         [pinspacing+x, x], [-x, x]]))


@adddocs(Element)
class BusConnect(Element):
    ''' Data bus connection.
        Anchors: `start`, `end`, `pX` for each data line X
    
        Parameters
        ----------
        n : int
            Number of parallel lines
        dy : float
            Distance between parallel lines
        up : bool
            Slant up or down
        lwbus : float
            Line width of bus line
        l : float
            length of connection lines
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        n = kwargs.get('n', 1)
        dy = kwargs.get('dy', .6)
        up = kwargs.get('up', True)  # Slant up or down
        lwbus = kwargs.get('lwbus', 4)
        
        self.params['theta'] = 0
        dx = kwargs.get('l', 3)
        slantx = .5
        slanty = slantx if up else -slantx
        
        for i in range(n):
            y = -i*dy
            self.segments.append(Segment([[0, y], [dx-slantx, y], [dx, y+slanty]], theta=0))
            self.anchors['p{}'.format(i+1)] = [0, y]
        self.segments.append(Segment([[dx, slantx], [dx, slanty-n*dy]], lw=lwbus))
        self.params['drop'] = [dx, slantx]
        self.anchors['start'] = [dx, slantx]
        self.anchors['end'] = [dx, slantx-n*dy]

    
@adddocs(Element)
class BusLine(Line):
    ''' Data bus line. Just a wide line.

        Parameters
        ----------
        lw : float
            Line width
    '''
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lw', 4)
        super().__init__(*args, **kwargs)


@adddocs(Element)
class DB9(Element):
    ''' DB9 Connector
        Anchors: `p1` thru `p9`

        Parameters
        ----------
        pinspacing : float
            Distance between pins [.6]
        edge : float
            Distance between edge and pins [.3]
        number : bool
            Draw pin numbers
        pinfill : string
            Color to fill pin circles
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pinspacing = kwargs.get('pinspacing', .6)
        edge = kwargs.get('edge', .3)
        number = kwargs.get('number', False)    
        pinfill = kwargs.get('pinfill', 'white')
        self.params['theta'] = 0        
        w = pinspacing + edge*2
        h1 = 4 * pinspacing + edge*2
        h2 = h1 + .5
        pinrad = .1

        self.segments.append(SegmentPoly([[0, 0], [0, h1], [w, h2], [w, -.5]], cornerradius=.25))

        for i in range(4):
            xy = [edge, h1-(i+.5)*pinspacing-edge]
            self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))
            self.anchors['p{}'.format(9-i)] = xy  
            if number:
                self.segments.append(SegmentText([xy[0], xy[1]+pinrad], 
                                                 str(9-i), fontsize=9,
                                                 align=('center', 'bottom')))            
        for i in range(5):
            xy = [edge+pinspacing, h2-(i+.75)*pinspacing-edge]
            self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))
            self.anchors['p{}'.format(5-i)] = xy
            if number:
                self.segments.append(SegmentText([xy[0], xy[1]+pinrad], 
                                                 str(5-i), fontsize=9,
                                                 align=('center', 'bottom')))            


@adddocs(Element)
class DB25(Element):
    ''' DB25 Connector
        Anchors: `p1` thru `p25`

        Parameters
        ----------
        pinspacing : float
            Distance between pins [.6]
        edge : float
            Distance between edge and pins [.3]
        number : bool
            Draw pin numbers
        pinfill : string
            Color to fill pin circles
    '''    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pinspacing = kwargs.get('pinspacing', .6)
        edge = kwargs.get('edge', .3)
        number = kwargs.get('number', False)
        pinfill = kwargs.get('pinfill', 'white')
        self.params['theta'] = 0
        w = pinspacing + edge*2
        h1 = 12 * pinspacing + edge*2
        h2 = h1 + .5
        pinrad = .1

        self.segments.append(SegmentPoly([[0, 0], [0, h1], [w, h2], [w, -.5]], cornerradius=.25))

        for i in range(12):
            xy = [edge, h1-(i+.5)*pinspacing-edge]
            self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))
            self.anchors['p{}'.format(25-i)] = xy            
            if number:
                self.segments.append(SegmentText([xy[0], xy[1]+pinrad], 
                                                 str(25-i), fontsize=9,
                                                 align=('center', 'bottom')))            
        for i in range(13):
            xy = [edge+pinspacing, h2-(i+.75)*pinspacing-edge]
            self.segments.append(SegmentCircle(xy, pinrad, fill=pinfill, zorder=4))
            self.anchors['p{}'.format(13-i)] = xy
            if number:
                self.segments.append(SegmentText([xy[0], xy[1]+pinrad], 
                                                 str(13-i), fontsize=9,
                                                 align=('center', 'bottom')))

@adddocs(Element)
class CoaxConnect(Element):
    ''' Coaxial connector
        Anchors: `center`, `N`, `S`, `E`, `W`

        Parameters
        ----------
        radius : float
            Radius of outer shell
        radiusinner : float
            Radius of inner conductor
        fillinner : string
            Color to fill inner conductor
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rad = kwargs.get('radius', .4)
        radinner = kwargs.get('radiusinner', .12)
        fillin = kwargs.get('fillinner', 'white')

        self.segments.append(SegmentCircle([0, 0], rad))
        self.segments.append(SegmentCircle([0, 0], radinner, fill=fillin, zorder=4))
        self.anchors['center'] = [0, 0]
        self.anchors['N'] = [0, rad]
        self.anchors['S'] = [0, -rad]
        self.anchors['E'] = [rad, 0]
        self.anchors['W'] = [-rad, 0]