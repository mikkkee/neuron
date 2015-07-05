import math
import random
import copy
from itertools import combinations, product

from PIL import Image, ImageDraw
import numpy as np

import settings


################################
############ Classes ###########
################################

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
            # Choose randomly from range(Hands_low, Hands_high + 1)
            return random.randrange(settings.Hands_low, settings.Hands_high + 1, 1)
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
        split = True if p < settings.SPLIT_PROBABILITY else False

        return split

    def avail_neighbours(self, node):
        '''Available neighbours of a node. Available means that this neighbour
        is not currently occupied by this neuron.'''
        avail = []
        for neighbour in node.neighbours:
            if neighbour not in (self.nodes + self.boundary_nodes):
                avail.append(neighbour)
        return avail

    def way_to_go(self, node, split, local=False, origin=None):
        '''Choose a way to go.
        Use split_check() to determine whether split or not.
        If local=True, consider local structure effects when determine which
        way to go. When local is True, origin is required as the origin node of
        the previous path.'''

        # Possible nodes to head to.
        possible_nodes = self.avail_neighbours(node)

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
            if local:
                '''Use local structure to decide which way to go instead of
                random.sample'''
                if split:
                    print("Spliting")
                    return self.local_sample(possible_nodes, node, origin, 2)
                else:
                    return self.local_sample(possible_nodes, node, origin, 1)
            else:
                if split:
                    return random.sample(possible_nodes, 2)
                else:
                    return random.sample(possible_nodes, 1)

    def local_sample(self, nodes, node, origin, n):
        '''Choose n elements from nodes according to their local structure with
        origin and node.'''
        prob = []
        d1 = np.array(node.coor) - np.array(origin.coor)
        for neighbour in nodes:
            d = np.array(neighbour.coor) - np.array(node.coor)
            if np.dot(d1, d) < 0:
                # Case 1: go back.
                prob.append((neighbour, settings.P1))
            elif abs(np.dot(d1, d1) - settings.MAX_PATH_LENGTH ** 2) < 0.01:
                # Case 2: go directly.
                prob.append((neighbour, settings.P2))
            else:
                # Case 3: turn left or right 60 degrees.
                prob.append((neighbour, settings.P3))

        real_way = []
        if n <= len(nodes):
            while len(real_way) < n:
                # Random number between 0 and sum of a probs.
                if sum([x[1] for x in prob]) == 0:
                    break
                a = random.random() * sum([x[1] for x in prob])
                c = 0
                for item in prob:
                    c = c + item[1]
                    if a < c:
                        real_way.append(item[0])
                        break
        return real_way

    def clean(self, local=True):
        '''Validate boundary_paths and boundary_nodes.
        local=True for cases that path.length is more than twice of max_length.'''

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
                # paths_to_del.append(path_copy)
                nodes_to_del.append(path_copy.dest)
                # New length.
                new_length = path.length - settings.MAX_PATH_LENGTH
                # Convert path.length to max_length to prepare for be appended.
                path.length = settings.MAX_PATH_LENGTH
                # Append path, node to self.paths, self.nodes
                self.paths.append(path)
                self.nodes.append(path.dest)

                paths_to_del.append(path)

                # Check new nodes.
                if local:
                    new_nodes = self.way_to_go(path.dest, self.split_check(), local=True, origin=path.origin)
                else:
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
        Delete nodes and paths in nodes_to_del and paths_to_del from
        self.nodes and self.paths.
        '''
        for node in nodes_to_del:
            while node in self.boundary_nodes:
                del self.boundary_nodes[self.boundary_nodes.index(node)]

        for path in paths_to_del:
            while path in self.boundary_paths:
                del self.boundary_paths[self.boundary_paths.index(path)]

        # Continue check until all boundary paths have reasonable length.
        if any([x.length > settings.MAX_PATH_LENGTH for x in self.boundary_paths]):
            self.clean(local=local)

    def check_alive(self):
        '''Check paths in self.boundary_paths, if no possible next_node,
        turn them to dead.'''
        for path in self.boundary_paths:
            node = path.origin
            if all([x in self.nodes for x in node.neighbours]):
                path.died()

    def cal_end(self, path):
        '''Calculate coordinates for endpoint for a path.'''
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

        # Draw origin node only.
        node = self.origin
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


class Exp(Object):
    '''A simulation of neuron experiment.'''
    pass

################################
########## Exceptions ##########
################################


class ErrorConnectionNumber(Exception):
    pass


class ErrorHandsNumber(Exception):
    pass



################################
########## Functions ###########
################################


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
    connected_dict = {x: True for x in connected}
    pairs = combinations(neurons, 2)
    print("    Generating pairs...")
    pairs = [x for x in pairs if any([y not in connected for y in x])]
    print("    {n} pairs generated.".format(n=len(pairs)))

    for pair in pairs:
        # Do not perform check if both element in pair are in connected.
        connectFlag = False
        '''
        Start checking for connections.
        1. If n1.nodes and n2.nodes have common elements, they are connected
        2. If n1.boundary_nodes and n2.boundary_nodes have commen elements,
           go to step 3.
        3. If the sum of common paths' length is larger than MAX_LEN,
           they are connected.
        '''

        node_pairs = product(pair[0].nodes, pair[1].nodes)

        for n1, n2 in node_pairs:
            if coor_equal(n1.coor, n2.coor):
                pair[0].connect()
                pair[1].connect()
                connectFlag = True
                break
                print("        Node connected.")

        # Continue check if previous check didnt turn connected to True.
        if not connectFlag:
            for (p1, p2) in product(pair[0].boundary_paths, pair[1].boundary_paths):
                '''
                If not connected, then no nodes are common in n1.nodes
                and n2.nodes. Then p1.origin must be different from
                p2.orgin.
                '''
                if (
                    coor_equal(p1.dest.coor, p2.origin.coor) and \
                    coor_equal(p2.dest.coor, p1.origin.coor) and \
                    p1.length + p2.length >= settings.MAX_PATH_LENGTH
                    ):
                        pair[0].connect()
                        pair[1].connect()
                        connectFlag = True
                        break

def stats_connections(neurons):
    '''Stats connected neurons.
    Return percentage of connected neurons to all neurons.'''
    count = 0
    for neuron in neurons:
        if neuron.connected:
            count += 1
    return float(count)/len(neurons)


def pattern42(N, nx, ny, p=0.3):
    '''Pattern 2 or pattern 4.
    N - number of edges
    nx - grid number along x
    ny - grid number along y
    p - number of neurons to all grids.'''

    grid = []
    lattice = settings.MAX_PATH_LENGTH

    n_neurons = int(nx*ny*p)

    for x in range(500, 500 + nx*lattice, lattice):
        for y in range(500, 500 + ny*lattice, lattice):
            grid.append((x,y))

    node_coors = random.sample(grid, n_neurons)

    neurons = [Neuron(Node(x, N)) for x in node_coors]

    return neurons


def pattern6(nx, ny, p=0.3):
    '''Pattern 6.'''

    ny1 = ny / 2
    ny2 = ny - ny1

    grid = []
    lattice = settings.MAX_PATH_LENGTH
    h = math.sqrt(3)

    n_neurons = int(nx*ny*p)

    for i in range(10, 10 + ny1):
        y = h*i
        for j in range(10, 10 + nx):
            x = j - 0.5
            grid.append((x*lattice, y*lattice))

    for i in range(10, 10 + ny2):
        y = h / 2 + i * h
        for j in range(10, 10 + nx):
            x = j
            grid.append((x*lattice, y*lattice))

    # Draw pattern
    img = Image.new('RGBA', (2000, 2000), 'white')
    draw = ImageDraw.Draw(img)
    points = [[(x[0], x[1]), (x[0]+5, x[1]+5)] for x in grid]
    for point in points:
        draw.ellipse(point, fill='black')
    img.save('pattern6.png', 'PNG')

    node_coors = random.sample(grid, n_neurons)
    nodes = [Node(x, 6) for x in node_coors]

    neurons = [Neuron(x) for x in nodes]

    return neurons
