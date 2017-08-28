import ide
import shutil
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_go_to_test_directory_01():
    r'''From material directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - materials directory',
        'Red Score (2017) - materials directory - tempi',
        'Red Score (2017) - test directory',
        ]

    input_ = 'red~score mm tempi tt q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_02():
    r'''From segment directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - segments directory',
        'Red Score (2017) - segments directory - A',
        'Red Score (2017) - test directory',
        ]

    input_ = 'red~score gg A tt q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_03():
    r'''From build directory to test directory.
    '''

    titles = [
        'Abjad IDE - scores directory',
        'Red Score (2017)',
        'Red Score (2017) - build directory',
        'Red Score (2017) - test directory',
        ]

    input_ = 'red~score bb tt q'
    abjad_ide._start(input_=input_)
    assert abjad_ide._io_manager._transcript.titles == titles


def test_AbjadIDE_go_to_test_directory_04():
    r'''No explosions if test directory is missing.
    '''

    with ide.Test():
        test_directory = ide.Path('red_score').test
        shutil.rmtree(str(test_directory))
        input_ = 'red~score tt q'
        abjad_ide._start(input_=input_)
        string = f'Directory does not exist: {abjad_ide._trim(test_directory)}'
        assert string in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_go_to_test_directory_05():
    r'''Filenames appear correctly.
    '''

    input_ = 'red~score tt q'
    abjad_ide._start(input_=input_)
    transcript = abjad_ide._io_manager._transcript.contents
    assert '1: test_dummy.py' in transcript
