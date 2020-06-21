''' Schemdraw transformations for converting local element definition to
    global position within the drawing
'''

import numpy as np


def mirror_point(pt, centerx):
    ''' Mirror point along x axis about the centerx point '''
    mirror_matrix = np.array([[-1, 0], [0, 1]])
    pt = [pt[0]-centerx, pt[1]]
    return np.dot(pt, mirror_matrix) + np.array([centerx, 0])


def mirror_array(pts, centerx):
    ''' Mirror all points along x axis about the centerx point '''
    return [mirror_point(pt, centerx) for pt in pts]


def flip_point(pt):
    return np.asarray([pt[0], -pt[1]])


class Transform(object):
    ''' Class defining transformation matrix

        Parameters
        ----------
        rotate: array-like
            Rotation matrix
        globalshift: array-like
            Shift matrix [x, y] (applied after zoom and rotation)
        localshift: array-like
            Local-shift matrix [x, y] (applied before zoom and rotation)
        zoom: float
            Zoom factor
    '''
    def __init__(self, theta, globalshift, localshift=[0, 0], zoom=1):
        self.theta = theta
        self.shift = np.asarray(globalshift)
        self.localshift = np.asarray(localshift)
        self.zoom = zoom

        # Set up initial translation matrix
        c = np.cos(np.radians(self.theta))
        s = np.sin(np.radians(self.theta))
        self.rotate = np.array([[c, s], [-s, c]])

    def __repr__(self):
        return 'Transform: xy={}; theta={}; scale={}'.format(self.shift, self.theta, self.zoom)

    def transform(self, pt, ref=None):
        ''' Apply the transform to the point

            Parameters
            ----------
            pt: [x, y] array
                Original coordinates
            ref: string
                'start', 'end', or None, transformation reference
                (whether to apply localshift)

            Returns
            -------
            pt: [x, y] array
                Transformed coordinates
        '''
        lshift = {'start': np.asarray([0, 0]),
                  'end': self.localshift*2}.get(ref, self.localshift)
        return np.dot((pt+lshift)*self.zoom, self.rotate) + self.shift

    def transform_array(self, pts):
        ''' Apply the transform to multiple points

            Parameters
            ----------
            pts: array
                List of points to transform
        '''
        arr = np.empty((len(pts), 2))
        for i, pt in enumerate(pts):
            arr[i] = self.transform(pt)
        return arr
