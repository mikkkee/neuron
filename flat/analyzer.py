from __future__ import print_function
import itertools
import random

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

def check_intersection(seg_node1, seg_node2, queue, left=True):
    '''Check intersection between seg1 and seg2.
    Return value - meaning
    True - red-blue intersection.
    False - no intersection or no red-blue intersection.
    '''
    seg1 = seg_node1.key
    seg2 = seg_node2.key
    if seg1 and seg2 and seg1 != seg2:
        # Check only if the two segments are different.
        # print(seg1, seg2)
        intersection = seg1.intersects(seg2)
        if isinstance(intersection, Point):
            # intersection is a point.
            # store intersecting segments info in intersection.
            intersection.segs = (seg1, seg2)
            # print("    {} and {} intersects at {}".format(seg1, seg2, intersection))

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
    for seg in neuron1 + neuron2:
        # When there are different nodes with the same key, delete may not
        # work properly. Change coordinate of repeated points slightly.

        while seg.left.coor in [x.coor for x in points]:
            seg.left.coor = (seg.left.x - random.randint(1, 10)/1000.0, seg.left.y + random.randint(1, 10)/1000.0)

        points.append(seg.left)

        while seg.right.coor in [x.coor for x in points]:
            seg.right.coor = (seg.right.x - random.random(1, 10)/1000.0, seg.right.y + random.randint(1, 10)/1000.0)

        points.append(seg.right)

    point_nodes = [TreeNode(p) for p in points]

    # Init event queue with all end points.
    EventQ = EventQueue(point_nodes[0])
    for item in point_nodes[1:]:
        EventQ.insert(item)
    # print("Initial queue length: {}".format(len(EventQ.nodes())))

    # Currently sweepline is empty.
    sweepline_empty = True

    # Container for intersection points.
    intersection_points = []

    # Start to check intersections.
    count = 0
    while EventQ.nodes():
        # While there are events in EventQ.
        # print("Current queue length: {}".format(len(EventQ.nodes())))

        # Pop the next event from EventQ.
        event_node = EventQ.minimum(EventQ.root)
        event = event_node.key
        print('Current Event: {} is {} left, is {} right, belongs to {}'.format(event, event.isleft, event.isright, event.segment))
        # print('EQ before insertion: {}'.format(EventQ.nodes()))
        # print("Event queue: {}\n".format(EventQ.nodes()))
        # print(event, event.isright, event.segment)
        if event.isleft:
            # print("    LEFT")
            # This is a left endpoint.
            # Select the segment that event belongs to.
            seg = event.segment
            seg_node = TreeNode(seg)

            print("INSERTING {} to {}".format(seg, SL.nodes() if not sweepline_empty else None))
            if not sweepline_empty:
                SL.print_ascii(use_slash=True)
            print("=>")


            # Insert current segment to the SweepLine SL.
            if sweepline_empty:
                SL = SweepLine(seg_node)
                sweepline_empty = False
            else:
                SL.insert_treenode(seg_node)

            SL.print_ascii(use_slash=True)

            # Select above and below segments.
            seg_above_node = seg_node.above
            seg_below_node = seg_node.below
            # print(seg, seg_above_node.key, seg_below_node.key)
            # Check intersection between seg and its above/below.
            if check_intersection(seg_node, seg_above_node, EventQ, left=True):
                return True
            if check_intersection(seg_node, seg_below_node, EventQ, left=True):
                return True

        elif event.isright:
            # This is a right endpoint.

            # Select this point's segment.
            seg = event.segment
            # print('    {}'.format(seg))
            # print("    Current SL: {}\n".format(SL.nodes()))
            seg_node = SL.find(seg)
            if not seg_node and seg in [x.key for x in SL.nodes()]:
                seg_node = SL.nodes()[[x.key for x in SL.nodes()].index(seg)]
            print("Find {} in {} => get {}".format(seg, SL.nodes(), seg_node.key))
            SL.print_ascii()

            # print("Find {} in {} get {}\n".format(seg, SL.nodes(), seg_node))
            # if SL.nodes():
            #     SL.print_ascii(use_slash=True)

            # Select current segment's above and below segments.
            seg_above_node = seg_node.above if SL.find(seg_node.above.key) else TreeNode.nil
            seg_below_node = seg_node.below if SL.find(seg_node.below.key) else TreeNode.nil
            print("    RIGHT\n    above: {}\n    below:{}".format(seg_above_node.key, seg_below_node.key))


            print("DELETING {}, with key {}, from {}".format(seg_node, seg_node.key, SL.nodes()))
            SL.print_ascii(use_slash=True)
            print("=>")

            # Delete seg from SL.
            print(seg_node.key, SL.root.key, seg_node.key < SL.root.key, seg_node.key > SL.root.key)
            SL.delete_treenode(seg_node)

            if not SL.nodes():
                sweepline_empty = True

            if not sweepline_empty:
                SL.print_ascii(use_slash=True)
                print(SL.nodes())

            # Check intersection between seg and its above/below.
            if check_intersection(seg_below_node, seg_above_node, EventQ, left=False):
                return True
            # check_intersection(seg_node, seg_below_node, EventQ, left=False)

        else:
            # event is an intersection point.
            # Add event to intersection points.
            # print('Current Event: {} is an intersection, belongs to {} and {}'.format(event, event.segs[0], event.segs[1]))
            intersection_points.append(event)
            seg_below_node, seg_above_node = [SL.find(x) for x in sorted(event.segs)]


            # print('    INTERSECTION')
            # print("    Current SL: {}\n".format(SL.nodes()))


            # Swap positions between seg_below and seg_above.
            if seg_above_node.above != seg_above_node:
                seg_below_node.above = seg_above_node.above
            else:
                seg_below_node.above = seg_below_node

            seg_below_node.below = seg_node.above

            if seg_below_node.below != seg_below_node:
                seg_above_node.below = seg_below_node.below
            else:
                seg_above_node.below = seg_above_node

            seg_above_node.above = seg_below_node

            # Swap their name.
            seg_above_node, seg_below_node = seg_below_node, seg_above_node
            if check_intersection(seg_above_node.above, seg_above_node, EventQ, left=False):
                return True
            if check_intersection(seg_below_node.below, seg_below_node, EventQ, left=False):
                return True


        print('\n\n', count)
        # print('EQ after insertion len: {}'.format(len(EventQ.nodes())))
        # print('{}'.format(sorted(EventQ.nodes())))
        print("Current SL len: {}".format(len(SL.nodes())))
        print("Current SL: {}\n".format(SL.nodes()))
        # EventQ.print_ascii(outfile=str(count), use_slash=True)
        count += 1
        # print("Queue before deletion: {}".format(EventQ.nodes()))
        EventQ.delete(event_node)
        # print("Queue after deletion: {}".format(EventQ.nodes()))

    return False #intersection_points


def have_bad_intersection(n1, n2):
    '''Bad solution'''
    for seg1 in n1:
        for seg2 in n2:
            if seg1.intersects(seg2):
                return True

def count_connections(timestep, connected_index):
    '''Count number of connected neurons and update connected_index.
    Do not check for neurons in connected_index.'''
    # List of connected neurons.
    connected_neurons = [timestep[x] for x in connected_index] if connected_index else []
    for n1, n2 in itertools.combinations(timestep, 2):
        # Check connection between each pair of neurons.
        # Only perform check if at least one neuron is not connected to any other neuron.
        if not (n1 in connected_neurons and n2 in connected_neurons):
            # print('\n', n1, '\n', n2)
            if have_bad_intersection(n1, n2):
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
    # print(results, len(results))
    # List that contains index of neurons that are connecting with other neurons.
    connected_index = []
    # Total number of neurons.
    neuron_num = len(results[0])
    # Count of connected neurons at each timestep.
    count_result = []

    for timestep in results:
        # Count connected neurons and update connected_index.
        connected_count = count_connections(timestep, connected_index)
        count_result.append(connected_count)

    return count_result
