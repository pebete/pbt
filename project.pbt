organization: pebete
name: pbt
version: 0.0.1
description: python build tool
url: https://github.com/pebete/pbt

license:
    name: Apache 2.0
    url: http://opensource.org/licenses/Apache-2.0

authors:
    - Mariano Guerra <mariano@marianoguerra>
    - jairot <jairotrad@gmail.com>
    - x-ip
    - joac
    - L1pe
    - GiLgAmEzH
    - Marcos Dione <mdione@grulic.org.ar>

dependencies:
    - ["org.python", "requests", "2.0.0"] # just to put something

min_pbt_version: 0.0.1

plugins:
    - ["marianoguerra", "sphinx", "1.0.0"]

repositories:
    - ["pypi", "http:/pypi.python.org/"]

plugin_repositories:

    - ["pypi", "http:/pypi.python.org/"]

#local_repo: local_repo

#hooks:
#    - ?

#these two come directly from distutils
packages: ["pbt"]
scripts: ["bin/pbt"]

test_paths: ["test"]
resource_paths: ["resources"]
entry_point: ["pbt_cli", "run"]

#repl_imports:
#    - "foo" # import foo
#    # ? from .. import .., import ... asd ..., from ... import .. as ..

python_cmd: "~/bin/pypy" # use a different python binary
python_opts: ["-tt"]
target_path: "target/"

python_versions:
    - "2.6"
    - "2.7"
    - "3.3"
    - "3.4"
    - ["pypy", "2.1"]
