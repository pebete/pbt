"""test for new plugin"""
import unittest
import pbt

from unittest import mock

from io import StringIO

gctx = pbt.global_ctx
gctx.initial_setup()


class fakepip(object):
    def main():
        pass


class fakeos(object):
    def path():
        def exists():
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
        fakepip.main = mock.MagicMock()
        fakeos.path.exists = mock.MagicMock(return_value=True)
        with mock.patch.dict('sys.modules', {"pip": fakepip}):
            with mock.patch.dict('sys.modules', {"os": fakeos}):
                gctx.run("install", [])
        fakepip.main.assert_called_once_with(["install", "-r",
                                              "requirements.txt"])

    def test_install_no_requirements(self):
        fakepip.main = mock.MagicMock()
        fakeos.path.exists = mock.MagicMock(return_value=False)
        with mock.patch.dict('sys.modules', {"pip": fakepip}):
            with mock.patch.dict('sys.modules', {"os": fakeos}):
                gctx.run("install", [])
        # Check that fake pip never get called
        self.assertEquals(fakepip.main.call_args_list, [])
