# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_score_01():
    r'''Works when score.pdf doesn't yet exist.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.pdf',
        )

    with abjad.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(pdf_path)
        assert abjad.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_score_02():
    r'''Works when score.pdf already exists.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.pdf',
        )

    with abjad.FilesystemState(keep=[tex_path, pdf_path]):
        assert os.path.exists(pdf_path)
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(pdf_path)


def test_AbjadIDE_interpret_score_03():
    r'''LaTeX error does not freeze IDE.
    '''

    preface_pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.pdf',
        )
    score_pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'score.pdf',
        )
    paths = [preface_pdf_path, score_pdf_path]

    with abjad.FilesystemState(keep=paths):
        os.remove(preface_pdf_path)
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'ERROR IN LATEX LOG FILE ...' in contents
