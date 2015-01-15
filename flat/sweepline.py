'''
Use Sweepline algorithm, or Bentley-Ottmann algorithm to analysis intersections
between different neurites.
For details of sweepline algorithm, visit
http://geomalgorithms.com/a09-_intersect-3.html .
'''

from llrbt import NIL, Node, Tree


########## Functions ##########

def xyorder(p1, p2):
    '''Determine the order of two points.
    Returns +1 if p1 > p2; -1 if p1 < p2; 0 if p1 == p2.'''
    if p1.x > p2.x:
        return 1
    if p1.x < p2.x:
        return -1
    if p1.y > p2.y:
        return 1
    if p1.y < p2.y:
        return -1
    return 0

def float_eq(x1, x2):
    '''Equal between two float point numbers.'''
    if abs(x1 - x2) <= 0.0000001:
        return True
    return False


########## Classes ##########

class Point(object):
    '''Endpoint of a segment.'''
    def __init__(self, coor):
        self.coor = coor
        self._x = coor[0]
        self._y = coor[1]

    def __eq__(self, other):
        '''Equal are guarenteed by float_eq().'''
        if float_eq(self.x, other.x) and float_eq(self.y, other.y):
            return True
        return False

    def __gt__(self, other):
        '''Comparisons are made x first then y.'''
        if self.x > other.x:
            return True
        if float_eq(self.x, other.x) and self.y > other.y:
            return True
        return False

    def __lt__(self, other):
        '''Comparisons are made x first then y.'''
        if self.x < other.x:
            return True
        if float_eq(self.x, other.x) and self.y < other.y:
            return True
        return False

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def isleft(self):
        return self == self.segment.left

    @property
    def isright(self):
        return self == self.segment.right

    @property
    def segment(self):
        try:
            return self._segment
        except AttributeError:
            return None

    @segment.setter
    def segment(self, val):
        '''Setter for segment.'''
        self._segment = val


class Segment(object):
    '''Class of segment. Used for determine whether there exist any
    intersection points between two sets of segments.'''

    def __init__(self, point1, point2, branch=0):
        '''coor1 and coor2 are the two endpoints of a segment.'''
        if point1.coor[0] < point2.coor[0]:
            self.left = point1
            self.right = point2
        elif point1.coor[0] == point2.coor[0] and \
            point1.coor[1] <= point2.coor[1]:
                self.left = point1
                self.right = point2
        else:
            self.left = point2
            self.right = point1

        point1.segment = self
        point2.segment = self
        self.branch = branch

    def intersects(self, seg):
        '''Calculate intersection point bewteen self and another
        segment seg.
        Read documents for mechanism.'''
        p = np.array(self.left.coor)
        r = np.array(self.right.coor) - p
        q = np.array(seg.left.coor)
        s = np.array(seg.right.coor) - q

        if np.cross(r, s) == 0:
            if np.cross(q - p, r) != 0:
                return False
            elif 0 <= np.inner(q - p, r) <= np.inner(r, r) or \
                0 <= np.inner(p - q, s) <= np.inner(s, s):
                return True
            else:
                return False
        else:
            btm = np.cross(r, s)
            t = np.cross(q - p, s) / btm
            u = np.cross(q - p, r) / btm
            if 0 <= t <= 1 and 0 <= u <= 1:
                return True
            else:
                return False
