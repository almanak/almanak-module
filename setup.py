#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='almanak',
    version='0.1',
    long_description='A command line interface for almanak',
    packages=['almanak'],
    description='A simple wrapper around optparse for '
                'powerful command line utilities.',
    include_package_data=True,
    install_requires=[
        'click',
    ],
    entry_points='''
        [console_scripts]
        almanak=almanak.scripts.cli:cli
    '''
)