# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_score_01():
    r'''Makes score.pdf when score.pdf doesn't yet exist.
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

    with abjad.systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(pdf_path)
        assert abjad.systemtools.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_score_02():
    r'''Preserves score.pdf when score.candidate.pdf compares
    equal to score.pdf.
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

    with abjad.systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        # remove existing pdf
        os.remove(pdf_path)
        # generate PDF a first time
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDF a second time
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'Preserving' in contents


def test_AbjadIDE_interpret_score_03():
    r'''LaTeX error does not freeze IDE.
    '''

    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.pdf',
        )

    with abjad.systemtools.FilesystemState(keep=[pdf_path]):
        # remove existing pdf
        os.remove(pdf_path)
        # attempt unsuccessfully to call pdflatex
        input_ = 'red~example~score bb letter-portrait si q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'ERROR in LaTeX log file ...' in contents
