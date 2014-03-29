"""The check plugin: your best friend and your worst nightmare"""
import pbt


@pbt.command(name="check")
def main(ctx, args, prj):
    """Checks the project with some checkers, like pep8 or pylint."""
    check_pep8(ctx, args, prj)


def check_pep8(ctx, args, prj):
    """The pepocher"""
    try:
        # flake8 seems to be more complete than pep8, so it should be the default
        import flake8.engine

        checkerFactory= flake8.engine.get_style_guide
        print("Using Flake8")
    except ImportError:
        import pep8

        print("Using pep8")
        checkerFactory= pep8.StyleGuide

    guide = checkerFactory(parse_argv=False, config_file=True)
    guide.check_files('.')
