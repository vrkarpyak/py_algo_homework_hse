import sys
import unittest


def two_sum(arr, k):
    seen = {}

    for index, number in enumerate(arr):
        needed = k - number

        if needed in seen:
            return seen[needed], index

        seen[number] = index

    raise ValueError("Пара с нужной суммой не найдена")


class TestTwoSum(unittest.TestCase):

    def test_first_example(self):
        self.assertEqual(two_sum([1, 3, 4, 10], 7), (1, 2))

    def test_second_example(self):
        self.assertEqual(two_sum([5, 5, 1, 4], 10), (0, 1))

    def test_two_elements(self):
        self.assertEqual(two_sum([2, 7], 9), (0, 1))

    def test_pair_at_ends(self):
        self.assertEqual(two_sum([10, 2, 8, 5], 15), (0, 3))

    def test_pair_in_middle(self):
        self.assertEqual(two_sum([9, 2, 6, 5], 8), (1, 2))

    def test_negative_numbers(self):
        self.assertEqual(two_sum([-8, 4, 12, 1], 4), (0, 2))

    def test_zero(self):
        self.assertEqual(two_sum([0, 5, 2, 9], 5), (0, 1))

    def test_same_values(self):
        self.assertEqual(two_sum([3, 3], 6), (0, 1))

    def test_input_not_modified(self):
        arr = [1, 3, 4, 10]
        original = arr.copy()

        two_sum(arr, 7)

        self.assertEqual(arr, original)


def run_input():
    arr = list(map(int, input("Введите числа через пробел: ").split()))
    k = int(input("Введите k: "))

    first, second = two_sum(arr, k)
    print(first, second)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTwoSum)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    if "--input" in sys.argv:
        run_input()
