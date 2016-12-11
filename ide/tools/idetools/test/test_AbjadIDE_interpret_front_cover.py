# -*- coding: utf-8 -*-
import abjad
import ide
import os
import pytest
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Fails under containerized Travis-CI."
    )
def test_AbjadIDE_interpret_front_cover_01():
    r'''Makes front-cover.pdf when front-cover.pdf doesn't yet exist.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.pdf',
        )

    with abjad.systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score bb letter-portrait fci q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(pdf_path)
        assert abjad.systemtools.TestManager._compare_backup(pdf_path)


@pytest.mark.skipif(
    os.environ.get('TRAVIS') == 'true',
    reason="Fails under containerized Travis-CI."
    )
def test_AbjadIDE_interpret_front_cover_02():
    r'''Preserves front-cover.pdf when front-cover.candidate.pdf 
    compares equal to front-cover.pdf.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'front-cover.pdf',
        )

    with abjad.systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        # remove existing PDF
        os.remove(pdf_path)
        # generate PDF first time
        input_ = 'red~example~score bb letter-portrait fci q'
        abjad_ide._start(input_=input_)
        # attempt (but fail) to generate PDF a second time
        input_ = 'red~example~score bb letter-portrait fci q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents

    assert 'Preserving' in contents
