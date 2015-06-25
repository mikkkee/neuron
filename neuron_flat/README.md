# NTMORPH like Model


# Neuron

## Structure

- Root: initial coordinates.
- Branch: a binary tree, each node of which represents a point of a segment.
  - fossile: frozen nodes which will not change in the future (has at least one child).
  - tip: a node which may shifrt, branch, and elongate at each step (thus has no child).

## Branch
`Branch` is a binary tree, each node of which represents an end point of a
segment.

`Branch` should support the following methods:
* `grow(self)`: For each tip, call its `grow()` mdthod.
* `leaves(self)`: return all `non-NIL` leaves, which are growing tips.

## Node

Nodes of  `Branch` are `node` instances, which have following properties:
* `parent`: parent node.
* `left`: left child node.
* `right`: right child node.
* `slope`: the slope of the segment determined by `self` and `self.parent`. For
the root of a branch, this value is `None`.
* `height`: height of the node.

Class properties
* `ave_velocity`: average grow velocity, set by `settings.AVE_VELOCITY`.
* `init_len`: initial length of children, set by `settings.INIT_LEN`.
* `timestep`: time interval between each step, unit is hour, set by
`settings.TIMESTEP`.


`Node` should support the following methods:
* `grow(self)`: Implement the following grow procedure:
  1. Check if need to branch, if yes, call `self.branch()`; else, go to step 2.
  2. Check if need to change direction, if yes, call `self.shift()`;
  else, go to step 3.
  3. Call `self.elongate()`

* `need_branch(self)`: check if need to branch, return `True` if need to, else
return `False`. The probablity of branching is discussed in Mechanisms section.

* `need_shift(self)`: check if need to shift, return `True` if need to, else
return `False`. The probablity of shifting is discussed in Mechanisms section.

* `branch(self)`: Generate two different directions (slope value) using
`self.direction()`. Then add left and right child to this node, each initiated with the
slope value of the two directions and the coordinates of this node. At last,
call its children's `elongate()` method to grow to `Node.init_len`.

* `shift(self)`: Generate a direction (slope value) using `self.direction()`. Then
generate a left child and a right child. Initiate the left child with the slope
value generated and the coordinates of this node. Initiate the right child with
`None`. Call left child's `elongate()` method to grow to desired length
(`self.velocity()`*`Node.timestep`).

* `elongate(self)`: Change `self.coordinates` to increase segment length by a
desired length (`self.velocity()`*`Node.timestep`).

* `velocity(self)`: Return a random velocity sampled in a Gaussian distribution
with the average value `Node.ave_velocity`.

* `direction(self)`: Return a slope value for a child to use. How the direction
is determined is discussed below in the Mechanisms section.


## Neuron grow procedures

1. At first, the neuron is nothing but a point (Root).
2. Then, at first timestep, the neuron starts to growing out several (`NBranch`)
branches. We use instances of the `Branch` class to represent these branches.
These `Branch` instances are initiated with a root, which has the neuron's
Root coordinates, and a left child, whose coordinates are calculated
3. In all following timesteps, all leaves in each branch will be checked
