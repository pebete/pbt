How to contribute to PBT
========================


Setup
-----

The best way of contributing to pbt is setting up a fork of your own in github, this guide asumes that you already forked pbt.

you are gonna need pip3 and git installed.

First we clone the repo::
    
    $ git clone git@github.com:<yourusername>/pbt.git
    $ cd pbt
    
Then we install the dependencies::

    $ pip3 install -r requirements.txt # sudo, --prefix or nothing if your are inside a virtualenv

Now you can use pbt using pbt.sh as a proxy::
    
    $ ./pbt.sh help

usage
-----

::

    # list of registered command

    ./pbt.sh help

    # help for dump command

    ./pbt.sh help dump

    # dump of all the information about the current project

    ./pbt.sh dump

    # run <command> passing args

    ./pbt.sh <command> [<arg>*]


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

testing your plugin
:::::::::::::::::::

first make sure the folder where your plugin is is in the plugin loading path
(see plugin search path section in this document), after that run::

    python3 -m unittest discover -s path-to-your-plugin

for example to test the hello world command run::

    python3 -m unittest discover -s plugins/helloworld

