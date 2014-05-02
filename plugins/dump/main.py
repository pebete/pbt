"""core commands for pbt"""
import yaml
import pbt

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
