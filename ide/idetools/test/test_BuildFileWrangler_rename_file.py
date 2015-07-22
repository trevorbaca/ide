# -*- encoding: utf-8 -*-
import os
import shutil
from abjad import *
import ide
configuration = ide.idetools.Configuration()
abjad_ide = ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_rename_file_01():
    r'''Works at home screen.
    '''

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'score.pdf',
        )
    new_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'foo-score.pdf',
        )

    assert os.path.exists(path)

    input_ = 'uu ren score.pdf~(Red~Example~Score)'
    input_ += ' foo-score.pdf y q'
    abjad_ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'uu ren foo-score.pdf~(Red~Example~Score)'
    input_ += ' score.pdf y q'
    abjad_ide._run(input_=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)


def test_BuildFileWrangler_rename_file_02():
    r'''Works in score package.
    '''

    path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'score.pdf',
        )
    new_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'red_example_score',
        'build',
        'foo-score.pdf',
        )

    assert os.path.exists(path)

    input_ = 'red~example~score u ren score.pdf'
    input_ += ' foo-score.pdf y q'
    abjad_ide._run(input_=input_)
    assert not os.path.exists(path)
    assert os.path.exists(new_path)

    # no shutil because need to rename file in repository
    input_ = 'red~example~score u ren foo-score.pdf'
    input_ += ' score.pdf y q'
    abjad_ide._run(input_=input_)
    assert not os.path.exists(new_path)
    assert os.path.exists(path)