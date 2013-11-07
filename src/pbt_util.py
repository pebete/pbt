"""utilities for pbt"""
import os

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
