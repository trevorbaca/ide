# -*- encoding: utf-8 -*-
from abjad import *
import os
import pytest
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)


def test_PackageManager_illustrate_definition_py_01():
    r'''Creates PDF and LilyPond files when none exists.
    '''

    segment_directory = os.path.join(
        abjad_ide._configuration.example_scores_directory,
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
        abjad_ide._run(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)

    contents = abjad_ide._transcript.contents
    assert 'Wrote ...' in contents
    assert ly_path in contents
    assert pdf_path in contents


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason='Cannot build on Travis-CI',
    )
def test_PackageManager_illustrate_definition_py_02():
    r'''Preserves existing PDF when candidate compares the same.
    '''

    segment_directory = os.path.join(
        abjad_ide._configuration.example_scores_directory,
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
        input_ = 'red~example~score g A i q'
        abjad_ide._run(input_=input_)

    contents = abjad_ide._transcript.contents
    assert 'The files ...' in contents
    assert pdf_path in contents
    assert candidate_pdf_path in contents
    assert ly_path not in contents
    assert '... compare the same.' in contents


def test_PackageManager_illustrate_definition_py_03():
    r'''Prompts composer to overwrite existing PDF when candidate compares
    differently.
    '''

    segment_directory = os.path.join(
        abjad_ide._configuration.example_scores_directory,
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
        abjad_ide._run(input_=input_)
        assert os.path.isfile(ly_path)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(ly_path)
        assert systemtools.TestManager._compare_backup(pdf_path)

    contents = abjad_ide._transcript.contents
    assert 'The files ...' in contents
    assert pdf_path in contents
    assert candidate_pdf_path in contents
    assert '... compare differently.' in contents