'''Settings for neuron.py'''

######## Experimental settings ########
OUT_NAME = '6_connectivity_result.dat'

# Number of different runs.
N_run = 1

# Number of timesteps to run.
T = 24

# Neuron percentage. Ratio of neuron number to the number of total grid points.
pn = 0.003

# Consider local structure effects.
Local = True


######## Neuron setting. ########

# Number of hands for type 6.
Hands_low = 1
Hands_high = 3

# Grow speed of neuron branches.
GROW_SPEED = 3.9

# Split probability of a branch when encounters a new node.
SPLIT_PROBABILITY = 0.02

# Probabilities of different directions.
# What matters here is the ratio between each probabilities, because not
# all ways are available when choosing.
P4_1 = 0.2
P4_2 = 0.8

P6_1 = 0
P6_2 = 0.2
P6_3 = 0.8

P8_1 = 0
P8_2 = 0.01
P8_3 = 0
P8_4 = 0.01

######## Pattern settings ########

# Maximum length of a path.
UNIT_PATH_LENGTH = 5

# Pattern grid settings.
Nx = 180
Ny = 140


######## Draw settings ########
# At least (Nx * MAX_PATH_LENGTH) * (Ny * MAX_PATH_LENGTH) to include all
# initial neuron nodes in the image.
Lx = 1000
Ly = 1000
