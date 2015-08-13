# -*- encoding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_front_cover_01():
    r'''Makes front-cover.pdf when front-cover.pdf doesn't yet exist.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.pdf',
        )

    with systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score u fci q'
        abjad_ide._run_main_menu(input_=input_)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_front_cover_02():
    r'''Preserves front-cover.pdf when front-cover.candidate.pdf 
    compares equal to front-cover.pdf.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'front-cover.pdf',
        )

    with systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        input_ = 'red~example~score u fci q'
        abjad_ide._run_main_menu(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents