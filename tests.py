from unittest import TestCase
import copy
import numpy as np

from neuron import Node, Path, Neuron
from neuron import coor_equal, check_connections, stats_connections

import settings

def float_equal(a, b):
    '''Equality check bewteen floats.'''

    # Convergence criteria.
    conv = 0.0001
    return True if abs(a -b) <= conv else False


class TestNode(TestCase):

    def setUp(self):
        self.coor = (0, 0)
        self.max_length = settings.MAX_PATH_LENGTH

    def test_equal(self):
        '''Test for equal operator overloading in Node.'''
        self.node1 = Node(self.coor, 2)
        self.node2 = Node(self.coor, 2)
        self.node3 = Node(self.coor, 4)
        self.node4 = Node((1, 1), 2)

        self.assertEqual(self.node1, self.node2)
        self.assertNotEqual(self.node1, self.node3)
        self.assertNotEqual(self.node1, self.node4)
        self.assertNotEqual(self.node3, self.node4)

    def test_node_2(self):
        '''Test for neighbour coordinates of node with 2 connections.'''
        self.node = Node(self.coor, 2)
        self.assertTrue(coor_equal(self.node.coor, self.coor))
        self.assertEqual(self.node.connections, 2)
        c1 = [self.coor[0] - 1*self.max_length, self.coor[1]]
        c2 = [self.coor[0] + 1*self.max_length, self.coor[1]]
        c1 = tuple(c1)
        c2 = tuple(c2)
        self.assertEqual(set([c1, c2]), set([x.coor for x in self.node.neighbours]))
        a1 = np.array(c1)
        a2 = np.array(c2)
        a = np.array(self.node.coor)
        self.assertTrue(np.linalg.norm(a-a1), self.max_length)
        self.assertTrue(np.linalg.norm(a-a2), self.max_length)
        self.assertTrue(np.linalg.norm(a1-a2), self.max_length*2)

    def test_node_4(self):
        '''Test for neighour coordinates of node with 4 connections.'''
        self.node = Node(self.coor, 4)
        pass

    def test_node_6(self):
        '''Test for neighour coordinates of node with 4 connections.'''
        self.node = Node(self.coor, 6)
        pass


class TestPath(TestCase):

    def setUp(self):
        self.max_length = settings.MAX_PATH_LENGTH
        # Initiate origin/destination node.
        origin_coor = (0, 0)
        dest_coor = (self.max_length, 0)
        origin_node = Node(origin_coor, 4)
        dest_node = Node(origin_coor, 4)
        self.path = Path(origin_node, dest_node)

    def test_init(self):
        self.assertEqual(self.path.length, 0)
        self.assertTrue(self.path.alive)

    def test_grow(self):
        distance = 8
        self.path.grow(distance)
        self.assertEqual(self.path.length, distance)


