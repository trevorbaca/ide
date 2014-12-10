# -*- encoding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = abjad_ide.idetools.AbjadIDE(is_test=True)


def test_BuildFileWrangler_copy_file_01():
    r'''Works in build depot.
    
    Partial test because we can't be sure any user score packages will be
    present. And because Score PackageManager allows copying into user score 
    packges only (because copying into example score packages could pollute the 
    example score packages).
    '''

    input_ = 'uu cp score.pdf~(Red~Example~Score) q'
    abjad_ide._run(input_=input_)
    contents = abjad_ide._transcript.contents

    titles = [
        'Abjad IDE - scores',
        'Abjad IDE - build depot',
        'Abjad IDE - build depot',
        ]
    assert abjad_ide._transcript.titles == titles
    assert 'Select storehouse:' in contents


def test_BuildFileWrangler_copy_file_02():
    r'''Works in build directory.
    '''

    source_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'score.pdf',
        )
    target_path = os.path.join(
        abjad_ide._configuration.example_score_packages_directory,
        'red_example_score',
        'build',
        'copied-score.pdf',
        )

    with systemtools.FilesystemState(keep=[source_path], remove=[target_path]):
        input_ = 'red~example~score u cp'
        input_ += ' score.pdf copied-score.pdf y q'
        abjad_ide._run(input_=input_)
        contents = abjad_ide._transcript.contents
        assert os.path.exists(source_path)
        assert os.path.exists(target_path)
        assert 'copied-score.pdf' in contents