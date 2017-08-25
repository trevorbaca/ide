import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_open_every_pdf_01():
    r'''In materials directory.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'magic_numbers',
        'illustration.pdf',
        )

    input_ = 'red~score mm magic~numbers pdfm mm pdf* q'

    with ide.Test():
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert abjad_ide._session._attempted_to_open_file
    message = f'Opening {abjad_ide._trim(path)} ...'
    assert message in contents


def test_AbjadIDE_open_every_pdf_02():
    r'''In segments directory.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_01',
        'illustration.pdf',
        )

    input_ = 'red~score %A pdfm gg pdf* q'

    with ide.Test():
        abjad_ide._start(input_=input_)

    contents = abjad_ide._io_manager._transcript.contents
    assert abjad_ide._session._attempted_to_open_file
    message = f'Opening {abjad_ide._trim(path)} ...'
    assert message in contents


def test_AbjadIDE_open_every_pdf_03():
    r'''In scores directory.
    '''

    path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'distribution',
        'red-score-score.pdf',
        )

    input_ = 'pdf* q'
    abjad_ide._start(input_=input_)
    contents = abjad_ide._io_manager._transcript.contents

    assert abjad_ide._session._attempted_to_open_file
    message = f'Opening {abjad_ide._trim(path)} ...'
    assert message in contents
