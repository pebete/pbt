"""example hello world plugin"""
import pbt
import sys

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
        try:
            fp = open("requirements.txt")
            fp.close()
        except FileNotFoundError:
            print("there is not requirements.txt file in the current folder")
        else:
            pip.main(["install", "-r", "requirements.txt"])
