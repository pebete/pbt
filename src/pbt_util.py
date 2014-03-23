"""utilities for pbt"""
import os
import subprocess
import shlex
import sys

def get_dirs_up_to_root(basepath):
    """return a list of all the paths that are directories from path up to root"""
    path = os.path.normpath(basepath)
    result = [path]

    old_dirname = path
    dirname, _ = os.path.split(path)

    while dirname != old_dirname:
        result.append(dirname)
        old_dirname = dirname
        dirname, _ = os.path.split(dirname)

    return result

def install_package(name_or_link):
    if query_yes_no("Package %s not found, install?" % name_or_link):
        print("trying to install package %s with pip3" % name_or_link)
        cmd = "pip3 install %s" % name_or_link
        if not running_under_virtual_env():
            cmd = "sudo %s" % cmd
        subprocess.check_call(shlex.split(cmd))
        print("Package %s installed" % name_or_link)
    else:
        print("Package %s not installed" % name_or_link)

def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via `raw_input()` and return their answer.

    :param question: A string that is presented to the user.
    :param default: The presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".

    Adapted from
    http://stackoverflow.com/questions/3041986/python-command-line-yes-no-input
    http://code.activestate.com/recipes/577058/

    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()

        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def running_under_virtual_env():
    """ Return True if is acctualy running under a VirtualEnv.
    Borrowed from:
    https://github.com/pypa/pip/blob/develop/pip/locations.py#L36
    http://www.python.org/dev/peps/pep-0405/#specification
    """
    #TODO: Make full compatible with pep-0405
    if hasattr(sys, 'real_prefix'):
        return True
    elif sys.prefix != getattr(sys, "base_prefix", sys.prefix):
        return True
    return False
