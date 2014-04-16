"""test for check plugin"""
import sys
import unittest
sys.path.append("src")
import pbt

from unittest import mock

gctx = pbt.global_ctx
gctx.initial_setup()


class fakeflake8():

    def engine():
        def get_style_guide():
            pass


class fakeguide():

    def check_files():
        pass


class CheckTestCase(unittest.TestCase):

    def test_check_is_loaded(self):
        self.assertTrue(gctx.is_command("check"))

    def test_check_no_args(self):
        fakeguide.check_files = mock.MagicMock()
        fakeflake8.engine.get_style_guide = mock.MagicMock(return_value=fakeguide)

        with mock.patch.dict('sys.modules', {"flake8": fakeflake8}):
            gctx.run("check", [])

        fakeflake8.engine.get_style_guide.assert_called_once_with(parse_argv=False,
                                                                  config_file=True)
        fakeguide.check_files.assert_called_once_with(".")

    def test_check_a_file(self):
        fakeguide.check_files = mock.MagicMock()
        fakeflake8.engine.get_style_guide = mock.MagicMock(return_value=fakeguide)

        with mock.patch.dict('sys.modules', {"flake8": fakeflake8}):
            gctx.run("check", ["src/pbt"])

        fakeflake8.engine.get_style_guide.assert_called_once_with(parse_argv=False,
                                                                  config_file=True)
        fakeguide.check_files.assert_called_once_with(["src/pbt"])

    def test_check_two_files(self):
        fakeguide.check_files = mock.MagicMock()
        fakeflake8.engine.get_style_guide = mock.MagicMock(return_value=fakeguide)

        with mock.patch.dict('sys.modules', {"flake8": fakeflake8}):
            gctx.run("check", ["plugins/check/main.py",
                               "plugins/check/test_check.py"])
        fakeflake8.engine.get_style_guide.assert_called_once_with(parse_argv=False,
                                                                  config_file=True)
        fakeguide.check_files.assert_called_once_with(["plugins/check/main.py",
                                                       "plugins/check/test_check.py"])
