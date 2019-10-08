============
Installation
============

Requirements
------------

promoe has several requirements, that all have to be met:

1. Python 3.7+
2. Pymol most recent python 2 version (Pymol versions supporting python 3+ are not tested!) => 'pymol' has to be available in your path
3. Pymol-psico (https://pymolwiki.org/index.php/Psico)
4. The most recent MOE version => 'moebatch' has to be available in your path

Stable release
--------------

To install promoe, run this command in your terminal:

.. code-block:: console

    $ pip install promoe

This is the preferred method to install promoe, as it will always install the most recent stable release. All required dependencies, except for the ones mentioned above will automatically be included.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for promoe can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/zethson/promoe

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://github.com/zethson/promoe/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/zethson/promoe
.. _tarball: https://github.com/zethson/promoe/tarball/master
