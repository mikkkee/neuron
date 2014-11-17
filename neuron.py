import math
import random

class Node():

    def __init__(self, coordinates, connections):
        '''Init instance.
        coordinates is a (x, y) tuple with x and y of number type.
        connections is a integer number. It can be 2, 3, 4, or 6.
        max_len is the max_length of path
        '''
        self.coor = tuple([float(x) for x in coordinates])
        self.connections = int(connections)

    @property
    def neighbours(self):
        '''Return coordinates of neighbours.
        Based on number of connections, i.e. type of pattern.
        '''
        neighbours = []
        length = PATH.max_length
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
        return neighbours


class Path():

    # Maximum length settings.
    max_length = 50

    def __init__(self, origin, dest, length=0):
        '''origin - the origin coordinates,
        dest - the destination coordinates,
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

    @property
    def direction(self):
        return "({n1[0], n1[1]}) -> ({n2[0], n2[1]})".format(
            n1=self.origin, n2=self.dest)


class Neuron():

    # Neuron settings.
    # Grow speed.
    speed = 5
    # Split probability.
    split_prob = 0.5

    def __init__(self, origin, vertex):
        '''Initialize a neuron instance.
        origin - root node coordinates.
        vertex - number of neighbour nodes.'''

        # Turn coordinates into node object.
        origin_node = Node(origin, vertex)
        self.origin = origin_node
        self.vertex = vertex
        # Not connected immediately after creation.
        self.connected = False

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
            return random.randrange(4, 7, 1)
        else:
            return ErrorHandsNumber()

    def born(self):
        '''Grow hands to init self.nodes, self.boundary_nodes,
        self.paths, and self.boundary_paths'''

        # Choose boundary nodes from neighbours.
        index = random.sample(range(self.vertex + 1), self.hands)

        for i in index:
            coor = self.origin.neighbours[i]
            node = Node(self.coor, self.vertex)
            self.boundary_nodes.append(node)



class ErrorConnectionNumber(Exception):
    pass


class ErrorHandsNumber(Exception):
    pass
