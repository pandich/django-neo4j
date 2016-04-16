#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import re
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def get_version(*file_paths):
    filename = os.path.join(os.path.dirname(__file__), *file_paths)
    version_file = open(filename).read()
    version_match = re.search(r'^__version__ = \'\d+\.\d+\.\d+\'', version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError(u'Unable to find version string.')

version = get_version(u'django_neo4j', u'__init__.py')

if sys.argv[-1] == u'publish':
    try:
        # noinspection PyUnresolvedReferences
        import wheel
    except ImportError:
        print(u'Wheel library missing. Please run \'pip install wheel\'')
        sys.exit()
    os.system(u'python setup.py sdist upload')
    os.system(u'python setup.py bdist_wheel upload')
    sys.exit()

if sys.argv[-1] == u'tag':
    print(u'Tagging the version on github:')
    os.system(u'git tag -a {0:s} -m \'version {1:s}\''.format(version, version))
    os.system(u'git push --tags')
    sys.exit()

readme = open(u'README.rst').read()
history = open(u'HISTORY.rst').read().replace(u'.. :changelog:', u'')

setup(
    name=u'django-neo4j',
    version=version,
    description=u'Restricts access to database resources via filtering.',
    long_description=readme + u'\n\n' + history,
    author=u'Stephen Pandich',
    author_email=u'steve@paradata.io',
    url=u'https://github.com/parapanda/django-neo4j',
    packages=[u'django_neo4j'],
    include_package_data=True,
    install_requires=[],
    license=u'Proprietary',
    zip_safe=False,
    keywords=u'django-neo4j',
    classifiers=[
        u'Development Status :: 3 - Alpha',
        u'Framework :: Django',
        u'Framework :: Django :: 1.8',
        u'Intended Audience :: Developers',
        u'Natural Language :: English',
        u'Programming Language :: Python :: 2',
        u'Programming Language :: Python :: 2.7',
        u'Programming Language :: Python :: 3',
        u'Programming Language :: Python :: 3.3',
        u'Programming Language :: Python :: 3.4',
        u'Programming Language :: Python :: 3.5',
    ],
)
