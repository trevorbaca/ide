# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_open_every_illustration_pdf_01():
    r'''Opens illustration PDF in every material package.
    '''

    package_names = ('pitch_range_inventory', 'tempo_inventory')
    paths = []
    for name in package_names:
        path = os.path.join(
            configuration.abjad_ide_example_scores_directory,
            'red_example_score',
            'red_example_score',
            'materials',
            name,
            'illustration.pdf',
            )
        paths.append(path)

    input_ = 'red~example~score mm io* y q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents
    assert abjad_ide._session._attempted_to_open_file
    assert 'Will open ...' in contents
    for path in paths:
        assert path in contents


def test_AbjadIDE_open_every_illustration_pdf_02():
    r'''Opens illustration PDF in every segment package.
    '''

    input_ = 'red~example~score gg io* y q'
    abjad_ide._start(input_=input_)

    assert abjad_ide._session._attempted_to_open_file