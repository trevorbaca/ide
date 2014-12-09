#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

install_requires = ('abjad',)

setuptools.setup(
    entry_points={
        'console_scripts': [
            'abjad = abjad.tools.systemtools.run_abjad:run_abjad',
            'ajv = abjad.tools.developerscripttools.run_ajv:run_ajv',
            ]
        },
    include_package_data=True,
    install_requires=install_requires,
    license='GPL',
    name='Abjad Score Manager',
    packages=('scoremanager',),
    platforms='Any',
    url='http://www.projectabjad.org',
    )