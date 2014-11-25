import random
import math
import argparse
import sys

from PIL import Image, ImageDraw

from neuron import Node, Path, Neuron
from neuron import coor_equal, check_connections, stats_connections
from neuron import pattern42, pattern6

import settings


def main(argv):

    # Parser
    parser = argparse.ArgumentParser()
    parser.add_argument('n', type=int, default=0)
    parser.add_argument('--no-draw', dest='draw', action='store_false')
    parser.set_defaults(draw=True)

    args = parser.parse_args(argv[1:])

    # Number of pattern edges
    if not args.n:
        N = 2
    else:
        N = args.n

    # Draw neuron or not.
    draw_flag = args.draw

    # Number of different runs.
    N_run = settings.N_run
    # Number of timesteps
    T = settings.T

    # Data file
    out_file_name = 't_percentage_{n}_speed_25.dat'.format(n=N)

    nx = settings.Nx
    ny = settings.Ny

    data = {}
    for r in range(N_run):
        # Set up neurons.
        print("Generating patterns...")

        if N != 6:
            neurons = pattern42(N, nx, ny, p=settings.pn)
        else:
            neurons = pattern6(nx, ny, p=settings.pn)

        print("Patterns generated.")

        print("Initiating neurons...")

        for item in neurons:
            item.born()

        print("Neurons initiated.")

        # Reset timestep and percentage.
        t = 0
        percentage = 0

        # Assign color
        if draw_flag:
            for neuron in neurons:
                neuron.color = tuple([random.randint(0, 255) for i in range(3)] + [100])

        # Run for T steps.
        while t<=T:
            # Grow and clean for each neuron.
            for i,item in enumerate(neurons):
                print("Growing {i}th neuron...".format(i=i))
                item.grow()
                print("Cleaning {i}th neuron...".format(i=i))
                item.clean(local=True)

            # Record connected neurons.
            connected = [x for x in neurons if x.connected]

            # Reset image.
            if draw_flag:
                img_name = "trj_{nn}_{rr}_{tt}.png".format(nn=N, rr=r, tt=t)
                img = Image.new('RGBA', (settings.Lx, settings.Ly), 'white')
                draw = ImageDraw.Draw(img)

                # Draw
                for neuron in neurons:
                    neuron.draw(draw, neuron.color)
                img.save(img_name, 'PNG')

            # Check connections
            print("Checking connections...")
            check_connections(neurons, connected)

            # Percentage for previous step.
            print r, t+1, percentage
            if t not in data.keys():
                data[t] = [percentage]
            else:
                data[t].append(percentage)

            # Stats connections after updated.
            percentage = stats_connections(neurons)

            # Increase timestep
            t += 1

        # Write data
        # Update data file after each run.
        with open(out_file_name, 'w') as data_file:
            time_series = sorted(data.keys())
            for t in time_series:
                data_file.write('\n{tt} '.format(tt=t))
                for p in data[t]:
                    data_file.write('{pp:.3f} '.format(pp=p))



if __name__ == '__main__':
    main(sys.argv)
