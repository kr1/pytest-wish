#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-wish',
    version='0.1.0',
    author='Alessandro Amici',
    author_email='alexamici@gmail.com',
    maintainer='Alessandro Amici',
    maintainer_email='alexamici@gmail.com',
    license='MIT',
    url='https://github.com/alexamici/pytest-wish',
    download_url = 'https://github.com/peterldowns/mypackage/tarball/0.1.0',
    description='Test-Driven-Nondevelopment for Pytest',
    long_description=read('README.rst'),
    py_modules=['pytest_wish'],
    install_requires=[
        'pytest>=2.8.1',
    ],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'wish = pytest_wish',
        ],
    },
)