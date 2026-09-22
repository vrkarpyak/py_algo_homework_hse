import sys
import unittest


def validate_stack_sequences(pushed, popped):
    stack = []
    index = 0

    for number in pushed:
        stack.append(number)

        while stack and index < len(popped) and stack[-1] == popped[index]:
            stack.pop()
            index += 1

    return index == len(popped)


class TestValidateStackSequences(unittest.TestCase):

    def test_example_true(self):
        self.assertTrue(
            validate_stack_sequences(
                [1, 2, 3, 4, 5],
                [1, 3, 5, 4, 2]
            )
        )

    def test_example_false(self):
        self.assertFalse(
            validate_stack_sequences(
                [1, 2, 3],
                [3, 1, 2]
            )
        )

    def test_same_order(self):
        self.assertTrue(
            validate_stack_sequences(
                [1, 2, 3],
                [1, 2, 3]
            )
        )

    def test_reverse_order(self):
        self.assertTrue(
            validate_stack_sequences(
                [1, 2, 3],
                [3, 2, 1]
            )
        )

    def test_one_element(self):
        self.assertTrue(
            validate_stack_sequences(
                [5],
                [5]
            )
        )

    def test_another_false_case(self):
        self.assertFalse(
            validate_stack_sequences(
                [1, 2, 3, 4, 5],
                [4, 3, 5, 1, 2]
            )
        )

    def test_100000_elements(self):
        pushed = list(range(100000))
        popped = pushed[::-1]

        self.assertTrue(
            validate_stack_sequences(pushed, popped)
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestValidateStackSequences)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    pushed = list(map(int, input("Введите pushed через пробел: ").split()))
    popped = list(map(int, input("Введите popped через пробел: ").split()))

    print(validate_stack_sequences(pushed, popped))


# Решение:
# Идём по pushed и по очереди кладём числа в стек. После каждого добавления смотрим на верх стека. Если верхний элемент совпадает с тем, который сейчас нужен в popped, сразу удаляем его. Так продолжаем, пока совпадения есть.
# Если в конце удалось удалить элементы в том же порядке, что указан в popped, возвращаем True. Если нет будет False.

# Оценка сложности:
# Время — O(n), потому что каждый элемент один раз добавляется в стек и максимум один раз удаляется. Память - O(n), потому что в худшем случае все элементы могут одновременно лежать в стеке.

# Визуализация:
# pushed = [1, 2, 3, 4, 5]
# popped = [1, 3, 5, 4, 2]
#
# В начале стек пустой, index = 0.
# Сейчас из popped нам нужен элемент 1.
#
# Берём 1 из pushed и кладём в стек:
# stack = [1]
#
# Верх стека равен popped[0], то есть 1.
# Поэтому сразу удаляем 1:
# stack = []
# index = 1
#
# Теперь нужен элемент 3.
#
# Кладём 2:
# stack = [2]
# Верх стека 2, а нужен 3, поэтому ничего не удаляем.
#
# Кладём 3:
# stack = [2, 3]
#
# Верх стека равен 3, поэтому удаляем его:
# stack = [2]
# index = 2
#
# Теперь нужен элемент 5.
#
# Кладём 4:
# stack = [2, 4]
# Верх стека 4, а нужен 5.
#
# Кладём 5:
# stack = [2, 4, 5]
#
# Верх равен 5, удаляем:
# stack = [2, 4]
#
# Теперь нужен 4.
# Он уже находится на вершине, поэтому тоже удаляем:
# stack = [2]
#
# Теперь нужен 2.
# Он тоже на вершине, удаляем:
# stack = []
#
# В итоге получили элементы в порядке:
# 1, 3, 5, 4, 2
#
# Это полностью совпадает с popped,
# поэтому функция возвращает True.
