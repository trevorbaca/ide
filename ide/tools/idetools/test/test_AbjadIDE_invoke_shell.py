import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_invoke_shell_01():

    input_ = 'red~example~score mm tempi !pwd q'
    abjad_ide._start(input_=input_)

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
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

    path = configuration.abjad_ide_example_scores_directory
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents


def test_AbjadIDE_invoke_shell_03():
    r'''Works in build directory.
    '''

    input_ = 'red~example~score bb !pwd q'
    abjad_ide._start(input_=input_)

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'build',
        )
    string = '\n{}\n'.format(path)
    assert string in abjad_ide._io_manager._transcript.contents
