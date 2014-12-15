import random

import settings
from bgm import Node

def random_coor(Lx, Ly, N=1:
    '''Generate N pairs of different (x, y) tuples.'''
    coors = []
    for i in range(N):
        x = random.random() * Lx
        y = random.random() * Ly
        while (x, y) in coors:
            x = random.random() * Lx
            y = random.random() * Ly
        coor.append((x, y))
    return coors


def main():
    '''Main simulation procedure.'''

    # Read settings from settings.py .
    # Number of neurons.
    n_neurons = settings.N_NEURONS
    # Number of timesteps to run.
    n_runs = settings.N_RUNS
    # Timestep.
    timestep = settings.TIMESTEP
    # Simulation area size.
    Lx = settings.LX
    Ly = settings.LY

    # Generate required number of neuron coordinates.
    coors = random_coor(Lx, Ly, n_neurons)
    # Initiating neurons with their coors and assign branch numbers to them.
    # Root nodes have no parent and no slope.
    # Generating a list of lists of branches.
    # [[branch0], [branch1], ..., [branchN-1]]
    neurons = [
        [Node(coor, parent=None, slope=None, height=0, branch=i)] for \
        i, coor in enumerate(coors)
        ]

    # Initiate each root node by calling their born() method.
    for branch in neurons:
        children = []
        for neuron in branch:
            children += neuron.born()
        branch += children
