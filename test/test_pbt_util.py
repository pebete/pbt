"""test for pbt_util.py"""
import sys
sys.path.append("src")
from pbt_util import *
import unittest

class PbtUtilTestCase(unittest.TestCase):

    def test_get_dirs_up_to_root(self):
        self.assertEqual(get_dirs_up_to_root("/"), ["/"])
        self.assertEqual(get_dirs_up_to_root("/asd"), ["/asd", "/"])
        self.assertEqual(get_dirs_up_to_root("/asd/"), ["/asd", "/"])
        self.assertEqual(get_dirs_up_to_root("/asd/foo"),
                ["/asd/foo", "/asd", "/"])
        self.assertEqual(get_dirs_up_to_root("/asd/foo/"),
                ["/asd/foo", "/asd", "/"])


if __name__ == "__main__":
    unittest.main()

