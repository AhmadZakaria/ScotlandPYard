#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.7',
    'networkx==2.1',
    'numpy==1.14.2',
    'PyQt5==5.10.1',
    'scipy==1.0.1'
]

setup_requirements = [
    'pytest-runner',
    # TODO(AhmadZakaria): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='ScotlandPYard',
    version='1.4.1',
    description="A python implementation of the board game 'Scotland Yard'",
    long_description=readme + '\n\n' + history,
    author="Ahmad Zakaria Mohammad",
    author_email='ahmadz1991@gmail.com',
    url='https://github.com/AhmadZakaria/ScotlandPYard',
    packages=['ScotlandPYard'],
    package_data={'package': ["ScotlandPYard/ScotlandPYard/resources*"]},
    entry_points={
        'console_scripts': [
            'ScotlandPYard=ScotlandPYard.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='ScotlandPYard',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
