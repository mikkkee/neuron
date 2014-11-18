# Neuron Simulation

# Classes

## `Node`
- `coor`: for coordinates
- `connections:` number of neighbours.
- `neighbours`: neighbour nodes of current node. Different calculation methods
  for different number of connections.

## `Path`
- `origin`: one of the nodes it is connecting. Origin node.
- `dest`: the other node it is connecting. Destination node.
- `length`: length of path.
- `direction`: `origin` -> `dest`.
- `alive`: If `True`, the path can grow at next step, else cannot grow.
- `died()`: Turn a path to dead state by setting `self.alive` to False.

## `Neuron`

Basic properties

- `origin`: the neuron's starting node.
- `speed`: the neuron's growing speed.
- `vertex`: how many neighbour nodes one node has in the pattern.
- `hand`: how many hands one neuron has at the beginning. {2:2, 3:3, 4:4, 6:(4,5,6)}
- `split_prob`: probability for one neutron's hand to split into 2 hands on a
  node.
  Assuming that each hand will split only when it encounters a new node.
- `max_path_len`: maximum length for each path.

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
- `clean()`: check if any path in `boundary_paths` has exceeded the maximum
  length. If one path exceeds the maximum length:
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
