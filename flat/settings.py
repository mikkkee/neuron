############################################
########## Individual Run Related ##########
############################################

# Number of Neurons.
N_NEURONS = 10

# Lengths of simulation area.
# TODO: units.
LX = 2000.0
LY = 2000.0

# Timestep length.
# TODO: Add required units.
TIMESTEP = 3

# Run time - number of timesteps to run.
N_RUNS = 24

# Dump frequency - dump neuron network to file every this number of steps.
# 0 - do not dump.
N_DUMP = 1

# Output file name.
DUMPFILE = 'test.txt'

# Average elongation velocity.
# TODO: Add required units.
AVE_VELOCITY = 45.0 / 24

# Initial length for children.
# TODO: Add required units.
INIT_LEN = 5.0

# Turns rate. How many turns a neurite makes during one unit of time.
# unit: turns/length.
TURNS_RATE = 15



##################################################
########## Simulation Mechanism Related ##########
##################################################

# Expected number of branching events at an isolated segment with infinite
# period of time - B.
BRANCH_COUNT_INFINITE = 17.38

# Exponetial decay parameter in baseline branching rate - tau.
BRANCH_DECAY_TAU = 14 * 4

# Branching competetion parameter between tip nodes - E.
BRANCH_COMPETETION_E = 0.39

# Parameter determine influence of segments with different heights.
TOPOLOGICAL_PARA_S = 0

# Parameter determin influence of segments with different distances to the tip
# node on shifting direction.
DIST_DEPEND = 0

# Minimal and maximumal rotation angle.
# Unit: rad.
ALPHA_MIN = -0.6
ALPHA_MAX = 0.6



##################################################
##########     Draw Results Related     ##########
##################################################

# RGBA color when draw neurons.
color = (238, 14, 88, 70)
