#!/usr/bin/env python
import setuptools


author = ["Trevor Bača", "Josiah Wolf Oberholtzer"]

author_email = ["trevor.baca@gmail.com", "josiah.oberholtzer@gmail.com"]

install_requires = [
    "abjad",
    "mypy",
    "roman",
    "sphinx",
    "sphinx-rtd-theme",
    "uqbar>=0.4.0",
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
        url="http://www.projectabjad.org",
    )
