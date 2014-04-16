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
        # TODO: add the new dep to the requierements
    else:
        # BUG: this is unconditional, use doit? make?
        with open ('requirements.txt', 'w+') as f:
            for dep in ctx.dependencies:
                f.write (dep)

        pip.main(["install", "-r", "requirements.txt"])
