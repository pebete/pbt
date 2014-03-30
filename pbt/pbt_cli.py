"""CLI entry point"""
import pbt
from pbt import pbt_core_commands

USAGE = """Usage: {command} <command> [<command-arg>*]

For example:
    $ {command} echo hi
    hi"""

def format_usage(program_name):
    """return the program usage as a string"""
    return USAGE.format(command=program_name)

def run(args):
    """main pbt entry point, receives *args* with sys.argv format"""
    if len(args) == 1:
        print(format_usage(args[0]))
    else:
        _, command, *command_args = args
        pbt.run(command, command_args)
