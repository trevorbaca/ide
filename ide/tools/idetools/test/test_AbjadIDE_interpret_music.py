# -*- coding: utf-8 -*-
import pytest
pytest.skip('reactivate me after creating letter-portrait build subdirectory')
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_music_01():
    r'''Makes music.pdf when music.pdf doesn't yet exist.
    '''

    ly_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'music.ly',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'music.pdf',
        )

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score bb mi q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_music_02():
    r'''Preserves music.pdf when music.candidate.pdf compares
    equal to music.pdf.
    '''

    ly_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'music.ly',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'music.pdf',
        )

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        # remove existing PDF
        os.remove(pdf_path)
        # generate PDF a first time
        input_ = 'red~example~score bb mi q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDF a second time
        input_ = 'red~example~score bb mi q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    # TODO: make messaging work like this again
    assert 'Preserving' in contents