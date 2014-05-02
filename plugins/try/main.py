"""Try plugin """
import pbt
import tempfile
import sys
import pip
from IPython import embed
from venv import create
from os.path import join



@pbt.command(runs_in_project=False,name='try')
def main(ctx, args):
    """opens a shell with a library available to try it


    pbt try [lib_to_try]        - create a disposable venv and install the passed lib, then give you
                                  a iPython terminal to try it.


    """
    if len(args) == 1:
        pbt_try(args[0])
    else:
        print('Usage: pbt try [lib_to_try]\n')



def pbt_try(lib_to_try):
    banner1='Testing {} in a disposable venv'.format(lib_to_try)
    exit_msg= 'Do you like de lib? You can install it with pbt install ;)'
    with tempfile.TemporaryDirectory() as tmp_venv_dir:
        #Creating venv
        create(tmp_venv_dir)
        #activating venv
        sys.base_prefix = sys.prefix
        sys.base_exec_prefix = sys.exec_prefix
        sys.prefix = tmp_venv_dir
        sys.exec_prefix = tmp_venv_dir
        lib_path = join(tmp_venv_dir,
                       'lib',
                       'python{}.{}'.format(*sys.version_info[:2]),
                       'site-packages')
        sys.path.insert(0,lib_path)
        #Installing lib to try
        pip_args = ['-v','install',"-t", lib_path,lib_to_try]
        pip.main(initial_args=pip_args)
        # Running iPython
        embed(banner1=banner1, exit_msg=exit_msg)

