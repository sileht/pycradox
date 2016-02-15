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

This a standalone library identical to this Ceph PR https://github.com/ceph/ceph/pull/7621

But this can be used with older version of Ceph from 0.80.X (firefly) to 10.0.X (perhaps more not tested)

This is designed for application that only want to use the Rados API, this can’t be used with the
ceph rbd.py or librbdpy

The API of this python lib is identical to the Ceph rados.py API. More detail can be found on
https://github.com/ceph/ceph/pull/7621.


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

  import cradox as rados


Tests
-----

  For python 2.X:
  $ ./test_rados.sh

  For python 3.X:
  $ ./test_rados.sh -3

  For python2-dbg + gdb
  $ ./test_rados.sh -b

  For python2-dbg + cygdb
  $ ./test_rados.sh -d

