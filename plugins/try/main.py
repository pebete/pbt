"""Try plugin """
import pbt
import tempfile
import sys
import pip
from IPython import embed


@pbt.command(runs_in_project=False,name='try')
def main(ctx, args):
    """opens a shell with a library available to try it


    pbt try [lib_to_try]        - Install the passed lib in a disposable path, then give you
                                  a iPython terminal to try it.


    """
    if len(args) == 1:
        pbt_try(args[0])
    else:
        print('Usage: pbt try [lib_to_try]\n')


def pbt_try(lib_to_try):
    banner1='''{0} is installed in a disposable path and ready to test.
    Maybe you should run "import {0}"'''.format(lib_to_try)
    exit_msg= '''Do you like this lib? You can add it to your
    project with "pbt install {}"'''.format(lib_to_try)
    # Installing
    pbt_try_install(lib_to_try)
    # Running iPython
    embed(banner1=banner1, exit_msg=exit_msg)


def pbt_try_install(lib_to_try):
    with tempfile.TemporaryDirectory() as tmp_pbt_try_dir:
        sys.path.insert(0,tmp_pbt_try_dir)
        pip_args = ['-v','install',"-t", tmp_pbt_try_dir, lib_to_try]
        pip.main(initial_args=pip_args)

