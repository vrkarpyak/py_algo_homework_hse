import sys
import unittest

def max_even_sum(numbers):
    total = 0
    min_odd = None

    for number in numbers:
        total += number

        if number % 2 != 0:
            if min_odd is None or number < min_odd:
                min_odd = number

    if total % 2 == 0:
        return total

    return total - min_odd

class TestMaxEvenSum(unittest.TestCase):

    def test_example(self):
        self.assertEqual(max_even_sum([5, 7, 13, 2, 14]), 36)

    def test_single_odd_number(self):
        self.assertEqual(max_even_sum([3]), 0)

    def test_single_even_number(self):
        self.assertEqual(max_even_sum([8]), 8)

    def test_all_even(self):
        self.assertEqual(max_even_sum([2, 4, 6]), 12)

    def test_even_sum_with_odd_numbers(self):
        self.assertEqual(max_even_sum([1, 3, 2]), 6)

    def test_remove_smallest_odd(self):
        self.assertEqual(max_even_sum([9, 5, 3, 2]), 16)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMaxEvenSum)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    numbers = list(map(int, input("Введите числа через пробел: ").split()))
    print(max_even_sum(numbers))


# Решение:
# Сначала считаем сумму всех элементов массива.
# Так как все числа положительные, берем максимальное количество элементов.
# Если общая сумма четная, она и будет максимальным ответом.
# Если сумма нечетная, нужно убрать одно нечетное число.
# Убираем минимальное нечетное число, чтобы потерять как можно меньше.

# Оценка сложности:
# Временная сложность - O(n), потому что массив проходим один раз.
# Пространственная сложность - O(1), потому что используется фиксированное количество дополнительных переменных.

# Визуализация:
# Массив: [8, 11, 6, 7, 14, 3, 2]
#
# Число | Общая сумма | Минимальное нечетное
# -------------------------------------------
#   8   |      8      |         -
#  11   |     19      |        11
#   6   |     25      |        11
#   7   |     32      |         7
#  14   |     46      |         7
#   3   |     49      |         3
#   2   |     51      |         3
#
# Общая сумма = 51, она нечетная.
# Чтобы сделать ее четной, нужно убрать одно нечетное число.
# Минимальное нечетное число = 3, поэтому убираем именно его, чтобы потерять как можно меньше от общей суммы.
#
# 51 - 3 = 48
# Ответ: 48