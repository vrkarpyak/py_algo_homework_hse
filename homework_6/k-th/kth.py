import random
import sys
import unittest


def kth_largest(nums, k):
    arr = nums[:]
    target = len(arr) - k
    left = 0
    right = len(arr) - 1

    while left <= right:
        pivot = arr[(left + right) // 2]
        less = left
        i = left
        greater = right

        while i <= greater:
            if arr[i] < pivot:
                arr[less], arr[i] = arr[i], arr[less]
                less += 1
                i += 1
            elif arr[i] > pivot:
                arr[greater], arr[i] = arr[i], arr[greater]
                greater -= 1
            else:
                i += 1

        if target < less:
            right = less - 1
        elif target > greater:
            left = greater + 1
        else:
            return arr[target]


class TestKthLargest(unittest.TestCase):

    def test_first_example(self):
        self.assertEqual(kth_largest([3, 2, 1, 5, 6, 4], 2), 5)

    def test_second_example(self):
        self.assertEqual(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4)

    def test_one_element(self):
        self.assertEqual(kth_largest([7], 1), 7)

    def test_two_elements(self):
        self.assertEqual(kth_largest([1, 9], 1), 9)
        self.assertEqual(kth_largest([1, 9], 2), 1)

    def test_largest(self):
        self.assertEqual(kth_largest([3, 7, 2, 9], 1), 9)

    def test_smallest(self):
        self.assertEqual(kth_largest([3, 7, 2, 9], 4), 2)

    def test_duplicate_values(self):
        self.assertEqual(kth_largest([5, 5, 4, 4, 3], 2), 5)
        self.assertEqual(kth_largest([5, 5, 4, 4, 3], 3), 4)

    def test_all_equal(self):
        self.assertEqual(kth_largest([3, 3, 3, 3], 2), 3)

    def test_negative_numbers(self):
        self.assertEqual(kth_largest([-4, -1, -9, -2], 2), -2)

    def test_zeros(self):
        self.assertEqual(kth_largest([0, -2, 0, 4], 2), 0)

    def test_already_sorted(self):
        self.assertEqual(kth_largest([1, 2, 3, 4, 5], 2), 4)

    def test_reverse_sorted(self):
        self.assertEqual(kth_largest([5, 4, 3, 2, 1], 4), 2)

    def test_input_not_modified(self):
        nums = [3, 2, 1, 5, 6, 4]
        original = nums[:]
        kth_largest(nums, 2)
        self.assertEqual(nums, original)

    def test_large_equal_array(self):
        self.assertEqual(kth_largest([8] * 10000, 5000), 8)

    def test_large_sorted_array(self):
        self.assertEqual(kth_largest(list(range(5000)), 100), 4900)

    def test_random_lists(self):
        rng = random.Random(42)
        for size in range(1, 21):
            for _ in range(12):
                nums = [rng.randint(-12, 12) for _ in range(size)]
                expected = sorted(nums, reverse=True)
                for k in range(1, size + 1):
                    self.assertEqual(kth_largest(nums, k), expected[k - 1])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestKthLargest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    nums = list(map(int, input("Введите числа через пробел: ").split()))
    k = int(input("Введите k: "))
    print(kth_largest(nums, k))
