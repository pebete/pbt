"""Try plugin """
import pbt
import tempfile
import sys
import pip


@pbt.command(runs_in_project=False, name='try')
def main(ctx, args):
    """opens a shell with a library available to try it


    pbt try [lib_to_try]        - Install the passed lib in a disposable path, then give you
                                  a interactive terminal to try it. (iPython if is installed)


    """
    if len(args) == 1:
        pbt_try(args[0])
    else:
        print('Usage: pbt try [lib_to_try]\n')


def pbt_try(lib_to_try):
    """opens a shell with a library available to try it"""

    banner = '''\n{0} is installed in a disposable path and ready to test.
Maybe you should run "import {0}"\n'''.format(lib_to_try)

    exit_msg = '''Do you like this lib? You can add it to your project
with "pbt install {}"'''.format(lib_to_try)
    with tempfile.TemporaryDirectory(prefix='pbt_try_') as tmp_pbt_try_dir:
        pbt_try_install(lib_to_try, tmp_pbt_try_dir)
        try:
            from IPython import embed
            embed(banner1=banner, exit_msg=exit_msg)
        except ImportError:
            print('\niPython is not available. '
                  'pbt recommends you install it!\n')
            import code
            code.interact(local=locals(), banner=banner)


def pbt_try_install(lib_to_try, path):
    """ Install a lib in a custom path using pip"""
    sys.path.insert(0, path)
    pip_args = ['install', "-t", path, lib_to_try]
    pip.main(initial_args=pip_args)
