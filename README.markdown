This is a tool which converts ReVo XML to a much simplified JSON
file. Python 2.X required.

How to use it
-------------

    $ mkvirtualenv revo_utils -p `which python2.7`
    $ pip install -r requirements.txt
    $ cd revo-export/
    $ python json_export.py

This will write a dictionary.json into revo-export/.

Directory structure
-------------------

dtd/ -- .dtd files for ReVo's XML structure

xml/ -- the XML files we extract from

revo-export/ -- all the Python code that does the work

ReVo documentation
------------------

ReVo's documentation could perhaps be more thorough, but is very
useful nonetheless. You can find it at
[http://www.reta-vortaro.de/revo/dok/manlibro.html](http://www.reta-vortaro.de/revo/dok/manlibro.html).


License
-------

This tools has an AGPLv3 licence, see COPYING for details.
