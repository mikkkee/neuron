import random

import settings
from bgm import Node
from bgm import random_coor, dump


def main():
    '''Main simulation procedure.'''

    # Read settings from settings.py .
    # Number of neurons.
    n_neurons = settings.N_NEURONS
    # Number of timesteps to run.
    n_runs = settings.N_RUNS
    # Frequency to write to file.
    n_dump = settings.N_DUMP
    # Timestep.
    timestep = settings.TIMESTEP
    # Dump file name. Truncate dump file.
    dumpfile = settings.DUMPFILE
    d = open(dumpfile, 'w')
    d.close()
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


    ########## Simulation Starts Here ##########
    print("n_dump", n_dump)
    # Initiate each root node by calling their born() method.
    print("Simulation Starts Now!\n")
    print("Generating {n} neuron roots.\n".format(n=n_neurons))
    for branch in neurons:
        children = []
        for neuron in branch:
            children += neuron.born()
        for child in children:
            child.elongate()
        branch += children

    # Continue run until specified steps are reached.
    print("All roots are generated now.\nStarting to grow.\n")
    for step in range(n_runs):
        print("Running now for {s}/{n} step\n".format(s=step, n=n_runs))
        for branch in neurons:
            # print('barnch', neurons.index(branch))
            children = []
            for neuron in branch:
                # print('neuron', branch.index(neuron))
                # Only node that are tips can grow.
                if not (neuron.left or neuron.right):
                    # children can be one-elemented, two-elemented, or empty
                    # list.
                    # print("Growing", neuron.coor)
                    children += neuron.grow(step + 1)
            branch += children

        # Write neuron network to file at certain steps.
        if n_dump and (step % n_dump == 0):
            with open(dumpfile, 'a') as outname:
                dump(neurons, outname, step)

if __name__ == '__main__':
    main()
