import pbt
import sys
import os


@pbt.command(name="run")
def run(ctx, args, project):
    deps_path = project.join_path("deps")
    sys.path.insert(0, deps_path)
    return project.run()

