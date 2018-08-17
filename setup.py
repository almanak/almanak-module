#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name='almanak',
    version='0.0.2',
    packages=find_packages(),
    description='Module and CLI for almanak.',
    long_description=long_description,
    url='https://github.com/clausjuhl/almanak',
    include_package_data=True,
    license='MIT',
    install_requires=[
        'click >= 6.7',
    ],
    entry_points="""
        [console_scripts]
        almanak=almanak.scripts.cli:cli
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)