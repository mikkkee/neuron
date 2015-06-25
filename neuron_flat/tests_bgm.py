from unittest import TestCase

from bgm import Node
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
