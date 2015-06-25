'''Left-lean Red-black tree implementation described in Robert Sedgewick's
Algorighm textbook.
'''
from __future__ import print_function
import itertools
import operator
import math


class NIL(object):
    '''A fake node used as NIL in Node.'''

    def __init__(self):
        self.key = None
        self.color = 'BLACK'
        self.left = None
        self.right = None
        self.parent = None

    def __nonzero__(self):
        return False

    def __repr__(self):
        return 'NIL'

    def flip_color(self):
        pass

    def is_red(self):
        return False


class Node(object):

    red = 'RED'
    black = 'BLACK'
    nil = NIL()

    def __init__(self, key):
        self.key = key
        self.parent = Node.nil
        self.left = Node.nil
        self.right = Node.nil
        self.color = None

    def __repr__(self):
        '''Node representation: (key, color, has_left, has_right).'''
        prop = (self.key, self.color, bool(self.left), bool(self.right))
        prop = [str(x) for x in prop]
        return ','.join(prop)

    def flip_color(self):
        if self.color:
            if self.color == Node.black:
                self.color = Node.red
            else:
                self.color = Node.black

    def is_red(self):
        if self.color == Node.red:
            return True
        return False

    @property
    def depth(self):
        '''Return the depth of a node counting from the root.
        root has a depth of 0.
        An empty tree has a depth of -1.'''
        node = self
        _depth = 0
        while node.parent:
            _depth += 1
            node = node.parent
        return _depth

    def space_count(self, min_horizontal_shift, max_depth):
        '''Assuming the tree is perfect with a depth of max_depth, this function
        returns the number of nodes on the left, not in the left subtree, of a
        given node.
        '''
        return int((self.horizontal_shift - min_horizontal_shift) * 2 ** (math.ceil(max_depth - 1)))

    @property
    def horizontal_shift(self):
        '''Return how much a node shifts from the root node.
        Negative values for shifting left, positive values for right.
        The root's left child shifts -1 from the root.
        The value of shifting is 2 ** (self.depth - 1).'''
        if not self:
            return 0
        if not self.parent:
            # No parent means root.
            return 0
        if self == self.parent.left:
            return self.parent.horizontal_shift - 1 * (0.5 ** (self.depth -1))
        else:
            return self.parent.horizontal_shift + 1 * (0.5 ** (self.depth -1))


