#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

author = [
    'Trevor Bača',
    'Josiah Wolf Oberholtzer',
    ]
author = ', '.join(author)

author_email = [
    'trevor.baca@gmail.com',
    'josiah.oberholtzer@gmail.com',
    ]
author_email = ', '.join(author_email)

entry_points = {
    'console_scripts': [
        'start-abjad-ide = ide.tools.idetools:AbjadIDE._entry_point',
        ],
    }

install_requires = ('abjad',)

setuptools.setup(
    author=author,
    author_email=author_email,
    entry_points=entry_points,
    include_package_data=True,
    install_requires=[
        'abjad[development]',
        ],
    license='GPL',
    name='Abjad IDE',
    packages=('ide',),
    platforms='Any',
    url='http://www.projectabjad.org',
    )