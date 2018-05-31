#!/usr/bin/env python
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

install_requires = ('abjad',)

setuptools.setup(
    author=author,
    author_email=author_email,
    include_package_data=True,
    install_requires=[
        'abjad',
        ],
    license='GPL',
    name='Abjad IDE',
    packages=('ide',),
    platforms='Any',
    url='http://www.projectabjad.org',
    )
