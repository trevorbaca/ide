# -*- encoding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_preface_01():
    r'''Makes preface.pdf when preface.pdf doesn't yet exist.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'preface.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'preface.pdf',
        )

    with systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score u pi q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_preface_02():
    r'''Preserves preface.pdf when preface.candidate.pdf compares
    equal to preface.pdf.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'preface.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'preface.pdf',
        )

    with systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        input_ = 'red~example~score u pi q'
        abjad_ide._run_main_menu(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents