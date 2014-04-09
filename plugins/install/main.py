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
        # try to fetch the requirements.txt of the project
        if os.path.exists("requirements.txt"):
            pip.main(["install", "-r", "requirements.txt"])
        else:
            print("there is not requirements.txt file in the current folder")
