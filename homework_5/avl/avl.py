import sys
import unittest


class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AVL:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def rotate_right(self, node):
        left = node.left
        node.left = left.right
        left.right = node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        left.height = 1 + max(self.height(left.left), self.height(left.right))
        return left

    def rotate_left(self, node):
        right = node.right
        node.right = right.left
        right.left = node

        node.height = 1 + max(self.height(node.left), self.height(node.right))
        right.height = 1 + max(self.height(right.left), self.height(right.right))
        return right

    def balance(self, node):
        node.height = 1 + max(self.height(node.left), self.height(node.right))
        difference = self.height(node.left) - self.height(node.right)

        if difference > 1:
            if self.height(node.left.left) < self.height(node.left.right):
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        if difference < -1:
            if self.height(node.right.right) < self.height(node.right.left):
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def insert(self, value):
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        if node is None:
            return Node(value)

        if value < node.value:
            node.left = self._insert(node.left, value)
        elif value > node.value:
            node.right = self._insert(node.right, value)
        else:
            return node

        return self.balance(node)

    def search(self, value):
        node = self.root

        while node is not None:
            if value == node.value:
                return True
            if value < node.value:
                node = node.left
            else:
                node = node.right

        return False

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left

            next_node = node.right
            while next_node.left is not None:
                next_node = next_node.left

            node.value = next_node.value
            node.right = self._delete(node.right, next_node.value)

        return self.balance(node)

    def inorder(self):
        result = []

        def walk(node):
            if node is None:
                return
            walk(node.left)
            result.append(node.value)
            walk(node.right)

        walk(self.root)
        return result


class TestAVL(unittest.TestCase):
    def build_tree(self, values):
        tree = AVL()
        for value in values:
            tree.insert(value)
        return tree

    def check_balance(self, node):
        if node is None:
            return 0

        left = self.check_balance(node.left)
        right = self.check_balance(node.right)
        self.assertLessEqual(abs(left - right), 1)
        self.assertEqual(node.height, max(left, right) + 1)
        return node.height

    def test_empty_tree(self):
        tree = AVL()
        self.assertFalse(tree.search(5))
        tree.delete(5)
        self.assertEqual(tree.inorder(), [])

    def test_insert_and_search(self):
        tree = self.build_tree([10, 5, 20])
        self.assertTrue(tree.search(10))
        self.assertTrue(tree.search(5))
        self.assertTrue(tree.search(20))
        self.assertFalse(tree.search(15))

    def test_one_node(self):
        tree = self.build_tree([7])
        self.assertEqual(tree.inorder(), [7])
        self.assertTrue(tree.search(7))
        tree.delete(7)
        self.assertIsNone(tree.root)

    def test_duplicate_values(self):
        tree = self.build_tree([5, 5, 5, 3, 7])
        self.assertEqual(tree.inorder(), [3, 5, 7])
        self.check_balance(tree.root)

    def test_right_rotation(self):
        tree = self.build_tree([30, 20, 10])
        self.assertEqual(tree.root.value, 20)
        self.assertEqual(tree.inorder(), [10, 20, 30])
        self.check_balance(tree.root)

    def test_left_rotation(self):
        tree = self.build_tree([10, 20, 30])
        self.assertEqual(tree.root.value, 20)
        self.assertEqual(tree.inorder(), [10, 20, 30])
        self.check_balance(tree.root)

    def test_left_right_rotation(self):
        tree = self.build_tree([30, 10, 20])
        self.assertEqual(tree.root.value, 20)
        self.assertEqual(tree.inorder(), [10, 20, 30])
        self.check_balance(tree.root)

    def test_right_left_rotation(self):
        tree = self.build_tree([10, 30, 20])
        self.assertEqual(tree.root.value, 20)
        self.assertEqual(tree.inorder(), [10, 20, 30])
        self.check_balance(tree.root)

    def test_delete_leaf(self):
        tree = self.build_tree([20, 10, 30])
        tree.delete(10)
        self.assertEqual(tree.inorder(), [20, 30])
        self.check_balance(tree.root)

    def test_delete_node_with_one_child(self):
        tree = self.build_tree([20, 10, 30, 25])
        tree.delete(30)
        self.assertEqual(tree.inorder(), [10, 20, 25])
        self.check_balance(tree.root)

    def test_delete_node_with_two_children(self):
        tree = self.build_tree([20, 10, 30, 5, 15, 25, 35])
        tree.delete(20)
        self.assertEqual(tree.inorder(), [5, 10, 15, 25, 30, 35])
        self.check_balance(tree.root)

    def test_delete_missing_value(self):
        tree = self.build_tree([2, 1, 3])
        tree.delete(99)
        self.assertEqual(tree.inorder(), [1, 2, 3])
        self.check_balance(tree.root)

    def test_delete_rebalances_tree(self):
        tree = self.build_tree([4, 2, 5, 1, 3])
        tree.delete(5)
        self.assertEqual(tree.inorder(), [1, 2, 3, 4])
        self.assertEqual(tree.root.value, 2)
        self.check_balance(tree.root)

    def test_negative_numbers_and_zero(self):
        tree = self.build_tree([-10, 0, -5, 3, -20])
        self.assertEqual(tree.inorder(), [-20, -10, -5, 0, 3])
        tree.delete(-10)
        self.assertEqual(tree.inorder(), [-20, -5, 0, 3])
        self.check_balance(tree.root)

    def test_many_inserts(self):
        tree = self.build_tree(range(100))
        self.assertEqual(tree.inorder(), list(range(100)))
        self.check_balance(tree.root)

    def test_many_deletes(self):
        tree = self.build_tree(range(100))
        for value in range(0, 100, 2):
            tree.delete(value)
            self.check_balance(tree.root)

        self.assertEqual(tree.inorder(), list(range(1, 100, 2)))

    def test_delete_everything(self):
        tree = self.build_tree([10, 20, 30, 40, 50, 25])
        for value in [10, 20, 30, 40, 50, 25]:
            tree.delete(value)
            self.check_balance(tree.root)
        self.assertEqual(tree.inorder(), [])
        self.assertIsNone(tree.root)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAVL)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    values = list(map(int, input("Введите числа через пробел: ").split()))
    tree = AVL()
    for value in values:
        tree.insert(value)

    print("Дерево:", tree.inorder())

    value = int(input("Какое число найти? "))
    print("Найдено:", tree.search(value))

    value = int(input("Какое число удалить? "))
    tree.delete(value)
    print("После удаления:", tree.inorder())
