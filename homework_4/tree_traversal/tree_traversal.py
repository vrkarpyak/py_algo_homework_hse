import sys
import unittest


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root is None:
            self.root = Node(value)
            return

        current = self.root

        while True:
            if value < current.value:
                if current.left is None:
                    current.left = Node(value)
                    return
                current = current.left

            elif value > current.value:
                if current.right is None:
                    current.right = Node(value)
                    return
                current = current.right

            else:
                return

    def preorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            result.append(node.value)
            visit(node.left)
            visit(node.right)

        visit(self.root)
        return result

    def inorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            visit(node.left)
            result.append(node.value)
            visit(node.right)

        visit(self.root)
        return result

    def postorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            visit(node.left)
            visit(node.right)
            result.append(node.value)

        visit(self.root)
        return result

    def reverse_preorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            result.append(node.value)
            visit(node.right)
            visit(node.left)

        visit(self.root)
        return result

    def reverse_inorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            visit(node.right)
            result.append(node.value)
            visit(node.left)

        visit(self.root)
        return result

    def reverse_postorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            visit(node.right)
            visit(node.left)
            result.append(node.value)

        visit(self.root)
        return result


class TestBinarySearchTree(unittest.TestCase):
    def build_tree(self, values):
        tree = BinarySearchTree()

        for value in values:
            tree.insert(value)

        return tree

    def check_traversals(self, tree, expected):
        methods = [
            tree.preorder,
            tree.inorder,
            tree.postorder,
            tree.reverse_preorder,
            tree.reverse_inorder,
            tree.reverse_postorder,
        ]

        for method, values in zip(methods, expected):
            with self.subTest(traversal=method.__name__):
                result = method()
                self.assertIsInstance(result, list)
                self.assertEqual(result, values)

    def check_bst(self, node, lower=None, upper=None):
        if node is None:
            return

        if lower is not None:
            self.assertGreater(node.value, lower)

        if upper is not None:
            self.assertLess(node.value, upper)

        self.check_bst(node.left, lower, node.value)
        self.check_bst(node.right, node.value, upper)

    def snapshot(self, node):
        if node is None:
            return None

        return (
            node.value,
            self.snapshot(node.left),
            self.snapshot(node.right),
        )

    def test_empty_tree(self):
        tree = BinarySearchTree()
        self.assertIsNone(tree.root)
        self.check_traversals(tree, [[], [], [], [], [], []])

    def test_single_node(self):
        tree = self.build_tree([4])
        self.assertEqual(tree.root.value, 4)
        self.assertIsNone(tree.root.left)
        self.assertIsNone(tree.root.right)
        self.check_traversals(tree, [[4], [4], [4], [4], [4], [4]])

    def test_two_nodes_left(self):
        tree = self.build_tree([4, 2])
        self.assertEqual(tree.root.left.value, 2)
        self.assertIsNone(tree.root.right)
        self.check_traversals(
            tree,
            [[4, 2], [2, 4], [2, 4], [4, 2], [4, 2], [2, 4]],
        )

    def test_two_nodes_right(self):
        tree = self.build_tree([4, 6])
        self.assertEqual(tree.root.right.value, 6)
        self.assertIsNone(tree.root.left)
        self.check_traversals(
            tree,
            [[4, 6], [4, 6], [6, 4], [4, 6], [6, 4], [6, 4]],
        )

    def test_balanced_tree(self):
        tree = self.build_tree([4, 2, 6, 1, 3, 5, 7])
        self.check_traversals(
            tree,
            [
                [4, 2, 1, 3, 6, 5, 7],
                [1, 2, 3, 4, 5, 6, 7],
                [1, 3, 2, 5, 7, 6, 4],
                [4, 6, 7, 5, 2, 3, 1],
                [7, 6, 5, 4, 3, 2, 1],
                [7, 5, 6, 3, 1, 2, 4],
            ],
        )

    def test_asymmetric_tree(self):
        tree = self.build_tree([8, 3, 10, 1, 6, 14, 4, 7, 13])
        self.check_traversals(
            tree,
            [
                [8, 3, 1, 6, 4, 7, 10, 14, 13],
                [1, 3, 4, 6, 7, 8, 10, 13, 14],
                [1, 4, 7, 6, 3, 13, 14, 10, 8],
                [8, 10, 14, 13, 3, 6, 7, 4, 1],
                [14, 13, 10, 8, 7, 6, 4, 3, 1],
                [13, 14, 10, 7, 4, 6, 1, 3, 8],
            ],
        )

    def test_left_chain(self):
        tree = self.build_tree([5, 4, 3, 2, 1])
        ascending = [1, 2, 3, 4, 5]
        descending = [5, 4, 3, 2, 1]
        self.check_traversals(
            tree,
            [descending, ascending, ascending, descending, descending, ascending],
        )

    def test_right_chain(self):
        tree = self.build_tree([1, 2, 3, 4, 5])
        ascending = [1, 2, 3, 4, 5]
        descending = [5, 4, 3, 2, 1]
        self.check_traversals(
            tree,
            [ascending, ascending, descending, ascending, descending, descending],
        )

    def test_zigzag_chain(self):
        tree = self.build_tree([10, 3, 8, 5, 7])
        self.check_traversals(
            tree,
            [
                [10, 3, 8, 5, 7],
                [3, 5, 7, 8, 10],
                [7, 5, 8, 3, 10],
                [10, 3, 8, 5, 7],
                [10, 8, 7, 5, 3],
                [7, 5, 8, 3, 10],
            ],
        )

    def test_negative_values_and_zero(self):
        tree = self.build_tree([0, -3, 4, -5, -1, 2, 7])
        self.check_traversals(
            tree,
            [
                [0, -3, -5, -1, 4, 2, 7],
                [-5, -3, -1, 0, 2, 4, 7],
                [-5, -1, -3, 2, 7, 4, 0],
                [0, 4, 7, 2, -3, -1, -5],
                [7, 4, 2, 0, -1, -3, -5],
                [7, 2, 4, -1, -5, -3, 0],
            ],
        )

    def test_same_values(self):
        tree = self.build_tree([5, 5, 5, 5])
        self.assertIsNone(tree.root.left)
        self.assertIsNone(tree.root.right)
        self.check_traversals(tree, [[5], [5], [5], [5], [5], [5]])

    def test_duplicate_root_and_children(self):
        tree = self.build_tree([4, 2, 6, 1, 3, 5, 7])
        before = self.snapshot(tree.root)
        root = tree.root

        for value in [4, 2, 6, 1, 3, 5, 7]:
            tree.insert(value)

        self.assertIs(tree.root, root)
        self.assertEqual(self.snapshot(tree.root), before)
        self.check_traversals(
            tree,
            [
                [4, 2, 1, 3, 6, 5, 7],
                [1, 2, 3, 4, 5, 6, 7],
                [1, 3, 2, 5, 7, 6, 4],
                [4, 6, 7, 5, 2, 3, 1],
                [7, 6, 5, 4, 3, 2, 1],
                [7, 5, 6, 3, 1, 2, 4],
            ],
        )

    def test_insert_preserves_global_bst_property(self):
        tree = BinarySearchTree()
        values = [8, 3, 10, 1, 6, 14, 4, 7, 13, 0, -5, 20, 6]

        for value in values:
            tree.insert(value)
            self.check_bst(tree.root)

        self.assertEqual(tree.root.left.right.left.value, 4)
        self.assertEqual(tree.root.right.right.left.value, 13)
        self.assertEqual(tree.inorder(), sorted(set(values)))

    def test_insert_after_traversals(self):
        tree = self.build_tree([4, 2, 6])
        previous_result = tree.inorder()
        tree.preorder()
        tree.postorder()
        tree.reverse_preorder()
        tree.reverse_inorder()
        tree.reverse_postorder()

        tree.insert(3)

        self.assertEqual(previous_result, [2, 4, 6])
        self.check_traversals(
            tree,
            [
                [4, 2, 3, 6],
                [2, 3, 4, 6],
                [3, 2, 6, 4],
                [4, 6, 2, 3],
                [6, 4, 3, 2],
                [6, 3, 2, 4],
            ],
        )

    def test_traversals_do_not_change_tree(self):
        tree = self.build_tree([8, 3, 10, 1, 6, 14, 4, 7, 13])
        before = self.snapshot(tree.root)
        root = tree.root

        for method in [
            tree.preorder,
            tree.inorder,
            tree.postorder,
            tree.reverse_preorder,
            tree.reverse_inorder,
            tree.reverse_postorder,
        ]:
            with self.subTest(traversal=method.__name__):
                method()
                self.assertIs(tree.root, root)
                self.assertEqual(self.snapshot(tree.root), before)

    def test_each_call_returns_new_list(self):
        tree = self.build_tree([4, 2, 6, 1, 3, 5, 7])

        for method in [
            tree.preorder,
            tree.inorder,
            tree.postorder,
            tree.reverse_preorder,
            tree.reverse_inorder,
            tree.reverse_postorder,
        ]:
            with self.subTest(traversal=method.__name__):
                first = method()
                second = method()
                self.assertIsNot(first, second)
                first.clear()
                self.assertEqual(method(), second)
                self.assertEqual(len(second), 7)

    def test_trees_are_independent(self):
        first = self.build_tree([2, 1, 3])
        second = self.build_tree([10, 8, 12])
        first.insert(0)

        self.assertIsNot(first.root, second.root)
        self.assertEqual(first.inorder(), [0, 1, 2, 3])
        self.check_traversals(
            second,
            [
                [10, 8, 12],
                [8, 10, 12],
                [8, 12, 10],
                [10, 12, 8],
                [12, 10, 8],
                [12, 8, 10],
            ],
        )

    def test_input_list_not_modified(self):
        values = [8, 3, 10, 1, 6, 14, 4, 7, 13]
        original = values.copy()
        self.build_tree(values)
        self.assertEqual(values, original)

    def test_insertion_order_changes_shape(self):
        first = self.build_tree([2, 1, 3])
        second = self.build_tree([1, 2, 3])

        self.assertEqual(first.inorder(), second.inorder())
        self.assertEqual(first.preorder(), [2, 1, 3])
        self.assertEqual(second.preorder(), [1, 2, 3])

    def test_long_right_chain(self):
        ascending = list(range(250))
        descending = ascending[::-1]
        tree = self.build_tree(ascending)
        self.check_traversals(
            tree,
            [ascending, ascending, descending, ascending, descending, descending],
        )

    def test_long_left_chain(self):
        ascending = list(range(250))
        descending = ascending[::-1]
        tree = self.build_tree(descending)
        self.check_traversals(
            tree,
            [descending, ascending, ascending, descending, descending, ascending],
        )

    def test_large_balanced_tree(self):
        tree = BinarySearchTree()

        def add_middle(left, right):
            if left > right:
                return

            middle = (left + right) // 2
            tree.insert(middle)
            add_middle(left, middle - 1)
            add_middle(middle + 1, right)

        add_middle(0, 1022)
        expected = list(range(1023))

        self.check_bst(tree.root)
        self.assertEqual(tree.inorder(), expected)
        self.assertEqual(tree.reverse_inorder(), expected[::-1])

        for method in [
            tree.preorder,
            tree.inorder,
            tree.postorder,
            tree.reverse_preorder,
            tree.reverse_inorder,
            tree.reverse_postorder,
        ]:
            with self.subTest(traversal=method.__name__):
                result = method()
                self.assertIsInstance(result, list)
                self.assertEqual(len(result), 1023)
                self.assertCountEqual(result, expected)

        self.assertEqual(tree.preorder()[0], 511)
        self.assertEqual(tree.reverse_preorder()[0], 511)
        self.assertEqual(tree.postorder()[-1], 511)
        self.assertEqual(tree.reverse_postorder()[-1], 511)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestBinarySearchTree)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    values = list(map(int, input("Введите числа через пробел: ").split()))
    tree = BinarySearchTree()

    for value in values:
        tree.insert(value)

    print("preorder:", tree.preorder())
    print("inorder:", tree.inorder())
    print("postorder:", tree.postorder())
    print("reverse preorder:", tree.reverse_preorder())
    print("reverse inorder:", tree.reverse_inorder())
    print("reverse postorder:", tree.reverse_postorder())
