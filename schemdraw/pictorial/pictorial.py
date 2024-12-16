''' Pictorial Style Elements '''
from __future__ import annotations
from typing import Optional
import math

from ..backends.svgunits import parse_size_to_px, PX_PER_IN
from ..segments import (Segment,
                        SegmentPath,
                        SegmentPoly,
                        SegmentArc,
                        SegmentCircle,
                        SegmentText)
from ..elements import Element, Element2Term
from ..style import validate_color


# Scale factors in terms of drawing units
# INCH chosen to scale the dimensioned pictorial elements to 
# approximately the right size relative to other schemdraw elements
INCH = 3.5  # Drawing units per inch
MILLIMETER = INCH / 25.4   # Drawing units per millimeter
PINSPACING = 0.1 * INCH  # Spacing between breadboard pins

HOUSING_COLOR = '#333'  # Color of ICs, Diodes, etc.
BORDER_COLOR = '#777'   # Border around housings
LEAD_COLOR = '#A0A0A0'  # Color of leads/metal


def parse_size_to_units(value: str) -> float:
    ''' Parse a SVG size string (sunh as '2in') to drawing units '''
    value_px = parse_size_to_px(value)
    value_units = value_px / PX_PER_IN * INCH
    return value_units


def resistor_colors(value: float,
                    tolerance: Optional[float] = None
                    ) -> tuple[str, str, str, Optional[str]]:
    ''' Determine Resistor color bands given the value (ohms) and tolerance (in percent)'''
    colors = {
        0: 'black',
        1: 'brown',
        2: 'red',
        3: 'orange',
        4: 'yellow',
        5: 'green',
        6: 'blue',
        7: 'violet',
        8: 'gray',
        9: 'white',
        -1: 'gold',
        -2: 'silver',
        -3: 'pink'}
    
    tol = {  # in percent
        1: 'brown',
        2: 'red',
        .05: 'orange',
        .02: 'yellow',
        .5: 'green',
        .25: 'blue',
        .1: 'violet',
        .01: 'gray',
        5: 'gold',
        10: 'silver',
        None: None}

    mult = int(math.log10(value))-1  # Third band/multiplier
    base = value / 10**mult
    if base < 10:
        mult-=1
        base = value / 10**mult
    band1 = int(base / 10)
    band2 = int(base % 10)
    return colors[band1], colors[band2], colors[mult], tol.get(tolerance, None)


class ElementPictorial(Element2Term):
    ''' This class gives pictorial 2-term elements silver lead extensions '''
    _element_defaults = {
        'leadcolor': LEAD_COLOR,
        'lw': 3,
    }


