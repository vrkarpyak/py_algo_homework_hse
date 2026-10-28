import sys
import unittest


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


def is_valid_bst(root):
    def check(node, minimum, maximum):
        if node is None:
            return True

        if minimum is not None and node.value <= minimum:
            return False

        if maximum is not None and node.value >= maximum:
            return False

        return check(node.left, minimum, node.value) and check(node.right, node.value, maximum)

    return check(root, None, None)


def build_tree(values):
    if not values or values[0] is None:
        return None

    root = Node(values[0])
    queue = [root]
    current = 0
    index = 1

    while current < len(queue) and index < len(values):
        node = queue[current]
        current += 1

        if values[index] is not None:
            node.left = Node(values[index])
            queue.append(node.left)
        index += 1

        if index < len(values):
            if values[index] is not None:
                node.right = Node(values[index])
                queue.append(node.right)
            index += 1

    return root


class TestValidateBST(unittest.TestCase):
    def test_empty_tree(self):
        self.assertTrue(is_valid_bst(None))

    def test_one_node(self):
        self.assertTrue(is_valid_bst(Node(10)))

    def test_valid_tree(self):
        root = build_tree([4, 2, 6, 1, 3, 5, 7])
        self.assertTrue(is_valid_bst(root))

    def test_invalid_right_child(self):
        root = build_tree([5, 1, 4, None, None, 3, 6])
        self.assertFalse(is_valid_bst(root))

    def test_invalid_left_child(self):
        root = build_tree([5, 7, 8])
        self.assertFalse(is_valid_bst(root))

    def test_invalid_deep_left_subtree(self):
        root = build_tree([10, 5, 15, 2, 12])
        self.assertFalse(is_valid_bst(root))

    def test_invalid_deep_right_subtree(self):
        root = build_tree([10, 5, 15, None, None, 6, 20])
        self.assertFalse(is_valid_bst(root))

    def test_equal_to_parent(self):
        root = build_tree([5, 5, 7])
        self.assertFalse(is_valid_bst(root))

    def test_equal_to_ancestor(self):
        root = build_tree([5, 3, 8, None, 5])
        self.assertFalse(is_valid_bst(root))

    def test_only_left_children(self):
        root = build_tree([5, 4, None, 3, None, 2])
        self.assertTrue(is_valid_bst(root))

    def test_only_right_children(self):
        root = build_tree([1, None, 2, None, 3, None, 4])
        self.assertTrue(is_valid_bst(root))

    def test_negative_numbers_and_zero(self):
        root = build_tree([0, -3, 5, -8, -1, 2, 7])
        self.assertTrue(is_valid_bst(root))

    def test_invalid_negative_numbers(self):
        root = build_tree([0, -3, 5, None, 1])
        self.assertFalse(is_valid_bst(root))

    def test_invalid_descendant_on_left_edge_of_right_subtree(self):
        root = build_tree([20, 10, 30, None, None, 25, 40, 15])
        self.assertFalse(is_valid_bst(root))


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestValidateBST)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    text = input("Введите узлы дерева через пробел (None - пустой узел): ").split()
    values = [None if x.lower() in ("none", "null", "-") else int(x) for x in text]
    root = build_tree(values)
    print(is_valid_bst(root))
