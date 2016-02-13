#!/bin/bash

set -e 
if [ "$1" == "-d" ] ; then
	cat > test.gdb <<EOF
set pagination off
cy run
cy bt
info breakpoints
EOF
	opt="-dbg"
	opt2="--inplace "
	cmd="cygdb . -- --batch --command=test.gdb --args python $(which nosetests)"
	shift
elif [ "$1" == "-b" ] ; then
	cat > test.gdb <<EOF
set pagination off
run
bt
info breakpoints
EOF
	cmd="gdb --batch --command=test.gdb --args python $(which nosetests)"
	shift

else
	cmd="nosetests"
fi
[ "$@" ] && tests=":$@"

ceph osd unset noup
for i in $(rados lspools | grep -e foo -e test_pool -e foo-cache) ; do 
	rados rmpool $i $i --yes-i-really-really-mean-it ; 
done ; 

rm -f cradox.c
python$opt setup.py build_ext $opt2 --build-lib .
$cmd -xvds test_rados$tests
