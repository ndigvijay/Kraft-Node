# coding: utf-8

import setuptools
import pypandoc
from setuptools import setup
from os import path

__version__ = '1.0.0'

requirements = [req.strip() for req in open('requirements.txt').readlines()]

short_description ='python raft implementation with resp interface'
long_description = pypandoc.convert_file('README.md', 'rst')

setup(
    name='pyraft',
    packages=setuptools.find_packages(),
    version=__version__,
    description=short_description,
    long_description=long_description,
    author='Lee, Ki-Yeul',
    author_email='lynix94@gmail.com',
    license='MIT',
    url='https://github.com/lynix94/pyraft',
    keywords=['python', 'raft', 'replication', 'pyraft'],
    install_requires=requirements,
	python_requires  = '>=3',
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
