import sys
import unittest


class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class Stack:
    def __init__(self):
        self.head = None

    def push(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node

    def pop(self):
        if self.head is None:
            raise IndexError("Стек пуст")

        value = self.head.value
        self.head = self.head.next
        return value

    def is_empty(self):
        return self.head is None


class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, value):
        new_node = Node(value)

        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node

    def dequeue(self):
        if self.head is None:
            raise IndexError("Очередь пуста")

        value = self.head.value
        self.head = self.head.next

        if self.head is None:
            self.tail = None

        return value

    def is_empty(self):
        return self.head is None


class TestStackAndQueue(unittest.TestCase):

    def test_stack(self):
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)

        self.assertEqual(stack.pop(), 3)
        self.assertEqual(stack.pop(), 2)
        self.assertEqual(stack.pop(), 1)

    def test_queue(self):
        queue = Queue()
        queue.enqueue(1)
        queue.enqueue(2)
        queue.enqueue(3)

        self.assertEqual(queue.dequeue(), 1)
        self.assertEqual(queue.dequeue(), 2)
        self.assertEqual(queue.dequeue(), 3)

    def test_empty_stack(self):
        stack = Stack()

        with self.assertRaises(IndexError):
            stack.pop()

    def test_empty_queue(self):
        queue = Queue()

        with self.assertRaises(IndexError):
            queue.dequeue()

    def test_is_empty(self):
        stack = Stack()
        queue = Queue()

        self.assertTrue(stack.is_empty())
        self.assertTrue(queue.is_empty())

        stack.push(10)
        queue.enqueue(10)

        self.assertFalse(stack.is_empty())
        self.assertFalse(queue.is_empty())


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStackAndQueue)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    numbers = list(map(int, input("Введите числа через пробел: ").split()))

    stack = Stack()
    queue = Queue()

    for number in numbers:
        stack.push(number)
        queue.enqueue(number)

    stack_result = []
    while not stack.is_empty():
        stack_result.append(stack.pop())

    queue_result = []
    while not queue.is_empty():
        queue_result.append(queue.dequeue())

    print("Стек:", stack_result)
    print("Очередь:", queue_result)


# Решение:
# Стек работает по принципу: последний добавили - первый забрали. Поэтому новый узел всегда ставим в начало списка и оттуда же удаляем.
# Очередь работает наоборот: первый добавили - первый забрали. Поэтому добавляем узлы в конец списка, а удаляем из начала. Для этого храним head и tail.

# Оценка сложности:
# Добавление и удаление в стеке - O(1). Добавление и удаление в очереди - O(1). Память - O(n), потому что для каждого элемента создаётся отдельный узел.


# Визуализация
# Сначала посмотрим на стек.
#
# push(1):
# head -> 1
#
# push(2):
# head -> 2 -> 1
#
# push(3):
# head -> 3 -> 2 -> 1
#
# Теперь начинаем удалять элементы.
# pop() возвращает 3, потому что он был добавлен последним.
# Остаётся: 2 -> 1
#
# Следующий pop() возвращает 2.
# Остаётся: 1
#
# Последний pop() возвращает 1.
# Стек становится пустым.
#
# Получаем порядок удаления: 3, 2, 1.
# То есть стек работает по принципу: последний добавили — первый забрали.
#
#
# Теперь очередь.
#
# enqueue(1):
# head -> 1 <- tail
#
# enqueue(2):
# head -> 1 -> 2 <- tail
#
# enqueue(3):
# head -> 1 -> 2 -> 3 <- tail
#
# Теперь удаляем элементы.
# dequeue() возвращает 1, потому что он был добавлен первым.
# Остаётся: 2 -> 3
#
# Следующий dequeue() возвращает 2.
# Остаётся: 3
#
# Последний dequeue() возвращает 3.
# Очередь становится пустой.
#
# Получаем порядок удаления: 1, 2, 3.
# То есть очередь работает по принципу: первый добавили — первый забрали.