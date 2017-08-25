import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_invoke_shell_01():

    input_ = 'red~score mm tempi !pwd q'
    abjad_ide._start(input_=input_)

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'tempi',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_invoke_shell_02():
    r'''Works at home.
    '''

    input_ = '!pwd q'
    abjad_ide._start(input_=input_)

    path = abjad_ide.configuration.example_scores_directory
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_invoke_shell_03():
    r'''Works in build directory.
    '''

    input_ = 'red~score bb !pwd q'
    abjad_ide._start(input_=input_)

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'build',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents
