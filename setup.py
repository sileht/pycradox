#
#
#

import collections
import os
import os.path

from distutils import ccompiler
from setuptools import Extension
from setuptools import setup


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
            msg = "* checking for librados >= %s (with function %s)" % (
                potential_version, method)
            print(msg)
            found = comp.has_function(method, libraries=['rados'])
            if found:
                version = potential_version
                print("%s done: FOUND" % msg)
            else:
                print("%s done: NOT FOUND" % msg)
                break

        if not version:
            raise Exception("gcc, python-dev, librados2 or "
                            "librados-dev >= 0.80 are missing")

    print("building cradox with %s api compatibility" % version)

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

    # Required by old version of setuptools
    if cmd_obj is not None:
        from Cython.Build import cythonize
        cmd_obj.extensions = cythonize(cmd_obj.extensions)
        for ext in cmd_obj.extensions:
            ext._needs_stub = False

if __name__ == '__main__':
    setup(
        setup_requires=['pbr', 'Cython', 'Jinja2'],
        pbr=True,
        ext_modules=[Extension("cradox", ["cradox.pyx"], libraries=["rados"])],
    )
