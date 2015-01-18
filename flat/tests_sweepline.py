from __future__ import print_function
from unittest import TestCase

from sweepline import TreeNode, Point, Segment, SweepLine, EventQueue


class PointTest(TestCase):
    '''Point related.'''

    def setUp(self):
        self.p1 = Point((0, 0))
        self.p2 = Point((1, 0))
        self.p3 = Point([0, -1])
        self.p4 = Point([-1, 0])
        self.p5 = Point([0, 1])

    def test_point_sort(self):
        '''Test to sort points by x first then y.'''
        point_list = [self.p1, self.p2, self.p3, self.p4, self.p5]
        point_list.sort()
        self.assertEqual(point_list, [self.p4, self.p3, self.p1, self.p5, self.p2])

    def test_no_seg(self):
        self.assertFalse(self.p1.segment or self.p2.segment)

    def test_isleft(self):
        self.seg = Segment(self.p2, self.p1, 1)
        self.assertTrue(self.p1.isleft and self.p2.isright)
        self.assertFalse(self.p1.isright or self.p2.isleft)

    def test_lt(self):
        p = Point((0, 0.5))
        self.assertTrue(self.p1 < p)
        self.assertTrue(self.p1 < self.p2)
        self.assertFalse(p < self.p1)
        self.assertFalse(self.p2 < self.p1)
        self.assertFalse(self.p1 < self.p1)

    def test_eq(self):
        p = Point((0, 0.0000000000001))
        self.assertTrue(self.p1 == p)
        self.assertFalse(self.p1 == self.p2)

    def test_gt__(self):
        p = Point((1, 0.5))
        self.assertTrue(p > self.p1)
        self.assertTrue(self.p2 > self.p1)
        self.assertTrue(p > self.p2)
        self.assertFalse(self.p1 > self.p2)
        self.assertFalse(self.p2 > p)


class SegmentTest(TestCase):
    '''Segment related.'''

    def setUp(self):
        self.p1 = Point((0, 0))
        self.p2 = Point((0, 1))
        self.p3 = Point((0, -1))
        self.p4 = Point((1, -1))
        self.p5 = Point((1, 0))

    def test_seg_left_right(self):
        '''Test for setting left and right end points.'''
        self.seg1 = Segment(self.p1, self.p2, 1)
        self.assertTrue(self.p1.isleft and self.p2.isright)

    def test_seg_intersects(self):
        '''Test for intersection judgement.'''

        # Two segments intersect with each other. self.intersects() gives
        # the right intersection point.
        self.seg1 = Segment(self.p1, self.p4, 1)
        self.seg2 = Segment(self.p3, self.p5, 1)
        intersection = self.seg1.intersects(self.seg2)
        self.assertTrue(intersection)
        self.assertTrue(isinstance(intersection, Point))
        self.assertTrue(intersection == Point((0.5, -0.5)))

        # Two segments do not intersect.
        self.seg1 = Segment(self.p1, self.p5, 1)
        self.seg2 = Segment(self.p3, self.p4, 1)
        self.assertFalse(self.seg1.intersects(self.seg2))


class SweepLineTest(TestCase):
    '''Test for sweepline, subclass of left-lean red-black tree.'''

    def setUp(self):
        self.node = TreeNode(5)
        self.sl = SweepLine(self.node)

    def test_insert(self):
        '''Insert a node to sweepline.'''
        n = TreeNode(4)
        self.sl.insert_treenode(n)
        self.assertTrue(len(self.sl.nodes()), 2)
