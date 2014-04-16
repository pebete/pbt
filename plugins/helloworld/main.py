"""example hello world plugin"""
from __future__ import print_function
import pbt

print("Hello world from plugin at load time")


@pbt.run_on_load
def my_on_load(ctx, my_path):
    """plugin function called when pbt finished loading all plugins"""
    print("on_load, hello world", my_path, ctx)


@pbt.command(runs_in_project=False)
def hello(_ctx, _args):
    """prints hello world"""
    print("Hello world!")
