pbt
===

[![Build Status](https://travis-ci.org/pebete/pbt.png)](https://travis-ci.org/pebete/pbt)

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


Install pbt
------------

To install pbt run the following commands::

    $ git clone https://www.github.com/pebete/pbt
    $ cd pbt
    $ pip3 install -r requirements.txt  # this is gonna be fixed soon
    $ python3 setup.py install          # add sudo or --prefix at will

and that's all now you can start using pbt. 

Basic usage
-----------

you can check the power of pbt witg this commands ::
    
    # opens an ipython console with flask available to try
    $ pbt try flask
    
    # makes a flask project from a template 
    $ pbt new flask                    
    
    # runs the flask app from the entry point in project.pbt
    $ cd flask
    $ pbt run                           
    
    # checks the code with flake8
    $ pbt check                         
    
    # run the tests 
    $ pbt test                        
    
    # makes the setup.py file from project.pbt  
    $ pbt setup                        

testing
-------

to run pbt core tests run from pbt base folder::

    $ python3 -m unittest discover -s test

dependencies
------------

* yaml
* cookicutter
* xdg
* flake8

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
