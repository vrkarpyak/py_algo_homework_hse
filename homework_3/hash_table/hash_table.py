import sys
import unittest


class HashTable:
    def __init__(self, capacity=8):
        if capacity <= 0:
            raise ValueError("Размер таблицы должен быть положительным")

        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(capacity)]

    def _index(self, key):
        return hash(key) % self.capacity

    def _resize(self):
        old_table = self.table

        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]
        self.size = 0

        for bucket in old_table:
            for pair in bucket:
                self._insert_without_resize(pair[0], pair[1])

    def _insert_without_resize(self, key, value):
        index = self._index(key)
        bucket = self.table[index]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return

        bucket.append([key, value])
        self.size += 1

    def insert(self, key, value):
        index = self._index(key)
        bucket = self.table[index]

        for pair in bucket:
            if pair[0] == key:
                pair[1] = value
                return

        if (self.size + 1) / self.capacity > 0.75:
            self._resize()

        self._insert_without_resize(key, value)

    def search(self, key):
        index = self._index(key)
        bucket = self.table[index]

        for pair in bucket:
            if pair[0] == key:
                return pair[1]

        raise KeyError(key)

    def delete(self, key):
        index = self._index(key)
        bucket = self.table[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                self.size -= 1
                return True

        return False

    def __len__(self):
        return self.size


class CollisionKey:
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, CollisionKey) and self.value == other.value


class TestHashTable(unittest.TestCase):

    def test_insert_and_search(self):
        table = HashTable()
        table.insert("name", "Alice")
        self.assertEqual(table.search("name"), "Alice")

    def test_update_existing_key(self):
        table = HashTable()
        table.insert("name", "Alice")
        table.insert("name", "Bob")

        self.assertEqual(table.search("name"), "Bob")
        self.assertEqual(len(table), 1)

    def test_delete_existing_key(self):
        table = HashTable()
        table.insert("a", 10)
        table.insert("b", 20)

        self.assertTrue(table.delete("a"))
        self.assertEqual(len(table), 1)

        with self.assertRaises(KeyError):
            table.search("a")

    def test_delete_missing_key(self):
        table = HashTable()
        self.assertFalse(table.delete("missing"))

    def test_search_missing_key(self):
        table = HashTable()

        with self.assertRaises(KeyError):
            table.search("missing")

    def test_collision(self):
        table = HashTable(capacity=4)

        first = CollisionKey("first")
        second = CollisionKey("second")
        third = CollisionKey("third")

        table.insert(first, 10)
        table.insert(second, 20)
        table.insert(third, 30)

        self.assertEqual(table.search(first), 10)
        self.assertEqual(table.search(second), 20)
        self.assertEqual(table.search(third), 30)

    def test_delete_from_collision_chain(self):
        table = HashTable(capacity=4)

        first = CollisionKey("first")
        second = CollisionKey("second")
        third = CollisionKey("third")

        table.insert(first, 10)
        table.insert(second, 20)
        table.insert(third, 30)

        self.assertTrue(table.delete(second))
        self.assertEqual(table.search(first), 10)
        self.assertEqual(table.search(third), 30)

        with self.assertRaises(KeyError):
            table.search(second)

    def test_resize(self):
        table = HashTable(capacity=4)

        table.insert("a", 1)
        table.insert("b", 2)
        table.insert("c", 3)
        old_capacity = table.capacity

        table.insert("d", 4)

        self.assertGreater(table.capacity, old_capacity)
        self.assertEqual(table.search("a"), 1)
        self.assertEqual(table.search("b"), 2)
        self.assertEqual(table.search("c"), 3)
        self.assertEqual(table.search("d"), 4)
        self.assertEqual(len(table), 4)

    def test_different_value_types(self):
        table = HashTable()

        table.insert("number", 10)
        table.insert("text", "hello")
        table.insert("list", [1, 2, 3])
        table.insert("none", None)

        self.assertEqual(table.search("number"), 10)
        self.assertEqual(table.search("text"), "hello")
        self.assertEqual(table.search("list"), [1, 2, 3])
        self.assertIsNone(table.search("none"))

    def test_negative_and_zero_keys(self):
        table = HashTable()

        table.insert(0, "zero")
        table.insert(-5, "negative")

        self.assertEqual(table.search(0), "zero")
        self.assertEqual(table.search(-5), "negative")

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            HashTable(0)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestHashTable)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    table = HashTable()

    while True:
        command = input("Введите insert, search, delete или exit: ").strip()

        if command == "exit":
            break

        if command == "insert":
            key = input("Введите ключ: ")
            value = input("Введите значение: ")
            table.insert(key, value)
            print("Добавлено")

        elif command == "search":
            key = input("Введите ключ: ")

            try:
                print(table.search(key))
            except KeyError:
                print("Ключ не найден")

        elif command == "delete":
            key = input("Введите ключ: ")

            if table.delete(key):
                print("Удалено")
            else:
                print("Ключ не найден")

        else:
            print("Неизвестная операция")