class Tree(object):

    def __init__(self, node=None):
        '''Init with a node object.'''
        self.root = node
        if self.root:
            self.root.color = Node.black

    def _color_check(self):
        '''Check red properties of the tree.'''
        color = True
        for node in self.nodes():
            if node.is_red():
                if (node == node.parent.left) and (not node.left.is_red()) and (not node.left.is_red()):
                    pass
                else:
                    return False
        return True


    def max_depth(self, node=None):
        '''Return the max depth of the subtree rooted at node.
        0 for empty tree.'''
        if node is None:
            node = self.root
        if not node:
            return 0
        l_depth = self.max_depth(node.left) if node.left else 0
        r_depth = self.max_depth(node.right) if node.right else 0
        return max(l_depth, r_depth) + 1

    def nodes(self, node=None):
        '''Return all nodes in the subtree rooted at node.'''
        if node is None:
            node = self.root
        if not node:
            return []
        l_nodes = self.nodes(node.left) if node.left else []
        r_nodes = self.nodes(node.right) if node.right else []
        return l_nodes + r_nodes + [node]

    @property
    def min_horizontal_shift(self):
        '''The horizontal shift value of the left most node in a tree.'''
        # Min horizontal shift.
        min_horizontal_shift = min([x.horizontal_shift for x in self.nodes()])

        return min_horizontal_shift

    def print_ascii(self, outfile=None, use_slash=None):
        '''Print ascii representation of the tree to outfile or to console.'''

        # Group nodes by their depths.
        nodes_by_depth_dict = {}
        for k, g in itertools.groupby(self.nodes(), operator.attrgetter('depth')):
            if nodes_by_depth_dict.get(k):
                nodes_by_depth_dict[k] += sorted(list(g), key=lambda x:x.key)
            else:
                nodes_by_depth_dict[k] = sorted(list(g), key=lambda x:x.key)
        max_depth = max(nodes_by_depth_dict.keys())
        item_len = max([len(str(x.key)) for x in self.nodes()])

        min_horizontal_shift = self.min_horizontal_shift

        # Print each row.
        out_string = []
        for i in range(max_depth + 1):
            nodes = nodes_by_depth_dict[i]
            fmt = ''
            left_index = []
            right_index = []
            for node in nodes:
                # space_count is the number of nodes, existing or not existing,
                # on the left of current node in the whole tree.
                #   3
                #     5
                # There are two nodes on the left of 5, one on the left of 3.
                space_count = node.space_count(min_horizontal_shift, max_depth)
                # effective_space_count is the number of spaces to print between
                # two nodes in a row.
                # item_len + 1 is due to the calculation in space_count, which
                # sets the minimal space between a child and its parent to be
                # one space.
                effective_space_count = space_count * (item_len + 1) - len(fmt)
                fmt += ' ' * effective_space_count
                fmt += str(node.key)

                if node.left:
                    left_index.append(len(fmt) - item_len - 1)
                if node.right:
                    right_index.append(len(fmt))
            fmt += '\n'
            out_string.append(fmt)
            # Add connecting lines between each row.
            # If the row of the last referred node is not the last row.
            if use_slash:
                lines = self._attach_slash_connection(node, max_depth, item_len, fmt, left_index, right_index)
            else:
                lines = self._attach_dash_connection(node, max_depth, item_len, fmt, left_index, right_index)
            out_string.append(lines)
        if outfile:
            with open(outfile, 'w') as output:
                output.write(''.join(out_string))
        else:
            print(''.join(out_string))


    @staticmethod
    def _attach_dash_connection(node, max_depth, item_len, fmt, left, right):
        '''Attach dash connection lines between each row.'''
        dash = '-'
        if node.depth == max_depth:
            return ''
        lines = []
        # Width of connection line.
        count = (1 + item_len) * (2 ** (max_depth - node.depth - 1)) - item_len
        connection = [' ' for x in range(len(fmt) + count)]
        connection[-1] = '\n'
        for l in left:
            for i in range(count):
                connection[l - i] = dash
        for r in right:
            for i in range(count):
                connection[r + i] = dash
        return ''.join(connection)

    @staticmethod
    def _attach_slash_connection(node, max_depth, item_len, fmt, left, right):
        '''Attach slash connection lines between each row.'''
        left_slash = '/'
        right_slash= '\\'
        if node.depth == max_depth:
            return ''
        lines = []
        count = (1 + item_len) * (2 ** (max_depth - node.depth - 1)) - item_len
        for i in range(count):
            connection = [' ' for x in range(len(fmt) + count)]
            connection[-1] = '\n'
            for l in left:
                connection[l - i] = left_slash
            for r in right:
                connection[r + i] = right_slash
            lines.append(''.join(connection))

        return ''.join(lines)

    def find(self, key, node=None):
        '''Search a key.
        Right - larger;
        Left - Smaller or equal.
        '''
        if isinstance(node, NIL):
            return Node.nil

        if node is None:
            node = self.root

        y = self.root
        if not y:
            return None

        if node.key == key:
            return node
        elif node.key < key:
            return self.find(key, node.right)
        else:
            return self.find(key, node.left)

    def maximum(self, node):
        while node.right:
            node = node.right
        return node

    def minimum(self, node):
        while node.left:
            node = node.left
        return node

    def successor(self, node):
        '''Return the successor of a node.
        The only situation where we will use successor is in deletion
        when the node has two children. Thus this successor function
        can be designed to only deal with simple cases when the node
        has two children.
        '''
        return self.minimum(node.right)

    def predecessor(self, node):
        '''Return the predecessor of a node.
        For the same reason in successor() metho. This funciton only
        deals with simple cases where the node has to children.
        '''
        return self.maximum(node.left)

    def left_rotate(self, node):
        '''Perform left rotate operation at node.
        Return the new root of this subtree.
        Unlike left_rotate() method in the rbt_clrs implementation,
        this rotation operation will switch color between the old and new
        subtree roots.
        '''
        y = node.right

        node.right = y.left
        if y.left:
            y.left.parent = node

        y.left = node

        y.parent = node.parent
        if not node.parent:
            self.root = y
        else:
            if node == node.parent.left:
                node.parent.left = y
            else:
                node.parent.right = y
        node.parent = y
        node.color, y.color = y.color, node.color

        return y

    def right_rotate(self, node):
        '''Perform right rotate operation at node.
        Return the new root of this subtree.'''
        y = node.left

        node.left = y.right
        if y.right:
            y.right.parent = node

        y.right = node

        y.parent = node.parent
        if not node.parent:
            self.root = y
        else:
            if node == node.parent.left:
                node.parent.left = y
            else:
                node.parent.right = y
        node.parent = y

        node.color, y.color = y.color, node.color

        return y

    def flip_colors(self, node):
        '''Flip the colors of node and its children.
        '''
        node.flip_color()
        node.left.flip_color()
        node.right.flip_color()

        if node == self.root:
            node.color = Node.black

    def insert(self, node, incision=None, parent=None):
        '''Insert a node into the subtree rooted at incision.
        parent is the incision's parent node.
        '''
        if not isinstance(node, Node):
            raise InsertNonNodeError()
        if incision is None:
            incision = self.root
        node.color = Node.red
        # When reaches leaves or tree is empty.
        if not incision:
            node.parent = parent
            if parent:
                if node.key > parent.key:
                    parent.right = node
                else:
                    parent.left = node
            return node

        # Do recursively.
        if node.key > incision.key:
            incision.right = self.insert(node, incision.right, incision)
        else:
            incision.left = self.insert(node, incision.left, incision)

        # To maintain 1-1 correspondence with 2-3 tree.
        if incision.right.is_red() and not incision.left.is_red():
            incision = self.left_rotate(incision)
        if incision.left.is_red() and incision.left.left.is_red():
            incision = self.right_rotate(incision)
        if incision.left.is_red() and incision.right.is_red():
            self.flip_colors(incision)

        return incision

    def fix_up(self, node):
        '''Clean up right-leaning reds and 4-nodes.'''
        if node.right.is_red():
            # Rotate left right-leaning reds.
            node = self.left_rotate(node)
        if node.left.is_red() and node.left.left.is_red():
            # Rotate right red-red pairs.
            node = self.right_rotate(node)
        if node.left.is_red() and node.right.is_red():
            # Split 4-nodes.
            self.flip_colors(node)
        return node

    def move_red_right(self, node):
        '''Move red nodes right down the tree.'''
        # Step 1, flip colors.
        self.flip_colors(node)
        # Step 2, if node.left.left is red, rotate to fix 4-node on node.left
        # because fix_up will not fix node.left.
        if node.left.left and node.left.left.is_red():
            node = self.right_rotate(node)
            self.flip_colors(node)
        return node

    def move_red_left(self, node):
        '''Move red nodes left down the tree.'''
        # Step 1, flip colors.
        self.flip_colors(node)
        # Step 2, if node.right.left is red, rotate to fix 4-nodes on node.right
        # because fix_up will not fix node.right.
        if node.right.left.is_red():
            node.right = self.right_rotate(node.right)
            node = self.left_rotate(node)
            self.flip_colors(node)
        return node

    def delete_min(self, node=None):
        '''Delete the minimum node in the subtree rooted at node.'''
        if node is None:
            node = self.root
        # If node is the minimum.
        if not node.left:
            x = node
            if node == node.parent.left:
                node.parent.left = Node.nil
            else:
                node.parent.right = Node.nil
            node.parent = Node.nil
            return Node.nil
        # If no reds on the left.
        if (not node.left.is_red()) and (not node.left.left.is_red()):
            node = self.move_red_left(node)

        node.left = self.delete_min(node.left)
        return self.fix_up(node)

    def delete(self, node, incision=None):
        '''Delete a arbitary node.'''
        if not incision:
            # print("None")
            incision = self.root
        if node.key < incision.key:
            # Left.
            # print("left")
            if (not incision.left.is_red()) and incision.left.left and (not incision.left.left.is_red()):
                # Move red left if necessary.
                incision = self.move_red_left(incision)
            incision.left = self.delete(node, incision=incision.left)
        else:
            # Right or Equal.
            # print("right or equal")
            if incision.left.is_red():
                # Rotate to push red right.
                incision = self.right_rotate(incision)
                # print(incision)
                # self.print_ascii()
            if node.key == incision.key and not incision.right:
                # Equal and at bottom -> delete node.
                incision.right.parent = Node.nil
                if incision == self.root:
                    self.root = Node.nil
                return Node.nil
            if (not incision.right.is_red()) and incision.right.left and (not incision.right.left.is_red()):
                # Move red right if necessary.
                incision = self.move_red_right(incision)
            if node.key == incision.key:
                # Equal but not at bottom.
                incision.key = self.successor(incision).key
                incision.right = self.delete_min(incision.right)
                # print(incision, self.root)
            else:
                incision.right = self.delete(node, incision.right)
                # print(incision, incision.right)
        return self.fix_up(incision)


class InsertNonNodeError(Exception):
    '''Raised when try to insert a non-node object into a tree.'''
    pass
