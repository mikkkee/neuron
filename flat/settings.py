############################################
########## Individual Run Related ##########
############################################

# Number of Neurons.
N_NEURONS = 1

# Lengths of simulation area.
# TODO: units.
LX = 2000.0
LY = 2000.0

# Timestep length.
# TODO: Add required units.
TIMESTEP = 5.0

# Run time - number of timesteps to run.
N_RUNS = 5

# Dump frequency - dump neuron network to file every this number of steps.
# 0 - do not dump.
N_DUMP = 5

# Output file name.
DUMPFILE = 'test.txt'

# Average elongation velocity.
# TODO: Add required units.
AVE_VELOCITY = 5

# Initial length for children.
# TODO: Add required units.
INIT_LEN = 5.0

# Turns rate. How many turns a neurite makes during one unit of time.
# unit: turns/length.
TURNS_RATE = 5



##################################################
########## Simulation Mechanism Related ##########
##################################################

# Expected number of branching events at an isolated segment with infinite
# period of time - B.
BRANCH_COUNT_INFINITE = 5

# Exponetial decay parameter in baseline branching rate - tau.
BRANCH_DECAY_TAU = 1

# Branching competetion parameter between tip nodes - E.
BRANCH_COMPETETION_E = 1

# Parameter determine influence of segments with different heights.
TOPOLOGICAL_PARA_S = 1

# Minimal and maximumal rotation angle.
# Unit: rad.
ALPHA_MIN = 0.0
ALPHA_MAX = 0.0
