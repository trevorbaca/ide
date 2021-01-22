#!/usr/bin/env python
import sys

import setuptools

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 6)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(
        """
==========================
Unsupported Python version
==========================

This version of the Abjad IDE requires Python {}.{}, but you're trying to
install it on Python {}.{}.

This may be because you are using a version of pip that doesn't
understand the python_requires classifier. Make sure you
have pip >= 9.0 and setuptools >= 24.2, then try again:

    $ python -m pip install --upgrade pip setuptools
    $ python -m pip install ide

This will install the latest version of Abjad which works on your
version of Python.
""".format(
            *(REQUIRED_PYTHON + CURRENT_PYTHON)
        )
    )
    sys.exit(1)

author = ["Trevor Bača", "Josiah Wolf Oberholtzer"]

author_email = ["trevor.baca@gmail.com", "josiah.oberholtzer@gmail.com"]

install_requires = [
    "black>=19.10b0",
    "flake8>=3.8.2",
    "isort>=4.3.21",
    "abjad>=3.1",
    "mypy>=0.770",
    "pytest>=5.4.2",
    "pytest-cov>=2.6.0",
    "roman>=1.4",
    "uqbar>=0.4.6",
]

keywords = [
    "abjad",
    "music composition",
    "music notation",
    "lilypond",
]

if __name__ == "__main__":
    setuptools.setup(
        author=", ".join(author),
        author_email=", ".join(author_email),
        include_package_data=True,
        install_requires=install_requires,
        keywords=", ".join(keywords),
        license="MIT",
        name="baca-ide",
        packages=["ide"],
        platforms="Any",
        url="http://abjad.io.github",
    )
