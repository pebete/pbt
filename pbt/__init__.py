"""pbt main API"""
import os
import imp
import yaml
import urllib
import logging
import xdg.BaseDirectory

from pbt import pbt_util

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
    """error that ocurrs when trying to load a project.pbt and it's not
    found"""

    def __str__(self):
        return "project.pbt file not found"

class ProjectSettings:
    """contains all the settings for a project"""
    def __init__(self, min_version, plugins, repositories, plugin_repositories,
        entry_point, python_cmd, python_opts, packages, scripts, test_paths,
        resource_paths, target_path, python_versions):

        self.min_version = min_version
        self.plugins = plugins
        self.repositories = repositories
        self.plugin_repositories = plugin_repositories
        self.entry_point = entry_point
        self.python_cmd = python_cmd
        self.python_opts = python_opts
        self.packages = norm_paths(packages)
        self.scripts = norm_paths(scripts)
        self.test_paths = norm_paths(test_paths)
        self.resource_paths = norm_paths(resource_paths)
        self.target_path = os.path.normpath(target_path)
        self.python_versions = python_versions

    def to_data(self):
        """return a data representation of the object"""
        return dict(min_version=self.min_version, plugins=self.plugins,
                repositories=self.repositories,
                plugin_repositories=self.plugin_repositories,
                entry_point=self.entry_point, python_cmd=self.python_cmd,
                python_opts=self.python_opts, source_paths=self.source_paths,
                test_paths=self.test_paths,
                resource_paths=self.resource_paths,
                target_path=self.target_path,
                python_versions=self.python_versions)

class Project:
    """contains information about the project"""
    def __init__(self, organization, name, version, description, url, license,
            authors, dependencies, settings):

        self.organization = organization
        self.name = name
        self.version = version
        self.description = description
        self.url = url
        self.license = license
        self.authors = authors
        self.dependencies = dependencies
        self.settings = settings

    def to_data(self):
        """return a data representation of the object"""
        return dict(organization=self.organization, name=self.name,
                version=self.version, description=self.description,
                url=self.url, license=self.license, authors=self.authors,
                dependencies=self.dependencies,
                settings=self.settings.to_data())

def norm_paths(paths):
    return [os.path.normpath(path) for path in paths]

