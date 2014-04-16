import pbt
import sys
import os


@pbt.command(name="install")
def install(ctx, args, project):
    """
    Works as a wrapper for pip, with some sugar
    """

    try:
        import pip
    except ImportError:
        print("You need pip in order to use install, please see "
              "http://www.pip-installer.org/en/latest/installing.html")
        sys.exit(0)

    if args:
        pip.main(["install"] + args)
    else:
        deps_spec = ["".join(dep) for dep in project.dependencies]
        # make it configurable?
        target_path = project.join_path("deps")
        ctx.ensure_dir_exists(target_path)

        args = ["install", "-t", target_path] + deps_spec
        pip.main(args)
