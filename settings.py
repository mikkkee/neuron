'''Settings for neuron.py'''

######## Experimental settings ########

# Number of different runs.
N_run = 1

# Number of timesteps to run.
T = 8

# Neuron percentage. Ratio of neuron number to the number of total grid points.
pn = 0.003

# Consider local structure effects.
Local = True


######## Neuron setting. ########

# Number of hands for type 6.
Hands_low = 4
Hands_high = 6

# Grow speed of neuron branches.
GROW_SPEED = 25

# Split probability of a branch when encounters a new node.
SPLIT_PROBABILITY = 0.00001

# Probabilities of different directions.
# What matters here is the ratio between each probabilities, because not
# all ways are available when choosing.
P1 = 0.03
P2 = 0.3
P3 = 1.2


######## Pattern settings ########

# Maximum length of a path.
MAX_PATH_LENGTH = 5

# Pattern grid settings.
Nx = 180
Ny = 140


######## Draw settings ########
# At least (Nx * MAX_PATH_LENGTH) * (Ny * MAX_PATH_LENGTH) to include all
# initial neuron nodes in the image.
Lx = 1000
Ly = 1000
