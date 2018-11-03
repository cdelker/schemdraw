"""
Electrical Schematic Drawing

https://cdelker.bitbucket.io/SchemDraw/
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
from matplotlib.patches import Arc
import copy

from . import elements

#--------------------------------------------------------------------
# Set up matplotlib parameters
#--------------------------------------------------------------------
mpl.rcParams['figure.subplot.left']   = 0.05
mpl.rcParams['figure.subplot.bottom'] = 0.05
mpl.rcParams['figure.subplot.right']  = 0.95
mpl.rcParams['figure.subplot.top']    = 0.90
mpl.rcParams['font.family'] = 'sans-serif'
mpl.rcParams['mathtext.fontset'] = 'stixsans'
mpl.rcParams['mathtext.default'] = 'regular'

#--------------------------------------------------------------------
# Define transformation matricies
#--------------------------------------------------------------------
mirror_matrix = np.array([[-1, 0], [0, 1]])
flip_matrix = np.array([[1, 0], [0, -1]])


#--------------------------------------------------------------------
# Internal functions
#--------------------------------------------------------------------
def _angle(a, b):
    """ Compute angle from coordinate a to b
    """
    theta = np.degrees(np.arctan2(b[1] - a[1], (b[0] - a[0])))
    return theta


def _distance(a, b):
    ''' Compute distance from A to B '''
    r = np.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)
    return r


def _merge_elements(elm_def):
    """ Combine element with it's base elements.
    """
    while 'base' in elm_def:
        base_elm = elm_def['base']
        elm_def.pop('base')

        elm_def['paths'] = elm_def.get('paths', []) + base_elm.get('paths',  [])
        elm_def['labels'] = elm_def.get('labels', []) + base_elm.get('labels', [])
        elm_def['shapes'] = elm_def.get('shapes', []) + base_elm.get('shapes', [])

        # New anchors with same name should overwrite old
        d = base_elm.get('anchors', {}).copy()
        d.update(elm_def.get('anchors', {}))
        elm_def['anchors'] = d

        for i in base_elm:
            # Everything that's not a list. New key/values overwrite old.
            # If base has a base, will be added and loop will pick it up.
            if i not in ['paths', 'labels', 'shapes', 'anchors'] and i not in elm_def:
                elm_def[i] = base_elm[i]
    return elm_def


#--------------------------------------------------------------------
def group_elements(drawing, anchors=None):
    ''' Combine all elements in a drawing into a single element that can be added to
        another drawing. Returns an element definition.

        drawing: The drawing object. All elements in the drawing will be combined.
        anchors: New anchor dictionary to use for the new element.
    '''
    new_elm = {'paths': [],
               'shapes': [],
               'labels': [],
               'anchors': {}}
    for elm in drawing._elm_list:
        new_elm['paths'].extend(elm.paths)
        for s in elm.shapes:
            s = s.copy()
            if s['shape'] == 'circle':
                s['center'] = elm.translate(s['center'] - elm.ofst)
            elif s['shape'] == 'poly':
                s['xy'] = elm.translate(s['xy'] - elm.ofst)
            elif s['shape'] == 'arc':
                s['center'] = elm.translate(s['center'] - elm.ofst)
            elif s['shape'] == 'arrow':
                s['start'] = elm.translate(s['start'] - elm.ofst)
                s['end'] = elm.translate(s['end'] - elm.ofst)
            new_elm['shapes'].append(s)

        if anchors is not None:
            new_elm['anchors'] = anchors

        for label, loc, align, size in elm.strs:
            loc = elm.translate(np.array(loc))
            new_elm['labels'].append({'label':label, 'pos':loc, 'align':align, 'size':size})
        new_elm['extend'] = False
        new_elm['drop'] = drawing.here

    return new_elm


#--------------------------------------------------------------------
# Main drawing class
#--------------------------------------------------------------------
class Drawing(object):
    def __init__(self, unit=3.0, inches_per_unit=0.5, txtofst=0.1, fontsize=16, font='sans-serif', color='black', lw=1.5):
        """ Set up a new circuit drawing.
    unit : Full length of a resistor element in matplotlib plot units.
           Inner portion of resistor is length 1.
    inches_per_unit : inches per unit to scale drawing.
    txtofst  : Default distance from element to text label
    fontsize : Default font size
    font     : matplotlib font-family
    color    : default color for elements
    lw       : default line width
    """
        # Default values
        self.unit = unit  # Default length of 2-terminal element, including leads
        self.inches_per_unit = inches_per_unit
        self.txtofst = txtofst
        self.fontsize = fontsize
        self.font = font
        self.color = color
        self.lw = lw

        # State variables
        self.here = np.array([0, 0])
        self.theta = 0
        self._state = []
        self._elm_list = []

    def add(self, elm_def, **kwargs):
        ''' Add an element to the schematic.

elm_def  : element definition dictionary (see below)

Element properties are specified using kwargs as follows.

Position of element [Default = endpoint of last element]:
    xy     : [x,y] starting coordiante.
             Element drawn in current direction and default length.
    endpts : [[x1,y1], [x2,y2]] start and end coordinates
    to     : [x,y] end coordinate
    tox    : x-value of end coordinate (y-value same as start)
    toy    : y-value of end coordinate (x-value same as start)
    l      : total length of element
    zoom   : zoom/magnification for element (default=1)
    anchor : 'xy' argument refers to this position within the element.
             For example, an opamp can be anchored to 'in1', 'in2', or 'out'

'to', 'tox', 'toy', 'l' can be used with 'xy' to define start and end points.

Direction [Default = direction of last element]:
    d       : direction ['up','down','left','right']
    theta   : angle (in degrees) to draw the element. Overrides 'd'.
    flip    : flip the element vertically (when theta=0)
    reverse : reverse a directional element (e.g. diode)

Labels [Default = no label]:
    label, toplabel, botlabel, lftlabel, rgtlabel:
        Add a string label to the element. Can be a string, or list
        of strings to be evenly spaced along element, e.g. ['-','R1','+']
        Use $ for latex-style symbols, e.g. '$R_1 = 100 \Omega$'

    lblofst : offset between text label and element

Other:
    move_cur : move the cursor after drawing. Default=True.
    color    : matplotlib color for element. e.g. 'red', '#34a4e6', (.8,0,.8)
    '''
        e = Element(elm_def, self, **kwargs)
        self._elm_list.append(e)
        if kwargs.get('move_cur', True) and elm_def.get('move_cur', True):
            self.here = e.here
            self.theta = e.theta
        return e

    def push(self):
        """ Push/save the drawing state. Location and angle are saved.
        """
        self._state.append((self.here, self.theta))

    def pop(self):
        """ Pop/load the drawing state.
            Location and angle are returned to previously pushed state.
        """
        if len(self._state) > 0:
            self.here, self.theta = self._state.pop()

    def draw(self, ax=None, showframe=False, showplot=True):
        """ Draw the diagram.
            ax : matplotlib axis to draw to.
            showframe : Show the plot frame/axis. Useful for debugging.
            showplot : Show the plot in matplotlib window in non-interactive mode.
        """

        mpl.rcParams['font.size'] = self.fontsize
        mpl.rcParams['font.family'] = self.font

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.get_figure()

        for e in self._elm_list:
            e.draw(ax)

        ax.autoscale_view(True)  # This autoscales all the shapes too
        # NOTE: arrows don't seem to be included in autoscale!
        xlim = np.array(ax.get_xlim())
        ylim = np.array(ax.get_ylim())
        xlim[0] = xlim[0]-.1   # Add a .1 unit border to pick up lost pixels
        ylim[0] = ylim[0]-.1
        xlim[1] = xlim[1]+.1
        ylim[1] = ylim[1]+.1
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
        w = xlim[1]-xlim[0]
        h = ylim[1]-ylim[0]

        if not showframe:
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            ax.set_frame_on(False)

        self.ax = ax
        self.fig = ax.get_figure()
        if not plt.isinteractive() and showplot:
            plt.show()

        # Grow the figure size so that elements are always the same
        # Do after show() because it messes with size.
        ax.get_figure().set_size_inches(self.inches_per_unit*w, self.inches_per_unit*h)

    def save(self, fname, transparent=True, dpi=72):
        """ Save figure to file.
            fname : filename to save.
                    File type automatically determined from extension.
        """
        self.fig.savefig(fname, bbox_extra_artists=self.ax.get_default_bbox_extra_artists(), bbox_inches='tight', transparent=transparent, dpi=dpi)

    # Functions to help define specific elements
    def labelI(self, elm, label='', arrowofst=0.4, arrowlen=2, reverse=False, top=True):
        ''' Add an arrow element along side another element
        elm       : element to add arrow to
        label     : string or list of strings to space along arrow
        arrowofst : distance from element to arrow
        arrowlen  : length of arrow in drawing units
        reverse   : reverse the arrow direction
        top       : [True,False] draw on top (or bottom) of element
         '''
        if not top:
            arrowofst = -arrowofst

        x = elm.center[0] - np.sin(np.deg2rad(elm.theta))*arrowofst
        y = elm.center[1] + np.cos(np.deg2rad(elm.theta))*arrowofst

        if reverse:
            arrowlen = -arrowlen

        arrow = copy.deepcopy(elements.ARROW_I)
        arrow['shapes'][0]['start'] = [1-arrowlen/2, 0]
        arrow['shapes'][0]['end'] = [1+arrowlen/2, 0]

        if top:
            self.add(arrow, theta=elm.theta, label=label, anchor='center', xy=[x, y])
        else:
            self.add(arrow, theta=elm.theta, botlabel=label, anchor='center', xy=[x, y])

    def loopI(self, elm_list, label='', d='cw', theta1=35, theta2=-35, pad=.2):
        ''' Label the loop current bordered by elements in list,
            elm_list : boundary elements in order of top, right, bot, left
            label    : text label for center of loop
            d        : arrow direction 'cw' or 'ccw'
            theta1   : start angle of arrow arc (degrees)
            theta2   : end angle of arrow arc (degrees)
            pad      : distance between element and arc
        '''
        bbox1 = elm_list[0].translate([elm_list[0].xmin, elm_list[0].ymin])
        bbox2 = elm_list[0].translate([elm_list[0].xmax, elm_list[0].ymax])
        top = min(bbox1[1], bbox2[1])
        bbox1 = elm_list[1].translate([elm_list[1].xmin, elm_list[1].ymin])
        bbox2 = elm_list[1].translate([elm_list[1].xmax, elm_list[1].ymax])
        rght = min(bbox1[0], bbox2[0])
        bbox1 = elm_list[2].translate([elm_list[2].xmin, elm_list[2].ymin])
        bbox2 = elm_list[2].translate([elm_list[2].xmax, elm_list[2].ymax])
        bot = max(bbox1[1], bbox2[1])
        bbox1 = elm_list[3].translate([elm_list[3].xmin, elm_list[3].ymin])
        bbox2 = elm_list[3].translate([elm_list[3].xmax, elm_list[3].ymax])
        left = max(bbox1[0], bbox2[0])

        top = top - pad
        bot = bot + pad
        rght = rght - pad
        left = left + pad
        center = [(left+rght)/2, (top+bot)/2]

        loop = {'shapes': [{'shape': 'arc',
                            'center': [0,0],
                            'theta1': theta1,
                            'theta2': theta2,
                            'width': rght-left,
                            'height': top-bot,
                            'arrow': d}],
                'move_cur': False,
                'lblloc': 'center',
                'lblofst': 0
                }

        L = self.add(loop, xy=center, d='right')
        L.add_label(label, loc='center', ofst=0, align=('center', 'center'))
        return L


#--------------------------------------------------------------------
# Circuit element class
#--------------------------------------------------------------------
class Element(object):
    def __init__(self, elm_def, drawing, **kwargs):
        """ Initialize the element.
