"""The check plugin: your best friend and your worst nightmare"""
import pbt
# flake8 is more complete than pep8, and depends on it anyways
import flake8.engine


@pbt.command(name="check")
def main(ctx, args, prj):
    """Checks the project with some checkers, like pep8 or pylint."""
    check_pep8(ctx, args, prj)


def check_pep8(ctx, args, prj):
    """The pepocher"""
    guide = flake8.engine.get_style_guide(parse_argv=False, config_file=True)
    guide.check_files('.')
