#! /usr/bin/env python3
from setuptools.dist import Distribution
from setuptools import setup

Distribution(dict(setup_requires="pyxdg==0.25"))

from os.path import join
from xdg.BaseDirectory import save_data_path, load_data_paths

# plugins
# according to the Debian Python Policy, they should go in /usr/share/<program>
# NOTE: for the time being, we're gonna install them in the user's xdg.data dir

# first, make sure the dir exists
save_data_path("pbt/")
save_data_path("pbt/plugins/")

# the user's dir comes first
user_xdg_data_dir = next(load_data_paths('pbt/plugins/'))

setup(
    name='pbt',
    version='0.0.1',
    description='python build tool',
    url='https://github.com/pebete/pbt',
    packages=['pbt'],
    scripts=['bin/pbt'],
    license='Apache 2.0',
    install_requires=["PyYAML==3.10", "flake8==2.0", "cookiecutter==0.7.0", "pyxdg==0.25"],
    data_files=[
        (join(user_xdg_data_dir, 'install'), ['plugins/install/main.py', ]),
        (join(user_xdg_data_dir, 'run'),     ['plugins/run/main.py', ]),
        (join(user_xdg_data_dir, 'new'),     ['plugins/new/main.py',
                                              'plugins/new/templates.json', ]),
        (join(user_xdg_data_dir, 'check'),   ['plugins/check/main.py', ]),
        (join(user_xdg_data_dir, 'setup'),   ['plugins/setup/main.py', ]),
        ],
    )
