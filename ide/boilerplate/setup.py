#!/usr/bin/env python

from distutils.core import setup

install_requires = (
    'abjad',
    )

def main():
    setup(
        author='COMPOSER_FULL_NAME',
        author_email='COMPOSER_EMAIL',
        install_requires=install_requires,
        name='PACKAGE_NAME',
        packages=('PACKAGE_NAME',),
        url='https://github.com/GITHUB_USERNAME/PACKAGE_NAME',
        version='0.1',
        zip_safe=False,
        )


if __name__ == '__main__':
    main()