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


@tracer
def factorial(n):
    if n < 0:
        raise ValueError("Число должно быть неотрицательным")
    if n == 0:
        return 1
    return n * factorial(n - 1)


class TestTracer(unittest.TestCase):
    def capture(self, func, *args, **kwargs):
        output = StringIO()
        with redirect_stdout(output):
            result = func(*args, **kwargs)
        return result, output.getvalue().splitlines()

    def test_factorial_zero(self):
        result, lines = self.capture(factorial, 0)
        self.assertEqual(result, 1)
        self.assertEqual(lines, [
            "Вход: factorial(0)",
            "Возврат: factorial(0) = 1"
        ])

    def test_factorial_three(self):
        result, lines = self.capture(factorial, 3)
        self.assertEqual(result, 6)
        self.assertEqual(lines, [
            "Вход: factorial(3)",
            "  Вход: factorial(2)",
            "    Вход: factorial(1)",
            "      Вход: factorial(0)",
            "      Возврат: factorial(0) = 1",
            "    Возврат: factorial(1) = 1",
            "  Возврат: factorial(2) = 2",
            "Возврат: factorial(3) = 6"
        ])

    def test_repeated_calls(self):
        _, first = self.capture(factorial, 2)
        _, second = self.capture(factorial, 2)
        self.assertEqual(first, second)

    def test_another_function(self):
        @tracer
        def double(x):
            return x * 2

        result, lines = self.capture(double, 5)
        self.assertEqual(result, 10)
        self.assertEqual(lines, [
            "Вход: double(5)",
            "Возврат: double(5) = 10"
        ])

    def test_keyword_argument(self):
        @tracer
        def add(a, b=0):
            return a + b

        result, lines = self.capture(add, 2, b=3)
        self.assertEqual(result, 5)
        self.assertEqual(lines, [
            "Вход: add(2, b=3)",
            "Возврат: add(2, b=3) = 5"
        ])

    def test_branching_recursion(self):
        @tracer
        def fibonacci(n):
            if n < 2:
                return n
            return fibonacci(n - 1) + fibonacci(n - 2)

        result, lines = self.capture(fibonacci, 3)
        self.assertEqual(result, 2)
        self.assertEqual(lines[0], "Вход: fibonacci(3)")
        self.assertEqual(lines[-1], "Возврат: fibonacci(3) = 2")
        self.assertEqual(sum("Вход:" in line for line in lines), 5)
        self.assertEqual(sum("Возврат:" in line for line in lines), 5)

    def test_none_result(self):
        @tracer
        def nothing():
            return None

        result, lines = self.capture(nothing)
        self.assertIsNone(result)
        self.assertEqual(lines[-1], "Возврат: nothing() = None")

    def test_depth_restored_after_error(self):
        with redirect_stdout(StringIO()):
            with self.assertRaises(ValueError):
                factorial(-1)

        result, lines = self.capture(factorial, 1)
        self.assertEqual(result, 1)
        self.assertEqual(lines[0], "Вход: factorial(1)")

    def test_factorial_one(self):
        result, lines = self.capture(factorial, 1)
        self.assertEqual(result, 1)
        self.assertEqual(lines[0], "Вход: factorial(1)")
        self.assertEqual(lines[-1], "Возврат: factorial(1) = 1")

    def test_many_recursive_levels(self):
        result, lines = self.capture(factorial, 7)
        self.assertEqual(result, 5040)
        self.assertEqual(len(lines), 16)
        self.assertEqual(lines[7], "              Вход: factorial(0)")
        self.assertEqual(lines[8], "              Возврат: factorial(0) = 1")

    def test_depth_restored_after_nested_error(self):
        @tracer
        def fail_at_zero(n):
            if n == 0:
                raise ValueError("ошибка")
            return fail_at_zero(n - 1)

        with redirect_stdout(StringIO()):
            with self.assertRaises(ValueError):
                fail_at_zero(3)

        output = StringIO()
        with redirect_stdout(output):
            with self.assertRaises(ValueError):
                fail_at_zero(0)
        self.assertEqual(output.getvalue().splitlines(), ["Вход: fail_at_zero(0)"])

    def test_original_exception_preserved(self):
        @tracer
        def broken():
            raise RuntimeError("пример")

        with redirect_stdout(StringIO()):
            with self.assertRaisesRegex(RuntimeError, "пример"):
                broken()

    def test_function_name_preserved(self):
        self.assertEqual(factorial.__name__, "factorial")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestTracer)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    n = int(input("Введите число для факториала: "))
    print("Результат:", factorial(n))
