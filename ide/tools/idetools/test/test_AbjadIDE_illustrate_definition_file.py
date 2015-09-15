# -*- coding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_illustrate_definition_file_01():
    r'''Creates PDF and LilyPond files when none exists.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    pdf_path = os.path.join(segment_directory, 'illustration.pdf')

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(ly_path)
        os.remove(pdf_path)
        input_ = 'red~example~score g A i q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Wrote ...' in contents
    assert ly_path in contents
    assert pdf_path in contents


def test_AbjadIDE_illustrate_definition_file_02():
    r'''Preserves existing PDF when candidate compares the same.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    pdf_path = os.path.join(segment_directory, 'illustration.pdf')
    candidate_pdf_path = os.path.join(
        segment_directory,
        'illustration.candidate.pdf',
        )

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        # remove existing PDF
        os.remove(ly_path)
        os.remove(pdf_path)
        assert not os.path.exists(ly_path)
        assert not os.path.exists(pdf_path)
        # generate PDF first time
        input_ = 'red~example~score g A i q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        # attempt to generate PDF second time (but blocked)
        input_ = 'red~example~score g A i q'
        abjad_ide._run_main_menu(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert pdf_path in contents
    assert candidate_pdf_path in contents
    assert ly_path not in contents
    assert '... compare the same.' in contents


def test_AbjadIDE_illustrate_definition_file_03():
    r'''Prompts composer to overwrite existing PDF when candidate compares
    differently.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    pdf_path = os.path.join(segment_directory, 'illustration.pdf')
    candidate_pdf_path = os.path.join(
        segment_directory,
        'illustration.candidate.pdf',
        )

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        with open(pdf_path, 'w') as file_pointer:
            file_pointer.write('text')
        input_ = 'red~example~score g A i y q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert pdf_path in contents
    assert candidate_pdf_path in contents
    assert '... compare differently.' in contents