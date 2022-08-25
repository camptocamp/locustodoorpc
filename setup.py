# -*- coding: utf-8 -*-

import re

from setuptools import setup

with open('locustodoorpc/__init__.py') as f:
    version = re.search('^__version__\s*=\s*\'(.*)\'', f.read(), re.M).group(1)
with open('README.rst') as f:
    readme = f.read()
with open('HISTORY.rst') as f:
    history = f.read()

setup(
    name='locustodoorpc',
    version=version,
    description='Locust custom client: odoorpc',
    long_description=readme + '\n\n' + history,
    author='Camptocamp',
    author_email='info@camptocamp.com',
    url='https://github.com/camptocamp/locustodoorpc',
    license='LGPLv3+',
    packages=['locustodoorpc'],
    install_requires=[
      'odoorpc >= 0.8.0',
      'locust >= 1.1.1',
    ],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: '
        'GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
    ),
)
