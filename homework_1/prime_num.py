import sys
import unittest


def count_primes(n):
    if n <= 2:
        return 0

    is_prime = [True] * (n // 2)
    is_prime[0] = False

    p = 3

    while p * p < n:
        if is_prime[p // 2]:
            for multiple in range(p * p, n, 2 * p):
                is_prime[multiple // 2] = False

        p += 2

    return 1 + sum(is_prime)

class TestCountPrimes(unittest.TestCase):
    
    def test_example(self):
        self.assertEqual(count_primes(10), 4)

    def test_one(self):
        self.assertEqual(count_primes(1), 0)

    def test_two(self):
        self.assertEqual(count_primes(2), 0)

    def test_three(self):
        self.assertEqual(count_primes(3), 1)

    def test_four(self):
        self.assertEqual(count_primes(4), 2)

    def test_prime_square(self):
        self.assertEqual(count_primes(25), 9)

    def test_hundred(self):
        self.assertEqual(count_primes(100), 25)

    def test_prime_boundary(self):
        self.assertEqual(count_primes(101), 25)

    def test_after_prime_boundary(self):
        self.assertEqual(count_primes(102), 26)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestCountPrimes)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    n = int(input("Введите целое число N: "))
    print(count_primes(n))


# Решение:
# Число 2 учитываем отдельно, а дальше рассматриваем только нечетные числа. (у четных всегда будет делитель 2 в любом случае)
# Для каждого найденного простого числа отмечаем его кратные как составные.
# Четные числа не проверяем, поэтому количество операций и размер массива меньше.
# В конце считаем оставшиеся простые числа и добавляем число 2.

# Оценка сложности:
# Временная сложность - O(n log log n), так как кратные числа последовательно исключаются для простых делителей.
# Пространственная сложность - O(n), потому что хранится массив отметок для чисел меньше N.

# Визуализация:
# К примеру N = 35
#
# Рассматриваем только нечетные числа:
# 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33
#
# Начинаем с 3:
# убираем его кратные 9, 15, 21, 27, 33
#
# Осталось:
# 3, 5, 7, 11, 13, 17, 19, 23, 25, 29, 31
#
# Следующее число - 5:
# убираем 25
#
# Осталось:
# 3, 5, 7, 11, 13, 17, 19, 23, 29, 31
# Дальше 7 уже не обрабатываем, потому что:
# 7 * 7 = 49 > 35
# Все составные числа меньше 35 уже были исключены.
# Добавляем отдельно число 2.
# Простые числа меньше 35:
# 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31
#
# Ответ: 11