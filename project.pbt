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
    - ["PyYAML", "==3.10"]
    - ["pyxdg", "==0.25"]
    - ["flake8", "==2.0"]
    - ["cookiecutter", "==0.7.0"]

min_pbt_version: 0.0.1

packages: ["pbt"]
scripts: ["bin/pbt"]

test_paths: ["test"]
resource_paths: ["resources"]
entry_point: ["pbt_cli", "run"]
