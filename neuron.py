import math
import random
import copy
from itertools import combinations

import settings

class Node():

    def __init__(self, coordinates, connections):
        '''Init instance.
        coordinates is a (x, y) tuple with x and y of number type.
        connections is a integer number. It can be 2, 3, 4, or 6.
        max_len is the max_length of path
        '''
        self.coor = tuple([float(x) for x in coordinates])
        self.connections = int(connections)

    def __eq__(self, other):
        '''Operatir overloading - comparison equal
        Need to rewrite for 3 connections.'''
        if isinstance(other, Node):
            return other.__hash__() == self.__hash__()

    def __hash__(self):
        '''Operator overloading - hash method
        Used for set and comparison.'''
        return (hash(self.coor) ^ hash(self.connections))

    def __repr__(self):
        return "Node: at ({c[0]}, {c[1]}) with {n} connections".format(
        c=self.coor, n=self.connections
        )

    @property
    def neighbours(self):
        '''Return coordinates of neighbours.
        Based on number of connections, i.e. type of pattern.
        '''
        neighbours = []
        length = settings.MAX_PATH_LENGTH
        x, y = self.coor

        if self.connections == 2:
            # Neighbours along x direction.
            neighbours.append((x + 1*length, y))
            neighbours.append((x - 1*length, y))
        elif self.connections == 4:
            # Neighbours along x and y directions.
            neighbours.append((x + 1*length, y))
            neighbours.append((x - 1*length, y))
            neighbours.append((x, y + 1*length))
            neighbours.append((x, y - 1*length))
        elif self.connections == 6:
            # Neighbours along 6 directions.
            d = math.sqrt(3)/2
            neighbours.append((x + 1*length, y))
            neighbours.append((x - 1*length, y))
            neighbours.append((x - 0.5*length, y - d*length))
            neighbours.append((x + 0.5*length, y - d*length))
            neighbours.append((x - 0.5*length, y + d*length))
            neighbours.append((x + 0.5*length, y + d*length))
        else:
            raise ErrorConnectionNumber()

        # Convert neighbour coordinates to neighbour nodes.
        neighbour_nodes = []
        for coor in neighbours:
            node = Node(coor, self.connections)
            neighbour_nodes.append(node)
        return neighbour_nodes


class Path():

    # Maximum length settings.
    max_length = settings.MAX_PATH_LENGTH

    def __repr__(self):
        return "({n1[0]}, {n1[1]}) -> ({n2[0]}, {n2[1]}), {length}".format(
            n1=self.origin.coor, n2=self.dest.coor, length=self.length)

    def __eq__(self, other):
        if isinstance(other, Path):
            return self.__hash__() == other.__hash__()

    def __hash__(self):
        return (hash(self.origin) ^ hash(self.dest) ^ hash(self.length))

    def __init__(self, origin, dest, length=0):
        '''origin - the origin node,
        dest - the destination node,
        length - the occupied length of this path.'''
        self.origin = origin
        self.dest = dest
        self.length = length
        # Default alive.
        self.alive = True

    def died(self):
        # Turn a path to dead.
        self.alive = False

    def grow(self, distance):
        # Grow by amount of distance.
        self.length += distance


