import sys
import unittest

def is_palindrome(number):
    original = number
    reversed_number = 0

    while number > 0:
        digit = number % 10
        reversed_number = reversed_number * 10 + digit
        number //= 10

    return original == reversed_number

class TestPalindrome(unittest.TestCase):
    def test_odd_length_palindrome(self):
        self.assertTrue(is_palindrome(121))

    def test_not_palindrome(self):
        self.assertFalse(is_palindrome(31))

    def test_single_digit(self):
        self.assertTrue(is_palindrome(7))

    def test_even_length_palindrome(self):
        self.assertTrue(is_palindrome(1221))

    def test_number_ending_with_zero(self):
        self.assertFalse(is_palindrome(10))

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestPalindrome)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    number = int(input("Введите положительное целое число: "))
    print(is_palindrome(number))




# Решение:
# Сохраняем исходное число, потому что дальше будем его изменять.
# Затем в цикле по одной достаём цифры справа налево:
# number % 10 — получаем последнюю цифру,
# number // 10 — удаляем последнюю цифру.
# Из полученных цифр постепенно собираем reversed_number.
# В конце сравниваем исходное число с перевёрнутым.
# Если они равны, число является палиндромом.

# Оценка сложности:
# Временная сложность - O(log n), потому что на каждой итерации число делится на 10, то есть цикл выполняется столько раз, сколько цифр в числе.
# Пространственная сложность - O(1), потому что используется фиксированное количество дополнительных переменных, не зависящее от размера входного числа.

# Визуализация работы алгоритма на примере 12021:
#
# Исходное число: 12021
# reversed_number = 0
#
# Шаг | number | digit = number % 10 | reversed_number
# -----------------------------------------------------
#  1  | 12021  |          1          |        1
#  2  | 1202   |          2          |       12
#  3  | 120    |          0          |      120
#  4  | 12     |          2          |     1202
#  5  | 1      |          1          |    12021
#
# После каждой итерации последняя цифра удаляется:
# number = number // 10
#
# Схема:
# 12021 -> 1
#  1202 -> 12
#   120 -> 120
#    12 -> 1202
#     1 -> 12021
#     0 -> цикл закончен
#
# В результате:
# original        = 12021
# reversed_number = 12021
#
# Числа равны -> функция возвращает True.

# Тесты:
# Проверяются несколько разных случаев:
# обычный палиндром (121),
# число, которое не является палиндромом (31),
# однозначное число (7),
# палиндром с чётным количеством цифр (1221),
# число, заканчивающееся на 0 (10).