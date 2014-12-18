from __future__ import print_function
import math
import random

import numpy as np

import settings


############################
########## Neuron ##########
############################


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
        self.left = Node(
            self.coor, parent=self, slope=slope, height=None, branch=self.branch
            )
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



###########################################
########## Intersection Analysis ##########
###########################################


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

        point1._segment = self
        point2._segment = self
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


class TreeNode(object):
    '''Tree node of red-black tree.'''

    def __init__(self, key=None):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = None


class RBT(object):
    '''A red-black tree used for implementing Bentley-Ottmann Algorithm.'''

    def __init__(self, key=None):
        '''Initiate with a root.'''
        self.root = TreeNode(key) if key else None
        self.root.color = BLACK

    def find(self, key, x=self.root):
        '''Find node from the tree.'''
        if x == None or x.key == key:
            return x
        if key < x.key:
            return self.find(key, x.left)
        else:
            return self.find(key, x.right)

    def minimum(self, node):
        '''Return minimum node in the subtree rooted at node.'''
        while node.left:
            node = node.left
        return node

    def maximum(self, node):
        '''Return maximum node in the subtree rooted at node.'''
        while node.right:
            node = node.right
        return node

    def next(self, node):
        '''Successor of one node.
        If node.right is None, the node's successor is its nearest ancestor
        whose left child is also the node's ancestor (a node is an ancestor
        of itself).'''
        if node.right:
            return self.minimum(node.right)
        p = node.parent
        while p and node == p.right:
            node = p
            p = p.parent
        return p

    def prev(self, node):
        '''Predecessor of one node.
        Symmetric to successor.'''
        if node.left:
            return self.maximum(node.left)
        p = node.parent
        while p and node == p.left:
            node = p
            p = p.parent
        return p

    def insert(self, node):
        '''Insert a new node into the Red-Black Tree.'''
        y = None
        x = self.root
        while x:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right

        node.parent = y

        if not y:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node

        node.left = None
        node.right = None
        node.color = RED
        self.insert_fixup(node)

    def insert_fixup(self, key):
        pass

    def delete(self, key):
        '''Delete a node from the tree.'''
        pass

    def delete_fixup(self, key):
        pass

    def left_rotate(self, node):
        '''Left rotate operation.'''
        y = x.right
        x.right = y.left
        if y.left:
            y.left.parent = x
        y.parent = x.parent
        if not x.parent:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y





class EventQ(object):
    '''Event queue used for implementing Bentley-Ottmann Algorithm.'''
    pass


class SweepLine(object):
    '''Swipe line used for implementing Bentley-Ottmann Algorithm.'''
    pass
