"""test for new plugin"""
import sys
import unittest
sys.path.append("src")
import pbt

from unittest import mock

from io import StringIO

gctx = pbt.global_ctx
gctx.initial_setup()

class fakepip(object):
    def main():
        pass

class InstallTestCase(unittest.TestCase):

    def test_install_is_loaded(self):
        self.assertTrue(gctx.is_command("install"))

    def test_install_pip_is_not_available(self):
        with mock.patch.dict('sys.modules', {"pip": None}):
            with mock.patch('sys.stdout', StringIO()) as out:
                try:
                   gctx.run("install", [])
                except SystemExit:
                    # The plugin must raise a SystemExit
                    self.assertTrue(True)

                output = out.getvalue().strip()
        self.assertIn("http://www.pip-installer.org/en/latest/installing.html",
                      output)

    def test_install_module(self):
        fakepip.main = mock.MagicMock()
        with mock.patch.dict('sys.modules', {"pip": fakepip}):
            gctx.run("install", ["fakelib"])
        fakepip.main.assert_called_once_with(["install", "fakelib"])

    def test_install_requirements(self):
        # This test counts on a requirements.txt file available in the path
        # in order to make a more deterministic test we should patch
        # the open and close function and that is not an easy task
        fakepip.main = mock.MagicMock()
        with mock.patch.dict('sys.modules', {"pip": fakepip}):
            gctx.run("install", [])
        fakepip.main.assert_called_once_with(["install", "-r",
                                              "requirements.txt"])
