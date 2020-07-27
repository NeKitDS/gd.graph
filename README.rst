gd.graph
========

.. image:: https://img.shields.io/pypi/l/gd.graph.svg
    :target: https://opensource.org/licenses/MIT
    :alt: Project License

.. image:: https://img.shields.io/pypi/v/gd.graph.svg
    :target: https://pypi.python.org/pypi/gd.graph
    :alt: PyPI Library Version

.. image:: https://img.shields.io/pypi/pyversions/gd.graph.svg
    :target: https://pypi.python.org/pypi/gd.graph
    :alt: Required Python Versions

.. image:: https://img.shields.io/pypi/status/gd.graph.svg
    :target: https://github.com/NeKitDS/gd.graph
    :alt: Project Development Status

.. image:: https://img.shields.io/pypi/dm/gd.graph.svg
    :target: https://pypi.python.org/pypi/gd.graph
    :alt: Library Downloads/Month

.. image:: https://img.shields.io/endpoint.svg?url=https%3A%2F%2Fshieldsio-patreon.herokuapp.com%2Fnekit%2Fpledges
    :target: https://patreon.com/nekit
    :alt: Patreon Page [Support]

gd.graph is a library that implements a CLI for plotting graphs in Geometry Dash.

Installing
----------

**Python 3.6 or higher is required**

To install the library, you can just run the following command:

.. code:: sh

    # Linux/OS X
    python3 -m pip install -U gd.graph

    # Windows
    py -3 -m pip install -U gd.graph

In order to install the library from source, you can do the following:

.. code:: sh

    $ git clone https://github.com/NeKitDS/gd.graph
    $ cd gd.graph
    $ python -m pip install -U .

Invoking
--------

You can invoke the command either like this:

.. code:: sh

    $ python -m gdgraph

Or like this:

.. code:: sh

    $ gd.graph

Quick example
-------------

Here is an example of plotting ``y = x`` function:

.. code:: sh

    $ gd.graph --color=0x55FF55 --func=x --level-name=identity --y-limit=5 --inclusive

.. code:: text

    Preparing database and levels...
    Preparing the level and the editor...
    Free color ID: 1.
    Generating points...
    Generating points to be skipped...
    Applying Ramer-Douglas-Peucker (RDP) algorithm...
    Generating objects...
    Shifting objects to the right...
    Saving...
    Done. Objects used: 286.

And here is the result we get:

.. image:: ./showcase.png
    :target: ./showcase.png
    :alt: Result

Authors
-------

This project is mainly developed by `NeKitDS <https://github.com/NeKitDS>`_.
