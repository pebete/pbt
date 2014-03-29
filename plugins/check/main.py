"""The check plugin: your best friend and your worst nightmare"""
import pbt
import pep8


@pbt.command(name="check")
def main(ctx, args, prj):
    """Checks the project with some checkers, like pep8 or pylint."""
    check_pep8(ctx, args, prj)


def check_pep8(ctx, args, prj):
    """The pepocher"""
    guide = pep8.StyleGuide(parse_argv=False, config_file=True)
    guide.check_files('.')
