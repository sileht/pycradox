#!/bin/bash

set -e 
[ "$@" ] && tests=":$@"

rm -f cradox.c
python setup.py  build_ext --inplace --build-lib .

for i in $(rados lspools | grep -e foo -e test_pool -e foo-cache) ; do 
	rados rmpool $i $i --yes-i-really-really-mean-it ; 
done ; 

nosetests -vd test_rados$tests
