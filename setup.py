#!/usr/bin/env python
from setuptools import setup

setup(
    name='scout',
    version='0.1dev',
    description='A basic search engine on Python.',
    author='Suraj Thapar',
    author_email='surajthapar.in@gmail.com',
    long_description=open('README.md').read(),
    packages=[
        'scout',
    ],
    python_requires='>=3.6.5, <4',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3.6.5',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)