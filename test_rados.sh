#!/bin/bash

set -e 

if [ "$1" == "-d" ] ; then
	cat > test.gdb <<EOF
set pagination off
cy run
cy bt
EOF
	opt="-dbg"
    opt_setup="--cython-gdb"
    python="python-dbg"
	launcher="cygdb . -- --batch --command=test.gdb --args"
	shift
elif [ "$1" == "-b" ] ; then
	cat > test.gdb <<EOF
set pagination off
run
bt
EOF
	opt="-dbg"
    opt_setup="--cython-gdb"
    python="python-dbg"
	launcher="gdb --batch --command=test.gdb --args"
	shift
else
    python="python"
	launcher=
fi
[ "$@" ] && tests=":$@"

ceph osd unset noup
for i in $(rados lspools | grep -e foo -e test_pool -e foo-cache -e 黄) ; do 
	rados rmpool $i $i --yes-i-really-really-mean-it ; 
done ; 

export CYTHON_OUTPUT_DIR="."
$python setup.py build_ext --inplace $opt_setup --build-lib .
$launcher $python $(which nosetests) -vds test_rados$tests
