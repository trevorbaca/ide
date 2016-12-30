# -*- coding: utf-8 -*-
import abjad
import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_interpret_preface_01():
    r'''Works when preface.pdf doesn't yet exist.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.pdf',
        )

    with abjad.systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        os.remove(pdf_path)
        assert not os.path.exists(pdf_path)
        input_ = 'red~example~score bb letter-portrait pi q'
        abjad_ide._start(input_=input_)
        assert os.path.isfile(pdf_path)
        assert abjad.systemtools.TestManager._compare_backup(pdf_path)


def test_AbjadIDE_interpret_preface_02():
    r'''Works when preface.pdf already exists.
    '''

    tex_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.tex',
        )
    pdf_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'letter-portrait',
        'preface.pdf',
        )

    with abjad.systemtools.FilesystemState(keep=[tex_path, pdf_path]):
        assert os.path.exists(pdf_path)
        input_ = 'red~example~score bb letter-portrait pi q'
        abjad_ide._start(input_=input_)
        assert os.path.exists(pdf_path)
