#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-kube-provider',
    version='0.1.0',
    author='Łukasz Piątkowski',
    author_email='lukasz@giantswarm.io',
    maintainer='Łukasz Piątkowski',
    maintainer_email='lukasz@giantswarm.io',
    license='Apache Software License 2.0',
    url='https://github.com/piontec/pytest-kube-provider',
    description='A simple plugin to use with pytest]: A plugin to provide different types and configs of Kubernetes clusters that can be used for testing.',
    long_description=read('README.rst'),
    py_modules=['pytest_kube_provider'],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=5.4.2'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: Apache Software License',
    ],
    entry_points={
        'pytest11': [
            'kube-provider = pytest_kube_provider',
        ],
    },
)