class Neuron():

    # Neuron settings.
    # Grow speed.
    speed = settings.GROW_SPEED
    # Split probability.
    split_prob = settings.SPLIT_PROBABILITY

    def __init__(self, origin):
        '''Initialize a neuron instance.
        origin - root node.
        vertex - number of neighbour nodes.'''

        self.origin = origin

        self.nodes = [self.origin]
        self.boundary_nodes = []
        self.paths = []
        self.boundary_paths = []

        # Not connected immediately after creation.
        self.connected = False

    def connect(self):
        # Trun self.connected to True.
        self.connected = True

    @property
    def vertex(self):
        return self.origin.connections

    @property
    def hands(self):
        '''Return number of initial hands for neuron.
        Randomly chose from (4,5,6) if self.vertex ==6 to ensure that
        not all neurons have the same number of hands.'''
        if self.vertex == 2:
            return 2
        elif self.vertex == 3:
            return 3
        elif self.vertex == 4:
            return 4
        elif self.vertex == 6:
            # Choose randomly from {4, 5, 6}
            return random.randrange(4, 7, 1)
        else:
            return ErrorHandsNumber()

    def born(self):
        '''Grow hands to init self.nodes, self.boundary_nodes,
        self.paths, and self.boundary_paths.
        Determine grow directions but do not grow now.'''

        # Choose boundary nodes from all neighbours.
        index = random.sample(range(self.vertex), self.hands)
        # Sort index for easier test.
        index.sort()

        for i in index:
            # Update boundary_nodes and boundary_paths.
            node = self.origin.neighbours[i]
            self.boundary_nodes.append(node)
            path = Path(self.origin, node)
            self.boundary_paths.append(path)

    def grow(self):
        '''Increase length for each alive path in boundary_paths.
        Do not validate paths now. Validate in self.clean().'''
        for path in self.boundary_paths:
            if path.alive:
                path.length += self.speed

    def split_check(self):
        '''Check if need split when a path exceeds MAX_PATH_LENGTH.'''

        # Split or not.
        p = random.random()
        split = True if p > 1/2 else False

        return split

    def way_to_go(self, node, split):
        '''Choose a way to go.
        Use split_check() to determine whether split or not.'''

        # Possible ways.
        possible_nodes = []
        for neighbour in node.neighbours:
            if neighbour not in (self.nodes + self.boundary_nodes):
                possible_nodes.append(neighbour)

        # Determin which way to go.
        ways = []
        possible_num = len(possible_nodes)
        if possible_num == 0:
            # No possible node, this path is dead.
            return None
        elif possible_num == 1:
            # Only one possible node.
            return possible_nodes
        elif possible_num >= 2:
            '''More than 1 possible nodes, return 2 nodes if split True, return
            only 1 node if split False.'''
            if split:
                return random.sample(possible_nodes, 2)
            else:
                return random.sample(possible_nodes, 1)

    def clean(self):
        '''Validate boundary_paths and boundary_nodes.'''

        # Boundary nodes and paths to delete.
        nodes_to_del = []
        paths_to_del = []

        # Check for each path in boundary_paths.
        for path in self.boundary_paths:
            if path.length > settings.MAX_PATH_LENGTH:
                '''
                Append to to_del list. Use deep copy in case of path
                changing
                '''
                path_copy = copy.deepcopy(path)
                paths_to_del.append(path_copy)
                nodes_to_del.append(path_copy.dest)
                # New length.
                new_length = path.length - settings.MAX_PATH_LENGTH
                # Convert path.length to max_length to prepare for be appended.
                path.length = settings.MAX_PATH_LENGTH
                # Append path, node to self.paths, self.nodes
                self.paths.append(path)
                self.nodes.append(path.dest)

                # Check new nodes.
                new_nodes = self.way_to_go(path.dest, self.split_check())
                if not new_nodes:
                    # No new path available.
                    pass
                else:
                    # Each node in new_nodes is a new destination.
                    for dest in new_nodes:
                        # Append new destination node to self.boundary_nodes.
                        self.boundary_nodes.append(dest)
                        # Init new path from old destination to new destination.
                        new_path = Path(path.dest, dest, new_length)
                        # Append new path to boundary_paths.
                        self.boundary_paths.append(new_path)

        '''
        Delete nodes and paths from nodes_to_del and paths_to_del from
        self.nodes and self.paths.
        '''
        for node in nodes_to_del:
            while node in self.boundary_nodes:
                del self.boundary_nodes[self.boundary_nodes.index(node)]

        for path in paths_to_del:
            while path in self.boundary_paths:
                del self.boundary_paths[self.boundary_paths.index(path)]

    def check_alive(self):
        '''Check paths in self.boundary_paths, if no possible next_node,
        turn them to dead.'''
        for path in self.boundary_paths:
            node = path.origin
            if all([x in self.nodes for x in node.neighbours]):
                path.died()

    def cal_end(self, path):
        p1 = path.origin.coor
        p2 = path.dest.coor
        l = float(path.length)
        m = settings.MAX_PATH_LENGTH
        # Calculate x and y
        x = l/m * p2[0] + (m - l)/m * p1[0]
        y = l/m * p2[1] + (m - l)/m * p1[1]

        return (x,y)

    def draw(self, draw, color):
        '''Draw neuron nodes and paths on draw object.'''

        # Draw nodes.
        for node in self.nodes:
            coor = node.coor
            draw.ellipse([(coor[0] - 5, coor[1] - 5), (coor[0] + 10, coor[1] + 10)], fill=color)
        # Draw full paths.
        for path in self.paths:
            line = [path.origin.coor, path.dest.coor]
            draw.line(line, fill=color, width=3)

        # Draw partial paths.
        for path in self.boundary_paths:
            line = [path.origin.coor, self.cal_end(path)]
            draw.line(line, fill=color, width=3)



'''
########## Exceptions ##########
'''


class ErrorConnectionNumber(Exception):
    pass


class ErrorHandsNumber(Exception):
    pass



'''
########## Functions. ##########
'''


def coor_equal(c1, c2):
    '''Check for equality bewteen two pair of float coordinates.'''
    d = 0.0001
    return all([abs(c1[i] - c2[i]) < d for i in range(2)])

def check_connections(neurons, connected):
    '''Check connections between neurons.
    neurons - the list of neurons.
    connected - a list of neurons that are already connected. Do not perform
    check between a pair if both elements in the pair are in connected list.
    '''
    pairs = combinations(neurons, 2)

    for pair in pairs:
        # Do not perform check if both element in pair are in connected.
        if any([x not in connected for x in pair]):
            connectFlag = False
            '''
            Start checking for connections.
            1. If n1.nodes and n2.nodes have common elements, they are connected
            2. If n1.boundary_nodes and n2.boundary_nodes have commen elements,
               go to step 3.
            3. If the sum of common paths' length is larger than MAX_LEN,
               they are connected.
            '''

            for node in pair[0].nodes:
                # check for common nodes in internal nodes.
                if any([coor_equal(node.coor, x.coor) for x in pair[1].nodes]):
                    pair[0].connect()
                    pair[1].connect()
                    connectFlag = True
                    break

            # Continue check if previous check didnt turn connected to True.
            if not connectFlag:
                for p1 in pair[0].boundary_paths:
                    for p2 in pair[1].boundary_paths:
                        '''
                        If not connected, then no nodes are commen in n1.nodes
                        and n2.nodes. Then p1.origin must be different from
                        p2.orgin.
                        '''
                        if (
                            coor_equal(p1.dest.coor, p2.origin.coor) and \
                            coor_equal(p2.dest.coor, p1.origin.coor)
                            ):
                            if p1.length + p2.length >= settings.MAX_PATH_LENGTH:
                                pair[0].connect()
                                pair[1].connect()
                                break

def stats_connections(neurons):
    '''Stats connected neurons.
    Return percentage of connected neurons to all neurons.'''
    count = 0
    for neuron in neurons:
        if neuron.connected:
            count += 1

    return float(count)/len(neurons)
