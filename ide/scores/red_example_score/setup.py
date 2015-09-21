#!/usr/bin/env python

from distutils.core import setup

install_requires = (
    'abjad',
    )

def main():
    setup(
        author='Composer Name',
        author_email='compser.name@gmail.com',
        install_requires=install_requires,
        name='red_example_score',
        packages=('red_example_score',),
        url='https://github.com/composer.name/red_example_score',
        version='0.1',
        zip_safe=False,
        )


if __name__ == '__main__':
    main()