class Resistor(ElementPictorial):
    ''' Carbon-film 1/4 Watt Resistor

        Args:
            value: Resistance value, used to set color bands
            tolerance: Tolerance value for 4th color band

        Note: Color bands will be closest possible value that can be represented
            with 3 bands
    '''
    _element_defaults = {
        'fill': 'blanchedalmond'
    }
    def __init__(self, value: float = 1000, tolerance: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        # Spec dimensions are w = 6.3mm, h = 2.3mm. This is close enough.
        w = PINSPACING    # width of straight part (in direction of current)
        h = PINSPACING/2  # height of rounded part
        h2 = h * 0.9      # height of straight part

        # for 2-term endpoints
        self.segments.append(Segment(((0, 0), (math.nan, math.nan), (h*3+w, 0))))
        self.segments.append(SegmentPath(
            ('M', (0, 0),
             'Q', (0, h), (h, h),
             'Q', (h*1.25, h), (h*1.5, h2),
             'L', (h*1.5+w, h2),
             'Q', (h*1.75+w, h), (h*2+w, h),
             'Q', (h*3+w, h), (h*3+w, 0),
             'Q', (h*3+w, -h), (h*2+w, -h),
             'Q', (h*1.75+w, -h), (h*1.5+w, -h2),
             'L', (h*1.5, -h2),
             'Q', (h*1.25, -h), (h, -h),
             'Q', (0, -h), (0, 0),
             'Z'),
            color='black',
            lw=1))

        # Color bands
        stripe1 = .16
        stripe2 = .32
        stripe3 = .48
        stripe4 = .68
        stripew = .08
        c1, c2, c3, ct = resistor_colors(value, tolerance)
        self.segments.append(SegmentPoly(((stripe1, h2), (stripe1, -h2),
                                          (stripe1+stripew, -h2), (stripe1+stripew, h2)),
                                          fill=c1, lw=.1, zorder=2))

        self.segments.append(SegmentPoly(((stripe2, h2), (stripe2, -h2),
                                          (stripe2+stripew, -h2), (stripe2+stripew, h2)),
                                          fill=c2, lw=.1, zorder=2))

        self.segments.append(SegmentPoly(((stripe3, h2), (stripe3, -h2),
                                          (stripe3+stripew, -h2), (stripe3+stripew, h2)),
                                          fill=c3, lw=.1, zorder=2))

        if ct:
            self.segments.append(SegmentPoly(((stripe4, h2), (stripe4, -h2),
                                              (stripe4+stripew, -h2), (stripe4+stripew, h2)),
                                              fill=ct, lw=.1, zorder=2))


class Diode(ElementPictorial):
    ''' Diode in DO-204 package '''
    _element_defaults = {
        'fill': HOUSING_COLOR,
        'stripe_color': 'silver'
    }
    def __init__(self, *, stripe_color: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        h = PINSPACING/2
        w = PINSPACING * 2.5
        stripex = w * .78
        stripew = .08
        stripe_color = self.params['stripe_color']
        validate_color(stripe_color)

        self.segments.append(Segment(((0, 0), (math.nan, math.nan), (w, 0))))  # 2-term endpoints
        self.segments.append(SegmentPoly(((0, h), (w, h), (w, -h), (0, -h)), closed=True, lw=1, color='black', zorder=2))
        self.segments.append(SegmentPoly(((stripex, h), (stripex+stripew, h), (stripex+stripew, -h), (stripex, -h)),
                                          closed=True, lw=1, color='none', fill=stripe_color, zorder=2))


class LED(Element):
    ''' Light Emitting Diode Use .fill() to set the color.
    
        Suggested fill colors for common LEDs:
            * red: #dd4433,
            * orange: #efa207
            * yellow: #f1de0f
            * green: #4be317
            * blue: #3892bc
            * white/clear: #e5e5e5
    '''
    _element_defaults = {
        'lead_length': PINSPACING*5,
        'fill': '#dd4433',
        'theta': 0,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # From datasheet
        width = .197 * INCH
        height = .338 * INCH

        # Leads
        lead_h = self.params['lead_length']  # Lead to bottom of LED
        ref = PINSPACING * 5
        self.segments.append(
            Segment(((0, 0), (0, lead_h)), color=LEAD_COLOR, lw=4))
        self.segments.append(
            Segment(((PINSPACING, 0), (PINSPACING, lead_h-ref*.3),
                     (PINSPACING*.6, lead_h-ref*.2), (PINSPACING*.6, lead_h)),
                     color=LEAD_COLOR, lw=4))

        top_r = width * .8
        left = PINSPACING/2 - width/2
        center = PINSPACING/2
        top = lead_h+height

        # Case
        self.segments.append(
            SegmentPath(('M', (left, lead_h),
                         'Q', (center, lead_h-ref*.2), (left+width, lead_h),
                         'L', (left+width, top-top_r),
                         'C', (left+width, top), (left, top), (left, top-top_r),
                         'Z'), color='none'))  # color set by fill

        # Accents - use white with transparency to be color-agnostic
        # NOTE: linewidth won't scale with zoom
        base_h = .039 * INCH
        self.segments.append(
            SegmentPath(('M', (left, lead_h+base_h/2),
                         'Q', (center*.5, lead_h-ref*.16+base_h), (left+width*.7, lead_h-ref*.03),
                         'L', (left+width+.0*INCH, lead_h+base_h/2)),
                        color='#FFFFFF55', lw=2))

        reflectionx = left+.03*INCH
        self.segments.append(
            SegmentPath(('M', (reflectionx, lead_h+base_h*2),
                         'L', (reflectionx, top-top_r),
                         'Q', (reflectionx, top-top_r+.04*INCH),
                              (reflectionx+.04*INCH, top-top_r+.07*INCH)),
                        color='#FFFFFF55', lw=3))


class LEDOrange(LED):
    ''' Orange Light Emitting Diode '''
    _element_defaults = {
        'fill': '#efa207'
    }


class LEDYellow(LED):
    ''' Yellow Light Emitting Diode '''
    _element_defaults = {
        'fill': '#f1de0f'
    }


class LEDGreen(LED):
    ''' Green Light Emitting Diode '''
    _element_defaults = {
        'fill': '#4be317'
    }


class LEDBlue(LED):
    ''' Blue Light Emitting Diode '''
    _element_defaults = {
        'fill': '#3892bc'
    }


class LEDWhite(LED):
    ''' White Light Emitting Diode '''
    _element_defaults = {
        'fill': '#e5e5e5'
    }



class CapacitorElectrolytic(Element):
    ''' Electrolytic capacitor

        Note: Use .fill() to change color.

        Args:
            cap_color: Color of the metal cap on top
            stripe_color: Color of the polarity stripe
    '''
    _element_defaults = {
        'fill': '#303b91',
        'lead_length': 0.2*INCH,
        'cap_color': '#CCC',
        'stripe_color': '#dff1f6',
        'theta': 0,
    }
    def __init__(self, *, lead_length: Optional[float] = None,
                 cap_color: Optional[str] = None,
                 stripe_color: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)

        width = PINSPACING*1.7
        height = .3*INCH

        # Leads
        lead_h = self.params['lead_length']  # Lead to bottom of LED
        self.segments.append(
            Segment(((0, 0), (0, lead_h)), color=LEAD_COLOR, lw=4))
        self.segments.append(
            Segment(((PINSPACING, 0), (PINSPACING, lead_h)), color=LEAD_COLOR, lw=4))

        ref = PINSPACING*2
        top_r = ref*.3
        left = PINSPACING/2 - width/2
        center = PINSPACING/2
        top = lead_h + height

        # Case
        self.segments.append(
            SegmentPath(('M', (left, lead_h),
                         'Q', (center, lead_h - ref*.3), (left+width, lead_h),
                         'L', (left+width, top-top_r),
                         'Q', (center, top), (left, top-top_r),
                         'Z'), color='none'))  # color set by fill

        # Cap
        self.segments.append(
            SegmentArc((center, top-top_r-.01*INCH), width-.03*INCH, top_r*.9, 0, 360,
                       fill=self.params['cap_color'], color='none', lw=.5, zorder=2))

        # Bottom accent
        base_h = .039*INCH / 2
        self.segments.append(
            SegmentPath(('M', (left, lead_h+base_h),
                         'Q', (center, lead_h-ref*.1), (left+width, lead_h+base_h)),
                        color='#FFFFFF99', fill='none', lw=1.5))

        # Polarity stripe
        stripex = left + 0.03*INCH
        self.segments.append(
            SegmentPath(('M', (stripex, lead_h+base_h),
                         'L', (stripex, top-top_r*2),),
                        color=self.params['stripe_color'], fill='none', lw=3))


class CapacitorMylar(Element):
    ''' Mylar Capacitor '''
    _element_defaults = {
        'fill': '#8c2510',
        'lead_length': 0.4*INCH,
        'theta': 0,
    }
    def __init__(self, *, lead_length: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        width = PINSPACING*1.75
        height = width*.75
        center = PINSPACING/2
        left = center-width/2

        # Leads
        lead_h = self.params['lead_length']
        self.segments.append(
            Segment(((0, 0), (0, lead_h)), color=LEAD_COLOR, lw=4))
        self.segments.append(
            Segment(((PINSPACING, 0), (PINSPACING, lead_h)), color=LEAD_COLOR, lw=4))

        bulge = .02*INCH
        self.segments.append(
            SegmentPath(('M', (left, lead_h),
                         'Q', (left-bulge, lead_h+height/2), (left, lead_h+height),
                         'Q', (center, lead_h+height+bulge), (left+width, lead_h+height),
                         'Q', (left+width+bulge, lead_h+height/2), (left+width, lead_h),
                         'Q', (center, lead_h+bulge/2), (left, lead_h),
                         'Z'),
                        color='none'))

        highlighty = lead_h+height-.025*INCH
        self.segments.append(
            Segment(((-.01*INCH, highlighty), (PINSPACING*.8, highlighty)),
                    color='#FFFFFF44', lw=3))


class CapacitorCeramic(Element):
    ''' Ceramic Disc Capacitor '''
    _element_defaults = {
        'fill': '#e2800b',
        'radius': 0.1*INCH,
        'lead_length': 0.4*INCH,
        'theta': 0,
    }
    def __init__(self, *, radius: Optional[float] = None,
                 lead_length: Optional[float] = None, **kwargs):
        super().__init__(**kwargs)
        rad = self.params['radius']
        lead_h = self.params['lead_length']
        center = PINSPACING/2, lead_h+rad-.05*INCH

        # Leads
        self.segments.append(
            Segment(((0, 0), (0, lead_h)), color=LEAD_COLOR, lw=4))
        self.segments.append(
            Segment(((PINSPACING, 0), (PINSPACING, lead_h)), color=LEAD_COLOR, lw=4))

        self.segments.append(
            SegmentCircle(center, rad, color='none', zorder=2))

        self.segments.append(
            SegmentArc(center, rad*2*.7, rad*2*.7, 100, 200,
                       color='#FFFFFF44', zorder=2))


class TO92(Element):
    ''' TO92 Transistor Package, with pins bent out to 0.1 inch breadboard spacing '''
    _element_defaults = {
        'theta': 0,
    }
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Dimensions from TO92 spec
        width = .175*INCH
        height = .170*INCH*.9  # .170 is standard height, but *.9 due to perspective
        topheight = PINSPACING*1.2

        # (0, 0) is left pin. case_x, y is lower left of the case
        case_y = PINSPACING*1.3
        case_x = PINSPACING-width/2
        center = PINSPACING
        self.segments.append(
            Segment(((0, 0), (0, PINSPACING*.8), (PINSPACING/2, case_y)),
                    color=LEAD_COLOR, lw=4))
        self.segments.append(
            Segment(((center, 0), (center, case_y)),
                    color=LEAD_COLOR, lw=4))
        self.segments.append(
            Segment(((PINSPACING*2, 0), (PINSPACING*2, PINSPACING*.8), (3*PINSPACING/2, case_y)),
                    color=LEAD_COLOR, lw=4))

        self.segments.append(
            SegmentPoly(((case_x, case_y), (case_x+width, case_y),
                         (case_x+width, case_y+height), (case_x, case_y+height)),
                        fill=HOUSING_COLOR, lw=1, color=BORDER_COLOR, zorder=2))
        self.segments.append(
            SegmentArc((center, case_y+height), width, topheight, 0, 180,
                       fill=HOUSING_COLOR, lw=1, color=BORDER_COLOR, zorder=2))

        # using "pin" since emitter/base/collector aren't standardized
        self.anchors['pin1'] = (0, 0)
        self.anchors['pin2'] = (PINSPACING, 0)
        self.anchors['pin3'] = (PINSPACING*2, 0)
        self.anchors['case_center'] = (center, case_y+height/2)
        self.elmparams['lblloc'] = 'case_center'
        self.elmparams['lblalign'] = ('center', 'center')


class DIP(Element):
    ''' Dual-Inline-Package IC

        Args:
            npins: Total number of pins
            wide: Use wide (0.6 inch) package instead of narrow
                (0.3 inch) package
    '''
    _element_defaults = {
        'theta': 0
    }
    def __init__(self, npins: int = 8, wide: bool = False, **kwargs):
        super().__init__(**kwargs)
        if npins % 2 != 0:
            npins += 1  # Can't have odd number, just round it up

        # Align Pin1 with (0, 0)
        # standard DIP width is 0.3 or 0.6 inch
        # width is from pin1 to pin8
        width = 3*PINSPACING if not wide else 6*PINSPACING

        pady = PINSPACING*.25  # padding to add above top pin and below bottom pin
        padx = PINSPACING*.25  # padding to remove left/right
        height = (npins//2-1) * PINSPACING #+ pady*2
        center = (width)/2
        notch_r = PINSPACING*.75
        body_left = padx
        body_right = width-padx
        leadw = 5
        
        for n in range(npins//2):
            self.segments.append(Segment(((0, -n*PINSPACING), (body_left, -n*PINSPACING)), color=LEAD_COLOR, lw=leadw, zorder=1))
            self.segments.append(Segment(((body_right, -n*PINSPACING), (body_right+padx, -n*PINSPACING)), color=LEAD_COLOR, lw=leadw, zorder=1))
            self.anchors[f'pin{n+1}'] = (0, -n*PINSPACING)
            self.anchors[f'pin{npins-n}'] = (body_right+padx, -n*PINSPACING)

        self.segments.append(SegmentPoly(((padx, pady), (body_right, pady),
                                          (body_right, -pady-height), (padx, -pady-height)), fill=HOUSING_COLOR, lw=1, color='#444'))
        self.segments.append(SegmentArc((center, pady), notch_r, notch_r, 180, 0, lw=1, color='#777', fill='#555'))

        self.elmparams['lblloc'] = 'center'
        self.elmparams['lblrotate'] = True
        self.elmparams['lblofst'] = 0


class Breadboard(Element):
    ''' Solderless Breadboard, 400-point (30 rows)

        Use .color() to set border color, and .fill() to set fill color.
    '''
    _element_defaults = {
        'color': '#DDD',  # Border
        'fill': '#F8F8F5',
        'shadow_color': '#E5E5E5',
        'text_color': '#666',
    }
    def __init__(self, *,
                 shadow_color: Optional[str] = None,
                 text_color: Optional[str] = None,
                 **kwargs):
        super().__init__(**kwargs)

        inner_radius = .02
        outer_radius = .1
        shadow_color = self.params.get('shadow_color')
        text_color = self.params.get('text_color')
        validate_color(shadow_color)
        validate_color(text_color)

        def hole(x, y):
            self.segments.append(SegmentPoly(((x-outer_radius, y+outer_radius), (x+outer_radius, y+outer_radius),
                                                (x+outer_radius, y-outer_radius)),
                                                fill=True, color=shadow_color, lw=2))
            self.segments.append(SegmentPoly(((x-inner_radius, y-inner_radius), (x-inner_radius, y+inner_radius),
                                                (x+inner_radius, y+inner_radius), (x+inner_radius, y-inner_radius)),
                                                fill=True, color=HOUSING_COLOR, lw=2))

        nrows = 30
        ncols = 5

        # Dimensionss from breadboard spec sheets
        strip_w = .37 * INCH  # Edge/power strips are 0.37 inch
        edgepad = (strip_w - PINSPACING)/2  # distance from edge to center of first pin in the strip
        width = 2.10 * INCH  # Total width
        height = 3.3 * INCH  # Total height
        top = 1.5 * edgepad  # Offset the top/left so that (0, 0) is top of left power strip
        left = -edgepad
        right = left+width

        # Frame - inherit color from element
        self.segments.append(
            SegmentPoly(((left, top), (right, top),
                         (right, top-height), (left, top-height)), lw=2))

        x = y = 0.
        # Left power strip holes
        for col in range(2):
            for row in range(nrows):
                if row % 6 == 0: continue
                xy1 = x, y-row*PINSPACING
                xy2 = x+PINSPACING, y-row*PINSPACING 
                hole(*xy1)
                hole(*xy2)
                self.anchors[f'L1_{row}'] = xy1
                self.anchors[f'L2_{row}'] = xy2

        # Right power strip holes
        x = right - edgepad
        for col in range(2):
            for row in range(nrows):
                if row % 6 == 0: continue
                xy1 = x, y-row*PINSPACING
                xy2 = x-PINSPACING, y-row*PINSPACING
                hole(*xy1)
                hole(*xy2)
                self.anchors[f'R1_{row}'] = xy2
                self.anchors[f'R2_{row}'] = xy1

        # Inner Rows
        x = strip_w
        for col in range(ncols):
            colname = chr(ord('A')+col)
            self.segments.append(SegmentText((x+col*PINSPACING, y+PINSPACING), colname,
                                             fontsize=8, rotation_global=False, align=('center', 'center'),
                                             color=text_color, zorder=1))
            for row in range(nrows):
                xy = x+col*PINSPACING, y-row*PINSPACING
                hole(*xy)
                self.anchors[f'{colname}{row+1}'] = xy
        
        for col in range(ncols):
            colname = chr(ord('F')+col)
            self.segments.append(SegmentText((x+ PINSPACING*7+col*PINSPACING, y+PINSPACING), colname,
                                             fontsize=8, rotation_global=False, align=('center', 'center'),
                                             color=text_color, zorder=1))
            for row in range(nrows):
                xy = x+ PINSPACING*7 + col*PINSPACING, y-row*PINSPACING
                hole(*xy)
                self.anchors[f'{colname}{row+1}'] = xy
        
        # Number Labels
        for row in range(0, nrows):
            self.segments.append(SegmentText((x-PINSPACING, y-row*PINSPACING-.04), str(row+1), fontsize=8,
                                             rotation_global=False, align=('center', 'bottom'), color=text_color, zorder=1))
            self.segments.append(SegmentText((x+PINSPACING*12, y-row*PINSPACING-.04), str(row+1), fontsize=8,
                                             rotation_global=False, align=('center', 'bottom'), color=text_color, zorder=1))


        # Vertical dividing lines
        self.segments.append(Segment(((left+edgepad*.4, top-PINSPACING*2), (left+edgepad*.4, top-height+PINSPACING)), color='red', lw=.5))
        self.segments.append(Segment(((left+strip_w-edgepad*.4, top-PINSPACING*2), (left+strip_w-edgepad*.4, top-height+PINSPACING)), color='blue', lw=.5))
        self.segments.append(Segment(((right-edgepad*.4, top-PINSPACING*2), (right-edgepad*.4, top-height+PINSPACING)), color='blue', lw=.5))
        self.segments.append(Segment(((right-strip_w+edgepad*.4, top-PINSPACING*2), (right-strip_w+edgepad*.4, top-height+PINSPACING)), color='red', lw=.5))
