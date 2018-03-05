#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='lammps_utils',
    version='0.1',
    description='Utilities for manipulating data from LAMMPS',
    packages=find_packages(),
    install_requires=['numpy']
)
