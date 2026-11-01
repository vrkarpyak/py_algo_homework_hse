import sys
import unittest
from contextlib import redirect_stdout
from functools import wraps
from io import StringIO


def tracer(func):
    depth = 0

    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal depth

        arguments = [str(value) for value in args]
        for key, value in kwargs.items():
            arguments.append(f"{key}={value}")
        call = f"{func.__name__}({', '.join(arguments)})"

        print("  " * depth + f"Вход: {call}")
        depth += 1

        try:
            result = func(*args, **kwargs)
        finally:
            depth -= 1

        print("  " * depth + f"Возврат: {call} = {result}")
        return result

    return wrapper


def permutations(nums):
    @tracer
    def build(remaining):
        if not remaining:
            return [[]]

        result = []

        for i in range(len(remaining)):
            number = remaining[i]
            rest = remaining[:i] + remaining[i + 1:]

            for p in build(rest):
                result.append([number] + p)

        return result

    return build(nums)


class TestPermutations(unittest.TestCase):
    def run_without_output(self, nums):
        with redirect_stdout(StringIO()):
            return permutations(nums)

    def test_first_example(self):
        self.assertEqual(self.run_without_output([1, 2, 3]), [
            [1, 2, 3], [1, 3, 2], [2, 1, 3],
            [2, 3, 1], [3, 1, 2], [3, 2, 1]
        ])

    def test_second_example(self):
        self.assertEqual(self.run_without_output([0, 1]), [[0, 1], [1, 0]])

    def test_third_example(self):
        self.assertEqual(self.run_without_output([1]), [[1]])

    def test_empty_list(self):
        self.assertEqual(self.run_without_output([]), [[]])

    def test_two_negative_numbers(self):
        self.assertEqual(self.run_without_output([-1, -2]), [[-1, -2], [-2, -1]])

    def test_different_numbers(self):
        self.assertEqual(self.run_without_output([5, 10, 15]), [
            [5, 10, 15], [5, 15, 10], [10, 5, 15],
            [10, 15, 5], [15, 5, 10], [15, 10, 5]
        ])

    def test_four_numbers(self):
        result = self.run_without_output([1, 2, 3, 4])
        self.assertEqual(len(result), 24)
        self.assertEqual(len({tuple(p) for p in result}), 24)
        self.assertIn([4, 3, 2, 1], result)
        self.assertIn([1, 2, 3, 4], result)

    def test_repeated_values(self):
        self.assertEqual(self.run_without_output([1, 1]), [[1, 1], [1, 1]])

    def test_input_not_modified(self):
        nums = [3, 1, 2]
        self.run_without_output(nums)
        self.assertEqual(nums, [3, 1, 2])

    def test_repeated_calls(self):
        first = self.run_without_output([1, 2])
        second = self.run_without_output([1, 2])
        self.assertEqual(first, second)

    def test_tracer_enters_and_returns(self):
        output = StringIO()
        with redirect_stdout(output):
            result = permutations([1])

        self.assertEqual(result, [[1]])
        self.assertEqual(output.getvalue().splitlines(), [
            "Вход: build([1])",
            "  Вход: build([])",
            "  Возврат: build([]) = [[]]",
            "Возврат: build([1]) = [[1]]"
        ])

    def test_tracer_branching(self):
        output = StringIO()
        with redirect_stdout(output):
            result = permutations([1, 2])

        lines = output.getvalue().splitlines()
        self.assertEqual(result, [[1, 2], [2, 1]])
        self.assertEqual(len(lines), 10)
        self.assertEqual(sum("Вход:" in line for line in lines), 5)
        self.assertEqual(sum("Возврат:" in line for line in lines), 5)
        self.assertEqual(lines[0], "Вход: build([1, 2])")
        self.assertEqual(lines[-1], "Возврат: build([1, 2]) = [[1, 2], [2, 1]]")

    def test_tracer_depth_restored(self):
        output = StringIO()
        with redirect_stdout(output):
            permutations([1, 2])

        self.assertEqual(output.getvalue().splitlines()[-1],
                         "Возврат: build([1, 2]) = [[1, 2], [2, 1]]")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPermutations)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    nums = list(map(int, input("Введите числа через пробел: ").split()))
    print("Результат:", permutations(nums))
