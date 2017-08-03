import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_check_every_definition_file_01():
    r'''In materials directory.
    '''

    input_ = 'red~example~score mm dfk* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    package_names = [
        'magic_numbers',
        'performers',
        'ranges',
        'tempi',
        'time_signatures',
        ]
    paths = []
    for package_name in package_names:
        path = os.path.join(
            configuration.abjad_ide_example_scores_directory,
            'red_example_score',
            'red_example_score',
            'materials',
            package_name,
            'definition.py',
            )
        paths.append(path)

    for path in paths:
        message = '{} ... OK'
        message = message.format(abjad_ide._trim_path(path))
        assert message in contents
    assert 'Total time ' in contents


def test_AbjadIDE_check_every_definition_file_02():
    r'''In segments directory.
    '''

    input_ = 'red~example~score gg dfk* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    package_names = [
        'segment_01',
        'segment_02',
        'segment_03',
        ]
    paths = []
    for package_name in package_names:
        path = os.path.join(
            configuration.abjad_ide_example_scores_directory,
            'red_example_score',
            'red_example_score',
            'segments',
            package_name,
            'definition.py',
            )
        paths.append(path)

    for path in paths:
        message = '{} ... OK'
        message = message.format(abjad_ide._trim_path(path))
        assert message in contents
    assert 'Total time ' in contents
