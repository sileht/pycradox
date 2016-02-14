#!/bin/bash

set -e 

if [ "$1" == "-d" ] ; then
	cat > test.gdb <<EOF
set pagination off
cy run
cy bt
EOF
	opt="-dbg"
	cmd="cygdb . -- --batch --command=test.gdb --args python-dbg $(which nosetests)"
	shift
elif [ "$1" == "-b" ] ; then
	cat > test.gdb <<EOF
set pagination off
run
bt
EOF
	opt="-dbg"
	cmd="gdb --batch --command=test.gdb --args python-dbg $(which nosetests)"
	shift

else
	cmd="nosetests"
fi
[ "$@" ] && tests=":$@"

ceph osd unset noup
for i in $(rados lspools | grep -e foo -e test_pool -e foo-cache -e 黄) ; do 
	rados rmpool $i $i --yes-i-really-really-mean-it ; 
done ; 

python$opt setup.py build_ext --inplace --build-lib .
$cmd -vds test_rados$tests
