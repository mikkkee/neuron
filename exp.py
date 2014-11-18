import random

from neuron import Node, Path, Neuron
from neuron import coor_equal, check_connections, stats_connections

import settings


def pattern42(N, nx, ny, p=0.3):
    '''Pattern 2 or pattern 4.
    N - number of edges
    nx - grid number along x
    ny - grid number along y
    p - number of neurons to all grids.'''

    grid = []
    lattice = settings.MAX_PATH_LENGTH

    n_neurons = int(nx*ny*p)

    for x in range(0, nx*lattice, lattice):
        for y in range(0, ny*lattice, lattice):
            grid.append((x,y))

    node_coors = random.sample(grid, n_neurons)

    neurons = [Neuron(Node(x, N)) for x in node_coors]

    return neurons


def main():

    N = 4
    nx = 18
    ny = 14
    # Number of timesteps
    T = 120

    neurons = pattern42(N, nx, ny)

    for item in neurons:
        item.born()

    t = 0
    while t<=T:
        # Grow and clean for each neuron.
        for item in neurons:
            item.grow()
            item.clean()

        # Record connected neurons.
        connected = [x for x in neurons if x.connected]

        # Check connections
        check_connections(neurons, connected)

        # Stats connections
        print stats_connections(neurons)

        # Increase timestep
        t += 1

if __name__ == '__main__':
    main()
