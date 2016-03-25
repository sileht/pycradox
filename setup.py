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
def stdchannel_redirected(stdchannel, dest_filename):
    try:
        oldstdchannel = os.dup(stdchannel.fileno())
        dest_file = open(dest_filename, 'w')
        os.dup2(dest_file.fileno(), stdchannel.fileno())

        yield
    finally:
        if oldstdchannel is not None:
            os.dup2(oldstdchannel, stdchannel.fileno())
        if dest_file is not None:
            dest_file.close()


def pre_build_ext(cmd_obj, recent=None):
    # Check librados2 requirements
    if recent is None:
        comp = ccompiler.new_compiler(force=True, verbose=True)
        rados_installed = comp.has_function('rados_connect',
                                            libraries=['rados'])
        if not rados_installed:
            raise Exception("librados2 or librados-dev >= 0.80 are missing")
        with stdchannel_redirected(sys.stderr, os.devnull):
            recent = comp.has_function('rados_pool_get_base_tier',
                                       libraries=['rados'])

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
