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

draft for now since it's not done yet::

    pbt help

    # list of registered commands here

    pbt help command

    # help for command here

    pbt dump

    # dump of all the information about the current project here

    pbt <command> [<arg>*]

    # result of running <command> passing args

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

license
-------

Apache

