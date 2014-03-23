import pbt

from json import load
from pbt_util import install_package

@pbt.run_on_load
def on_load(ctx, path):
    with open(ctx.path_to_plugin_file("new", "templates.json")) as fp:
        ctx.TEMPLATES = load(fp)
    pass

@pbt.command(runs_in_project=False, name="new")
def main(ctx, args):
    """

    new command is powered by cookiecutter and allows you to create environments from predefined and custom templates

    Usage:

    pbt new [TEMPLATE] [list]

    in the template option you can put the name of a predefined templates or
    the link of a git/mercurial repo that holds your custom template.

    """
    # TODO: find a fuzzy, offline way of listing and finding templates
    if "list" in args:
        print()
        for template in ctx.TEMPLATES:
            print("%s: %s" % (template["name"], template["description"]))
            print()
        return

    if args:
        for template in ctx.TEMPLATES:
            if template["name"] == args[0]:
                args[0] = template["link"]
                break
    else:
        args.append(ctx.TEMPLATES[0]["link"])

    try:
        import cookiecutter
    except ImportError:
        install_package("cookiecutter")
        import cookiecutter

    try:
        cookiecutter.main.cookiecutter(args[0])
    except FileNotFoundError as err:
        if "'git'" in err.strerror:
            print("Git version control application is needed for this action, "
                  "please install it, see instructions at http://git-scm.com/downloads")
        else:
            raise