elm_def  : element definition dictionary (see below)
drawing  : drawing to add the element to

Element properties are specified using kwargs as follows.

Position of element [Default = endpoint of last element]:
    xy     : [x,y] starting coordiante.
             Element drawn in current direction and default length.
    endpts : [[x1,y1], [x2,y2]] start and end coordinates
    to     : [x,y] end coordinate
    tox    : x-value of end coordinate (y-value same as start)
    toy    : y-value of end coordinate (x-value same as start)
    l      : total length of element
    zoom   : zoom/magnification for element (default=1)
    anchor : 'xy' argument refers to this position within the element.
             For example, an opamp can be anchored to 'in1', 'in2', or 'out'

'to', 'tox', 'toy', 'l' can be used with 'xy' to define start and end points.

Direction [Default = direction of last element]:
    d       : direction ['up','down','left','right']
    theta   : angle (in degrees) to draw the element. Overrides 'd'.
    flip    : flip the element vertically (when theta=0)
    reverse : reverse a directional element (e.g. diode)

Labels [Default = no label]:
    label, toplabel, botlabel, lftlabel, rgtlabel:
        Add a string label to the element. Can be a string, or list
        of strings to be evenly spaced along element, e.g. ['-','R1','+']
        Use $ for latex-style symbols, e.g. '$R_1 = 100 \Omega$'

    lblofst : offset between text label and element

