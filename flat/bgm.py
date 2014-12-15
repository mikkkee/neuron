from __future__ import print_function
import math
import random

import numpy as np

import settings


########## Functions ##########


def dump(neurons, dumpfile, step):
    '''Write neurons network to dump file.'''
    # Statistic info about the network.
    n_branches = len(neurons)
    n_nodes = sum([len(x) for x in neurons])
    # Write head info.
    head = '\nTIMESTEP: {s}, '.format(s=step)
    head += 'Number of Neurons: {nb}, '.format(nb=n_branches)
    head += 'Number of nodes: {nn} \n'.format(nn=n_nodes)
    dumpfile.write(head)
    # Dump each branch in format of many segments.
    # e.g.
    # root root.left
    # root root.right
    for i, branch in enumerate(neurons):
        # Write statistic info about the branch.
        n_branch_nodes = len(branch)
        branch_info = 'Neuron {i}, '.format(i=i)
        branch_info += 'Number of nodes: {n}\n'.format(n=n_branch_nodes)
        dumpfile.write(branch_info)
        # Write segments to dumpfile.
        # Segments fmt string.
        seg_fmt = "{c1[0]:.4f} {c1[1]:.4f} {c2[0]:.4f} {c2[1]:.4f}\n"
        # Start writing.
        for neuron in branch:
            if neuron.left:
                dumpfile.write(
                    seg_fmt.format(c1=neuron.coor, c2=neuron.left.coor)
                    )
            if neuron.right:
                dumpfile.write(
                    seg_fmt.format(c1=neuron.coor, c2=neuron.right.coor)
                    )

def random_coor(Lx, Ly, N=1):
    '''Generate N pairs of different (x, y) tuples.'''
    coors = []
    for i in range(N):
        x = random.random() * Lx
        y = random.random() * Ly
        while (x, y) in coors:
            x = random.random() * Lx
            y = random.random() * Ly
        coors.append((x, y))
    return coors

def branch_prob(tips, t, dt, h):
    '''Branch probablity.
    See documentation for function details.'''

    # Expected number of branching events at an isolated segment with infinite
    # period of time.
    B = settings.BRANCH_COUNT_INFINITE
    # Exponetial decay parameter in baseline branching rate.
    tau = settings.BRANCH_DECAY_TAU
    # Branching competetion parameter between tip nodes.
    E = settings.BRANCH_COMPETETION_E
    # Parameter determine influence of segments with different heights.
    S = settings.TOPOLOGICAL_PARA_S
    # Number of total terminal tips.
    n = len(tips)
    # Centrifugal base.
    C = 0
    for tip in tips:
        C += 2 ** (-S * tip.height)
    C = C/n
    # Calculate probablity.
    p = (n ** -E)*B*math.exp(-t/tau)*(math.exp(dt/tau)-1)*(2 ** (-S*h))/C

    return p

def rotate(direction):
    '''Rotate direction by a small degree alpha.
    Range of alpha is defined in settings.py'''
    alpha_min = settings.ALPHA_MIN
    alpha_max = settings.ALPHA_MAX
    r = random.random()
    alpha = alpha_min + (alpha_max - alpha_min) * r
    x = direction[0] * math.cos(alpha) - direction[1] * math.sin(alpha)
    y = direction[0] * math.sin(alpha) + direction[1] * math.cos(alpha)
    return np.array([x, y])


########## Classes ##########


