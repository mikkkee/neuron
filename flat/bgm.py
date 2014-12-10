from __future__ import print_function
import math
import numpy as np

import settings


class Node():
    '''Node class.
    Used to represent end point of segments in branches.'''

    # Read simulating settings from settings file.
    ave_velocity = settings.AVE_VELOCITY
    init_len = settings.INIT_LEN
    timestep = settings.TIMESTEP

    def __init__(self, coor, parent, slope=None):
        self.coor = coor
        self.parent = parent
        # Calculate height from parent's height.
        self.height = parent.height + 1
        self.slope = slope

    def velocity(self):
        '''Return a velocity randomly sampled from a Gaussian distribution.'''

        # Set Gaussian distribution parameters.

        # Mean
        mu = Node.ave_velocity
        # Standard deviation.
        sigma = mu

        return np.random.normal(mu, sigma)


    def need_branch(self):





class Branch():
    '''Branch class.
    Each neuron has several branches which are consisted by many
    segments.'''

    def __init__(self, ):
        self.root = Node()
