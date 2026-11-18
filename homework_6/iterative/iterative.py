import random
import sys
import unittest


def merge_sort(nums):
    arr = nums[:]
    width = 1

    while width < len(arr):
        merged = []

        for start in range(0, len(arr), 2 * width):
            left = arr[start:start + width]
            right = arr[start + width:start + 2 * width]
            i = 0
            j = 0

            while i < len(left) and j < len(right):
                if left[i] <= right[j]:
                    merged.append(left[i])
                    i += 1
                else:
                    merged.append(right[j])
                    j += 1

            merged.extend(left[i:])
            merged.extend(right[j:])

        arr = merged
        width *= 2

    return arr


def quick_sort(nums):
    arr = nums[:]
    stack = [(0, len(arr) - 1)]

    while stack:
        left, right = stack.pop()

        if left >= right:
            continue

        pivot = arr[right]
        position = left

        for i in range(left, right):
            if arr[i] <= pivot:
                arr[position], arr[i] = arr[i], arr[position]
                position += 1

        arr[position], arr[right] = arr[right], arr[position]

        stack.append((left, position - 1))
        stack.append((position + 1, right))

    return arr


class TestSorting(unittest.TestCase):

    def check_both(self, nums):
        expected = sorted(nums)
        self.assertEqual(merge_sort(nums), expected)
        self.assertEqual(quick_sort(nums), expected)

    def test_example(self):
        self.check_both([4, 2, 7, 1, 3])

    def test_empty(self):
        self.check_both([])

    def test_single_element(self):
        self.check_both([5])

    def test_two_elements(self):
        self.check_both([2, 1])

    def test_sorted(self):
        self.check_both([1, 2, 3, 4, 5])

    def test_reverse_sorted(self):
        self.check_both([5, 4, 3, 2, 1])

    def test_same_values(self):
        self.check_both([3, 3, 3, 3, 3])

    def test_duplicates(self):
        self.check_both([4, 1, 4, 2, 1, 3, 2])

    def test_negative_numbers(self):
        self.check_both([-5, 2, 0, -1, 2, -9])

    def test_zeros(self):
        self.check_both([0, 0, 2, -2, 0])

    def test_input_unchanged(self):
        nums = [4, 1, 3, 2]
        original = nums[:]
        merge_sort(nums)
        quick_sort(nums)
        self.assertEqual(nums, original)

    def test_random_numbers(self):
        nums = list(range(250))
        random.Random(42).shuffle(nums)
        self.check_both(nums)

    def test_large_sorted(self):
        self.check_both(list(range(1100)))

    def test_large_reverse_sorted(self):
        self.check_both(list(range(1100, 0, -1)))

    def test_large_same_values(self):
        self.check_both([8] * 1100)

    def test_many_small_random_lists(self):
        rng = random.Random(7)
        for n in range(15):
            for _ in range(20):
                nums = [rng.randint(-10, 10) for _ in range(n)]
                self.check_both(nums)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSorting)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    nums = list(map(int, input("Введите числа через пробел: ").split()))
    print("Merge sort:", merge_sort(nums))
    print("Quick sort:", quick_sort(nums))