class Node(object):
    '''Node class.
    Used to represent end point of segments in branches.'''

    # Read simulating settings from settings file.
    # Average elongation velocity.
    ave_velocity = settings.AVE_VELOCITY
    # Initial length for children segments.
    init_len = settings.INIT_LEN
    # Time inteval between each step.
    timestep = settings.TIMESTEP
    # Rate to change direction. (turns/length)
    turns_rate = settings.TURNS_RATE
    # Distance dependence parameter.
    dist_depend = settings.DIST_DEPEND

    def __init__(self, coor, parent, slope=None, height=None, branch=None):
        self.coor = coor
        self.parent = parent
        # Calculate height from parent's height if no height is specified.
        self.height = height if height is not None else parent.height + 1
        self.slope = slope
        self.branch_num = branch
        # Default no children.
        self.left = None
        self.right = None

    @property
    def root(self):
        '''Return the root node of the branch that current node belongs to.
        For root node r, r.parent = None .
        TODO: if this method is taking too much time. consider to rewrite this
        method as a property points to the root node.'''
        ancestor = self.parent
        # Look for ancestors if self.parent is not None.
        if ancestor:
            while ancestor.parent:
                ancestor = ancestor.parent
            self._root = ancestor
        else:
            self._root = self
        return self._root

    @property
    def ancestors(self):
        '''Return a list of ancestors of current node.
        Current node itself is also an ancestor of it.'''
        ancestors = [self]
        p = self.parent
        while p:
            ancestors.append(p)
            p = p.parent
        self._ancestors = ancestors
        return self._ancestors

    @property
    def leaves(self):
        '''Return all leaves in the subtree rooted at current node.
        Find leaves recursively.
        TODO: if this method is taking too much time, consider to
        rewrite it iteratively.'''
        leaves = []
        if self.left:
            leaves += self.left.leaves
        elif self.right:
            leaves += self.right.leaves
        else:
            leaves.append(self)
        self._leaves = leaves
        return self._leaves

    @property
    def length(self):
        '''Length of the segment determined by current node and its parent node.'''
        end = np.array(self.coor)
        start = np.array(self.parent.coor)
        self._length = np.linalg.norm(end - start)
        return self._length

    @property
    def cos(self):
        '''Trigonometric functions sin related to slope.'''
        self._cos = 1 / math.sqrt(1 + self.slope ** 2)
        return self._cos

    @property
    def sin(self):
        '''Trigonometric functions cos related to slope.'''
        self._sin = self.cos * self.slope
        return self._sin

    @property
    def velocity(self):
        '''Return a velocity randomly sampled from a Gaussian distribution.'''

        # Set Gaussian distribution parameters.
        # Mean
        mu = Node.ave_velocity
        # Standard deviation.
        sigma = mu

        return np.random.normal(mu, sigma)

    def born(self):
        '''Initiating of a root node.'''
        # Generate slope for first neurite.
        a, b = random.random(), 0
        while b == 0:
            b = random.random()
        slope = a/b
        self.left = Node(self.coor, parent=self, slope=slope, height=None, branch=self.branch)
        return [self.left]

    def need_branch(self, step):
        '''Determine whether a tip node needs to branch at a timestep.
        Generate a random number r in [0,1) and compare it with the
        probablity generated by p = branch_prob(n, t, dt, h). Return True if r is
        smaller than p, else return False.
        '''

        r = random.random()
        # Time now
        time_now = step * Node.timestep
        # All terminal tips.
        tips = self.root.leaves
        # Branching probablity.
        prob_branch = branch_prob(tips, time_now, Node.timestep, self.height)

        if r <= prob_branch:
            return True
        else:
            return False

    def need_shift(self):
        '''Determine whether a tip node needs to shift at a timestep.
        Determined by multiply turning rate with the length to increase before
        next timestep.
        Turning rate has unit of turns/length.'''

        # Velocity used for growing. Need to be passed to elongate.
        v = self.velocity
        # Shift probablity.
        p = Node.turns_rate * v * Node.timestep
        # Random test flag sampled from uniform distribution over [0,1).
        r = random.random()

        if r <= p:
            return True, v
        else:
            return False, v

    def direction(self):
        '''Return a slope value for a child to use.
        Read documents for details on how this slope value is generated.'''
        direction = np.array([0, 0])
        node = self
        base_dist = 0
        # Calculate direction from previous segments.
        print("while 1 in direction started.")
        while node.parent:
            # Unit vector of the segment represented by current node.
            u = np.array([node.cos, node.sin])
            # Volume of the segment represented by current node.
            m = node.length
            # Distance from the segment represented by current node to current node.
            d = node.length / 2 + base_dist
            # Increase base_dist to include the segment now considered.
            base_dist += m
            # Calculate direction.
            direction += m/(d ** Node.dist_depend) * u
            # Update node to be its parent.
            node = node.parent
        print("while 1 in direction finished.")
        print(direction)
        # Rotate the direction by a small degree alpha.
        direction_rotated = rotate(direction)
        while not direction_rotated[0]:
            direction_rotated = rotate(direction)
        return direction_rotated[1]/direction_rotated[0]

    def elongate(self, length=None):
        '''Elongate along current slope.
        If length is not given, use v * timestep with v randomly sampled v from
        self.velocity,else, use length.'''

        # Length to elongate.
        length = length if length else self.velocity * Node.timestep

        # Calculate Trigonometric functions from slope.
        cos = 1 / math.sqrt(1 + self.slope ** 2)
        sin = cos * self.slope

        # Calculate dx and dy from sin cos.
        dx = length * cos
        dy = length * sin

        # New x and y.
        x = self.coor[0] + dx
        y = self.coor[1] + dy
        self.coor = (x, y)

        # Return new (x, y) for current node.
        return (x, y)

    def branch(self):
        '''Branch to two sub branches. Each sub branch has an initial length.'''

        # Generate two directions.
        d1 = self.direction()
        d2 = d1
        while d2 == d1:
            d2 = self.direction()
        # Initiating two childeren.
        self.left = Node(
            self.coor, parent=self, slope=d1, height=None, branch=self.branch_num
            )
        self.right = Node(
            self.coor, parent=self, slope=d2, height=None, branch=self.branch_num
            )
        # Initial length.
        self.left.elongate(Node.init_len)
        self.right.elongate(Node.init_len)

        return [self.left, self.right]

    def shift(self):
        '''Shift the direction of current segment.
        It is the same as generating two children, initiate left child with
        a new slope while initiate the right child to None.'''
        # Generate a direction.
        d1 = self.direction()
        # Initiate left children with the generated slope.
        self.left = Node(
            self.coor, parent=self, slope=d1, height=None, branch=self.branch_num
            )
        self.right = None
        # Grow for a time step.
        self.left.elongate()
        # Return new neurons to append them to their branches.
        return [self.left]


    def grow(self, step):
        '''Grow for this tip node.
        1. Check if need to branch. If yes, branch; else go to step 2.
        2. Check if need to shift. If yes, shift, else, go to step 3.
        3. Elongate for a timestep.'''
        if not self.parent:
            return []
        # Random number for branching determination.
        rb = random.random()
        # Random number for shifting determination.
        rs = random.random()
        if rb <= self.need_branch(step):
            print("Branching.")
            children = self.branch()
        elif rs <= self.need_shift():
            print('Shifting.')
            children = self.shift()
        else:
            print('Elongating.')
            self.elongate()
            children = []

        return children


class Segment(object):
    '''Class of segment. Used for determine whether there exist any
    intersection points between two sets of segments.'''
