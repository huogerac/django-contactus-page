#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import contactuspage

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = contactuspage.__version__

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    print("You probably want to also tag the version now:")
    print("  git tag -a %s -m 'version %s'" % (version, version))
    print("  git push --tags")
    sys.exit()

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-contactus-page',
    version=version,
    description="""A pluggable app for creating a contact us page""",
    long_description=readme + '\n\n' + history,
    author='Roger Camargo',
    author_email='roger.camargo@djenie.com',
    url='https://github.com/huogerac/django-contactus-page',
    packages=[
        'contactuspage',
    ],
    include_package_data=True,
    install_requires=[
        'django-multisites-utils',
    ],
    dependency_links=[
        "git+http://github.com/DjenieLabs/django-multisites-utils.git#egg=django-multisites-utils"
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-contactus-page',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ],
)
