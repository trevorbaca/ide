# -*- coding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_make_pdf_01():
    r'''In material directory.
    
    Creates PDF and LilyPond files when none exists.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        )
    ly_path = os.path.join(segment_directory, 'illustration.ly')
    pdf_path = os.path.join(segment_directory, 'illustration.pdf')

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(ly_path)
        os.remove(pdf_path)
        input_ = 'red~example~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Calling LilyPond on' in contents
    assert 'Writing' in contents
    assert abjad_ide._trim_path(ly_path) in contents
    assert abjad_ide._trim_path(pdf_path) in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_02():
    r'''In material directory.
    
    Preserves existing PDF when candidate compares the same.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
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
        input_ = 'red~example~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        # attempt to generate PDF second time (but blocked)
        input_ = 'red~example~score mm magic~numbers pdfm q'
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'Calling LilyPond on' in contents
    assert 'Preserving' in contents
    assert abjad_ide._trim_path(ly_path) in contents
    assert abjad_ide._trim_path(pdf_path) in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_03():
    r'''In segment directory.

    Creates PDF and LilyPond files when none exists.
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
    illustrate_file_path = os.path.join(
        segment_directory,
        '__illustrate_segment__.py',
        )

    with systemtools.FilesystemState(keep=[ly_path, pdf_path]):
        os.remove(ly_path)
        os.remove(pdf_path)
        input_ = 'red~example~score gg A pdfm q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)

    message = 'Calling Python on {} ...'
    message = message.format(abjad_ide._trim_path(illustrate_file_path))
    assert message in contents
    assert 'Abjad runtime' in contents
    assert 'LilyPond runtime' in contents
    message = 'Writing {} ...'
    message = message.format(abjad_ide._trim_path(ly_path))
    assert message in contents
    message = 'Writing {} ...'
    message = message.format(abjad_ide._trim_path(pdf_path))
    assert message in contents
    message = 'Opening {} ...'
    message = message.format(abjad_ide._trim_path(pdf_path))
    assert message in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_04():
    r'''In segment directory.
    
    Preserves existing PDF when candidate compares the same.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    illustrate_file_path = os.path.join(
        segment_directory,
        '__illustrate_segment__.py',
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
        input_ = 'red~example~score gg A pdfm q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        # attempt to generate PDF second time (but blocked)
        input_ = 'red~example~score gg A pdfm q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    message = 'Calling Python on {} ...'
    message = message.format(abjad_ide._trim_path(illustrate_file_path))
    assert message in contents
    assert 'Abjad runtime' in contents
    assert 'LilyPond runtime' in contents
    message = 'Preserving {} ...'
    message = message.format(abjad_ide._trim_path(ly_path))
    assert message in contents
    message = 'Preserving {} ...'
    message = message.format(abjad_ide._trim_path(pdf_path))
    assert message in contents
    assert 'Total time ' in contents


def test_AbjadIDE_make_pdf_05():
    r'''In segment directory.
    
    Overwrites existing PDF.
    '''

    segment_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        )
    illustrate_file_path = os.path.join(
        segment_directory,
        '__illustrate_segment__.py',
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
        input_ = 'red~example~score gg A pdfm q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)

    message = 'Calling Python on {} ...'
    message = message.format(abjad_ide._trim_path(illustrate_file_path))
    assert message in contents
    assert 'Abjad runtime' in contents
    assert 'LilyPond runtime' in contents
    message = 'Preserving {} ...'
    message = message.format(abjad_ide._trim_path(ly_path))
    assert message in contents
    message = 'Overwriting {} ...'
    message = message.format(abjad_ide._trim_path(pdf_path))
    assert message in contents
    message = 'Opening {} ...'
    message = message.format(abjad_ide._trim_path(pdf_path))
    assert message in contents
    assert 'Total time ' in contents