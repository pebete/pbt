"""pbt main API"""
import os
import yaml
import logging

import pbt_util

class PbtError(Exception):
    """pbt base exception, all pbt exceptions inherit from this one, useful
    to catch this one to catch pbt specific errors only"""

    pass

class CommandNotFoundError(PbtError):
    """error that ocurrs when trying to run a command that's not registered"""

    def __init__(self, command_name):
        PbtError.__init__(self)
        self.command_name = command_name

    def __str__(self):
        return "Command not found '{}'".format(self.command_name)

class ProjectNotFoundError(PbtError):
    """error that ocurrs when trying to load a project.pbt and it's not found"""

    def __str__(self):
        return "project.pbt file not found"

class ProjectSettings:
    """contains all the settings for a project"""
    def __init__(self, min_version, plugins, repositories, plugin_repositories,
        entry_point, python_cmd, python_opts, source_paths, test_paths,
        resource_paths, target_path, python_versions):

        self.min_version = min_version
        self.plugins = plugins
        self.repositories = repositories
        self.plugin_repositories = plugin_repositories
        self.entry_point = entry_point
        self.python_cmd = python_cmd
        self.python_opts = python_opts
        self.source_paths = norm_paths(source_paths)
        self.test_paths = norm_paths(test_paths)
        self.resource_paths = norm_paths(resource_paths)
        self.target_path = os.path.normpath(target_path)
        self.python_versions = python_versions

class Project:
    """contains information about the project"""
    def __init__(self, organization, name, version, description, url, license,
            authors, dependencies):

        self.organization = organization
        self.name = name
        self.version = version
        self.description = description
        self.url = url
        self.license = license
        self.authors = authors
        self.dependencies = dependencies

def norm_paths(paths):
    return [os.path.normpath(path) for path in paths]

class Context:
    """contains all the information to run pbt commands"""

    def __init__(self, log=None):
        self.commands = {}
        self.log = log if log is not None else logging.getLogger()
        self.project_descriptor_name = "project.pbt"

    def parse_project_descriptor(self, path):
        """parse a project descriptor from path and return it"""

        with open(path) as file_in:
            data = yaml.load(file_in)

        organization = data.get("organization", "no-organization")
        name = data.get("name", "no-name")
        version = data.get("version", "no-version")
        description = data.get("description", "No description")
        url = data.get("url", "No url")
        license = data.get("license", "No license")
        authors = data.get("authors", [])
        dependencies = data.get("dependencies", [])

        project = Project(organization, name, version, description, url,
                license, authors, dependencies)

        min_version = data.get("min_version", "0.0.1")
        plugins = data.get("plugins", [])
        repositories = data.get("repositories", [])
        plugin_repositories = data.get("plugin_repositories", [])
        entry_point = data.get("entry_point", ["src/main.py", "main"])
        python_cmd = data.get("python_cmd", "python3")
        python_opts = data.get("python_opts", [])
        source_paths = data.get("source_paths", ["src/"])
        test_paths = data.get("test_paths", ["test/"])
        resource_paths = data.get("resource_paths", ["resources/"])
        target_path = data.get("target_path", "target/")
        python_versions = data.get("python_versions", [])

        settings = ProjectSettings(min_version, plugins, repositories,
                plugin_repositories, entry_point, python_cmd, python_opts,
                source_paths, test_paths, resource_paths, target_path,
                python_versions)

        return project, settings

    def load_project(self, basepath="."):
        """loads the project description and related information from
        project.pbt, raise ProjectNotFoundError if no project.pbt is found"""
        # TODO: implement
        for dirname in pbt_util.get_dirs_up_to_root(basepath):
            project_path = os.path.join(dirname, self.project_descriptor_name)
            self.log.debug("Looking for '{}'".format(project_path))

            if os.path.isfile(project_path):
                return self.parse_project_descriptor(project_path)

        raise ProjectNotFoundError()

    def is_command(self, command_name):
        """returns True if command is registered, False otherwise"""
        return command_name in self.commands

    def run(self, command_name, args):
        """look for a registered command named *command* call it with *args*
        if found, raise *CommandNotFoundError* if not found"""
        if self.is_command(command_name):
            command_handler, runs_in_project = self.commands[command_name]
            if runs_in_project:
                project = self.load_project()
                return command_handler(self, args, project)
            else:
                return command_handler(self, args)
        else:
            raise CommandNotFoundError(command_name)

    def get_command_handler(self, command_name):
        if self.is_command(command_name):
            command_handler = self.commands[command_name][0]
            return command_handler
        else:
            raise CommandNotFoundError(command_name)

    def register_command(self, name, command_handler, runs_in_project):
        """register a function to be called when command named *name* is
        called"""
        if self.is_command(name):
            self.log.warning("Overriding command named {}, old {}, new {}"
                    .format(name, self.get_command_handler(name),
                        command_handler))

        self.commands[name] = (command_handler, runs_in_project)

    def command(self, runs_in_project=True, name=None):
        """decorator to declare a function that is a pbt command
        runs_in_project: if True context will look for a project.pbt, load it
        and pass it to the command and fail if not in a project. If False
        it won't try to load a project for the command
        
        name: command name, if not set it will use the name of the function"""

        def outter(command_handler):
            """function that is the actual decorator"""
            if name is None:
                command_name = command_handler.__name__
            else:
                command_name = name

            self.register_command(command_name, command_handler,
                    runs_in_project)

            return command_handler

        return outter


global_ctx = Context()

def run(command_name, args):
    """convenience function to run a command on the global context"""
    global_ctx.run(command_name, args)

def command(runs_in_project=True, name=None):
    """convenience function to wrap a command on the global context"""
    return global_ctx.command(runs_in_project, name)

