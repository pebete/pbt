pbt
===

python build tool

what?
-----

this tool plans to bring all the development tools from python into a single,
comprehensive and coherent set of commands that will provide a default setup
and workflow to make it easy to start, build, test, package and publish a
python project.

all commands will be plugins, you can add and/or implement yours to suit your
needs.

pbt will provide the default setup and workflow with sensible defaults, but the
idea is that you can tweak every aspect if you need it.

how?
----

::

    # list of registered command

    pbt help

    # help for dump command

    pbt help dump

    # dump of all the information about the current project

    pbt dump

    # run <command> passing args

    pbt <command> [<arg>*]

examples
--------

::

    $ pwd

    /home/mariano/src/pbt/test/data

    $ ../../src/pbt help

    Pbt is a tool for working with Python projects.

    Several tasks are available:

    dump             dumps all project configuration for the current project
    help             show commands' descriptions or command help if command specified

    $ ../../src/pbt help help

    show commands' descriptions or command help if command specified

        pbt help         - displays all available commands with a brief description
        pbt help command - displays detailed help about a command

    $ ../../src/pbt help dump

    dumps all project configuration for the current project

        This commands prints back all the information about the project
        that it knows, it serves as a tool to diagnose configuration problems
        and also as an example for a minimal project command

    $ ../../src/pbt dump

    authors: [Mariano Guerra <mariano@marianoguerra>, x-ip, joac, L1pe]
    dependencies:
    - [org.python, requests, 2.0.0]
    description: python build tool
    license: {name: Apache 2.0, url: 'http://opensource.org/licenses/Apache-2.0'}
    name: pbt
    organization: pebete
    settings:
      entry_point: [src/pbt_cli.py, run]
      min_version: 0.0.1
      plugin_repositories:
      - [pypi, 'http:/pypi.python.org/']
      plugins:
      - [marianoguerra, sphinx, 1.0.0]
      python_cmd: ~/bin/pypy
      python_opts: [-tt]
      python_versions:
      - '2.6'
      - '2.7'
      - '3.3'
      - '3.4'
      - [pypy, '2.1']
      repositories:
      - [pypi, 'http:/pypi.python.org/']
      resource_paths: [resources]
      source_paths: [src]
      target_path: target
      test_paths: [test]
    url: https://github.com/pebete/pbt
    version: 0.0.1

how to implement commands?
--------------------------

just decorate your command with the @command decorator to register it as a command::

    @pbt.command()
    def echo(ctx, args, project):
        """prints the arguments to standard output"""
        print(args)

the code above will register a *project* command that when run with "pbt echo"
will display the args (in this case the empty list)

the name of the command is taken from the name of the function if not provided,
you can provide the name explicitly like this::

    @pbt.command(name="echo")
    def echo_command(ctx, args, project):
        """prints the arguments to standard output"""
        print(args)

you can also register global commands, this are commands that don't require
to be in a project to run (for example the help command), for that you need to
specify the runs_in_project option and set it to false::

    @pbt.command(runs_in_project=False, name="help")
    def help_command(ctx, args):
        """lists registered commands and their description"""
        # do stuff here

global commands don't receive the project argument.

the docstring from a command is used for two functions, the first line (which
should be shorted than 72 chars for readability) is the short description of
the command that will be displayed alongside the command name when running "pbt
help".

the following lines if provided are the command help that will be displayed when
requiring the detailed help when running "pbt help command".

plugins
-------

plugins are folders with a standard structure that are loaded when pbt loads
and can be used to provide commands.

plugin search path
::::::::::::::::::

plugins are searched in order starting from `$XDG_CONFIG_DIR <http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>`_/pbt/plugins and if $PBT_PLUGINS_PATH is
set as an environment variable (a colon separated list of directory paths to
look) they will be searched after the default plugins folder.

for example, to test your plugins during development you can run the following
command (or put it in your bash/zsh/whatever rc file)::

    export PBT_PLUGINS_PATH=path1:path2:$HOME/my-pbt-plugin-dir

relative paths are converted to absolute using the current working directory
whent pbt is run, prefer absolute paths to avoid weird problems.

plugin dir structure
::::::::::::::::::::

a plugin for now is simply a folder with a main.py file inside, main.py will be
loaded at pbt load time if found, so you can do any initialization at top level
(try to avoid doing expensive work at load time to avoid slowing down pbt load
time).

you can use pbt.command decorator to register commands as explained before.

you can also use pbt.run_on_load decorator to register a function that will be
called after all plugins are loaded and will receive two parameters, first
the pbt context object and second the path to the directory where the plugin
lives, an example of a main.py file for a helloworld plugin would be::

    import pbt

    print("Hello world from plugin at load time")

    @pbt.run_on_load
    def my_on_load(ctx, my_path):
        print("on_load, hello world", my_path, ctx)

    @pbt.command(runs_in_project=False)
    def hello(ctx, args):
        """prints hello world"""
        print("hello world!")

this plugin will print "Hello world from plugin at load time" when pbt loads
it, for example when you run pbt::

    $ pbt help

    Hello world from plugin at load time
    on_load, hello world /home/mariano/.config/pbt/plugins/helloworld/main.py <pbt.Context object at 0x7f8cecf7d890>
    Pbt is a tool for working with Python projects.

    Several tasks are available:

    dump             dumps all project configuration for the current project
    hello            prints hello world
    help             show commands' descriptions or command help if command specified
    new

then it prints "on_load, hello world" and the path to the plugin

as you can see the plugin registered a command which is listed, let's run it::

    $ pbt hello
    Hello world from plugin at load time
    on_load, hello world /home/mariano/.config/pbt/plugins/helloworld/main.py <pbt.Context object at 0x7fa1aac85890>
    hello world!

and that's almost all there's to writing a plugin

testing
-------

to run pbt core tests run from pbt base folder::

    python3 -m unittest discover -s test

testing your plugin
:::::::::::::::::::

first make sure the folder where your plugin is is in the plugin loading path
(see plugin search path section in this document), after that run::

    python3 -m unittest discover -s path-to-your-plugin

for example to test the hello world command run::

    python3 -m unittest discover -s plugins/helloworld

dependencies
------------

yes, this will be later in the project.pbt

* yaml
* cookicutter
* xdg

license
-------

Apache

