#!/bin/bash

set -e 

cleanup(){
    rm -f a.out test.gdb
}

trap cleanup EXIT

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
elif [ "$1" == "-3" ]; then
	shift
	python="python3"
	launcher=
else
	python="python"
	launcher=
fi

[ "$@" ] && tests=":$@"

ceph osd unset noup
for i in $(rados lspools | grep -e foo -e test_pool -e foo-cache -e 黄 -e 黅) ; do 
	rados rmpool $i $i --yes-i-really-really-mean-it ; 
done ; 

$python -c "import setup; setup.pre_build_ext(None)"
$python setup.py build_ext --inplace $opt_setup --build-lib .
$launcher $python $(which nosetests) -vds test_rados$tests
