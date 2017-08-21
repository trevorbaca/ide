import ide
import pathlib
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_check_definition_01():
    r'''In material directory.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'materials',
        'magic_numbers',
        'definition.py',
        )

    input_ = 'red~example~score %magic dfk q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    message = '{!s} ... OK'
    message = message.format(abjad_ide._trim(path))
    assert message in contents
    assert 'Total time ' in contents


def test_AbjadIDE_check_definition_02():
    r'''In segment directory.
    '''

    path = pathlib.Path(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'segments',
        'segment_01',
        'definition.py',
        )

    input_ = 'red~example~score %A dfk q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    message = '{!s} ... OK'
    message = message.format(abjad_ide._trim(path))
    assert message in contents
    assert 'Total time ' in contents
