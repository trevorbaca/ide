import ide
import os
abjad_ide = ide.tools.idetools.AbjadIDE(is_test=True)
configuration = ide.tools.idetools.AbjadIDEConfiguration()


def test_AbjadIDE_open_every_pdf_01():
    r'''In materials directory.
    '''

    # only these three packages have PDFs
    package_names = (
        'ranges',
        'tempi',
        'magic_numbers',
        )
    paths = []
    for name in package_names:
        path = os.path.join(
            configuration.abjad_ide_example_scores_directory,
            'red_example_score',
            'red_example_score',
            'materials',
            name,
            'illustration.pdf',
            )
        paths.append(path)

    input_ = 'red~example~score mm pdf* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert abjad_ide._session._attempted_to_open_file
    for path in paths:
        message = 'Opening {} ...'
        message = message.format(abjad_ide._trim_path(path))
        assert message in contents


def test_AbjadIDE_open_every_pdf_02():
    r'''In segments directory.
    '''

    package_names = ('segment_01', 'segment_02', 'segment_03')
    paths = []
    for name in package_names:
        path = os.path.join(
            configuration.abjad_ide_example_scores_directory,
            'red_example_score',
            'red_example_score',
            'segments',
            name,
            'illustration.pdf',
            )
        paths.append(path)

    input_ = 'red~example~score gg pdf* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert abjad_ide._session._attempted_to_open_file
    assert abjad_ide._session._attempted_to_open_file
    for path in paths:
        message = 'Opening {} ...'
        message = message.format(abjad_ide._trim_path(path))
        assert message in contents


def test_AbjadIDE_open_every_pdf_03():
    r'''In scores directory.
    '''

    red_score_path = os.path.join(
        configuration.abjad_ide_example_scores_directory,
        'red_example_score',
        'red_example_score',
        'distribution',
        'red-example-score-score.pdf',
        )

    input_ = 'pdf* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert abjad_ide._session._attempted_to_open_file
    message = 'Opening {} ...'
    message = message.format(abjad_ide._trim_path(red_score_path))
    assert message in contents
