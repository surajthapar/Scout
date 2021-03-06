#!/usr/bin/env python
from setuptools import setup

setup(
    name='scout',
    version='0.1',
    description='A basic search engine on Python.',
    author='Suraj Thapar',
    author_email='surajthapar.in@gmail.com',
    packages=[
        'scout',
    ],
    python_requires='>=3.6.5, <4',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)