from __future__ import print_function

from sweepline import Point, Segment, SweepLine, EventQueue

###############################
########## Functions ##########
###############################

########## Parse simulation files ##########

def _parse_segments(lines, branch=None):
    '''Parse list of lines into segments.
    The segments may belong to one branch of Neuron.
    Format of a line: p1.x p1.y p2.x p2.y
    '''
    segs = []
    for item in lines:
        item = [float(x) for x in item.split()]
        p1 = Point(item[0:2])
        p2 = Point(item[2:4])
        seg = Segment(p1, p2, branch)
        segs.append(seg)
    return segs

def _group_by_neuron(neuron_lines):
    '''Group list of lines by neurons.'''
    neuron_list = []
    neuron = []
    for line in neuron_lines:
        if line.startswith('Neuron'):
            # Starts another neuron when encounters 'Neuron'
            # If it is not the first time, store current neuron to the list.
            if neuron:
                neuron_list.append(neuron)
            neuron = []
        else:
            neuron.append(line)
    return neuron_list

def _group_by_timestep(time_lines):
    '''Group list of lines by timestep.'''
    time_list = []
    timestep = []

    for line in time_list:
        if line.startswith('TIMESTEP'):
            # Starts another timestep when encounters 'TIMESTEP'.
            # If it is not the first time, store current timestep to the list.
            if timestep:
                time_list.append(timestep)
            timestep = []
        else:
            timestep.append(line)
    return time_list

def parse_results(outfile):
    '''Parse simulation file into neuron nodes grouped by neurons and timesteps.
    '''
    time_lines = outfile.readlines()
    timestep_list = _group_by_timestep(time_lines)
    results = []
    timestep_neuron_list = []

    for neuron_lines in timestep_list:
        timestep_neuron_list.append(_group_by_neuron(neuron_lines))