DEFAULT_REGISTRY_URL = "https://raw.github.com/pebete/registry/master/plugins/"
logging.basicConfig()
class Context:
    """contains all the information to run pbt commands"""

    def __init__(self, log=None, env=None):
        self.env = env if env is not None else os.environ
        self.commands = {}
        self.on_load_functions = []
        self.log = log if log is not None else logging.getLogger("pbt")
        self.registry_url = self.env.get("PBT_REGISTRY_URL",
                DEFAULT_REGISTRY_URL)

        if log is None:
            log_file = self.env.get("PBT_LOG_FILE")
            if log_file:
                self.log.addHandler(logging.FileHandler(log_file))
            else:
                self.log.addHandler(logging.StreamHandler())

            if self.env.get("PBT_DEBUG"):
                self.log.setLevel(logging.DEBUG)
            else:
                self.log.setLevel(logging.INFO)

        self.project_descriptor_name = "project.pbt"
        self._config_dir_path = None

    @property
    def config_dir_path(self):
        """return the config_dir_path for this context, ensure it exists
        and initialize it the first time it's required"""
        if self._config_dir_path is None:
            xdg.BaseDirectory.save_config_path("pbt")
            path = xdg.BaseDirectory.load_first_config("pbt")
            self._config_dir_path = path

        return self._config_dir_path

    def path_to_plugin_file(self, plugin_name, *path):
        """return the path to a resource from a plugin"""
        # If the resource is in the default config path return it
        resource = os.path.join(self.config_dir_path, "plugins",
                                  plugin_name, *path)
        if os.path.exists(resource):
            return resource

        #if the resource doesn't exists look into the environment paths
        plugins_dir_paths =  self.plugins_dir_paths

        for plugins_dir_path in plugins_dir_paths:
            if os.path.isdir(plugins_dir_path):
                fullpath = os.path.join(plugins_dir_path, plugin_name, *path)
                if os.path.exists(fullpath):
                    resource = fullpath
        return resource

    def url_to_plugin_file(self, plugin_name, *path):
        """return the url to a resource from   plugin"""
        return self.registry_url + plugin_name + "/" + "/".join(path)

    def fetch_resource(self, url, path):
        """fetch a resource from a url and store it in path"""
        urllib.urlretrieve(url, path)

    def ensure_dir_for_file_exists(self, path):
        """ensure directory for file exists, if not create it"""
        dirname = os.path.dirname(path)
        self.ensure_dir_exists(dirname)

    def ensure_dir_exists(self, dirname):
        """ensure directory exists, if not create it"""
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def fetch_plugin_file(self, plugin_name, *path):
        """fetch a resource from a plugin from the registry and store it
        in the local path for that resource"""
        url = self.url_to_plugin_file(plugin_name, *path)
        path = self.path_to_plugin_file(plugin_name, *path)
        self.ensure_dir_for_file_exists(path)
        self.fetch_resource(url, path)
        return url, path

    @property
    def plugins_dir_paths(self):
        """return the list of places to look for plugins"""

        paths = self.env.get("PBT_PLUGINS_PATH", "")
        result = [os.path.abspath(path.strip()) for path in paths.split(":") if path.strip()]

        result.insert(0, self.join_config("plugins"))

        return result

    def load_plugins(self):
        """load plugins and return loaded modules and errors"""
        plugins_dir_paths =  self.plugins_dir_paths

        self.log.debug("looking for plugins in %s", ":".join(plugins_dir_paths))
        errors = []
        modules = []
        for plugins_dir_path in plugins_dir_paths:
            if os.path.isdir(plugins_dir_path):
                _dirpath, dirnames, _filenames = next(os.walk(plugins_dir_path))
                for dirname in dirnames:
                    mod_name = os.path.basename(dirname)
                    plugin_dir = os.path.join(plugins_dir_path, dirname)
                    entry_point = os.path.join(plugin_dir, "main.py")
                    try:
                        plugin = imp.load_source(mod_name, entry_point)
                        modules.append(plugin)
                    except Exception as error:
                        errors.append(error)

        return modules, errors

    def join_config(self, *parts):
        """join parts with the config dir path as base"""
        return os.path.join(self.config_dir_path, *parts)

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

        min_version = data.get("min_version", "0.0.1")
        plugins = data.get("plugins", [])
        repositories = data.get("repositories", [])
        plugin_repositories = data.get("plugin_repositories", [])
        python_cmd = data.get("python_cmd", "python3")
        python_opts = data.get("python_opts", [])
        packages = data.get("packages", [name])
        entry_point = data.get("entry_point", ["%s/main.py" % packages[0],
                                               "main"])
        scripts = data.get("scripts", [])
        test_paths = data.get("test_paths", ["test/"])
        resource_paths = data.get("resource_paths", ["resources/"])
        target_path = data.get("target_path", "target/")
        python_versions = data.get("python_versions", [])

        settings = ProjectSettings(min_version, plugins, repositories,
                plugin_repositories, entry_point, python_cmd, python_opts,
                packages, scripts, test_paths, resource_paths, target_path,
                python_versions)

        project = Project(organization, name, version, description, url,
                license, authors, dependencies, settings)

        return project

    def load_project(self, basepath="."):
        """loads the project description and related information from
        project.pbt, raise ProjectNotFoundError if no project.pbt is found"""
        for dirname in pbt_util.get_dirs_up_to_root(basepath):
            project_path = os.path.join(dirname, self.project_descriptor_name)
            self.log.debug("Looking for '{}'".format(project_path))

            if os.path.isfile(project_path):
                return self.parse_project_descriptor(project_path)

        raise ProjectNotFoundError()

    def is_command(self, command_name):
        """returns True if command is registered, False otherwise"""
        return command_name in self.commands

    def run_on_load_functions(self):
        for function in self.on_load_functions:
            self.log.debug("Running on load function: %s", function)
            function_dir_path = os.path.abspath(function.__code__.co_filename)
            function(self, function_dir_path)

    def initial_setup(self):
        """do initial setup, useful to run when testing a plugin or before
        running a command"""
        self.log.debug("Loading plugins")
        plugins_loaded, errors = self.load_plugins()
        self.log.debug("Running on load functions")
        self.run_on_load_functions()

        if errors:
            for error in errors:
                self.log.warning("Error loading plugin %s" % str(error))

        for plugin_path in plugins_loaded:
            self.log.debug("Plugin loaded %s" % plugin_path)


    def run(self, command_name, args, basepath="."):
        """look for a registered command named *command* call it with *args*
        if found, raise *CommandNotFoundError* if not found"""
        self.initial_setup()

        if self.is_command(command_name):
            command_handler, runs_in_project = self.commands[command_name]
            if runs_in_project:
                project = self.load_project(basepath)
                return command_handler(self, args, project)
            else:
                return command_handler(self, args)
        else:
            raise CommandNotFoundError(command_name)

    def get_command_handler(self, command_name):
        """return the handler associated with a command name, raise
        CommandNotFoundError if not found"""
        if self.is_command(command_name):
            command_handler = self.commands[command_name][0]
            return command_handler
        else:
            raise CommandNotFoundError(command_name)

    def get_command_names(self):
        """return an iter of all the registered commands"""
        return sorted(self.commands.keys())

    def get_command_description(self, command_name):
        """return the first line of the command docstring if found, if not
        found raise CommandNotFoundError"""
        if self.is_command(command_name):
            handler = self.get_command_handler(command_name)
            doc = handler.__doc__
            if doc is None:
                return "No description"
            else:
                return doc.split("\n")[0].strip()
        else:
            raise CommandNotFoundError(command_name)

    def get_command_docs(self, command_name):
        """return the command's docstring if found, if not
        found raise CommandNotFoundError"""
        if self.is_command(command_name):
            handler = self.get_command_handler(command_name)
            doc = handler.__doc__
            if doc is None:
                return "No description"
            else:
                return doc.strip()
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

    def run_on_load(self, function):
        """decorator to declare a function that should be run at pbt load
        time right after all plugins have been loaded"""

        self.on_load_functions.append(function)

        return function

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
    try:
        global_ctx.run(command_name, args)
    except CommandNotFoundError as e:
        print(e)

def command(runs_in_project=True, name=None):
    """convenience function to wrap a command on the global context"""
    return global_ctx.command(runs_in_project, name)

def run_on_load(function):
    """convenience function to wrap a on load function on the global context"""
    return global_ctx.run_on_load(function)
