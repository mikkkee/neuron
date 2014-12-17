from unittest import TestCase

from bgm import Node, Point, Segment
from bgm import dump, random_coor, branch_prob, rotate

import settings


class RandomCoorTest(TestCase):
    '''Tests for random_coor() function.'''

    def setUp(self):
        self.n = 3
        self.x = 100
        self.y = 100

    def test_return_n(self):
        '''Shoud return a list of self.n different tuples.'''
        self.result = random_coor(self.x, self.y, self.n)
        self.assertEqual(len(self.result), self.n)
        self.assertEqual(len(set(self.result)), self.n)


class RotateTest(TestCase):
    '''Test when alpha_min == alpha_max == 0.'''

    def setUp(self):
        self.alpha_min = settings.ALPHA_MIN
        self.alpha_max = settings.ALPHA_MAX

    def test_rotate(self):
        if self.alpha_min == self.alpha_max == 0:
            self.direction = [1.0, 2.0]
            self.assertEqual(rotate(self.direction)[0], self.direction[0])
            self.assertEqual(rotate(self.direction)[1], self.direction[1])


class NodeTest(TestCase):
    '''Node Related tests.'''

    def setUp(self):
        pass


class PointTest(TestCase):
    '''Point related.'''

    def setUp(self):
        self.p1 = Point((0, 0))
        self.p2 = Point((1, 0))

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
        self.seg1 = Segment(self.p1, self.p2, 1)
        self.assertTrue(self.p1.isleft and self.p2.isright)

    def test_seg_intersects(self):
        '''Test for intersection judgement.'''

        # Two segments intersect with each other.
        self.seg1 = Segment(self.p1, self.p4, 1)
        self.seg2 = Segment(self.p3, self.p5, 1)
        self.assertTrue(self.seg1.intersects(self.seg2))

        # Two segments do not intersect.
        self.seg1 = Segment(self.p1, self.p5, 1)
        self.seg2 = Segment(self.p3, self.p4, 1)
        self.assertFalse(self.seg1.intersects(self.seg2))
