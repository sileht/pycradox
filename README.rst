======
cradox
======

.. image:: https://img.shields.io/pypi/v/cradox.svg
   :target: https://pypi.python.org/pypi/cradox/
   :alt: Latest Version

.. image:: https://img.shields.io/pypi/dm/cradox.svg
   :target: https://pypi.python.org/pypi/cradox/
   :alt: Downloads


Python libraries for the Ceph librados library with use cython instead of ctypes

This a standalone library initially comes from this Ceph PR https://github.com/ceph/ceph/pull/7621

But can be built against older version of Ceph from 0.80.X (firefly) to 10.1.X (perhaps more not tested)

This is designed for application that want to use a recent python-rados API without upgrading
the whole ceph cluster.

Rados C handles provided by this library can’t be used with the ceph rbd.py or librbdpy.

The API of this python lib will be keep in sync with the upstream Ceph rados.py API.

* Free software: LGPL 2.1
* Documentation: http://docs.ceph.com/docs/master/rados/api/python/
* Source: http://github.com/sileht/pycradox


Installation
------------

Pre-requires::

    $ sudo apt-get install cython librados2 librados-dev

Then, at the command line::

    $ pip install cradox

Or, if you have virtualenvwrapper installed::

    $ mkvirtualenv cradox
    $ pip install cradox

Usage
-----

::

  import cradox as rados


Functionnal Tests
-----------------

A running ceph cluster is needed, the authentification must be disabled or done
automatically with the configuration in /etc/ceph/ceph.conf.

For python 2.X::

  $ ./test_rados.sh

For python 3.X::

  $ ./test_rados.sh -3

For python2-dbg + gdb::

  $ ./test_rados.sh -b

For python2-dbg + cygdb::

  $ ./test_rados.sh -d

