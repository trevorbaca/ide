# -*- coding: utf-8 -*-
import os
from abjad import *
import ide
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_go_to_test_directory_01():
    r'''From material package.
    '''

    input_ = 'red~example~score mm tempo~inventory tt q'
    abjad_ide._run_main_menu(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - materials directory',
        'Red Example Score (2013) - materials directory - tempo inventory',
        'Red Example Score (2013) - test directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_02():
    r'''From segment package.
    '''

    input_ = 'red~example~score gg A tt q'
    abjad_ide._run_main_menu(input_=input_)

    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - segments directory',
        'Red Example Score (2013) - segments directory - A',
        'Red Example Score (2013) - test directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_03():
    r'''From build directory to test directory.
    '''

    input_ = 'red~example~score bb tt q'
    abjad_ide._run_main_menu(input_=input_)
    titles = [
        'Abjad IDE - all score directories',
        'Red Example Score (2013)',
        'Red Example Score (2013) - build directory',
        'Red Example Score (2013) - test directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_04():
    r'''No explosions if test directory is missing.
    '''


    test_directory = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'test',
        )

    with systemtools.FilesystemState(keep=[test_directory]):
        command = 'rm -rf {}'
        command = command.format(test_directory)
        os.system(command)
        input_ = 'red~example~score tt q'
        abjad_ide._run_main_menu(input_=input_)

    string = 'Directory does not exist:'
    assert string in abjad_ide._io_manager._transcript.contents