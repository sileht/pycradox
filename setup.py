# Largely taken from
# https://blog.kevin-brown.com/programming/2014/09/24/combining-autotools-and-setuptools.html
import os
import os.path
import sys

from setuptools.command.egg_info import egg_info
from distutils.core import setup
from distutils import ccompiler
from distutils.extension import Extension
from Cython.Build import cythonize


#with open(os.path.join(os.path.dirname(__file__), 'cradox.pxi'), 'w') as fd:
#    hammer = ccompiler.has_function('rados_pool_get_base_tier', libraries=('rados',))
#    fd.write('DEF HAMMER = %d\n' % int(hammer))


class EggInfoCommand(egg_info):
    def finalize_options(self):
        egg_info.finalize_options(self)
        if "build" in self.distribution.command_obj:
            build_command = self.distribution.command_obj["build"]
            self.egg_base = build_command.build_base
            self.egg_info = os.path.join(self.egg_base,
                                         os.path.basename(self.egg_info))


# Disable cythonification if we're not really building anything
if (len(sys.argv) >= 2 and
        any(i in sys.argv[1:] for i in ('--help', 'clean', 'egg_info',
                                        '--version'))):
    def cythonize(x, **kwargs):
        return x

setup(
    name='cradox',
    version="1.0.0",
    description=("Python libraries for the Ceph librados library with use "
                 "cython instead of ctypes"),
    long_description="""This package contains Python libraries for interacting
with Ceph's rados library.

It requires at 0.94.X (hammer) release to compile.
""",
    ext_modules=cythonize(
        [Extension("cradox", ["cradox.pyx"], libraries=["rados"])],
        build_dir=os.environ.get("CYTHON_BUILD_DIR", None),
        output_dir=os.environ.get("CYTHON_OUTPUT_DIR", None)),
    cmdclass={
        "egg_info": EggInfoCommand,
    },
)
