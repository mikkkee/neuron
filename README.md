# Neuron Simulation

# Classes

## `Node`
- `coor`: (x, y) coordinates.
- `connections:` number of neighbours, can be 2, 3, 4, 6, or 8.
- `neighbours`: return the neighbour nodes of current node. Number of neighbours
  is determined by `self.connections`.
- `__hash__()`: operator overloading, used for comparison and in `set`.
- `__eq__()`: operator overloading, used for comparison.
- `__repr__()`: operator overloading, representation.

## `Path`
- `origin`: one of the nodes the path is connecting. Origin node.
- `dest`: the other node the path is connecting. Destination node. Grow
  direction of path is `self.origin` -> `self.dest`.
- `length`: length of path.
- `alive`: if `True`, the path can grow at next step, otherwise it cannot grow.
- `max_length`: the max allowed length of current path. The path will be divided
  into 2 or more paths in `Neuron.clean()` if `self.length` > `self.max_length`.
- `died()`: Turn a path to dead state by setting `self.alive` to False.
- `grow()`: increase `self.length`.
- `__hash__()`: operator overloading, used for comparison and in `set`.
- `__eq__()`: operator overloading, used for comparison.
- `__repr__()`: operator overloading, representation.

## `Neuron`

A neuron is a collection of `Node`s and `Path`s. It grows as time passes.

Basic properties

- `origin`: the neuron's starting node.
- `speed`: the grow speed for each path.
- `vertex`: number of neighbours for each node.
- `hand`: number of neurites one neuron has at the beginning of a simulation.
- `split_prob`: probability for one neurite to split into 2 neurites on a
  node. A neurite will split only when it encounters a new node.

Conformation properties

- `connected`: True if the neuron is connected to any other neurons.
- `nodes`: nodes that are occupied by one neuron.
- `boundary_nodes`: nodes that are in the grow direction of one neuron.
- `paths`: paths that are fully occupied by one neuron.
- `boundary_paths`: paths that are partially occupied by one neuron.

Methods

- `born()`: initiate bare neuron with hands. Update `boundary_paths` and
  `boundary_nodes`.
- `grow()`: increase the length of one neuron's alive `boundary_paths` by amount
  of `speed`.
- `clean()`: check if any path in `boundary_paths` has exceeded its maximum
  length. If one path exceeds its maximum length:
  1. include the destination node to current neuron's `nodes`.
  2. Decide whether to split or not by using `split_check()`.
  3. Decide which way to grow by using `way_to_go()`.
  4. Include new boundary paths and boundary nodes to `boundary_paths` and
     `boundary_nodes`.
- `connect()`: Turn `self.connected` to True.
- `check_alive()`: Check paths in `boundary_paths` if they are alive or not.
- `split_check()`: Decide whether to split at a node by using `self.split_prob`.
  Return `True` or `False` to decide whether to split and possible boundary
  nodes for `way_to_go()` to choose.
- `way_to_go()`: Decide which way to go when encountering a new node. Just
  choose from possible destination nodes `split_check()` passes.
- `cal_end(self, path)`: calculate coordinates of a endpoint for a path.
- `draw()`: Draw origin node and current paths on a `Draw` object.


## `Exp`

Simulation class placeholder.

# Functions

## `check_connection()`

1. Check if any two neurons are connected. If two neurons are connected, call
   their `connect()` method to update their status.
2. Connections can only occur between boundary nodes.
2. Checking method:
   - Store a list of connected tuples (neuron1, neuron2), do not
   check for these combinations.
   - For each combination `n1` and `n2`:
     1. Check `n1.nodes` and `n2.nodes` for duplication. If there are
     duplications, mark `n1` and `n2` as connected and stop checking. If no
     duplications, go to step 2.
     2. Check for duplications between `n1.boundary_nodes` and
     `n2.boundary_nodes`. If there are duplications, say `n1.boundary_node`
     and `n2.boundary_node`, let `path1` be the boundary path for `n1` that
     ends with `n2.boundary_node`, and `path2` be the boundary path for `n2`
     that ends with `n1.boundary_node`. Check the sum for `path1.length` and
     `path2.length`. If the sum exceeds maximum path length, mark `n1` and `n2`
     as connected, else stop checking.

## `stats_connections()`

Count the percentage of connected neurons.

## `coor_equal()`

Check equality for two pairs of float coordinates.

## Patterns

### `pattern42()`

Generate pattern grid for type 2 and type 4. Then randomly select nodes as
neuron origin nodes.

### `pattern6()`

Generate pattern grid for type 6. Then randomly select nodes as neuron origin
nodes.


# Process
1. Initiate grid and neurons.
2. `T = 0`, For each neuron, born().
3. `T > 0`, for each time step:
   1. For each neuron `grow()`.
   2. For each neuron `clean()`.
   3. For each neuron `check_alive()`.
   4. `check_connections()`.
4. If percentage of connected neurons exceeds the pre-defined max-percentage,
   stop iteration.
