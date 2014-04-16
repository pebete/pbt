"""core commands for pbt"""
import yaml

import pbt

@pbt.command(runs_in_project=False, name="help")
def help_command(ctx, args, print=print):
    """show commands' descriptions or command help if command specified

    pbt help         - displays all available commands with a brief description
    pbt help command - displays detailed help about a command"""
    if len(args) == 0:
        print("Pbt is a tool for working with Python projects.")
        print()
        print("Several tasks are available:")
        print()

        command_names = ctx.get_command_names()
        for name in command_names:
            command_description = ctx.get_command_description(name)
            print(name, "\t\t", command_description)
    elif len(args) == 1:
        command_name = args[0]
        try:
            command_docs = ctx.get_command_docs(command_name)
            print(command_docs)
        except pbt.CommandNotFoundError as e:
            print(e)
    else:
        print("Usage: pbt help [command]")

@pbt.command(name="dump")
def dump_command(ctx, args, project, print=print):
    """dumps all project configuration for the current project

    This commands prints back all the information about the project
    that it knows, it serves as a tool to diagnose configuration problems
    and also as an example for a minimal project command"""

    data = project.to_data()
    data_str = yaml.dump(data)
    print(data_str)
    return data
