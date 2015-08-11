# -*- encoding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_Wrangler_interpret_music_01():
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
        input_ = 'red~example~score u mi q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)


def test_Wrangler_interpret_music_02():
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
        input_ = 'red~example~score u mi q'
        abjad_ide._run(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents