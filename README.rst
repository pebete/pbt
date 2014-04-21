pbt
===

Python build tool

what?
-----

this tool plans to bring all the development tools from python into a single,
comprehensive and coherent set of commands that will provide a default setup
and workflow to make it easy to start, build, test, package and publish a
python project.

all commands will be plugins, you can add and/or implement yours to suit your
needs.

pbt will provide the default setup and workflow with sensible defaults, but the
idea is that you can tweak every aspect if you need it.

how?
----

::

    # list of registered command

    pbt help

    # help for dump command

    pbt help dump

    # dump of all the information about the current project

    pbt dump

    # run <command> passing args

    pbt <command> [<arg>*]

examples
--------

::

    $ pwd

    /home/mariano/src/pbt/test/data

    $ ../../bin/pbt help

    Pbt is a tool for working with Python projects.

    Several tasks are available:

    dump             dumps all project configuration for the current project
    help             show commands' descriptions or command help if command specified

    $ ../../bin/pbt help help

    show commands' descriptions or command help if command specified

        pbt help         - displays all available commands with a brief description
        pbt help command - displays detailed help about a command

    $ ../../bin/pbt help dump

    dumps all project configuration for the current project

        This commands prints back all the information about the project
        that it knows, it serves as a tool to diagnose configuration problems
        and also as an example for a minimal project command

    $ ../../bin/pbt dump

    authors: [Mariano Guerra <mariano@marianoguerra>, x-ip, joac, L1pe]
    dependencies:
    - [org.python, requests, 2.0.0]
    description: python build tool
    license: {name: Apache 2.0, url: 'http://opensource.org/licenses/Apache-2.0'}
    name: pbt
    organization: pebete
    settings:
      entry_point: [src/pbt_cli.py, run]
      min_version: 0.0.1
      plugin_repositories:
      - [pypi, 'http:/pypi.python.org/']
      plugins:
      - [marianoguerra, sphinx, 1.0.0]
      python_cmd: ~/bin/pypy
      python_opts: [-tt]
      python_versions:
      - '2.6'
      - '2.7'
      - '3.3'
      - '3.4'
      - [pypy, '2.1']
      repositories:
      - [pypi, 'http:/pypi.python.org/']
      resource_paths: [resources]
      source_paths: [src]
      target_path: target
      test_paths: [test]
    url: https://github.com/pebete/pbt
    version: 0.0.1

dependencies
------------

yes, this will be later in the project.pbt

* yaml
* cookicutter
* xdg
* flake8

Installation
-------------

    $ git clone https://www.github.com/pebete/pbt
    $ cd pbt
    $ python3 setup.py install          # add sudo or --prefix at will

and that's almost all there's to writing a plugin

testing
-------

to run pbt core tests run from pbt base folder::

    $ python3 -m unittest discover -s test


resources
---------

* http://python-packaging-user-guide.readthedocs.org/en/latest/tutorial.html
* http://www.jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/
* http://docs.python-guide.org/en/latest/writing/structure/
* http://www.reddit.com/r/Python/comments/22326i/what_is_the_standard_way_to_organize_a_python/
* http://learnpythonthehardway.org/book/ex46.html
* https://gist.github.com/wickman/2371638
* https://www.youtube.com/watch?v=eLPiPHr6TVI
* https://www.youtube.com/watch?v=nHWRN5gCPSI
* http://pip2014.com/

license
-------

Apache
