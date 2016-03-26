#
#
#

import contextlib
import collections
import os
import os.path
import sys


from setuptools import Extension
from setuptools import setup
from distutils import ccompiler


@contextlib.contextmanager
def output_redirected():
    oldstderr = os.dup(sys.stderr.fileno())
    oldstdout = os.dup(sys.stdout.fileno())
    null = open(os.devnull, 'w')
    os.dup2(null.fileno(), sys.stdout.fileno())
    os.dup2(null.fileno(), sys.stderr.fileno())
    yield
    os.dup2(oldstderr, sys.stderr.fileno())
    os.dup2(oldstdout, sys.stdout.fileno())
    null.close()


ceph_version_map = collections.OrderedDict(sorted({
    "firefly": "rados_connect",
    "hammer": "rados_pool_get_base_tier",
    "jewel": "rados_inconsistent_pg_list",
}.items(), key=lambda t: t[0]))


def pre_build_ext(cmd_obj, version=None):
    if version == "latest":
        version = sorted(ceph_version_map.keys())[-1]
    elif version is None:
        comp = ccompiler.new_compiler(force=True, verbose=True)
        for potential_version, method in ceph_version_map.items():
            sys.stdout.write("looking for librados >= %s (with %s)" %
                             (potential_version, method))
            sys.stdout.flush()
            with output_redirected():
                found = comp.has_function(method, libraries=['rados'])
            if found:
                version = potential_version
                print(", FOUND")
            else:
                print(", NOT FOUND")
                break

        if not version:
            raise Exception("librados2 or librados-dev >= 0.80 are missing")

    print("building cradox with %s api compatibility" % version)

    # Generate the source file from template
    from jinja2 import Template
    cradox_out = os.path.join(os.path.dirname(__file__), 'cradox.pyx')
    cradox_in = "%s.in" % cradox_out
    with open(cradox_in, 'r') as src:
        with open(cradox_out, 'w') as dst:
            template = Template(src.read())
            dst.write(template.render(version=version))


if __name__ == '__main__':
    setup(
        setup_requires=['pbr', 'Cython', 'Jinja2'],
        pbr=True,
        ext_modules=[Extension("cradox", ["cradox.pyx"], libraries=["rados"])],
    )
