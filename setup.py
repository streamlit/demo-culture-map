#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'mnowotka'

from setuptools import setup

setup(
    name='culture_map',
    version='0.0.1',
    author='Michal Nowotka',
    author_email='michal.nowotka@snowflake.com',
    description='Hofstede culture distance streamlit app',
    url='https://github.com/sfc-gh-mnowotka/culture_map',
    license='MIT',
    packages=['culture_map',
              'culture_map.country_data'
              ],
    long_description=open('README.md').read(),
    include_package_data=False,
    zip_safe=False,
)