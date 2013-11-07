"""test for pbt.py"""
import sys
sys.path.append("src")
from pbt import *
import unittest

TESTS_DIR = os.path.dirname(__file__)
TEST_DATA_DIR = os.path.abspath(os.path.join(TESTS_DIR, "data"))

class FakeLogger():
    """if it walks like a logger, it quaks like a logger..."""

    def __init__(self):
        self.warns = []
        self.debugs = []

    def warning(self, msg):
        """logging.warning fake"""
        self.warns.append(msg)

    def debug(self, msg):
        """logging.debug fake"""
        self.debugs.append(msg)

@command(runs_in_project=False)
def reverse(ctx, args):
    """command that takes some args and returns them reversed"""
    return list(reversed(args))

@command(runs_in_project=False, name="reverse1")
def reverse_with_name(ctx, args):
    """command that takes some args and returns them reversed"""
    return list(reversed(args))

@command(name="identity")
def identity_command(ctx, args, project):
    "return the args that are received"
    return ctx, args, project

class PbtTestCase(unittest.TestCase):

    def test_command_not_found_error_str(self):
        try:
            raise CommandNotFoundError("echo")
        except CommandNotFoundError as error:
            self.assertEqual(str(error), "Command not found 'echo'")

    def test_register_command_decorator(self):
        ctx = global_ctx
        self.assertFalse(ctx.is_command("somecommand"))
        self.assertTrue(ctx.is_command("reverse"))
        self.assertTrue(ctx.is_command("reverse1"))

        self.assertIs(ctx.get_command_handler("reverse"), reverse)
        self.assertIs(ctx.get_command_handler("reverse1"), reverse_with_name)

    def test_overriding_command_warns(self):
        log = FakeLogger()
        ctx = Context(log=log)
        @ctx.command(runs_in_project=False)
        def dummy_command(ctx_, args):
            """dummy command"""
            return args

        @ctx.command(runs_in_project=False, name="dummy_command")
        def dummy_command_1(ctx_, args):
            """dummy command 1"""
            return args

        self.assertEqual(len(log.warns), 1)
        self.assertEqual(log.warns[0],
                "Overriding command named {}, old {}, new {}".format(
                    "dummy_command", dummy_command, dummy_command_1))

    def test_run_global_command(self):
        ctx = global_ctx
        result = ctx.run("reverse", [1, 2])
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], 2)
        self.assertEqual(result[1], 1)

    def test_run_project_command(self):
        ctx = global_ctx
        path = os.path.join(TEST_DATA_DIR, ctx.project_descriptor_name)
        cx, args, project = ctx.run("identity", [1, 2], path)
        settings = project.settings

        self.assertEqual(args, [1, 2])
        self.assertIs(ctx, cx)

        self.assertEqual(project.organization, "pebete")
        self.assertEqual(project.name, "pbt")
        self.assertEqual(project.version, "0.0.1")
        self.assertEqual(project.description, "python build tool")
        self.assertEqual(project.url, "https://github.com/pebete/pbt")
        self.assertEqual(project.license,
                {"name": "Apache 2.0",
                 "url": "http://opensource.org/licenses/Apache-2.0"})
        self.assertEqual(project.authors,
                ["Mariano Guerra <mariano@marianoguerra>", "x-ip", "joac",
                    "L1pe"])
        self.assertEqual(project.dependencies,
                [["org.python", "requests", "2.0.0"]])

        self.assertEqual(settings.min_version, "0.0.1")
        self.assertEqual(settings.plugins,
                [["marianoguerra", "sphinx", "1.0.0"]])
        self.assertEqual(settings.repositories,
                [["pypi", "http:/pypi.python.org/"]])
        self.assertEqual(settings.plugin_repositories,
                [["pypi", "http:/pypi.python.org/"]])
        self.assertEqual(settings.entry_point, ["src/pbt_cli.py", "run"])
        self.assertEqual(settings.python_cmd, "~/bin/pypy")
        self.assertEqual(settings.python_opts, ["-tt"])
        self.assertEqual(settings.source_paths, ["src"])
        self.assertEqual(settings.test_paths, ["test"])
        self.assertEqual(settings.resource_paths, ["resources"])
        self.assertEqual(settings.target_path, "target")
        self.assertEqual(settings.python_versions,
                ["2.6", "2.7", "3.3", "3.4", ["pypy", "2.1"]])


    def test_load_project_fails_when_not_found(self):
        log = FakeLogger()
        ctx = Context(log=log)

        try:
            ctx.load_project("/foo/bar/")
            self.fail("this should raise an exception ProjectNotFoundError")
        except ProjectNotFoundError:
            pass

        self.assertEqual(log.debugs, ["Looking for '/foo/bar/project.pbt'",
            "Looking for '/foo/project.pbt'", "Looking for '/project.pbt'"]) 

    def test_load_null_project(self):
        log = FakeLogger()
        ctx = Context(log=log)
        path = os.path.join(TEST_DATA_DIR, "null_project",
                ctx.project_descriptor_name)
        project = ctx.parse_project_descriptor(path)
        settings = project.settings
        
        self.assertEqual(project.organization, "no-organization")
        self.assertEqual(project.name, "no-name")
        self.assertEqual(project.version, "no-version")
        self.assertEqual(project.description, "No description")
        self.assertEqual(project.url, "No url")
        self.assertEqual(project.license, "No license")
        self.assertEqual(project.authors, [])
        self.assertEqual(project.dependencies, [])

        self.assertEqual(settings.min_version, "0.0.1")
        self.assertEqual(settings.plugins, [])
        self.assertEqual(settings.repositories, [])
        self.assertEqual(settings.plugin_repositories, [])
        self.assertEqual(settings.entry_point, ["src/main.py", "main"])
        self.assertEqual(settings.python_cmd, "python3")
        self.assertEqual(settings.python_opts, [])
        self.assertEqual(settings.source_paths, ["src"])
        self.assertEqual(settings.test_paths, ["test"])
        self.assertEqual(settings.resource_paths, ["resources"])
        self.assertEqual(settings.target_path, "target")
        self.assertEqual(settings.python_versions, [])

    def test_load_project(self):
        log = FakeLogger()
        ctx = Context(log=log)
        path = os.path.join(TEST_DATA_DIR, ctx.project_descriptor_name)
        project = ctx.parse_project_descriptor(path)
        settings = project.settings
        
        self.assertEqual(project.organization, "pebete")
        self.assertEqual(project.name, "pbt")
        self.assertEqual(project.version, "0.0.1")
        self.assertEqual(project.description, "python build tool")
        self.assertEqual(project.url, "https://github.com/pebete/pbt")
        self.assertEqual(project.license,
                {"name": "Apache 2.0",
                 "url": "http://opensource.org/licenses/Apache-2.0"})
        self.assertEqual(project.authors,
                ["Mariano Guerra <mariano@marianoguerra>", "x-ip", "joac",
                    "L1pe"])
        self.assertEqual(project.dependencies,
                [["org.python", "requests", "2.0.0"]])

        self.assertEqual(settings.min_version, "0.0.1")
        self.assertEqual(settings.plugins,
                [["marianoguerra", "sphinx", "1.0.0"]])
        self.assertEqual(settings.repositories,
                [["pypi", "http:/pypi.python.org/"]])
        self.assertEqual(settings.plugin_repositories,
                [["pypi", "http:/pypi.python.org/"]])
        self.assertEqual(settings.entry_point, ["src/pbt_cli.py", "run"])
        self.assertEqual(settings.python_cmd, "~/bin/pypy")
        self.assertEqual(settings.python_opts, ["-tt"])
        self.assertEqual(settings.source_paths, ["src"])
        self.assertEqual(settings.test_paths, ["test"])
        self.assertEqual(settings.resource_paths, ["resources"])
        self.assertEqual(settings.target_path, "target")
        self.assertEqual(settings.python_versions,
                ["2.6", "2.7", "3.3", "3.4", ["pypy", "2.1"]])

if __name__ == "__main__":
    unittest.main()
