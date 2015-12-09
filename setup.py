# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015 CERN.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Flask Celery integration."""

import os
import re
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):

    """Integration of PyTest with setuptools."""

    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        """Initialize options."""
        TestCommand.initialize_options(self)
        try:
            from ConfigParser import ConfigParser
        except ImportError:
            from configparser import ConfigParser
        config = ConfigParser()
        config.read("pytest.ini")
        self.pytest_args = config.get("pytest", "addopts").split(" ")

    def finalize_options(self):
        """Finalize options."""
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        """Run tests."""
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)

# Get the version string.  Cannot be done with import!
with open(os.path.join('flask_celeryext', 'version.py'), 'rt') as f:
    version = re.search(
        '__version__\s*=\s*"(?P<version>.*)"\n',
        f.read()
    ).group('version')

tests_require = [
    'check-manifest>=0.25',
    'coverage>=4.0',
    'isort>=4.2.2',
    'pep257>=0.7.0',
    'pytest-cache>=1.0',
    'pytest-cov>=1.8.0',
    'pytest-pep8>=1.0.6',
    'pytest>=2.8.0',
]

setup(
    name='Flask-CeleryExt',
    version=version,
    url='http://github.com/inveniosoftware/flask-cli/',
    license='BSD',
    author='Invenio Collaboration',
    author_email='info@invenio-software.org',
    description=__doc__,
    long_description=open('README.rst').read(),
    packages=['flask_celeryext', ],
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    extras_require={
        'tests': tests_require,
    },
    install_requires=[
        'Flask>=0.10',
        'celery>=3.0',
    ],
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Utilities',
    ],
)
