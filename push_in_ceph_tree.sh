#!/bin/bash

set -e

python -c "import setup; setup.generate_pyx(recent=True)"
cp cradox.pyx ../ceph/src/pybind/rados/rados.pyx
cp cradox.pxd ../ceph/src/pybind/rados/rados.pxd
sed -e 's/cradox/rados/g' test_rados.py > ../ceph/src/test/pybind/test_rados.py
