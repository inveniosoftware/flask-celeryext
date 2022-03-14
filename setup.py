# -*- coding: utf-8 -*-
#
# This file is part of Flask-CeleryExt
# Copyright (C) 2015-2019 CERN.
# Copyright (C) 2018-2019 infarm - Indoor Urban Farming GmbH.
# Copyright (C) 2022 Graz University of Technology.
#
# Flask-CeleryExt is free software; you can redistribute it and/or modify it
# under the terms of the Revised BSD License; see LICENSE file for more
# details.

"""Flask-CeleryExt is a simple integration layer between Celery and Flask."""

import os

from setuptools import find_packages, setup

readme = open('README.rst').read()
history = open('CHANGES.rst').read()

tests_require = [
    'check-manifest>=0.42',
    'coverage>=5.3,<6',
    'docker-services-cli>=0.4.0',
    'msgpack-python>=0.5.6',
    'pytest-cov>=3.0.0',
    'pytest-flask>=1.2.0',
    'pytest-isort>=3.0.0',
    'pytest-mock>=2.0.0',
    'pytest-pycodestyle>=2.2.0',
    'pytest-pydocstyle>=2.2.0',
    'pytest>=6,<7',
    'redis>=4.1.4',
]

extras_require = {
    'docs': [
        'Sphinx>=4.2.0',
    ],
    'tests': tests_require,
}

extras_require['all'] = []
for reqs in extras_require.values():
    extras_require['all'].extend(reqs)

install_requires = [
    'Flask>=1.1',
    'celery>=5.1.0',
]

packages = find_packages()


# Get the version string. Cannot be done with import!
g = {}
with open(os.path.join('flask_celeryext', 'version.py'), 'rt') as fp:
    exec(fp.read(), g)
    version = g['__version__']

setup(
    name='Flask-CeleryExt',
    version=version,
    description=__doc__,
    long_description=readme + '\n\n' + history,
    keywords='flask celery',
    license='BSD',
    author='CERN',
    author_email='info@inveniosoftware.org',
    url='https://github.com/inveniosoftware/flask-celeryext',
    packages=packages,
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Object Brokering',
        'Topic :: System :: Distributed Computing',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 5 - Production/Stable',
    ],
)
