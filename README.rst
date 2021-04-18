gd.graph
========

.. image:: https://img.shields.io/pypi/l/gd.graph.svg
    :target: https://opensource.org/licenses/MIT
    :alt: Project License

.. image:: https://img.shields.io/pypi/v/gd.graph.svg
    :target: https://pypi.python.org/pypi/gd.graph
    :alt: Library Version

.. image:: https://img.shields.io/pypi/pyversions/gd.graph.svg
    :target: https://pypi.python.org/pypi/gd.graph
    :alt: Required Python Versions

.. image:: https://img.shields.io/pypi/status/gd.graph.svg
    :target: https://github.com/nekitdev/gd.graph
    :alt: Development Status

.. image:: https://img.shields.io/pypi/dw/gd.graph.svg
    :target: https://pypi.python.org/pypi/gd.graph
    :alt: Library Downloads / Week

.. image:: https://app.codacy.com/project/badge/Grade/e791035c646345a88423fd62fb9a6b26
    :target: https://www.codacy.com/gh/nekitdev/gd.graph
    :alt: Code Quality

gd.graph is a library that implements a CLI for plotting graphs in Geometry Dash.

Installing
----------

**Python 3.6 or higher is required**

To install the library, you can just run the following command:

.. code:: sh

    # Linux/OS X
    python3 -m pip install --upgrade gd.graph

    # Windows
    py -3 -m pip install --upgrade gd.graph

In order to install the library from source, you can do the following:

.. code:: sh

    $ git clone https://github.com/nekitdev/gd.graph
    $ cd gd.graph
    $ python -m pip install --upgrade .

Invoking
--------

You can invoke the command either like this:

.. code:: sh

    $ python -m gd.graph

Or like this:

.. code:: sh

    $ gd.graph

Quick example
-------------

Here is an example of plotting ``y = x`` function:

.. code:: sh

    $ gd.graph --color=0x55FF55 --function=x --level-name=identity --y-limit=5 --inclusive

.. code:: text

    Processing...
    Parsing and compiling function...
    Preparing database and levels...
    Preparing the level and the editor...
    Free color ID: 1.
    Generating points...
    Generating points to be skipped...
    Applying Ramer-Douglas-Peucker (RDP) algorithm...
    Generating objects...
    Shifting objects to the right...
    Saving...
    Done. Objects used: 286. Time spent: Ns.

And here is the result we get:

.. image:: ./y=x.png
    :target: ./y=x.png
    :alt: y = x

Or something more complex, ``y = sin(x)``:

.. code:: sh

    $ gd.graph -c 0xFF5555 -f sin(x) -l "wave" -i

.. code:: text

    Processing...
    Parsing and compiling function...
    Preparing database and levels...
    Preparing the level and the editor...
    Free color ID: 1.
    Generating points...
    Generating points to be skipped...
    Applying Ramer-Douglas-Peucker (RDP) algorithm...
    Generating objects...
    Shifting objects to the right...
    Saving...
    Done. Objects used: 548. Time spent: Ns.

And the result:

.. image:: ./y=sin(x).png
    :target: ./y=sin(x).png
    :alt: y = sin(x)

Command Line Interface
----------------------

Here are all parameters ``gd.graph`` currently accepts:

.. code:: sh

    $ gd.graph --help

.. code:: text

    Usage: gd.graph [OPTIONS]

    Options:
      -c, --color TEXT              Color to use, written in hex format.
      -var, -v, --variable TEXT     Variable name to use, which should be valid as
                                    an identifier. Default is x.

      -func, -f, --function TEXT    Mathematical function to graph, like sin(x).
      -name, -l, --level-name TEXT  Name of the level to save graph to.
      --start FLOAT                 Value of the argument to start plotting from.
      --stop FLOAT                  Value of the argument to stop plotting at.
      --step FLOAT                  Value of the step to add to the argument.
      -y, --y-limit FLOAT           Limit of absolute y value of any point.
      -e, --epsilon FLOAT           Epsilon to use for decimating function a curve
                                    to a similar curve with fewer points.

      -s, --scale FLOAT             Scale constant used to enlarge the graph.
      -r, --rounding INTEGER        Number of decimal places to round each
                                      argument to.

      -i, --inclusive               Whether last argument in given range should be
                                    included.

      --help                        Show this message and exit.

Authors
-------

This project is mainly developed by `nekitdev <https://github.com/nekitdev>`_.
