import sys
import unittest


def group_anagrams(strs):
    groups = {}

    for word in strs:
        key = "".join(sorted(word))

        if key not in groups:
            groups[key] = []

        groups[key].append(word)

    return list(groups.values())


def normalize(groups):
    return sorted(sorted(group) for group in groups)


class TestGroupAnagrams(unittest.TestCase):

    def test_example(self):
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        expected = [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_one_word(self):
        result = group_anagrams(["cat"])
        expected = [["cat"]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_empty_list(self):
        self.assertEqual(group_anagrams([]), [])

    def test_no_anagrams(self):
        result = group_anagrams(["cat", "dog", "sun"])
        expected = [["cat"], ["dog"], ["sun"]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_all_anagrams(self):
        result = group_anagrams(["abc", "bca", "cab"])
        expected = [["abc", "bca", "cab"]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_duplicate_words(self):
        result = group_anagrams(["abc", "abc", "bca"])
        expected = [["abc", "abc", "bca"]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_empty_strings(self):
        result = group_anagrams(["", "", "a"])
        expected = [["", ""], ["a"]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_different_group_sizes(self):
        result = group_anagrams(["listen", "silent", "enlist", "rat", "tar", "art", "cat"])
        expected = [["listen", "silent", "enlist"], ["rat", "tar", "art"], ["cat"]]
        self.assertEqual(normalize(result), normalize(expected))

    def test_input_not_modified(self):
        strs = ["eat", "tea", "tan"]
        original = strs.copy()

        group_anagrams(strs)

        self.assertEqual(strs, original)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestGroupAnagrams)
    result = unittest.TextTestRunner(verbosity=2).run(suite)

    if not result.wasSuccessful():
        sys.exit(1)

    strs = input("Введите слова через пробел: ").split()
    print(group_anagrams(strs))
