import pbt
from pbt_util import install_package

TEMPLATES = [
{"name": "pysimple", "description": "A simple python template project", "link":"https://github.com/jairot/cookiecutter-simplepypackage"},
{"name": "pypackage", "description": "Full, github ready, Python project template", "link": "https://github.com/audreyr/cookiecutter-pypackage"},
{"name": "flask", "description": "A Flask template with Bootstrap 3 and user registration.", "link": "https://github.com/sloria/cookiecutter-flask"},
{"name": "flask-env", "description": "A lucuma-flavored flask app template", "link": "https://github.com/lucuma/cookiecutter-flask-env"},
{"name": "simple-django", "description": "template for creating reusable Django projects quickly.", "link": "https://github.com/marcofucci/cookiecutter-simple-django"},
{"name":"django", "description": "bleeding edge Django project template with Bootstrap 3.", "link": "https://github.com/pydanny/cookiecutter-django"},
{"name":"djangopackage", "description": "template designed to create PyPI friendly Django apps.", "link": "https://github.com/pydanny/cookiecutter-djangopackage"},
{"name":"django-cms", "description": "template for Django CMS with simple Bootstrap 3 template.", "link": "https://github.com/palazzem/cookiecutter-django-cms"},
{"name":"openstack", "description": "template for an OpenStack project.", "link": "https://github.com/openstack-dev/cookiecutter"},
{"name":"docopt", "description": "template for a Python command-line script that uses docopt for arguments parsing.", "link": "https://github.com/sloria/cookiecutter-docopt"},
{"name":"django-crud", "description": "template to create a Django app with boilerplate CRUD around a model including a factory and tests.", "link": " https://github.com/wildfish/cookiecutter-django-crud"},
{"name":"quokka-module", "description": "template to create a blueprint module for Quokka Flask CMS.", "link": "https://github.com/pythonhub/cookiecutter-quokka-module"},
{"name":"django-lborgav", "description": "Another cookiecutter template for Django project with Booststrap 3 and FontAwesome 4.", "link": "https://github.com/lborgav/cookiecutter-django"}]

def on_load(ctx, path):
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
        for template in TEMPLATES:
            print("%s: %s" % (template["name"], template["description"]))
            print()
        return

    if args:
        for template in TEMPLATES:
            if template["name"] == args[0]:
                args[0] = template["link"]
                break
    else:
        args.append(TEMPLATES[0]["link"])

    try:
        import cookiecutter.main as cookiecutter
    except ImportError:
        install_package("cookiecutter")
        import cookiecutter.main as cookiecutter

    try:
        cookiecutter.cookiecutter(args[0])
    except FileNotFoundError as err:
        if "'git'" in err.strerror:
            print("Git version control application is needed for this action, "
                  "please install it, see instructions at http://git-scm.com/downloads")
        else:
            raise
