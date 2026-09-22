import sys
import unittest


class ListNode:
    def __init__(self, value):
        self.value = value
        self.next = None


def list_to_linked_list(values):
    if not values:
        return None

    head = ListNode(values[0])
    current = head

    for value in values[1:]:
        current.next = ListNode(value)
        current = current.next

    return head


def linked_list_to_list(head):
    result = []

    while head is not None:
        result.append(head.value)
        head = head.next

    return result


def merge_with_dummy(list1, list2):
    dummy = ListNode(0)
    current = dummy

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next

        current = current.next

    if list1 is not None:
        current.next = list1
    else:
        current.next = list2

    return dummy.next


def merge_without_dummy(list1, list2):
    if list1 is None:
        return list2

    if list2 is None:
        return list1

    if list1.value <= list2.value:
        head = list1
        list1 = list1.next
    else:
        head = list2
        list2 = list2.next

    current = head

    while list1 is not None and list2 is not None:
        if list1.value <= list2.value:
            current.next = list1
            list1 = list1.next
        else:
            current.next = list2
            list2 = list2.next

        current = current.next

    if list1 is not None:
        current.next = list1
    else:
        current.next = list2

    return head


class TestMergeLists(unittest.TestCase):

    def test_example_with_dummy(self):
        list1 = list_to_linked_list([1, 2, 4])
        list2 = list_to_linked_list([1, 3, 4])

        result = merge_with_dummy(list1, list2)

        self.assertEqual(
            linked_list_to_list(result),
            [1, 1, 2, 3, 4, 4]
        )

    def test_example_without_dummy(self):
        list1 = list_to_linked_list([1, 2, 4])
        list2 = list_to_linked_list([1, 3, 4])

        result = merge_without_dummy(list1, list2)

        self.assertEqual(
            linked_list_to_list(result),
            [1, 1, 2, 3, 4, 4]
        )

    def test_empty_first_list(self):
        list1 = list_to_linked_list([])
        list2 = list_to_linked_list([1, 2, 3])

        self.assertEqual(
            linked_list_to_list(merge_with_dummy(list1, list2)),
            [1, 2, 3]
        )

    def test_empty_second_list(self):
        list1 = list_to_linked_list([1, 2, 3])
        list2 = list_to_linked_list([])

        self.assertEqual(
            linked_list_to_list(merge_without_dummy(list1, list2)),
            [1, 2, 3]
        )

    def test_both_empty(self):
        self.assertEqual(
            linked_list_to_list(merge_with_dummy(None, None)),
            []
        )

        self.assertEqual(
            linked_list_to_list(merge_without_dummy(None, None)),
            []
        )

    def test_negative_numbers(self):
        list1 = list_to_linked_list([-5, -1, 4])
        list2 = list_to_linked_list([-3, 0, 2])

        self.assertEqual(
            linked_list_to_list(merge_with_dummy(list1, list2)),
            [-5, -3, -1, 0, 2, 4]
        )

    def test_duplicates(self):
        list1 = list_to_linked_list([1, 1, 3])
        list2 = list_to_linked_list([1, 2, 3])

        self.assertEqual(
            linked_list_to_list(merge_without_dummy(list1, list2)),
            [1, 1, 1, 2, 3, 3]
        )


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMergeLists)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    values1 = list(map(int, input("Введите первый список через пробел: ").split()))
    values2 = list(map(int, input("Введите второй список через пробел: ").split()))

    list1 = list_to_linked_list(values1)
    list2 = list_to_linked_list(values2)
    result1 = merge_with_dummy(list1, list2)

    list1 = list_to_linked_list(values1)
    list2 = list_to_linked_list(values2)
    result2 = merge_without_dummy(list1, list2)

    print("С фиктивным элементом:", linked_list_to_list(result1))
    print("Без фиктивного элемента:", linked_list_to_list(result2))


# Решение:
# В обоих вариантах сравниваем первые узлы двух списков и каждый раз берём тот, где значение меньше. Потом двигаемся дальше только по тому списку, из которого взяли узел. Когда один список заканчивается, просто присоединяем остаток второго.
# В варианте с dummy сначала создаётся фиктивный узел, чтобы не обрабатывать первый элемент отдельно. В варианте без dummy сначала вручную выбирается голова нового списка, а дальше логика такая же.
# Новые узлы для результата не создаются: мы соединяем уже существующие узлы двух списков.

# Оценка сложности:
# Время алогритма O(n + m), т.к. каждый узел двух списков просматривается один раз. Память - O(1) потому что используется только несколько дополнительных ссылок. Один узел в первом способе тоже считается O(1).

# Визуализация:
# list1 = 1 -> 2 -> 4
# list2 = 1 -> 3 -> 4
#
# Смотрим на первые элементы двух списков.
#
# Сравниваем 1 и 1.
# Они равны, поэтому берём 1 из list1.
#
# Результат:
# 1
#
# Теперь list1 начинается с 2,
# а list2 всё ещё начинается с 1.
#
# Сравниваем 2 и 1.
# Меньше 1, поэтому берём его из list2.
#
# Результат:
# 1 -> 1
#
# Теперь сравниваем 2 и 3.
# Меньше 2, берём его из list1.
#
# Результат:
# 1 -> 1 -> 2
#
# Теперь сравниваем 4 и 3.
# Меньше 3, берём его из list2.
#
# Результат:
# 1 -> 1 -> 2 -> 3
#
# Теперь сравниваем 4 и 4.
# Берём 4 из list1.
#
# Результат:
# 1 -> 1 -> 2 -> 3 -> 4
#
# list1 закончился.
# В list2 остался последний элемент 4, поэтому просто присоединяем его в конец.
#
# Итоговый список:
# 1 -> 1 -> 2 -> 3 -> 4 -> 4
#
# В варианте с dummy перед первым элементом временно есть фиктивный узел, но в ответ он не попадает.
#
# В варианте без dummy первый элемент результата выбирается сразу из list1 или list2.
#
# Сам принцип слияния дальше одинаковый: каждый раз сравниваем два текущих элемента и берём меньший.