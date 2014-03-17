"""utilities for pbt"""
import os
import subprocess
import shlex

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
    # TODO: Ask if we are in a a virtualenv
    subprocess.call(shlex.split("sudo pip3 install %s" % name_or_link))



