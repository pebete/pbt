"""test for new plugin"""
import unittest
import pbt
import os

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
        # TODO: auto sync the deps listed in proyects
        fakepip.main.assert_called_once_with(['install',
                                              'PyYAML>=3.10', 'pyxdg>=0.25',
                                              'flake8>=2.0',
                                              'cookiecutter>=0.7.0'])

    def test_install_requirements_custom_folder(self):
        fakepip.main = mock.MagicMock()
        fakeos.path.exists = mock.MagicMock(return_value=True)
        with mock.patch.dict('sys.modules', {"pip": fakepip}):
            with mock.patch.dict('sys.modules', {"os": fakeos}):
                gctx.run("install", ["-t", "deps"])
        fakepip.main.assert_called_once_with(['install', '-t',
                                              os.getcwd() + "/deps",
                                              'PyYAML>=3.10', 'pyxdg>=0.25',
                                              'flake8>=2.0',
                                              'cookiecutter>=0.7.0'])

    def test_install_lib_custom_folder(self):
        fakepip.main = mock.MagicMock()
        fakeos.path.exists = mock.MagicMock(return_value=True)
        with mock.patch.dict('sys.modules', {"pip": fakepip}):
            with mock.patch.dict('sys.modules', {"os": fakeos}):
                gctx.run("install", ["-t", "deps","fakelib"])
        fakepip.main.assert_called_once_with(['install', '-t',
                                              os.getcwd() + "/deps",
                                              'fakelib'])
