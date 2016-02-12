#!/bin/bash

set -e 
if [ "$1" == "-d" ] ; then
	cat > test.gdb <<EOF
set pagination off
cy run
cy bt
info breakpoints
EOF
	cmd="cygdb . -- --batch --command=test.gdb --args python $(which nosetests)"
	shift
else
	cmd="nosetests"
fi
[ "$@" ] && tests=":$@"

rm -f cradox.c
python-dbg setup.py  build_ext --inplace --build-lib .

for i in $(rados lspools | grep -e foo -e test_pool -e foo-cache) ; do 
	rados rmpool $i $i --yes-i-really-really-mean-it ; 
done ; 

$cmd -vds test_rados$tests
