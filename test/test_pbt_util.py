"""test for pbt_util.py"""
import sys
from pbt import pbt_util
import unittest
from unittest.mock import MagicMock
import shlex

class PbtUtilTestCase(unittest.TestCase):

    def test_get_dirs_up_to_root(self):
        self.assertEqual(pbt_util.get_dirs_up_to_root("/"), ["/"])
        self.assertEqual(pbt_util.get_dirs_up_to_root("/asd"), ["/asd", "/"])
        self.assertEqual(pbt_util.get_dirs_up_to_root("/asd/"), ["/asd", "/"])
        self.assertEqual(pbt_util.get_dirs_up_to_root("/asd/foo"),
                ["/asd/foo", "/asd", "/"])
        self.assertEqual(pbt_util.get_dirs_up_to_root("/asd/foo/"),
                ["/asd/foo", "/asd", "/"])

    def test_install_package_under_venv(self):
        pbt_util.running_under_virtual_env = MagicMock(return_value=True)
        pbt_util.query_yes_no = MagicMock(return_value=True)
        pbt_util.subprocess.check_call = MagicMock(return_value=None)
        pbt_util.install_package("foo")
        pbt_util.subprocess.check_call.assert_called_with(shlex.split("pip3 install foo"))

    def test_install_package_out_of_venv(self):
        pbt_util.running_under_virtual_env = MagicMock(return_value=False)
        pbt_util.query_yes_no = MagicMock(return_value=True)
        pbt_util.subprocess.check_call = MagicMock(return_value=None)
        pbt_util.install_package("foo")
        pbt_util.subprocess.check_call.assert_called_with(shlex.split("sudo pip3 install foo"))

        #TODO: Test running_under_virtual_env(). First I should learn how to Mock sys.real_prefix


if __name__ == "__main__":
    unittest.main()