Other:
    move_cur : move the cursor after drawing. Default=True.
    color    : matplotlib color for element. e.g. 'red', '#34a4e6', (.8,0,.8)
    ls       : line style. same as matplotlib: ['-', ':', '--']
    lw       : line width. same as matplotlib. Default=1
    """
        # Flatten element def with base elements
        self.defn = elm_def.copy()
        if 'base' in self.defn:
            self.defn = _merge_elements(self.defn)

        # Get some parameters
        self.drawing = drawing
        self.shapes = self.defn.get('shapes', [])
        self.color = kwargs.get('color', self.defn.get('color', drawing.color))
        self.ls = kwargs.get('ls', self.defn.get('ls', '-'))
        self.lw = kwargs.get('lw', self.defn.get('lw', drawing.lw))
        totlen = kwargs.get('l', drawing.unit)

        # Determine theta angle of element
        default_theta = self.defn.get('theta', drawing.theta)
        if 'endpts' in kwargs:
            endpts = kwargs['endpts']
            self.theta = _angle(endpts[0], endpts[1])
        elif 'theta' in kwargs:
            self.theta = kwargs['theta']
        elif 'd' in kwargs:
            self.theta = {'up':90, 'right':0, 'left':180, 'down':270}[kwargs['d']]
        elif 'to' in kwargs:
            self.theta = _angle(kwargs.get('xy', drawing.here), kwargs['to'])
        else:
            self.theta = default_theta

        # Get offset to element position
        if 'endpts' in kwargs:
            self.trans = kwargs['endpts'][0]
        elif 'xy' in kwargs:
            self.trans = np.array(kwargs['xy'])
        else:
            self.trans = drawing.here

        # Get offset due to anchoring
        if 'anchor' in kwargs:
            anchor = kwargs['anchor']
            if 'anchors' in self.defn and anchor in self.defn['anchors']:
                self.ofst = np.array(self.defn['anchors'][anchor])
            else:
                print('Anchor %s not defined in element' % anchor)
                self.ofst = np.array([0, 0])  # Default to 'start'
        else:
            self.ofst = np.array([0, 0])

        # Last path in list should be the one to get lead extensions.
        # The others should just have extend offset applied.
        self.path_def = [np.array(p) for p in self.defn.get('paths', [])]
        self.paths = []   # Translated paths

        if len(self.path_def) == 0:
            start = np.array([0, 0])
            end = np.array([0, 0])
        elif self.defn.get('extend', True):
            in_path = self.path_def[-1]
            dz = in_path[-1]-in_path[0]
            in_len = np.sqrt(dz[0]*dz[0]+dz[1]*dz[1])

            if 'endpts' in kwargs:
                endpts = kwargs['endpts']
                totlen = _distance(endpts[0], endpts[1])
            elif 'to' in kwargs:
                # Move until X or Y position is 'end'. Depends on direction
                endpt = kwargs['to']
                totlen = _distance(self.trans, endpt)
            elif 'tox' in kwargs:
                # Allow either full coordinate (only keeping x), or just an x value
                if isinstance(kwargs['tox'], float) or isinstance(kwargs['tox'], int):
                    x = float(kwargs['tox'])
                else:
                    x = kwargs['tox'][0]
                endpt = [x, self.trans[1]]
                totlen = _distance(self.trans, endpt)
            elif 'toy' in kwargs:
                # Allow either full coordinate (only keeping y), or just a y value
                if isinstance(kwargs['toy'], float) or isinstance(kwargs['toy'], int):
                    y = kwargs['toy']
                else:
                    y = kwargs['toy'][1]
                endpt = [self.trans[0], y]
                totlen = _distance(self.trans, endpt)

            lead_len = (totlen - in_len)/2
            start = in_path[0] - np.array([lead_len, 0])
            end = in_path[-1] + np.array([lead_len, 0])
            p = np.vstack((start, in_path, end))
            if _distance(self.ofst, [0, 0]) == 0:
                self.ofst = start  # Offset due to lead extension
            p = p - self.ofst
            self.paths.append(p)
        else:
            # Don't extend leads
            self.paths.append(self.path_def[-1] - self.ofst)

        # Process all the other paths, adding in extend offset
        for p in self.path_def[:-1]:
            self.paths.append(p - self.ofst)

        if len(self.path_def) == 0:
            self.drop = np.array([0, 0])
        else:
            self.drop = self.defn.get('drop', self.paths[0][-1])

        self.flip = kwargs.get('flip', False)       # Flip (up/down when theta=0)
        self.reverse = kwargs.get('reverse', False) # Reverse (left/right)

        self.xmin, self.ymin, self.xmax, self.ymax = self.get_bbox()

        # Get labels from arguments.
        # 'label' defaults to 'top' unless overridden in element def.
        self.strs = []
        if 'base' not in self.defn:
            label = kwargs.get('label', None)
            dfltlbl = kwargs.get('lblloc', self.defn.get('lblloc', 'top'))
            toplabel = kwargs.get('toplabel', None)
            botlabel = kwargs.get('botlabel', None)
            rgtlabel = kwargs.get('rgtlabel', None)
            lftlabel = kwargs.get('lftlabel', None)
            self.lbl_ofst = kwargs.get('lblofst', self.defn.get('lblofst', drawing.txtofst))
            if label is not None:    self.add_label(label, dfltlbl,  ofst=self.lbl_ofst, size=drawing.fontsize)
            if toplabel is not None: self.add_label(toplabel, 'top', ofst=self.lbl_ofst, size=drawing.fontsize)
            if botlabel is not None: self.add_label(botlabel, 'bot', ofst=self.lbl_ofst, size=drawing.fontsize)
            if rgtlabel is not None: self.add_label(rgtlabel, 'rgt', ofst=self.lbl_ofst, size=drawing.fontsize)
            if lftlabel is not None: self.add_label(lftlabel, 'lft', ofst=self.lbl_ofst, size=drawing.fontsize)

        txtlist = self.defn.get('labels', [])
        for txtlbl in txtlist:
            align = txtlbl.get('align', ('center', 'center'))
            size = txtlbl.get('size', drawing.fontsize)
            pos = txtlbl.get('pos', [0, 0])
            self.strs.append(((txtlbl['label'], np.array(pos)-self.ofst, align, size)))

        self.z = kwargs.get('zoom', 1)

        # Generate rotation matrix from theta
        c = np.cos(np.radians(self.theta))
        s = np.sin(np.radians(self.theta))
        self.m = np.array([[c, s],[-s, c]])

        # Translate paths
        for i in range(len(self.paths)):
            self.paths[i] = self.translate(self.paths[i])

        # Define anchors
        if len(self.path_def) == 0:
            setattr(self, 'start',  self.translate(np.array([0, 0])))
            setattr(self, 'end',    self.translate(np.array([0, 0])))
            setattr(self, 'center', self.translate(np.array([0, 0])))
        else:
            setattr(self, 'start', self.paths[0][0])
            setattr(self, 'end',   self.paths[0][-1])
            setattr(self, 'center', (self.paths[0][0] + self.paths[0][-1])/2)
        if 'anchors' in self.defn:
            for aname, apoint in self.defn['anchors'].items():
                if getattr(self, aname, None) is not None:  # Try not to clobber element parameter names!
                    aname = 'anchor_' + aname
                setattr(self, aname, self.translate(np.array(apoint)-self.ofst))

        # Translated end point for new drawing position
        self.here = self.translate(self.drop, doflip=False)

    def get_bbox(self):
        """ Get element bounding box, including path and shapes.
        """
        xmin = ymin = np.inf
        xmax = ymax = -np.inf
        for path in self.paths:
            for p in path:
                xmin = min(xmin, p[0])
                ymin = min(ymin, p[1])
                xmax = max(xmax, p[0])
                ymax = max(ymax, p[1])
        for s in self.shapes:
            if s['shape'] == 'arrow':
                start = np.array(s['start']) - self.ofst
                end   = np.array(s['end']) - self.ofst
                xmin = min(xmin, start[0], end[0])
                ymin = min(ymin, start[1], end[1])
                xmax = max(xmax, start[0], end[0])
                ymax = max(ymax, start[1], end[1])
            elif s['shape'] == 'circle':
                center = np.array(s['center']) - self.ofst
                rad    = s['radius']
                xmin = min(xmin, center[0]-rad)
                ymin = min(ymin, center[1]-rad)
                xmax = max(xmax, center[0]+rad)
                ymax = max(ymax, center[1]+rad)
            elif s['shape'] == 'poly':
                for v in s['xy']:
                    v = v - self.ofst
                    xmin = min(xmin, v[0])
                    ymin = min(ymin, v[1])
                    xmax = max(xmax, v[0])
                    ymax = max(ymax, v[1])
            elif s['shape'] == 'arc':
                center = s['center'] - self.ofst
                xmin = min(xmin, center[0] - s['width'])
                ymin = min(ymin, center[1] - s['height'])
                xmax = max(xmax, center[0] + s['width'])
                ymax = max(ymax, center[1] + s['height'])

        # Don't want to propogate infinities (e.g. shape not defined above)
        if xmax == -np.Inf: xmax = 0
        if ymax == -np.Inf: ymax = 0
        if xmin ==  np.Inf: xmin = 0
        if ymin ==  np.Inf: ymin = 0
        return xmin, ymin, xmax, ymax

    def add_label(self, label, loc='top', ofst=None, align=None, size=None):
        """ Add a label at the appropriate position
            label: text label to add
            loc: location for the label ['top', 'bot', 'lft', 'rgt'].
            ofst: unit offset between element bounding box and label.
            align: alignment tuple for (horizontal, vertical):
                   (['center', 'left', 'right'], ['center', 'top', 'bottom'])
            size: font size
        """
        if isinstance(ofst, list) and loc is not 'center':
            raise TypeError('Offset must not be list for loc=%s'%loc)

        if ofst is None:
            ofst = self.lbl_ofst

        # This ensures a 'top' label is always on top, regardless of rotation
        if (self.theta % 360) > 90 and (self.theta % 360) <= 270:
            if loc == 'top':
                loc = 'bot'
            elif loc == 'bot':
                loc = 'top'
            elif loc == 'lft':
                loc = 'rgt'
            elif loc == 'rgt':
                loc = 'lft'

        if align is None:   # Determine best alignment for label based on angle
            th = self.theta
            # Below alignment divisions work for label on top. Rotate angle for other sides.

            if loc == 'lft':
                th = th + 90
            elif loc == 'bot':
                th = th + 180
            elif loc == 'rgt':
                th = th + 270
            th = th % 360  # Normalize angle so it's positive, clockwise

            if th < 22.5:         # 0 to +22 deg
                align = ('center', 'bottom')
            elif th < 22.5+45:    #22 to 67
                align = ('right', 'bottom')
            elif th < 22.5+45*2:  # 67 to 112
                align = ('right', 'center')
            elif th < 22.5+45*3:  # 112 to 157
                align = ('right', 'top')
            elif th < 22.5+45*4:  # 157 to 202
                align = ('center', 'top')
            elif th < 22.5+45*5:  # 202 to 247
                align = ('left', 'top')
            elif th < 22.5+45*6:  # 247 to 292
                align = ('left', 'center')
            elif th < 22.5+45*7:  # 292 to 337
                align = ('left', 'bottom')
            else:                 #337 to 0
                align = ('center', 'bottom')

        xmax = self.xmax
        xmin = self.xmin
        ymax = self.ymax
        ymin = self.ymin

        if size is None:
            size=self.drawing.fontsize

        if self.flip:
            ymax, ymin = ymin, ymax
            if loc == 'top' or loc == 'bot':
                ofst = -ofst
        if self.reverse:
            xmax, xmin = xmin, xmax
            if loc == 'lft' or loc == 'rgt':
                ofst = -ofst

        if isinstance(label, list):
            # Divide list along length
            if loc == 'top':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    lbl_pt = [xmin+xdiv*(i+1), ymax+ofst]
                    self.strs.append((label[i], lbl_pt, align, size))
            elif loc == 'bot':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    lbl_pt = [xmin+xdiv*(i+1), ymin-ofst]
                    self.strs.append((label[i], lbl_pt, align, size))
            elif loc == 'lft':
                for i, lbltxt in enumerate(label):
                    ydiv = (ymax-ymin)/(len(label)+1)
                    lbl_pt = [xmin-ofst, ymin+ydiv*(i+1)]
                    self.strs.append((label[i], lbl_pt, align, size))
            elif loc == 'rgt':
                for i, lbltxt in enumerate(label):
                    ydiv = (ymax-ymin)/(len(label)+1)
                    lbl_pt = [xmax+ofst, ymin+ydiv*(i+1)]
                    self.strs.append((label[i], lbl_pt, align, size))
            elif loc == 'center':
                for i, lbltxt in enumerate(label):
                    xdiv = (xmax-xmin)/(len(label)+1)
                    lbl_pt = [xmin+xdiv*(i+1), ofst]
                    self.strs.append((label[i], lbl_pt, align, size))
        elif isinstance(label, str):
            # Place in center
            if loc == 'top':
                lbl_pt = [(xmax+xmin)/2, ymax+ofst]
            elif loc == 'bot':
                lbl_pt = [(xmax+xmin)/2, ymin-ofst]
            elif loc == 'lft':
                lbl_pt = [xmin-ofst, (ymax+ymin)/2]
            elif loc == 'rgt':
                lbl_pt = [xmax+ofst, (ymax+ymin)/2]
            elif loc == 'center':
                if isinstance(ofst, list):
                    lbl_pt = [(xmax+xmin)/2+ofst[0], (ymax+ymin)/2+ofst[1]]
                else:
                    lbl_pt = [(xmax+xmin)/2, (ymax+ymin)/2+ofst]
            self.strs.append((label, lbl_pt, align, size))

    def translate(self, pt, doflip=True):
        """ Translate the coordinate(s) to drawing position based on
            element's parameters.
            pt     : single coordinate or array of coordinates
            doflip : translate includes mirror/flip?
        """
        pt = np.array(pt)
        if doflip and self.reverse:
            pt = np.dot(pt, mirror_matrix) + [self.drop[0], 0]
        if doflip and self.flip:
            pt = np.dot(pt, flip_matrix)
        return np.dot(pt*self.z, self.m) + self.trans

    def draw(self, ax, showframe=False):
        """ Draw the element
            ax        : matplotlib axis
            showframe : Draw the axis frame. Useful for debugging.
        """
        for path in self.paths:
            ax.plot(path[:, 0], path[:, 1], color=self.color, lw=self.lw,
                    solid_capstyle='round', ls=self.ls)

        for s in self.shapes:
            if s.get('shape') == 'circle':
                xy = np.array(s.get('center', [0, 0]))
                xy = self.translate(xy - self.ofst)
                rad = s.get('radius', 1) * self.z
                fill = s.get('fill', False)
                fillcolor = s.get('fillcolor', self.color)
                circ = plt.Circle(xy=xy, radius=rad, ec=self.color,
                                  fc=fillcolor, fill=fill, zorder=3, lw=self.lw)
                ax.add_patch(circ)
            elif s.get('shape') == 'poly':
                xy = np.array(s.get('xy', [[0, 0]]))
                xy = self.translate(xy - self.ofst)
                closed = s.get('closed', True)
                fill = s.get('fill', False)
                fillcolor = s.get('fillcolor', self.color)
                poly = plt.Polygon(xy=xy, closed=closed, ec=self.color,
                                   fc=fillcolor, fill=fill, zorder=3, lw=self.lw)
                ax.add_patch(poly)
            elif s.get('shape') == 'arc':
                xy = np.array(s.get('center', [0, 0]))
                xy = self.translate(xy - self.ofst)

                w = s.get('width', 1) * self.z
                h = s.get('height', 1) * self.z
                th1 = s.get('theta1', 35)
                th2 = s.get('theta2', -35)
                if self.reverse: th1, th2 = th1+180, th2+180

                angle = s.get('angle', self.theta)
                arc = Arc(xy, width=w, height=h, theta1=th1,
                          theta2=th2, angle=angle, color=self.color, lw=self.lw)
                ax.add_patch(arc)

                # Add an arrowhead to the arc
                arrow = s.get('arrow', None)  # 'cw' or 'ccw' or None
                if arrow is not None:
                    # Apply stretch to theta to match MPL's arc
                    # (See change https://github.com/matplotlib/matplotlib/pull/8047/files)
                    x, y = np.cos(np.deg2rad(th2)), np.sin(np.deg2rad(th2))
                    th2 = np.rad2deg(np.arctan2((w/h)*y, x))
                    x, y = np.cos(np.deg2rad(th1)), np.sin(np.deg2rad(th1))
                    th1 = np.rad2deg(np.arctan2((w/h)*y, x))
                    if arrow == 'ccw':
                        
                        dx = np.cos(np.deg2rad(th2+90)) / 100
                        dy = np.sin(np.deg2rad(th2+90)) / 100
                        s = [xy[0] + w/2*np.cos(np.deg2rad(th2)),
                             xy[1] + h/2*np.sin(np.deg2rad(th2))]
                    else:
                        dx = -np.cos(np.deg2rad(th1+90)) / 100
                        dy = - np.sin(np.deg2rad(th1+90)) / 100

                        s = [xy[0] + w/2*np.cos(np.deg2rad(th1)),
                             xy[1] + h/2*np.sin(np.deg2rad(th1))]

                    # Rotate the arrow head
                    co = np.cos(np.radians(angle))
                    so = np.sin(np.radians(angle))
                    m = np.array([[co, so],[-so, co]])
                    s = np.dot(s-xy, m)+xy
                    darrow = np.dot([dx, dy], m)

                    ax.arrow(s[0], s[1], darrow[0], darrow[1], head_width=.15,
                             head_length=.25, color=self.color)

            elif s.get('shape') == 'arrow':
                start = np.array(s.get('start', [0, 0]))
                end = np.array(s.get('end', [1, 0]))
                start = self.translate(start - self.ofst)
                end = self.translate(end - self.ofst)
                hw = s.get('headwidth', .1)
                hl = s.get('headlength', .2)
                ax.arrow(start[0], start[1], end[0]-start[0], end[1]-start[1],
                         head_width=hw, head_length=hl,
                         length_includes_head=True, color=self.color, lw=self.lw)

        for label, loc, align, size in self.strs:
            loc = self.translate(np.array(loc))
            ha = align[0]
            va = align[1]
            ax.text(loc[0], loc[1], label, transform=ax.transData,
                    horizontalalignment=ha, verticalalignment=va,
                    fontsize=size)
