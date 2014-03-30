"""test for pbt.py"""
import os
import sys
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

@command(runs_in_project=False, name="no-help")
def no_help(ctx, args):
    pass

@command(runs_in_project=False, name="just-description")
def just_description(ctx, args):
    """this command has just a description"""
    pass

@command(runs_in_project=False, name="full-docs")
def full_docs(ctx, args):
    """this command not only has just a description

    but also some extended documentation
    and this is the last line"""
    pass

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

    def test_build_plugin_file_path(self):
        ctx = Context()
        path = ctx.path_to_plugin_file("new", "templates.json")
        #expected a path, but only check the last folders
        self.assertTrue("plugins/new/templates.json" in path)

    def test_build_url_plugin_file_path(self):
        ctx = Context()
        url = ctx.url_to_plugin_file("new", "templates.json")
        expected = os.path.expanduser(ctx.registry_url + "new/templates.json")
        self.assertEqual(url, expected)

    def test_build_url_plugin_file_path(self):
        ctx = Context()
        url = ctx.url_to_plugin_file("new", "templates.json")
        expected = os.path.expanduser(ctx.registry_url + "new/templates.json")
        self.assertEqual(url, expected)

    def test_fetch_plugin_file(self):
        ctx = Context()
        resulting_dirname = []
        resulting_url = []
        resulting_path = []

        def dummy_ensure_dir_exists(dirname):
            resulting_dirname.append(dirname)

        def dummy_fetch_resource(url, path):
            resulting_url.append(url)
            resulting_path.append(path)

        ctx.ensure_dir_exists = dummy_ensure_dir_exists
        ctx.fetch_resource = dummy_fetch_resource
        expected_path = ctx.path_to_plugin_file("new", "templates.json")
        expected_url = ctx.url_to_plugin_file("new", "templates.json")

        url, path = ctx.fetch_plugin_file("new", "templates.json")

        self.assertEqual(path, expected_path)
        self.assertEqual(url, expected_url)

        self.assertEqual(resulting_url[0], expected_url)
        self.assertEqual(resulting_path[0], expected_path)
        self.assertEqual(resulting_dirname[0], os.path.dirname(expected_path))

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
        self.assertEqual(settings.packages, ["null"])
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
        self.assertEqual(settings.entry_point, ["no-name/main.py", "main"])
        self.assertEqual(settings.python_cmd, "python3")
        self.assertEqual(settings.python_opts, [])
        self.assertEqual(settings.packages, ["no-name"])
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
        self.assertEqual(settings.packages, ["null"])
        self.assertEqual(settings.test_paths, ["test"])
        self.assertEqual(settings.resource_paths, ["resources"])
        self.assertEqual(settings.target_path, "target")
        self.assertEqual(settings.python_versions,
                ["2.6", "2.7", "3.3", "3.4", ["pypy", "2.1"]])

    def test_get_command_description_no_help(self):
        description = global_ctx.get_command_description("no-help")
        self.assertEqual(description, "No description")

        docs = global_ctx.get_command_docs("no-help")
        self.assertEqual(docs, "No description")

    def test_get_command_description_just_description(self):
        description = global_ctx.get_command_description("just-description")
        self.assertEqual(description, "this command has just a description")

        docs = global_ctx.get_command_docs("just-description")
        self.assertEqual(docs, "this command has just a description")

    def test_get_command_description_full_docs(self):
        description = global_ctx.get_command_description("full-docs")
        self.assertEqual(description,
                "this command not only has just a description")

        docs = global_ctx.get_command_docs("full-docs")
        self.assertEqual(docs, full_docs.__doc__)

    def test_get_command_description_fails_if_not_found(self):
        self.assertRaises(CommandNotFoundError,
                global_ctx.get_command_description, "not-existing")

        self.assertRaises(CommandNotFoundError,
                global_ctx.get_command_docs, "not-existing")

    def test_plugins_dir_paths_works_without_env_plugin_path(self):
        ctx = Context(env={})
        self.assertEqual(ctx.plugins_dir_paths, [ctx.join_config("plugins")])

    def test_plugins_dir_paths_works_with_empty_env_plugin_path(self):
        ctx = Context(env={"PBT_PLUGINS_PATH": ""})
        self.assertEqual(ctx.plugins_dir_paths, [ctx.join_config("plugins")])

    def test_plugins_dir_paths_works_with_one_env_plugin_path(self):
        ctx = Context(env={"PBT_PLUGINS_PATH": "foo"})
        self.assertEqual(ctx.plugins_dir_paths, [ctx.join_config("plugins"),
            os.path.abspath("foo")])

    def test_plugins_dir_paths_works_with_one_env_plugin_path_with_spaces(self):
        ctx = Context(env={"PBT_PLUGINS_PATH": "foo  "})
        self.assertEqual(ctx.plugins_dir_paths, [ctx.join_config("plugins"),
            os.path.abspath("foo")])

    def test_plugins_dir_paths_works_with_one_env_plugin_path_with_extra_colon(self):
        ctx = Context(env={"PBT_PLUGINS_PATH": "foo:"})
        self.assertEqual(ctx.plugins_dir_paths, [ctx.join_config("plugins"),
            os.path.abspath("foo")])

    def test_plugins_dir_paths_works_with_one_env_plugin_path_with_extra_garbage(self):
        ctx = Context(env={"PBT_PLUGINS_PATH": ":::::foo:::::   :"})
        self.assertEqual(ctx.plugins_dir_paths, [ctx.join_config("plugins"),
            os.path.abspath("foo")])

    def test_plugins_dir_paths_works_with_multiple_env_plugin_paths_with_extra_garbage(self):
        ctx = Context(env={"PBT_PLUGINS_PATH": ":::::foo::::bar: baz  :"})
        self.assertEqual(ctx.plugins_dir_paths, [ctx.join_config("plugins"),
            os.path.abspath("foo"), os.path.abspath("bar"),
            os.path.abspath("baz")])

    def test_on_load_decorator_works(self):
        ctx = Context(env={})
        params = []

        @ctx.run_on_load
        def my_on_load(ctx, path):
            params.append((ctx, path))

        self.assertEqual(ctx.on_load_functions, [my_on_load])

        ctx.run_on_load_functions()
        self.assertEqual(params, [(ctx, os.path.abspath(__file__))])



if __name__ == "__main__":
    unittest.main()
