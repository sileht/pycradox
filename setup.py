# Largely taken from
# https://blog.kevin-brown.com/programming/2014/09/24/combining-autotools-and-setuptools.html
import os
import os.path

from setuptools import Extension
from setuptools import setup
from distutils import ccompiler

VERSION = "1.1.2"


def generate_extensions(recent=None):
    from Cython.Build import cythonize

    # Check librados2 requirements
    if recent is None:
        comp = ccompiler.new_compiler(force=True, verbose=True)
        rados_installed = comp.has_function('rados_connect',
                                            libraries=['rados'])
        if not rados_installed:
            raise Exception("librados2 and/or librados-dev are missing")
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

    # Return cythonized extension
    return cythonize(
        [Extension("cradox", ["cradox.pyx"], libraries=["rados"])],
        build_dir=os.environ.get("CYTHON_BUILD_DIR", None),
        output_dir=os.environ.get("CYTHON_OUTPUT_DIR", None))


class lazy_cythonize(list):
    def __init__(self, callback):
        self._list, self.callback = None, callback

    def c_list(self):
        if self._list is None:
            self._list = self.callback()
        return self._list

    def __iter__(self):
        for e in self.c_list():
            yield e

    def __getitem__(self, ii):
        return self.c_list()[ii]

    def __len__(self):
        return len(self.c_list())


if __name__ == '__main__':
    with open(os.path.join(os.path.dirname(__file__), "README.rst")) as f:
        description = f.read()

    setup(
        name='cradox',
        version=VERSION,
        license="LGPL 2.1",
        author="Mehdi Abaakouk",
        author_email="sileht@sileht.net",
        classifiers=("Intended Audience :: Information Technology",
                     "Intended Audience :: System Administrators",
                     "License :: OSI Approved :: GNU Lesser General "
                     "Public License v2 (LGPLv2)",
                     "Operating System :: POSIX :: Linux",
                     "Programming Language :: Python",
                     "Programming Language :: Python :: 2",
                     "Programming Language :: Python :: 2.7",
                     "Programming Language :: Python :: 3",
                     "Programming Language :: Python :: 3.4"),
        url="https://github.com/sileht/pycradox",
        description=("Python libraries for the Ceph librados library with "
                     "use cython instead of ctypes"),
        long_description=description,
        setup_requires=["Cython"],
        ext_modules=lazy_cythonize(generate_extensions),
    )
