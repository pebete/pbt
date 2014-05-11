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

    pipargs = ["install"]

    if "-t" in args or "--target" in args:
        if "-t" in args:
            t = args.index("-t")
        else:
            t = args.index("--target")
        # The destination folder is the next element in the list
        folder = args.pop(t+1)
        pipargs.append(args.pop(t))

        target_path = project.join_path(folder)
        ctx.ensure_dir_exists(target_path)
        pipargs.append(target_path)

    if args:
        pipargs += args
        # TODO: add the new dep to the requierements
    else:
        deps_spec = ["".join(dep) for dep in project.dependencies]
        pipargs += deps_spec

    pip.main(pipargs)
