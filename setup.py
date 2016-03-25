#
#
#

import contextlib
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


def pre_build_ext(cmd_obj, recent=None):
    # Check librados2 requirements
    if recent is None:
        comp = ccompiler.new_compiler(force=True, verbose=True)
        with output_redirected():
            rados_installed = comp.has_function('rados_connect',
                                                libraries=['rados'])
        if not rados_installed:
            raise Exception("librados2 or librados-dev >= 0.80 are missing")
        with output_redirected():
            recent = comp.has_function('rados_pool_get_base_tier',
                                       libraries=['rados'])

    print("librados %s 0.94 detected (method rados_pool_get_base_tier %s)" %
          (">=" if recent else "<=",
           "detected" if recent else "absent"))

    # Generate the source file from template
    cradox_out = os.path.join(os.path.dirname(__file__), 'cradox.pyx')
    cradox_in = "%s.in" % cradox_out
    with open(cradox_in, 'r') as src:
        with open(cradox_out, 'w') as dst:
            skip = False
            for line in src:
                if line == "@@BEGIN_BEFORE_HAMMER@@\n":
                    skip = recent
                    continue
                elif line == "@@END_BEFORE_HAMMER@@\n":
                    skip = False
                    continue
                elif line == "@@BEGIN_HAMMER_OR_LATER@@\n":
                    skip = not recent
                    continue
                elif line == "@@END_HAMMER_OR_LATER@@\n":
                    skip = False
                    continue
                elif skip:
                    continue
                else:
                    dst.write(line)


if __name__ == '__main__':
    setup(
        setup_requires=['pbr', 'Cython'],
        pbr=True,
        ext_modules=[Extension("cradox", ["cradox.pyx"], libraries=["rados"])],
    )
