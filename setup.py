# -*- coding: utf-8 -*-

"""
The setup script is the centre of all activity in building, distributing,
and installing modules using the Distutils. It is required for ``pip install``.
See more: https://docs.python.org/2/distutils/setupscript.html
"""

from __future__ import print_function
from setuptools import setup, find_packages

import learn_opensearch as package

if __name__ == "__main__":
    PKG_NAME = package.__name__
    PACKAGES, INCLUDE_PACKAGE_DATA, PACKAGE_DATA, PY_MODULES = (
        None, None, None, None,
    )

    PACKAGES = [PKG_NAME,] + [
        "%s.%s" % (PKG_NAME, i)
        for i in find_packages(PKG_NAME)
    ]

    # Include everything in package directory
    INCLUDE_PACKAGE_DATA = True
    PACKAGE_DATA = {
        "": ["*.*"],
    }


    def read_requirements_file(path):
        """
        Read requirements.txt, ignore comments
        """
        requires = list()
        f = open(path, "rb")
        for line in f.read().decode("utf-8").split("\n"):
            line = line.strip()
            if "#" in line:
                line = line[:line.find("#")].strip()
            if line:
                requires.append(line)
        return requires

    setup(
        name=PKG_NAME,
        version=package.__version__,
        packages=PACKAGES,
        include_package_data=INCLUDE_PACKAGE_DATA,
        package_data=PACKAGE_DATA,
        py_modules=PY_MODULES,
        install_requires=read_requirements_file("requirements.txt"),
    )
