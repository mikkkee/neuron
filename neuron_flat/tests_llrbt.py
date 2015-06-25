from unittest import TestCase

from llrbt import Node, Tree, NIL

class LLRBTTestInitAndInsert(TestCase):

    def setUp(self):
        self.a = Node(5)
        self.b = Node(4)
        self.c = Node(3)
        self.d = Node(2)

    def test_init(self):
        self.t = Tree(self.a)

        self.assertEqual(self.t.root, self.a)
        self.assertEqual(self.a.color, Node.black)

        self.assertFalse(self.a.left)
        self.assertFalse(self.a.right)

        self.assertEqual(self.a.depth, 0)
        self.assertEqual(self.a.horizontal_shift, 0)

        self.assertTrue(self.t._color_check())

    def test_insert_at_root(self):
        self.t = Tree(self.a)
        self.t.insert(self.b)

        self.assertEqual(self.t.root, self.a)

        self.assertEqual(self.a.color, Node.black)
        self.assertEqual(self.b.color, Node.red)

        self.assertEqual(self.a.left, self.b)
        self.assertFalse(self.a.right)
        self.assertFalse(self.b.left)
        self.assertFalse(self.b.right)

        self.assertEqual(self.b.depth, 1)
        self.assertEqual(self.b.horizontal_shift, -1)
        self.assertEqual(self.a.depth, 0)
        self.assertEqual(self.a.horizontal_shift, 0)

        self.assertTrue(self.t._color_check())

    def test_insert_to_single_3_node_left(self):
        '''Insert to a single 3-node.
        Insert to the 3-node's left.
        '''

        # Construct a single 3-node by inserting at root.
        self.t = Tree(self.a)
        self.t.insert(self.c)

        # Insert into the 3-node's left.
        self.t.insert(self.d)
        # Check structure.
        self.assertEqual(self.t.root, self.c)
        self.assertEqual(self.c.left, self.d)
        self.assertEqual(self.c.right, self.a)
        self.assertFalse(self.c.parent)
        self.assertEqual(self.a.parent, self.c)
        self.assertEqual(self.d.parent, self.c)
        self.assertFalse(self.a.right or self.a.left)
        self.assertFalse(self.d.left or self.d.right)
        # Check color.
        self.assertEqual(self.a.color, Node.black)
        self.assertEqual(self.c.color, Node.black)
        self.assertEqual(self.d.color, Node.black)

        self.assertTrue(self.t._color_check())

    def test_insert_to_single_3_node_middle(self):
        '''Insert to a single 3-node.
        Insert to the 3-node's middle.
        '''

        # Construct a single 3-node by inserting at root.
        self.t = Tree(self.a)
        self.t.insert(self.c)

        # Insert into the 3-node's middle.
        self.t.insert(self.b)
        # Check structure.
        self.assertEqual(self.t.root, self.b)
        self.assertEqual(self.b.left, self.c)
        self.assertEqual(self.b.right, self.a)
        self.assertFalse(self.b.parent)
        self.assertEqual(self.a.parent, self.b)
        self.assertEqual(self.c.parent, self.b)
        self.assertFalse(self.a.left or self.a.right)
        self.assertFalse(self.c.left or self.c.right)
        # Check color.
        self.assertEqual(self.a.color, Node.black)
        self.assertEqual(self.b.color, Node.black)
        self.assertEqual(self.c.color, Node.black)

        self.assertTrue(self.t._color_check())

    def test_insert_to_single_3_node_right(self):
        '''Insert to a single 3-node.
        Insert to the 3-node's right.
        '''

        # Construct a single 3-node.
        self.t = Tree(self.b)
        self.t.insert(self.c)

        # Insert into the 3-node's right.
        self.t.insert(self.a)
        # Check structure.
        self.assertEqual(self.t.root, self.b)
        self.assertEqual(self.b.left, self.c)
        self.assertEqual(self.b.right, self.a)
        self.assertFalse(self.b.parent)
        self.assertEqual(self.c.parent, self.b)
        self.assertEqual(self.a.parent, self.b)
        self.assertFalse(self.c.left or self.c.right)
        self.assertFalse(self.a.left or self.a.right)
        # Check color.
        self.assertEqual(self.a.color, Node.black)
        self.assertEqual(self.b.color, Node.black)
        self.assertEqual(self.c.color, Node.black)

        self.assertTrue(self.t._color_check())