class TestNeuron(TestCase):

    def setUp(self):
        self.max_length = settings.MAX_PATH_LENGTH
        self.origin_coor = (0, 0)
        self.origin_node = Node(self.origin_coor, 4)
        self.neuron = Neuron(self.origin_node)

    def test_init(self):
        '''Test initiate of neuron.'''
        self.assertEqual(self.neuron.vertex, self.origin_node.connections)
        self.assertFalse(self.neuron.boundary_nodes)
        self.assertFalse(self.neuron.paths)
        self.assertFalse(self.neuron.boundary_paths)
        self.assertEqual(self.neuron.nodes, [self.origin_node])

    def test_hands(self):
        '''Number of hands'''
        if self.neuron.vertex != 6:
            self.assertEqual(self.neuron.hands, self.neuron.vertex)
        # Hands test for neuron with 6 connections origin node.
        node6 = Node(self.origin_coor, 6)
        neuron6 = Neuron(node6)
        hands = []
        '''The probability that neuron.hands only give 2 unique values in
        40 calls is less than 0.00000001'''
        for i in range(40):
            hands.append(neuron6.hands)
        hands = set(hands)
        self.assertEqual(hands, set([4, 5, 6]))

    def test_born(self):
        '''Test for born method of neuron.
        After born, a neuron has several boundary_nodes and the same number
        of boundary_paths.'''

        self.neuron.born()

        if self.neuron.vertex != 6:
            # Neighbours are now boundary nodes.
            self.assertEqual(self.neuron.boundary_nodes, self.neuron.origin.neighbours)
            # Number of boundary paths is the same with vertex number.
            self.assertEqual(len(self.neuron.boundary_paths), self.neuron.vertex)
            # Nodes used by boundary paths.
            path_nodes = [path.origin for path in self.neuron.boundary_paths] +\
                [path.dest for path in self.neuron.boundary_paths]
            # Remove duplicated nodes.
            path_nodes = set(path_nodes)
            # Nodes used by boundary paths are boundary nodes plus origin node.
            self.assertEqual(len(path_nodes), self.neuron.vertex + 1)

        # All boundary_paths are now 0.
        self.assertTrue(all([x.length == 0 for x in self.neuron.boundary_paths]))

    def test_grow(self):
        '''Test for grow function. Grow for 1 and 2 steps.'''
        # Born first to determine grow directions.
        self.neuron.born()
        # Grow for one step.
        self.neuron.grow()
        self.assertTrue(all([x.length == settings.GROW_SPEED for x in self.neuron.boundary_paths]))

        # Grow for another 2 steps.
        for i in range(2):
            self.neuron.grow()
        self.assertTrue(all([x.length == settings.GROW_SPEED*3 for x in self.neuron.boundary_paths]))

    def test_way_to_go_no_way(self):
        '''No way available.'''

        # Node coors for neuron.
        node_coors = [(0, 1), (-1, 1), (-2, 1), (-2, 0), (-2, -1), (-1, -1), (-1, 0)]
        # Test coordinates.
        test = (-1, 0)
        # Assign nodes to self.neuron
        for x in node_coors:
            node = Node([y*self.max_length for y in x], 4)
            self.neuron.nodes.append(node)
        test_node = Node([y*self.max_length for y in test], 4)
        # Assert no way available.
        self.assertFalse(self.neuron.way_to_go(test_node, True))

    def test_way_to_go_one_way(self):
        '''Only one way available.'''

        # Node coordinates to be assigned.
        node_coors = [(0, 1), (0, 2), (-1, 2), (-2, 2), (-2, 1), (-2, 0), (-2, -1), (-1, -1), (-1, 0)]
        # Test coordinates.
        test = (-1, 0)
        # Assign nodes to self.neuron
        for x in node_coors:
            node = Node([y*self.max_length for y in x], 4)
            self.neuron.nodes.append(node)
        test_node = Node([y*self.max_length for y in test], 4)
        # Assert only one way, the only way is (-1, 1)
        target = Node([y*self.max_length for y in (-1, 1)], 4)
        self.assertEqual(self.neuron.way_to_go(test_node, True), [target])

    def test_clean(self):
        '''Test for clean to update boundary conditions.'''

        self.neuron.born()
        # Grow to exceed max_length.
        steps = int(self.max_length)/5 + 1
        for i in range(steps):
            self.neuron.grow()
        # Check that all boundary_paths has the expected length.
        self.assertTrue(all([x.length == steps*Neuron.speed for x in self.neuron.boundary_paths]))

        pre_boundary_nodes = copy.deepcopy(self.neuron.boundary_nodes)
        pre_boundary_paths = copy.deepcopy(self.neuron.boundary_paths)

        self.neuron.clean()

        # All nodes in previous boundary nodes are now in self.neuron.nodes.
        self.assertTrue(all([x in self.neuron.nodes for x in pre_boundary_nodes]))
        # All nodes in previous boundary nodes are not in boundary nodes any more.
        self.assertTrue(all([x not in self.neuron.boundary_nodes for x in pre_boundary_nodes]))
        # All paths in previous boundary paths are not in boundary paths any more.
        self.assertTrue(all([x not in self.neuron.boundary_paths for x in pre_boundary_paths]))


class TestCheckConnections(TestCase):
    '''Tests for check_connections() function.'''

    def setUp(self):

        c0 = (0, 0)
        c1 = (0, 50)
        node0 = Node(c0, 4)
        node1 = Node(c1, 4)

        path0 = Path(node0, node1, 30)
        path1 = Path(node1, node0, 30)
        path2 = Path(node1, node0, 10)

        self.n0 = Neuron(node0)
        self.n1 = Neuron(node1)
        self.n2 = Neuron(node1)

        self.n0.boundary_nodes.append(node1)
        self.n1.boundary_nodes.append(node0)
        self.n2.boundary_nodes.append(node0)

        self.n0.boundary_paths.append(path0)
        self.n1.boundary_paths.append(path1)
        self.n2.boundary_paths.append(path2)

        self.neurons = [self.n0, self.n1, self.n2]

    def test_no_connections_at_init(self):
        # No neuron is connected before checking.
        self.assertEqual(stats_connections(self.neurons), 0)

    def test_common_nodes(self):
        # Check connections for neurons with common nodes.
        check_connections([self.n1, self.n2], [])
        self.assertTrue(self.n1.connected and self.n2.connected)

    def test_common_path_sum_exceeds(self):
        # Check connections for neurons with common path and sum of path length
        # exceeds max_length,
        check_connections([self.n0, self.n1], [])
        self.assertTrue(self.n0.connected and self.n1.connected)

    def test_common_path_sum_not_enough(self):
        # Check connections for neurons with common path but the sum of path
        # length is less than max length
        check_connections([self.n0, self.n2], [])
        self.assertFalse(self.n0.connected)
        self.assertFalse(self.n2.connected)


class TestEqualCoor(TestCase):

    def setUp(self):
        self.c1 = (0, 0)
        self.c2 = (0, 0)
        self.c3 = (0, 1)
        self.c4 = (1, 0)

    def test_coor_equal(self):
        self.assertTrue(coor_equal(self.c1, self.c2))
        self.assertFalse(coor_equal(self.c1, self.c3))
        self.assertFalse(coor_equal(self.c1, self.c4))
        self.assertFalse(coor_equal(self.c3, self.c4))
