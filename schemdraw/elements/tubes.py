''' Vacuum Tubes '''
from __future__ import annotations
import math

from .elements import Element, gap
from ..segments import Segment, SegmentPoly, SegmentArc, SegmentCircle

tube_top = 0
tube_w = 2.5  # Default tube radius/width
tube_r = tube_w / 2
half_overhang = 20  # Degrees from vertical

grid_w = tube_w * .4
grid_ygap = tube_w / 9   # Vertical space between grids
anode_xgap = tube_w / 6  # Horizontal distance between multiple anodes


class TubeBase(Element):
    ''' Base class for vacuum tubes '''
    _element_defaults = {
        'tube_lw': 3,
        'anode_lw': 2,
        'cathode_lw': 2,
        'heat_lw': 2,
        'grid_lw': 2,
        'n_grid_dashes': 3,
        'dot_radius': 0.075,
        'theta': 0,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def _draw_envelope(self, height: float, width: float, split: str = 'none'):
        ''' Draw tube envelope '''
        bot = -height    # (0, 0) is top center (anode) position
        halfw = width/2
        left = -halfw
        right = halfw
        center = 0, -height/2
        corner = min(width/2, height/2)

        # Draw tube outline
        if split == 'left':
            self.segments.append(
                SegmentArc(center, width, height, theta1=90-half_overhang, theta2=270+half_overhang,
                           lw=self.params['tube_lw'])
            )
        elif split == 'right':
            self.segments.append(
                SegmentArc(center, width, height, theta1=270-half_overhang, theta2=90+half_overhang,
                           lw=self.params['tube_lw'])
            )
        else:
            self.segments.append(
                SegmentPoly(((left, tube_top), (right, tube_top),
                             (right, bot), (left, bot)),
                            cornerradius=corner,
                            lw=self.params['tube_lw'])
            )
        self.anchors['N'] = (0, 0)
        self.anchors['S'] = (0, -height)
        self.anchors['E'] = (right, -height/2)
        self.anchors['W'] = (left, -height/2)

    def _draw_elements(self, x: float, height: float, grids: int, cathode: str, anodetype: str, anchorid=''):
        ''' Draw anode/grids/cathode for one element '''
        dot_r = self.params['dot_radius']

        grid_top = tube_top - height/2 + (max(0, (grids-1))*grid_ygap)/2  # Topmost grid
        grid_bot = grid_top - grid_ygap * max(0,(grids-1))   # Bottom-most grid
        grid_left = x-grid_w/2
        grid_right = x+grid_w/2

        # Draw anode
        anodey = grid_top + grid_ygap
        if anodetype == 'narrow':
            self.segments.append(
                Segment(((x-dot_r, anodey), (x+dot_r, anodey)), lw=self.params['anode_lw'])
            )
        elif anodetype == 'dot':
            anodey += dot_r*2
            self.segments.append(
                SegmentCircle((x, anodey-dot_r), dot_r, lw=self.params['anode_lw'])
            )
        elif anodetype not in ['none', None]:
            self.segments.append(
                Segment(((grid_left, anodey), (grid_right, anodey)), lw=self.params['anode_lw'])
            )

        if anodetype not in ['none', None]:
            self.segments.append(Segment(((x, tube_top), (x, anodey)), lw=self.params['anode_lw']))
            self.anchors[f'anode{anchorid}'] = (x, tube_top)

        # Draw Grids
        n_grid_dashes = self.params['n_grid_dashes']
        grid_xgap = grid_w / (n_grid_dashes+2)
        grid_dashw = (grid_w - grid_xgap*(n_grid_dashes-1)) / n_grid_dashes
        grid_x = [grid_left + i*(grid_dashw+grid_xgap) for i in range(n_grid_dashes)]

        for j in range(grids):
            grid_y = grid_top - grid_ygap * j
            for i in range(n_grid_dashes):
                self.segments.append(
                    Segment(((grid_x[i], grid_y), (grid_x[i]+grid_dashw, grid_y)),
                            lw=self.params['grid_lw'])
                )

            if grids == 1:
                self.anchors[f'grid{anchorid}'] = (grid_left-grid_xgap, grid_y)
                self.anchors[f'grid{anchorid}_R'] = (grid_right+grid_xgap, grid_y)
            else:
                self.anchors[f'grid{anchorid}_{j+1}'] = (grid_left-grid_xgap, grid_y)
                self.anchors[f'grid{anchorid}_{j+1}R'] = (grid_right+grid_xgap, grid_y)

        # Draw Cathode
        cat_y = grid_bot - grid_ygap
        cat_drop = dot_r * 2

        if cathode == 'cold':
            self.segments.append(
                Segment(((x, cat_y-dot_r*2), (x, -height)))
            )
            self.segments.append(
                SegmentCircle((x, cat_y-dot_r), dot_r)
            )
            self.anchors[f'cathode{anchorid}'] = (x, -height)

        elif cathode not in ['none', None]:  # 'heated' or True
            self.segments.append(
                Segment(((grid_left, cat_y-cat_drop), (grid_left, cat_y),
                         (grid_right, cat_y), (grid_right, cat_y-cat_drop)),
                        lw=self.params['cathode_lw'])
            )
            self.anchors[f'cathode{anchorid}'] = (grid_left, cat_y-cat_drop)
            self.anchors[f'cathode{anchorid}_R'] = (grid_right, cat_y-cat_drop)
        return cat_y

    def _draw_heat(self, cat_y: float, height: float):
        ''' Draw Heater filament '''
        heat_top = cat_y - grid_ygap*1.25
        heat_left = -grid_w/3.5
        heat_right = grid_w/3.5
        heat_bot = tube_top - height - grid_ygap
        heat_bendy = heat_top - math.sqrt(2)*heat_right

        self.segments.append(
            Segment(((heat_left, heat_bot), (heat_left, heat_bendy),
                     (0, heat_top), (heat_right, heat_bendy),
                     (heat_right, heat_bot)),
                    lw=self.params['heat_lw'])
        )
        self.anchors['heat1'] = (heat_left, heat_bot)
        self.anchors['heat2'] = (heat_right, heat_bot)


class VacuumTube(TubeBase):
    ''' Generic Configrable Vacuum Tube

        Keyword Args:
            cathode: Cathode style 'heated', 'cold', or 'none'
            anodetype: Anode style 'plate', 'dot', 'narrow', or 'none'
            grids: Number of grids
            heater: Show heater filament
            split: Draw open envelope on 'left' or 'right' side

        Style Parameters:
            tube_lw: linewidth of envelope
            anode_lw: linewidth of anode
            cathode_lw: linewidth of cathode
            heat_lw: linewidth of heater
            grid_lw' linewidth of grid
            n_grid_dashes: number of grid dashes
            dot_radius: radius of dot for cold cathode

        Anchors:
            * anode
            * grid[_X]
            * grid_[X]R
            * cathode
            * cathode_R
            * heat1
            * heat2
    '''
    def __init__(
        self, *,
        cathode: str = 'heated',
        anodetype: str = 'plate',
        grids: int = 1,
        heater: bool = True,
        split: str = 'none',
        **kwargs
    ):
        super().__init__(**kwargs)

        # Height grows with more than 4 grids
        height = max(tube_w, tube_w + (grids-4)*grid_ygap)

        self._draw_envelope(height, tube_w, split)
        cathode_y = self._draw_elements(0, height, grids, cathode, anodetype)
        if heater:
            self._draw_heat(cathode_y, height)


class DualVacuumTube(TubeBase):
    ''' Dual Vacuum Tube

        Keyword Args:
            cathode: Cathode style 'heated', 'cold', or 'none'
            anodetype: Anode style 'plate', 'dot', or 'none'
            grids_left: Number of grids for left element
            grids_right: Number of grids for right element
            heater: Show heater filament

        Anchors:
            * anodeA
            * anodeB
            * gridA[_X]
            * gridA_[X]R
            * gridB[_X]
            * gridB_[X]R
            * cathodeA
            * cathodeA_R
            * cathodeB
            * cathodeB_R
            * heat1
            * heat2
    '''
    def __init__(
        self,
        cathode: str = 'heated',
        anodetype: str = 'plate',
        grids_left: int = 1,
        grids_right: int = 1,
        heater: bool = True,
        **kwargs
    ):
        super().__init__(**kwargs)

        # Height grows with more than 4 grids
        maxgrids = max(grids_left, grids_right)
        height = max(tube_w, tube_w + (maxgrids-4)*grid_ygap)

        width = tube_w * 1.5
        left = -width*.2
        right = width*.2

        self._draw_envelope(height, width)

        cathode_y1 = self._draw_elements(left, height, grids_left, cathode, anodetype, anchorid='A')
        cathode_y2 = self._draw_elements(right, height, grids_right, cathode, anodetype, anchorid='B')
        if heater:
            self._draw_heat(min(cathode_y1, cathode_y2), height)


class NixieTube(TubeBase):
    ''' Nixie Tube

        Keyword Args:
            anodes: Number of anode connections
            cathode: Cathode style 'T', 'cold', or 'none'
            anodetype: Anode type 'narrow' or 'dot'
            grid: Show grid

        Anchors:
            * anode[X]
            * cathode
            * grid
            * grid_R
    '''
    def __init__(self,
                 anodes: int = 3,
                 cathode: str = 'T',
                 anodetype: str = 'narrow',
                 grid: bool = False,
                 **kwargs):
        super().__init__(**kwargs)

        height = tube_w
        width = max(tube_w, (anodes-1)*anode_xgap+tube_w)
        left = -width*.2
        right = width*.2

        self._draw_envelope(height, width)

        if grid:
            self._draw_grid(anodes)

        self._draw_anodes(anodes, anodetype)
        self._draw_cathode(anodes, cathode)

    def _draw_anodes(self, n: int, anodetype: str):
        ''' Draw multiple anodes for nixie tube '''
        anodey = -tube_w/4
        anodew = (n-1)*anode_xgap
        left = -anodew/2
        dot_r = self.params['dot_radius']

        for i in range(n):
            x = left + i*anode_xgap
            if anodetype == 'narrow':
                self.segments.append(
                    Segment(((x-dot_r, anodey), (x+dot_r, anodey)), lw=self.params['anode_lw'])
                )
            elif anodetype == 'dot':
                self.segments.append(
                    SegmentCircle((x, anodey-dot_r), dot_r, lw=self.params['anode_lw'])
                )
            else:
                self.segments.append(
                    Segment(((grid_left, anodey), (grid_right, anodey)), lw=self.params['anode_lw'])
                )
            self.segments.append(Segment(((x, tube_top), (x, anodey)), lw=self.params['anode_lw']))
            self.anchors[f'anode{i}'] = (x, tube_top)

    def _draw_grid(self, nanodes: int):
        ''' Draw grid '''
        anodew = (nanodes-1)*anode_xgap
        left = -anodew/2

        n_grid_dashes = nanodes+1
        grid_xgap = anodew / (n_grid_dashes+2)
        grid_dashw = (anodew - grid_xgap*(n_grid_dashes-1)) / n_grid_dashes
        grid_x = [left + i*(grid_dashw+grid_xgap) for i in range(n_grid_dashes)]
        grid_y = -tube_w / 2
        for i in range(n_grid_dashes):
            self.segments.append(
                Segment(((grid_x[i], grid_y), (grid_x[i]+grid_dashw, grid_y)),
                        lw=self.params['grid_lw'])
            )

        self.anchors[f'grid'] = (left-grid_xgap, grid_y)
        self.anchors[f'grid_R'] = (left+anodew+grid_xgap, grid_y)

    def _draw_cathode(self, nanodes: int, cathode: str):
        dot_r = self.params['dot_radius']
        cat_y = -3 * tube_w / 4
        cat_drop = dot_r
        anodew = (nanodes-1)*anode_xgap

        if cathode == 'cold':
            self.segments.append(
                Segment(((0, cat_y-dot_r*2), (0, -tube_w)),
                        lw=self.params['cathode_lw'])
            )
            self.segments.append(
                SegmentCircle((0, cat_y-dot_r), dot_r)
            )
            self.anchors['cathode'] = (0, -tube_w)

        elif cathode == 'heated':
            self.segments.append(
                Segment(((-grid_w/2, cat_y-cat_drop), (-grid_w/2, cat_y),
                         (grid_w/2, cat_y), (grid_w/2, cat_y-cat_drop)),
                        lw=self.params['cathode_lw'])
            )
            self.anchors['cathode'] = (-grid_w/2, cat_y-cat_drop)
            self.anchors['cathode_R'] = (grid_w/2, cat_y-cat_drop)

        elif cathode not in ['none', None]:  # 'T'
            self.segments.append(
                Segment(((0, -tube_w), (0, cat_y), gap, (-anodew/2, cat_y), (anodew/2, cat_y)),
                        lw=self.params['cathode_lw'])
            )
            self.anchors['cathode'] = (0, -tube_w)


class TubeDiode(VacuumTube):
    ''' Vacuum Tube Diode

        Keyword Args:
            heater: Show heater filament
            split: Draw open envelope on 'left' or 'right' side

        Anchors:
            * anode
            * cathode
            * cathode_R
            * heat1
            * heat2
    '''
    def __init__(self, heater: bool = False, split: str = 'none', **kwargs):
        super().__init__(cathode='heated', grids=0, heater=heater, split=split, **kwargs)


class Triode(VacuumTube):
    ''' Triode Vacuum Tube

        Keyword Args:
            heater: Show heater filament
            split: Draw open envelope on 'left' or 'right' side

        Anchors:
            * anode
            * cathode
            * cathode_R
            * control
            * control_R
            * heat1
            * heat2
    '''
    def __init__(self, heater: bool = False, split: str = 'none', **kwargs):
        super().__init__(cathode='heated', grids=1, heater=heater, split=split, **kwargs)
        self.anchors['control'] = self.anchors['grid']
        self.anchors['control_R'] = self.anchors['grid_R']


class Tetrode(VacuumTube):
    ''' Tetrode Vacuum Tube

        Keyword Args:
            heater: Show heater filament
            split: Draw open envelope on 'left' or 'right' side

        Anchors:
            * anode
            * cathode
            * cathode_R
            * screen
            * screen_R
            * control
            * control_R
            * heat1
            * heat2
    '''
    def __init__(self, heater: bool = False, split: str = 'none', **kwargs):
        super().__init__(cathode='heated', grids=2, heater=heater, split=split, **kwargs)
        self.anchors['screen'] = self.anchors['grid_1']
        self.anchors['screen_R'] = self.anchors['grid_1R']
        self.anchors['control'] = self.anchors['grid_2']
        self.anchors['control_R'] = self.anchors['grid_2R']


class Pentode(VacuumTube):
    ''' Pentode Vacuum Tube

        Keyword Args:
            strap: Connect suppressor grid to cathode
            heater: Show heater filament
            split: Draw open envelope on 'left' or 'right' side

        Anchors:
            * anode
            * cathode
            * cathode_R
            * suppressor
            * suppressor_R
            * screen
            * screen_R
            * control
            * control_R
            * heat1
            * heat2
    '''
    def __init__(self, strap: bool = False, heater: bool = False, split: str = 'none', **kwargs):
        super().__init__(cathode='heated', grids=3, heater=heater, split=split, **kwargs)
        self.anchors['suppressor'] = self.anchors['grid_1']
        self.anchors['suppressor_R'] = self.anchors['grid_1R']
        self.anchors['screen'] = self.anchors['grid_2']
        self.anchors['screen_R'] = self.anchors['grid_2R']
        self.anchors['control'] = self.anchors['grid_3']
        self.anchors['control_R'] = self.anchors['grid_3R']

        if strap:
            dot_r = self.params['dot_radius']
            c = self.anchors['cathode_R']
            c = c[0], c[1]+dot_r*2
            s = grid_w/2, self.anchors['suppressor_R'][1]
            r = c[0]+grid_ygap*.75, c[1]+grid_ygap/2
            r2 = r[0], s[1]-grid_ygap/2
            self.segments.append(
                Segment((c, r, r2, s),
                lw=self.params['cathode_lw'])
            )