class LLRBTTestDelete(TestCase):
    '''Left-lean red-black tree deletion tests.'''

    def setUp(self):
        self.a = Node(0)
        self.t = Tree(self.a)

    def test_deletion_at_root(self):
        # Deletion at root
        for i in range(1, 7):
            self.t.insert(Node(i))
        self.assertEqual(len(self.t.nodes()), 7)
        # Delete root.
        self.t.delete(Node(3))
        self.assertEqual(len(self.t.nodes()), 6)
        self.assertFalse(3 in [x.key for x in self.t.nodes()])
        self.assertEqual(self.t.root.key, 4)

        self.assertTrue(self.t._color_check())

    def test_deletion_single_3_node_left(self):
        '''Deletion at a single 3-node - left.
        Single 3-node - Case 1/2.
        '''
        self.t.insert(Node(1))
        # Delete left node in the single 3-node.
        self.t.delete(Node(0))
        self.assertEqual(self.t.root.key, 1)
        self.assertFalse(self.t.root.left or self.t.root.right)

        self.assertTrue(self.t._color_check())

    def test_deletion_single_3_node_right(self):
        '''Deletion at a single 3-node - right.
        Single 3-node - Case 2/2.
        '''
        self.t.insert(Node(1))
        # Delete right node in the single 3-node.
        self.t.delete(Node(1))
        self.assertEqual(self.t.root.key, 0)
        self.assertFalse(self.t.root.left or self.t.root.right)

        self.assertTrue(self.t._color_check())

    def test_deletion_2_node_at_bottom_left(self):
        '''Deletion of a 2-node at bottom - left child.
        2-node bottom - Case 1/2.
        '''
        for i in range(1, 7):
            self.t.insert(Node(i))
        self.t.delete(Node(4))
        self.assertEqual(len(self.t.nodes()), 6)
        self.assertFalse(4 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_2_node_at_bottom_right(self):
        '''Deletion of a 2-node at bottom - right child.
        2-node bottom - Case 2/2.
        '''
        for i in range(1, 7):
            self.t.insert(Node(i))
        self.t.delete(Node(6))
        self.assertEqual(len(self.t.nodes()), 6)
        self.assertFalse(6 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_3_node_at_bottom_left(self):
        '''Deletion of a 3-node at bottom - left node.
        3-node bottom - Case 1/2.
        '''
        for i in range(1, 8):
            self.t.insert(Node(i))
        self.t.delete(Node(6))
        self.assertEqual(len(self.t.nodes()), 7)
        self.assertFalse(6 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_3_node_at_bottom_right(self):
        '''Deletion of a 3-node at bottom - right node.
        3-node bottom - Case 2/2.
        '''
        for i in range(1, 8):
            self.t.insert(Node(i))
        self.t.delete(Node(7))
        self.assertEqual(len(self.t.nodes()), 7)
        self.assertFalse(7 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_3_node_middle_smaller(self):
        '''Deletion of 3-node at bottom - smaller than red node.
        3-node middle - Case 1/5.
        '''
        for i in range(1, 9):
            self.t.insert(Node(i))
        self.t.delete(Node(4))
        self.assertEqual(len(self.t.nodes()), 8)
        self.assertFalse(4 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_3_node_middle_left(self):
        '''Deletion of 3-node at bottom - red node.
        3-node middle - Case 2/5.
        '''
        for i in range(1, 9):
            self.t.insert(Node(i))
        self.t.delete(Node(5))
        self.assertEqual(len(self.t.nodes()), 8)
        self.assertFalse(5 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_3_node_middle_between(self):
        '''deletion of 3 node in the middle - between two nodes.
        3-node middle - Case 3/5.
        '''
        for i in range(1, 9):
            self.t.insert(Node(i))
        self.t.delete(Node(6))
        self.assertEqual(len(self.t.nodes()), 8)
        self.assertFalse(6 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_3_node_middle_right(self):
        '''deletion of 3 node in the middle - right node.
        3-node middle - Case 4/5.
        '''
        for i in range(1, 9):
            self.t.insert(Node(i))
        self.t.delete(Node(7))
        self.assertEqual(len(self.t.nodes()), 8)
        self.assertFalse(7 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_3_node_middle_larger(self):
        '''deletion of 3 node in the middle - right node.
        3-node middle - Case 5/5.
        '''
        for i in range(1, 9):
            self.t.insert(Node(i))
        self.t.delete(Node(8))
        self.assertEqual(len(self.t.nodes()), 8)
        self.assertFalse(8 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_2_node_middle_left(self):
        '''Deletion of 2 node in the middle - node is a left child.
        2-node middle - Case 1/2.
        '''
        for i in range(1, 9):
            self.t.insert(Node(i))
        self.t.delete(Node(1))
        self.assertEqual(len(self.t.nodes()), 8)
        self.assertFalse(1 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())

    def test_deletion_2_node_middle_right(self):
        '''Deletion of 2 node in the middle - node is a left child.
        2-node middle - Case 1/2.
        '''
        for i in range(1, 15):
            self.t.insert(Node(i))
        self.t.delete(Node(11))
        self.assertEqual(len(self.t.nodes()), 14)
        self.assertFalse(11 in [x.key for x in self.t.nodes()])

        self.assertTrue(self.t._color_check())
