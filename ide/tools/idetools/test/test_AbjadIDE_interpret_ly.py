import ide
import pathlib
abjad_ide = ide.AbjadIDE(is_test=True)


def test_AbjadIDE_interpret_ly_01():
    r'''In material directory.
    '''

    ly_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'tempi',
        'illustration.ly',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'materials',
        'tempi',
        'illustration.pdf',
        )

    with ide.Test():
        if pdf_path.exists():
            pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~score mm tempi lyi q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert pdf_path.is_file()

    message = 'Calling LilyPond on {} ...'
    message = message.format(abjad_ide._trim(ly_path))
    message = 'Writing {} ...'
    message = message.format(abjad_ide._trim(pdf_path))
    assert message in contents


def test_AbjadIDE_interpret_ly_02():
    r'''In segment directory.
    '''

    ly_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_01',
        'illustration.ly',
        )
    pdf_path = pathlib.Path(
        abjad_ide.configuration.example_scores_directory,
        'red_score',
        'red_score',
        'segments',
        'segment_01',
        'illustration.pdf',
        )

    with ide.Test():
        if pdf_path.exists():
            pdf_path.unlink()
        assert not pdf_path.exists()
        input_ = 'red~score gg A lyi q'
        abjad_ide._start(input_=input_)
        contents = abjad_ide._io_manager._transcript.contents
        assert pdf_path.is_file()

    message = 'Calling LilyPond on {} ...'
    message = message.format(abjad_ide._trim(ly_path))
    message = 'Writing {} ...'
    message = message.format(abjad_ide._trim(pdf_path))
    assert message in contents
