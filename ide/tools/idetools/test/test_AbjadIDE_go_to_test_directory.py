import ide
import os
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_test_directory_01():
    r'''From material directory.
    '''

    input_ = 'red~score mm tempi tt q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - test directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_02():
    r'''From segment directory.
    '''

    input_ = 'red~score gg A tt q'
    abjad_ide._start(input_=input_)

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - test directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_03():
    r'''From build directory to test directory.
    '''

    input_ = 'red~score bb tt q'
    abjad_ide._start(input_=input_)
    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - build directory',
        'Red Score (2017) - test directory',
        ]
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_04():
    r'''No explosions if test directory is missing.
    '''

    test_directory = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'test',
        )

    with ide.Test():
        command = 'rm -rf {}'
        command = command.format(test_directory)
        os.system(command)
        input_ = 'red~score tt q'
        abjad_ide._start(input_=input_)

    string = 'Directory does not exist:'
    assert string in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_go_to_test_directory_05():
    r'''Filenames appear correctly.
    '''

    input_ = 'red~score tt q'
    abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert '1: test_dummy.py' in contents
