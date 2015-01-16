'''
Use Sweepline algorithm, or Bentley-Ottmann algorithm to analysis intersections
between different neurites.
For details of sweepline algorithm, visit
http://geomalgorithms.com/a09-_intersect-3.html .

Procedures:

'''
import numpy as np
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
        if isinstance(other, Point):
            return float_eq(self.x, other.x) and float_eq(self.y, other.y)
        return NotImplemented

    def __ne__(self, other):
        '''Not equal.'''
        if isinstance(other, Point):
            return not self.__eq__(other)
        return NotImplemented

    def __gt__(self, other):
        '''Comparisons are made x first then y.'''
        if isinstance(other, Point):
            if self.x > other.x:
                return True
            if float_eq(self.x, other.x) and self.y > other.y:
                return True
            return False
        return NotImplemented

    def __lt__(self, other):
        '''Comparisons are made x first then y.'''
        if isinstance(other, Point):
            if self.x < other.x:
                return True
            if float_eq(self.x, other.x) and self.y < other.y:
                return True
            return False
        return NotImplemented

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def isleft(self):
        if self.segment:
            return self == self.segment.left
        return False

    @property
    def isright(self):
        if self.segment:
            return self == self.segment.right
        return False

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
        Return True is two segments overlap, False if two segments do not
        intersect, intersection point if two segments have intersection.
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
            # np.array() and np.cross() does not guarantee float number.
            btm = float(np.cross(r, s))
            t = np.cross(q - p, s) / btm
            u = np.cross(q - p, r) / btm
            if 0 <= t <= 1 and 0 <= u <= 1:
                coor = tuple(p + t * r)
                intersection = Point(coor)
                return intersection
            else:
                return False

    def __gt__(self, seg):
        '''A segment is considered to be greater than another if it is above
        the left point of another segment.
        '''
        if isinstance(seg, Segment):
            point = seg.left
            y = (self.right.y - self.left.y)/(self.right.x - self.left.x) * (point.x - self.left.x) + self.left.y
            return y > point.y
        return NotImplemented

    def __lt__(self, seg):
        '''A segment is considered to be less than another segment if it is
        below the left point of another segment.
        '''
        if isinstance(seg, Segment):
            point = seg.left
            y = (self.right.y - self.left.y)/(self.right.x - self.left.x) * (point.x - self.left.x) + self.left.y
            return y < point.y
        return NotImplemented

    def __eq__(self, seg):
        '''A segment is considered to be equal to another segment if they have
        the same left and right point.
        '''
        if isinstance(seg, Segment):
            return self.left == seg.left and self.right == seg.right


class SweepLine(Tree):
    '''Sweep line class.'''

    def insert(self, node):
        '''Insert a node into SweepLine and change the corresponding
        above-below relation.
        '''
        super(SweepLine, self).insert(node)
        node.below = self.predecessor(node)
        node.above = self.successor(node)
        node.below.above = node
        node.above.below = node

    def delete(self, node):
        '''Delete a node from SweepLine and change the corresponding
        above-below relation.
        Since Tree.delete() does not return the node be deleted, you have to
        find the node to be deleted before delete it. That is:
        node = SL.find(key=seg)
        SL.delete(node)
        Do not delete by using another node object with the same key:
        SL.delete(Node(seg)).
        '''
        super(SweepLine, self).delete(node)
        if node.above == node:
            node.below.above = node.below
        else:
            node.below.above = node.above

        if node.below == node:
            node.above.below = node.above
        else:
            node.above.below = node.below


class EventQueue(Tree):
    '''Event queue class used to maintain segment end points and intersection
    points.
    '''
    def pop(self):
        '''Delete the minimum node.'''
        to_pop = self.min()
        self.delete_min()
        return to_pop
