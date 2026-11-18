import random
import sys
import unittest
from time import perf_counter


def merge_sort(nums):
    if len(nums) <= 1:
        return nums[:]

    middle = len(nums) // 2
    left = merge_sort(nums[:middle])
    right = merge_sort(nums[middle:])

    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def quick_sort(nums):
    result = nums[:]

    def sort(left, right):
        if left >= right:
            return

        pivot = result[right]
        position = left

        for i in range(left, right):
            if result[i] <= pivot:
                result[position], result[i] = result[i], result[position]
                position += 1

        result[position], result[right] = result[right], result[position]

        sort(left, position - 1)
        sort(position + 1, right)

    sort(0, len(result) - 1)
    return result


def timer(func):
    def wrapper(*args, **kwargs):
        start = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start
        print(f"{func.__name__}: {elapsed:.6f} сек")
        return result

    return wrapper


@timer
def timed_merge_sort(nums):
    return merge_sort(nums)


@timer
def timed_quick_sort(nums):
    return quick_sort(nums)


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

    def test_input_unchanged(self):
        nums = [4, 1, 3, 2]
        original = nums[:]
        merge_sort(nums)
        quick_sort(nums)
        self.assertEqual(nums, original)

    def test_many_numbers(self):
        numbers = list(range(250))
        random.Random(42).shuffle(numbers)
        self.check_both(numbers)

    def test_large_sorted(self):
        self.check_both(list(range(350)))

    def test_large_equal(self):
        self.check_both([8] * 350)

    def test_timer_returns_result(self):
        def add_one(number):
            return number + 1

        import io
        from contextlib import redirect_stdout

        output = io.StringIO()
        with redirect_stdout(output):
            result = timer(add_one)(5)

        self.assertEqual(result, 6)
        self.assertIn("add_one:", output.getvalue())


def compare_times():
    size = 750
    random_numbers = list(range(size))
    random.Random(42).shuffle(random_numbers)

    examples = [
        ("Случайный порядок", random_numbers),
        ("Уже отсортирован", list(range(size))),
        ("Обратный порядок", list(range(size, 0, -1))),
        ("Одинаковые числа", [5] * size),
    ]

    for name, nums in examples:
        print(f"\n{name}, n = {len(nums)}")
        timed_merge_sort(nums)
        timed_quick_sort(nums)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestSorting)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    nums = list(map(int, input("Введите числа через пробел: ").split()))
    print("Merge sort:", timed_merge_sort(nums))
    print("Quick sort:", timed_quick_sort(nums))

    print("\nСравнение на разных массивах:")
    compare_times()
