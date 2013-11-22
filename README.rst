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
        print args

the code above will register a *project* command that when run with "pbt echo"
will display the args (in this case the empty list)

the name of the command is taken from the name of the function if not provided,
you can provide the name explicitly like this::

    @pbt.command(name="echo")
    def echo_command(ctx, args, project):
        """prints the arguments to standard output"""
        print args

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

dependencies
------------

yes, this will be later in the project.yaml

* cookicutter
* xdg

license
-------

Apache

