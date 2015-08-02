# -*- encoding: utf-8 -*-
from abjad import *
import os
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_Wrangler_interpret_back_cover_01():
    r'''Creates back-cover.pdf when back-cover.pdf doesn't exist.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'back-cover.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'back-cover.pdf',
        )

    with systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score u bci q'
        abjad_ide._run(input_=input_)
        assert os.path.isfile(pdf_path)
        assert systemtools.TestManager._compare_backup(pdf_path)


def test_Wrangler_interpret_back_cover_02():
    r'''Preserves back-cover.pdf when back-cover.candidate.pdf compares
    the same.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'back-cover.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'back-cover.pdf',
        )

    with systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        input_ = 'red~example~score u bci q'
        abjad_ide._run(input_=input_)

    contents = abjad_ide._session._transcript.contents
    assert 'The files ...' in contents
    assert '... compare the same.' in contents
    assert 'Preserved' in contents