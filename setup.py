#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

author = [
    'Trevor Bača',
    'Josiah Wolf Oberholtzer',
    'Víctor Adán',
    ]
author = ', '.join(author)

author_email = [
    'trevorbaca@gmail.com',
    'josiah.oberholtzer@gmail.com',
    'contact@victoradan.net',
    ]
author_email = ', '.join(author_email)

entry_points = {
    'console_scripts': [
        'start-abjad-ide = ide.idetools.start_abjad_ide:start_abjad_ide',
        ],
    }

install_requires = ('abjad',)

setuptools.setup(
    author=author,
    author_email=author_email,
    entry_points=entry_points,
    include_package_data=True,
    install_requires=('abjad',),
    license='GPL',
    name='Abjad IDE',
    packages=('ide',),
    platforms='Any',
    url='http://www.projectabjad.org',
    )