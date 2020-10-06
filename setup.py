#!/usr/bin/env python3
#
# setup.py
#
# Michael Potter
# 2020-10-06

from setuptools import setup

setup(
        name='ratton',
        version='0.1',
        packages=[
            'ratton',
            'ratton.lib'
            ],
        install_requires=[
            'blessed'
            ]
)
