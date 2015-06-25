'''Settings for neuron.py'''

######## Experimental settings ########

# Number of different runs.
N_run = 1

# Number of timesteps to run.
T = 30

# Neuron percentage. Ratio of neuron number to the number of total grid points.
pn = 0.1

# Consider local structure effects.
Local = False


######## Neuron setting. ########

# Number of hands for type 6.
Hands_low = 4
Hands_high = 6

# Grow speed of neuron branches.
GROW_SPEED = 10

# Split probability of a branch when encounters a new node.
SPLIT_PROBABILITY = 0.001

# Probabilities of different directions.
# What matters here is the ratio between each probabilities, because not
# all ways are available when choosing.
P1 = 0.03
P2 = 0.3
P3 = 1.2


######## Pattern settings ########

# Maximum length of a path.
MAX_PATH_LENGTH = 50

# Pattern grid settings.
Nx = 18
Ny = 14


######## Draw settings ########
# At least (Nx * MAX_PATH_LENGTH) * (Ny * MAX_PATH_LENGTH) to include all
# initial neuron nodes in the image.
Lx = 2000
Ly = 2000
