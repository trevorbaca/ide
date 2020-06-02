#!/usr/bin/env python
import setuptools

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
    "pytest-helpers-namespace>=2019.1.8",
    "roman>=1.4",
    "uqbar>=0.4.6",
]

keywords = [
    "abjad",
    "music composition",
    "music notation",
    "formalized score control",
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
        name="Abjad IDE",
        packages=["ide"],
        platforms="Any",
        url="http://abjad.io.github",
    )
