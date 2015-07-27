# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_PackageWrangler_open_every_illustration_pdf_01():
    r'''Opens illustration PDF in every material package.
    '''

    package_names = ('pitch_range_inventory', 'tempo_inventory')
    paths = []
    for name in package_names:
        path = os.path.join(
            abjad_ide._configuration.example_score_packages_directory,
            'red_example_score',
            'red_example_score',
            'materials',
            name,
            'illustration.pdf',
            )
        paths.append(path)

    input_ = 'red~example~score m io* y q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents
    assert abjad_ide._session._attempted_to_open_file
    assert 'Will open ...' in contents
    for path in paths:
        assert path in contents


def test_PackageWrangler_open_every_illustration_pdf_02():
    r'''Opens illustration PDF in every segment package.
    '''

    input_ = 'red~example~score g io* y q'
    abjad_ide._run(input_=input_)

    assert abjad_ide._session._attempted_to_open_file