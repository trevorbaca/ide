# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_ly_01():
    r'''In material directory.
    
    LilyPond file exists but PDF does not exist.
    '''

    ly_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempi',
        'illustration.ly',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'tempi',
        'illustration.pdf',
        )

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score mm tempi lyi q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.isfile(pdf_path)
        assert abjad.TestManager._compare_backup(pdf_path)

    message = 'Calling LilyPond on {} ...'
    message = message.format(abjad_ide._trim_path(ly_path))
    message = 'Writing {} ...'
    message = message.format(abjad_ide._trim_path(pdf_path))
    assert message in contents


def test_AbjadIDE_interpret_ly_02():
    r'''In segment directory.

    LilyPond file exists but PDF does not exist.
    '''

    ly_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'illustration.ly',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'illustration.pdf',
        )

    with abjad.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score gg A lyi q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.isfile(pdf_path)
        assert abjad.TestManager._compare_backup(pdf_path)

    message = 'Calling LilyPond on {} ...'
    message = message.format(abjad_ide._trim_path(ly_path))
    message = 'Writing {} ...'
    message = message.format(abjad_ide._trim_path(pdf_path))
    assert message in contents
