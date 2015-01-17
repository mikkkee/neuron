from __future__ import print_function
import itertools

from sweepline import TreeNode, Point, Segment, SweepLine, EventQueue

# TODO: get clear with TreeNode and TreeNode.key

###############################
########## Functions ##########
###############################

########## Parse simulation files ##########

def _parse_to_segments(lines, branch=None):
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
    neuron_list.append(neuron)
    return neuron_list

def _group_by_timestep(time_lines):
    '''Group list of lines by timestep.'''
    time_list = []
    timestep = []

    for line in time_lines:
        line = line.strip()
        if line.startswith('TIMESTEP'):
            # Starts another timestep when encounters 'TIMESTEP'.
            # If it is not the first time, store current timestep to the list.
            if timestep:
                time_list.append(timestep)
            timestep = []
        else:
            if line:
                timestep.append(line)
    time_list.append(timestep)
    return time_list

def parse_result(outfile):
    '''Parse simulation file into segments grouped by neurons and timesteps.
    '''
    time_lines = outfile.readlines()
    timestep_list = _group_by_timestep(time_lines)
    results = []
    timestep_neuron_list = []

    for neuron_lines in timestep_list:
        neurons = [_parse_to_segments(x, i) for i, x in enumerate(_group_by_neuron(neuron_lines))]
        timestep_neuron_list.append(neurons)

    return timestep_neuron_list


########## Analysis Function ##########

def check_intersection(seg1, seg2, queue, left=True):
    '''Check intersection between seg1 and seg2.
    Return value - meaning
    True - red-blue intersection.
    False - no intersection or no red-blue intersection.
    '''
    if seg1 != seg2:
        # Check only if the two segments are different.
        intersection = seg1.intersects(seg2)
        if isinstance(intersection, Point):
            # intersection is a point.
            # store intersecting segments info in intersection.
            intersection.segs = (seg1, seg2)

            # Insert intersection point to EventQ.
            if left:
                # Left endpoint event.
                queue.insert(TreeNode(intersection))
            else:
                # Right endpoint event.
                if not queue.find(intersection):
                    queue.insert(TreeNode(intersection))

            if seg1.branch != seg2.branch:
                # seg1 and seg2 belong to different neurons.
                return True
    return False


def have_intersection(neuron1, neuron2):
    '''Determine whether two neurons consists of several segments have
    intersections.
    '''
    points = []
    # coors = [] Use coors to perturb common points' coors.
    for seg in neuron1:
        points.append(seg.left)
        points.append(seg.right)
    for seg in neuron2:
        points.append(seg.left)
        points.append(seg.right)

    point_nodes = [TreeNode(p) for p in points]

    # Init event queue with all end points.
    EventQ = EventQueue(point_nodes[0])
    for item in point_nodes[1:]:
        EventQ.insert(item)

    # Currently sweepline is empty.
    sweepline_empty = True

    # Container for intersection points.
    intersection_points = []

    # Start to check intersections.
    while EventQ.nodes():
        # While there are events in EventQ.

        # Pop the next event from EventQ.
        event = EventQ.pop().key
        if event.isleft:
            # This is a left endpoint.
            # Select the segment that event belongs to.
            seg = event.segment
            # Insert current segment to the SweepLine SL.
            if sweepline_empty:
                SL = SweepLine(TreeNode(seg))
                sweepline_empty = False
            else:
                SL.insert(TreeNode(seg))
            # Select above and below segments.
            seg_above = seg.above
            seg_below = seg.below
            # Check intersection between seg and its above/below.
            check_intersection(seg, seg_above, EventQ, left=True)
            check_intersection(seg, seg_below, EventQ, left=True)

        elif event.isright:
            # This is a right endpoint.

            # Select this point's segment.
            seg = event.segment
            # Select current segment's above and below segments.
            seg_above = seg.above
            seg_below = seg.below
            # Check intersection between seg and its above/below.
            check_intersection(seg, seg_above, EventQ, left=False)
            check_intersection(seg, seg_below, EventQ, left=False)
            # Delete seg from SL.
            SL.delete(TreeNode(seg))

        else:
            # event is an intersection point.
            # Add event to intersection points.
            intersection_points.append(event)
            seg_below, seg_above = sorted(event.segs)
            # Swap positions between seg_below and seg_above.
            if seg_above.above != seg_above:
                seg_below.above = seg_above.above
            else:
                seg_below.above = seg_below

            seg_below.below = seg.above

            if seg_below.below != seg_below:
                seg_above.below = seg_below.below
            else:
                seg_above.below = seg_above

            seg_above.above = seg_below

            # Swap their name.
            seg_above, seg_below = seg_below, seg_above
            check_intersection(seg, seg_above, EventQ, left=False)
            check_intersection(seg, seg_below, EventQ, left=False)

    return intersection_points

def count_connections(timestep, connected_index):
    '''Count number of connected neurons and update connected_index.
    Do not check for neurons in connected_index.'''
    # List of connected neurons.
    connected_neurons = [timestep[x] for x in connected_index] if connected_index else []
    for n1, n2 in itertooles.combinations(timestep, 2):
        # Check connection between each pair of neurons.
        # Only perform check if at least one neuron is not connected to any other neuron.
        if not (n1 in connected_neurons and n2 in connected_neurons):
            if have_intersection(n1, n2):
                # Have intersection. -> update connected neurons and index list.
                if n1 not in connected_neurons:
                    connected_neurons.append(n1)
                    connected_index.append(timestep.index(n1))
                if n2 not in connected_neurons:
                    connected_neurons.append(n2)
                    connected_index.append(timestep.index(n2))
    # Return number of connected neurons.
    return len(connected_index)

def analyze(outfile):
    '''Main analysis function.'''
    results = parse_result(outfile)
    # List that contains index of neurons that are connecting with other neurons.
    connected_index = []
    # Total number of neurons.
    neuron_num = len(segments[0])
    # Count of connected neurons at each timestep.
    count_result = []

    for timestep in results:
        # Count connected neurons and update connected_index.
        connected_count = count_connections(timestep, connected_index)
        count_result.append(connected_count)

    return count_result
