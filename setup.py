#
#
#

from __future__ import print_function

import collections
import os
import os.path
import sys

from distutils import ccompiler
from setuptools import Extension
from setuptools import setup

ceph_version_map = collections.OrderedDict(sorted({
    "jewel": "rados_inconsistent_pg_list",
    "kraken": "rados_aio_exec",
    "luminous": "rados_read_op_omap_get_keys2",
}.items(), key=lambda t: t[0]))


def log(msg):
    print(msg, file=sys.stderr)


def setup_hook(cmd_obj, version=None):
    if version == "latest":
        version = sorted(ceph_version_map.keys())[-1]
    elif version is None:
        comp = ccompiler.new_compiler(force=True, verbose=True)
        for potential_version, method in ceph_version_map.items():
            msg = "* checking for librados >= %s (with function %s)" % (
                potential_version, method)
            log(msg)
            found = comp.has_function(method, libraries=['rados'])
            if found:
                version = potential_version
                log("%s done: FOUND" % msg)
            else:
                log("%s done: NOT FOUND" % msg)
                break

        if not version:
            raise Exception("gcc, python-dev, librados2 or "
                            "librados-dev >= 0.80 are missing")

    log("building cradox with %s api compatibility" % version)

    # Generate the source file from template
    from jinja2 import Environment
    env = Environment(trim_blocks=True, lstrip_blocks=True)
    cradox_out = os.path.join(os.path.dirname(__file__), 'cradox.pyx')
    cradox_in = "%s.in" % cradox_out
    with open(cradox_in, 'r') as src:
        with open(cradox_out, 'w') as dst:
            template = env.from_string(src.read())
            dst.write(template.render(version=version))
    test_out = os.path.join(os.path.dirname(__file__), 'test_rados.py')
    test_in = "%s.in" % test_out
    with open(test_in, 'r') as src:
        with open(test_out, 'w') as dst:
            template = env.from_string(src.read())
            dst.write(template.render(version=version))


if __name__ == '__main__':
    setup(
        setup_requires=['pbr', 'Cython', 'Jinja2'],
        pbr=True,
        ext_modules=[Extension("cradox", ["cradox.pyx"], libraries=["rados"])],
    )
