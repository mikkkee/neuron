import random
import math
import argparse

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


def pattern6(nx, ny, p=0.3):
    '''Pattern 6.'''

    ny1 = ny / 2
    ny2 = ny - ny1

    grid = []
    lattice = settings.MAX_PATH_LENGTH
    h = math.sqrt(3)

    n_neurons = int(nx*ny*p)

    for i in range(ny1):
        y = h*i
        for j in range(nx):
            x = j - 0.5
            grid.append((x*lattice, y*lattice))

    for i in range(ny2):
        y = h / 2 + i * h
        for j in range(nx):
            x = j
            grid.append((x*lattice, y*lattice))
            

    node_coors = random.sample(grid, n_neurons)

    neurons = [Neuron(Node(x, 6)) for x in node_coors]

    return neurons


def main():

    # Number of pattern edges
    N = 2
    # Number of runs.
    N_run = 3
    # Data file
    out_file_name = 't_percentage_{n}.dat'.format(n=N)
    nx = 18
    ny = 14
    # Number of timesteps
    T = 9

    data = {}
    for r in range(N_run):
        # Set up neurons.
        if N != 6:
            neurons = pattern42(N, nx, ny)
        else:
            neurons = pattern6(nx, ny)

        for item in neurons:
            item.born()

        # Reset timestep and percentage.
        t = 0
        percentage = 0

        # Run for T steps.
        while t<=T:
            # Grow and clean for each neuron.
            for item in neurons:
                item.grow()
                item.clean()

            # Record connected neurons.
            connected = [x for x in neurons if x.connected]

            # Check connections
            check_connections(neurons, connected)

            # Percentage for previous step.
            print t+1, percentage
            if t not in data.keys():
                data[t] = [percentage]
            else:
                data[t].append(percentage)

            # Stats connections after updated.
            percentage = stats_connections(neurons)

            # Increase timestep
            t += 1

    # Write data
    with open(out_file_name, 'w') as data_file:
        time_series = sorted(data.keys())
        for t in time_series:
            data_file.write('\n{tt} '.format(tt=t))
            for p in data[t]:
                data_file.write('{pp:.3f} '.format(pp=p))

if __name__ == '__main__':
    main()
