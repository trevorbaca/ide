# -*- coding: utf-8 -*-
import os
from abjad import *
from definition import OUTPUT_OBJECT


lilypond_file = None

if hasattr(OUTPUT_OBJECT, '__illustrate__'):
    lilypond_file = OUTPUT_OBJECT.__illustrate__()
else:
    import definition
    definition_pyc_path = definition.__file__
    package_directory = os.path.dirname(definition_pyc_path)
    illustrate_file = os.path.join(package_directory, '__illustrate__.py')
    if os.path.isfile(illustrate_file):
        from __illustrate__ import __illustrate__
        lilypond_file = __illustrate__(OUTPUT_OBJECT)

if lilypond_file is not None:
    path = os.path.abspath(__file__)
    directory = os.path.dirname(path)
    candidate_path = os.path.join(directory, 'illustration.candidate.pdf')
    persist(lilypond_file).as_pdf(candidate_path)